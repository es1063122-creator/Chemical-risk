import json
from pathlib import Path

CAS_LIST_FILE = "cas_list.txt"
NAME_MAP_FILE = "chemical_name_map_500.json"
OUTPUT_FILE = "chemical-db-800.js"


# -----------------------------
# 파일 로드
# -----------------------------
def load_cas_list(path: str):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    cas_list = []
    for line in lines:
        v = line.strip()
        if v:
            cas_list.append(v)
    return cas_list


def load_name_map(path: str):
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


# -----------------------------
# 기본 유틸
# -----------------------------
def uniq_keep_order(items):
    seen = set()
    result = []
    for item in items:
        if not item:
            continue
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def title_case_name(name: str):
    if not name:
        return ""
    return " ".join(part[:1].upper() + part[1:] if part else "" for part in name.split())


# -----------------------------
# 영문명 생성
# -----------------------------
# 주의:
# - 지금은 외부 API 없이 동작하게 만들기 위해
#   chemical_name_map_500.json에 있으면 그 key(영문명)를 활용하고
#   없으면 CAS 기반 임시 영문명을 생성합니다.
# - 나중에 PubChem/ECHA 연결하면 이 부분만 바꾸면 됩니다.
# -----------------------------
def build_reverse_name_map(name_map: dict):
    reverse_map = {}
    for en, ko in name_map.items():
        reverse_map[en.lower().strip()] = ko
    return reverse_map


def infer_name_en_from_cas(cas: str, name_map: dict):
    """
    현재는 CAS -> 실명 API 연결이 없으므로
    1) name_map에 이미 대표 화학명 key들이 있으면 그중 일부를 순환 배치하는 것이 아니라
       CAS로부터는 실명을 알 수 없으므로
    2) 안전하게 임시 이름을 만듭니다.
    """
    return f"Chemical {cas}"


def normalize_name_ko(name_en: str, name_map: dict):
    key = name_en.lower().strip()
    return name_map.get(key, name_en)


def normalize_name_ja(name_en: str, name_ko: str):
    # 현재는 일본어 자동 번역기 없이 기본값 처리
    # 대표님 시스템은 우선 구조 완성이 목적이므로
    # 한글명이 있으면 그대로 두지 않고 영문명 우선
    return name_en


# -----------------------------
# 이름 패턴 기반 위험성 추정
# -----------------------------
def infer_ghs(name: str):
    name_l = name.lower()
    ghs = []

    flammable_keywords = [
        "benz", "tolu", "xylene", "hexane", "octane", "ethanol", "methanol",
        "acetone", "propanol", "isopropyl", "butanol", "ketone", "styrene",
        "ethyl acetate", "butyl acetate", "chloroform", "solvent", "cresol"
    ]

    corrosive_keywords = [
        "acid", "hydrochloric", "sulfuric", "nitric", "phosphoric", "formic",
        "acetic", "chloride", "caustic", "hydroxide"
    ]

    toxic_keywords = [
        "amine", "ammonia", "phenol", "cresol", "dinitro", "aldehyde",
        "chloro", "aniline", "formaldehyde", "nitro", "cyan", "chlorobenz"
    ]

    carcinogenic_keywords = [
        "benzene", "formaldehyde"
    ]

    eye_irritation_keywords = [
        "acid", "aldehyde", "cresol", "phenol", "amine", "chloride"
    ]

    skin_irritation_keywords = [
        "phenol", "cresol", "aldehyde", "amine", "acid"
    ]

    if any(k in name_l for k in flammable_keywords):
        ghs.append("인화성")

    if any(k in name_l for k in corrosive_keywords):
        ghs.append("부식성")

    if any(k in name_l for k in toxic_keywords):
        ghs.append("독성")

    if any(k in name_l for k in carcinogenic_keywords):
        ghs.append("발암성")

    if any(k in name_l for k in eye_irritation_keywords):
        ghs.append("눈 자극")

    if any(k in name_l for k in skin_irritation_keywords):
        ghs.append("피부 자극")

    return uniq_keep_order(ghs)


# -----------------------------
# PPE 생성
# -----------------------------
def infer_ppe(name: str, ghs: list):
    name_l = name.lower()
    ppe = ["보호장갑", "보호안경"]

    if "인화성" in ghs:
        ppe += ["유기용제용 방독마스크", "보호복", "국소배기"]

    if "부식성" in ghs:
        ppe += ["내화학성 장갑", "안면보호구", "화학방호복"]

    if "독성" in ghs:
        ppe += ["방독마스크", "국소배기"]

    if "발암성" in ghs:
        ppe += ["화학방호복", "방독마스크", "국소배기"]

    if "눈 자극" in ghs or "피부 자극" in ghs:
        ppe += ["보호복"]

    # 추가 이름 기반 보정
    if any(k in name_l for k in ["powder", "dust"]):
        ppe += ["방진마스크"]

    return uniq_keep_order(ppe)


# -----------------------------
# Storage 생성
# -----------------------------
def infer_storage(name: str, ghs: list):
    name_l = name.lower()
    storage = []

    if "인화성" in ghs:
        storage += ["화기엄금", "환기보관", "밀폐용기", "정전기 방지"]

    if "부식성" in ghs:
        storage += ["산 전용 보관", "금속 접촉 주의", "건냉소 보관"]

    if "독성" in ghs:
        storage += ["누출 방지", "잠금 보관"]

    if not storage:
        storage += ["건냉소 보관", "밀폐보관"]

    # 이름 기반 약간의 보정
    if "ammonia" in name_l or "amine" in name_l:
        storage += ["환기보관"]

    return uniq_keep_order(storage)


# -----------------------------
# 점수 계산
# -----------------------------
def infer_scores(name: str, ghs: list):
    name_l = name.lower()

    hazard = 3
    danger = 3

    if "인화성" in ghs:
        danger += 1

    if "부식성" in ghs:
        hazard += 1

    if "독성" in ghs:
        hazard += 1

    if "발암성" in ghs:
        hazard += 2

    # 개별 강한 물질 보정
    if "benzene" in name_l or "formaldehyde" in name_l:
        hazard = max(hazard, 5)
        danger = max(danger, 4)

    if "methanol" in name_l or "ammonia" in name_l or "phenol" in name_l or "cresol" in name_l:
        hazard = max(hazard, 4)

    if "octane" in name_l or "hexane" in name_l or "toluene" in name_l or "xylene" in name_l or "acetone" in name_l:
        danger = max(danger, 4)

    hazard = min(hazard, 5)
    danger = min(danger, 5)

    return hazard, danger


# -----------------------------
# 노출 경로 생성
# -----------------------------
def infer_exposure(name: str, ghs: list):
    exposure = []

    if "인화성" in ghs or "독성" in ghs:
        exposure += ["흡입", "피부 접촉"]

    if "부식성" in ghs or "눈 자극" in ghs:
        exposure += ["피부 접촉", "눈"]

    if "발암성" in ghs:
        exposure += ["흡입"]

    if not exposure:
        exposure += ["피부 접촉"]

    return uniq_keep_order(exposure)


# -----------------------------
# 메인 레코드 생성
# -----------------------------
def build_item(cas: str, name_en: str, name_map: dict):
    name_ko = normalize_name_ko(name_en, name_map)
    name_ja = normalize_name_ja(name_en, name_ko)

    ghs = infer_ghs(name_en)
    ppe = infer_ppe(name_en, ghs)
    storage = infer_storage(name_en, ghs)
    hazard_score, danger_score = infer_scores(name_en, ghs)
    exposure = infer_exposure(name_en, ghs)

    item = {
        "cas": cas,
        "name_ko": name_ko,
        "name_en": name_en,
        "name_ja": name_ja,
        "category": "chemical",
        "ghs": ghs,
        "exposure": exposure,
        "ppe": ppe,
        "storage": storage,
        "hazard_score": hazard_score,
        "danger_score": danger_score
    }
    return item


# -----------------------------
# 대표 화학물질 영문명 우선 매핑
# -----------------------------
# 대표님이 만든 500개 이름맵은 "영문명 -> 한국어명" 구조라
# CAS만으로는 영문명을 알아낼 수 없습니다.
# 그래서 자주 쓰는 일부 물질은 아래 CAS 사전으로 먼저 잡고,
# 나머지는 임시명으로 생성합니다.
# 나중에 PubChem API 붙이면 이 사전은 거의 필요 없어집니다.
# -----------------------------
KNOWN_CAS_NAME_EN = {
    "67-64-1": "Acetone",
    "67-56-1": "Methanol",
    "64-17-5": "Ethanol",
    "71-43-2": "Benzene",
    "108-88-3": "Toluene",
    "1330-20-7": "Xylene",
    "110-54-3": "n-Hexane",
    "111-65-9": "Octane",
    "69-72-7": "Salicylic Acid",
    "95-48-7": "O-Cresol",
    "108-39-4": "M-Cresol",
    "50-00-0": "Formaldehyde",
    "7647-01-0": "Hydrochloric Acid",
    "7664-93-9": "Sulfuric Acid",
    "7664-41-7": "Ammonia",
    "67-63-0": "Isopropanol",
    "141-78-6": "Ethyl Acetate",
    "123-86-4": "Butyl Acetate",
    "78-93-3": "Methyl Ethyl Ketone",
    "108-10-1": "Methyl Isobutyl Ketone",
    "79-01-6": "Trichloroethylene",
    "75-09-2": "Dichloromethane",
    "67-66-3": "Chloroform",
    "62-53-3": "Aniline",
    "100-42-5": "Styrene",
    "107-13-1": "Acrylonitrile",
    "75-21-8": "Ethylene Oxide",
    "75-07-0": "Acetaldehyde",
    "64-19-7": "Acetic Acid",
    "64-18-6": "Formic Acid",
    "7664-38-2": "Phosphoric Acid",
    "7697-37-2": "Nitric Acid",
    "1310-73-2": "Sodium Hydroxide",
    "1310-58-3": "Potassium Hydroxide",
    "1305-62-0": "Calcium Hydroxide",
    "7722-84-1": "Hydrogen Peroxide",
    "108-95-2": "Phenol",
    "97-00-7": "1-Chloro-2,4-Dinitrobenzene"
}


def main():
    cas_list = load_cas_list(CAS_LIST_FILE)
    name_map = load_name_map(NAME_MAP_FILE)

    db = []

    for cas in cas_list:
        name_en = KNOWN_CAS_NAME_EN.get(cas)
        if not name_en:
            name_en = infer_name_en_from_cas(cas, name_map)

        item = build_item(cas, name_en, name_map)
        db.append(item)

    output = "const CHEMICAL_DB = " + json.dumps(db, ensure_ascii=False, indent=2) + ";\n"
    Path(OUTPUT_FILE).write_text(output, encoding="utf-8")

    print("완료")
    print("총 화학물질 수:", len(db))
    print("출력 파일:", OUTPUT_FILE)


if __name__ == "__main__":
    main()