import json
from pathlib import Path

INPUT_FILE = "chemical-db-800.js"
OUTPUT_FILE = "chemical-db-800-upgraded.js"
NAME_MAP_FILE = "chemical_name_map_500.json"


# -----------------------------
# 화학물질 이름 매핑 로드
# -----------------------------
def load_name_map():
    path = Path(NAME_MAP_FILE)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}

NAME_MAP = load_name_map()


# -----------------------------
# JS DB 로드
# -----------------------------
def load_js_db(path: str):

    text = Path(path).read_text(encoding="utf-8").strip()

    prefix = "const CHEMICAL_DB ="

    if not text.startswith(prefix):
        raise ValueError("chemical-db 형식 오류")

    json_text = text[len(prefix):].strip()

    if json_text.endswith(";"):
        json_text = json_text[:-1]

    return json.loads(json_text)


# -----------------------------
# 한국어 이름 변환
# -----------------------------
def normalize_name_ko(name):

    key = name.lower().strip()

    return NAME_MAP.get(key, name)


# -----------------------------
# 중복 제거
# -----------------------------
def uniq(items):

    seen = set()
    result = []

    for i in items:

        if i not in seen:
            seen.add(i)
            result.append(i)

    return result


# -----------------------------
# GHS 자동 추론
# -----------------------------
def infer_ghs(name):

    name = name.lower()

    ghs = []

    if any(k in name for k in ["benzene","toluene","xylene","octane","hexane","acetone"]):
        ghs.append("인화성")

    if "acid" in name:
        ghs.append("부식성")

    if any(k in name for k in ["amine","phenol","cresol"]):
        ghs.append("독성")

    if "formaldehyde" in name:
        ghs.append("발암성")

    if any(k in name for k in ["acid","aldehyde","cresol"]):
        ghs.append("눈 자극")

    return uniq(ghs)


# -----------------------------
# PPE 자동 생성
# -----------------------------
def infer_ppe(name, ghs):

    ppe = ["보호장갑","보호안경"]

    if "인화성" in ghs:
        ppe.append("유기용제용 방독마스크")
        ppe.append("보호복")

    if "부식성" in ghs:
        ppe.append("내화학성 장갑")
        ppe.append("안면보호구")

    if "독성" in ghs:
        ppe.append("방독마스크")

    if "발암성" in ghs:
        ppe.append("화학방호복")

    return uniq(ppe)


# -----------------------------
# 보관방법 자동 생성
# -----------------------------
def infer_storage(name, ghs):

    storage = []

    if "인화성" in ghs:
        storage += ["화기엄금","환기보관","밀폐용기"]

    if "부식성" in ghs:
        storage += ["산 전용 보관","금속 접촉 주의"]

    if not storage:
        storage += ["건냉소 보관"]

    return uniq(storage)


# -----------------------------
# 위험도 점수 계산
# -----------------------------
def infer_scores(name, ghs):

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

    hazard = min(hazard,5)
    danger = min(danger,5)

    return hazard, danger


# -----------------------------
# DB 항목 업그레이드
# -----------------------------
def upgrade_item(item):

    name = item.get("name_en") or ""

    # 한국어 이름 변환
    name_ko = normalize_name_ko(name)

    ghs = infer_ghs(name)

    ppe = infer_ppe(name, ghs)

    storage = infer_storage(name, ghs)

    hazard_score, danger_score = infer_scores(name, ghs)

    item["name_ko"] = name_ko
    item["ghs"] = ghs
    item["ppe"] = ppe
    item["storage"] = storage
    item["hazard_score"] = hazard_score
    item["danger_score"] = danger_score

    return item


# -----------------------------
# 메인 실행
# -----------------------------
def main():

    db = load_js_db(INPUT_FILE)

    upgraded = []

    for item in db:

        upgraded.append(upgrade_item(item))

    output = "const CHEMICAL_DB = " + json.dumps(upgraded, ensure_ascii=False, indent=2) + ";"

    Path(OUTPUT_FILE).write_text(output, encoding="utf-8")

    print("완료")
    print("총 화학물질:",len(upgraded))
    print("파일:",OUTPUT_FILE)


if __name__ == "__main__":
    main()