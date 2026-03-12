import requests
import json
import time

INPUT_FILE = "chemical_db_ghs.json"
OUTPUT_FILE = "chemical_db_upgraded.json"

def get_pubchem_synonyms(cas):

    if not cas:
        return []

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/synonyms/JSON"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        syns = data["InformationList"]["Information"][0]["Synonym"]

        return syns[:10]

    except:
        return []


def translate_stub(name):
    return name


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    db = json.load(f)


for i, chem in enumerate(db):

    cas = chem.get("cas") or chem.get("cas_no")

    print(i+1, cas)

    synonyms = get_pubchem_synonyms(cas)

    chem["synonyms"] = synonyms

    name_en = chem.get("name_en", "")

    if not name_en and synonyms:
        name_en = synonyms[0]

    chem["name_en"] = name_en

    if not chem.get("name_ko"):
        chem["name_ko"] = translate_stub(name_en)

    if not chem.get("name_ja"):
        chem["name_ja"] = translate_stub(name_en)

    time.sleep(0.2)


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("완료:", OUTPUT_FILE)