import json
import requests
import time

INPUT_FILE = "chemical_db_filled.json"
OUTPUT_FILE = "chemical_db_ghs.json"

def get_pubchem_hazard(cas):

    try:

        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/classification/JSON"

        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return None

        return r.json()

    except:
        return None


def detect_ghs(hazard_text):

    ghs = {
        "physical": [],
        "health": [],
        "environment": []
    }

    text = hazard_text.lower()

    if "flammable" in text:
        ghs["physical"].append("Flammable")

    if "explosive" in text:
        ghs["physical"].append("Explosive")

    if "corrosive" in text:
        ghs["health"].append("Corrosive")

    if "toxic" in text:
        ghs["health"].append("Toxic")

    if "carcinogen" in text:
        ghs["health"].append("Carcinogenic")

    if "hazardous to aquatic" in text:
        ghs["environment"].append("Aquatic Hazard")

    return ghs


def generate_ppe(ghs):

    ppe = []

    if "Flammable" in ghs["physical"]:
        ppe.append("보호안경")
        ppe.append("내화학 장갑")

    if "Toxic" in ghs["health"]:
        ppe.append("방독마스크")

    if "Corrosive" in ghs["health"]:
        ppe.append("보안면")
        ppe.append("내화학 장갑")

    if "Carcinogenic" in ghs["health"]:
        ppe.append("호흡보호구")

    return list(set(ppe))


def generate_storage(ghs):

    storage = []

    if "Flammable" in ghs["physical"]:
        storage.append("화기엄금")
        storage.append("환기보관")

    if "Corrosive" in ghs["health"]:
        storage.append("산/알칼리 분리보관")

    return list(set(storage))


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chemicals = json.load(f)

    total = len(chemicals)

    for i, chem in enumerate(chemicals):

        cas = chem["cas_no"]

        print(f"{i+1}/{total} hazard 조회:", cas)

        data = get_pubchem_hazard(cas)

        if data:

            text = json.dumps(data)

            ghs = detect_ghs(text)

            chem["ghs"] = ghs
            chem["ppe"] = generate_ppe(ghs)
            chem["storage"] = generate_storage(ghs)

        time.sleep(0.2)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chemicals, f, indent=2, ensure_ascii=False)

    print("완료:", OUTPUT_FILE)


if __name__ == "__main__":
    main()