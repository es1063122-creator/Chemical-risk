import json
import requests
import time

INPUT_FILE = "chemical_db_upgraded.json"
OUTPUT_FILE = "chemical_db_translated.json"

def translate(text, target):

    if not text:
        return ""

    url = "https://translate.googleapis.com/translate_a/single"

    params = {
        "client":"gtx",
        "sl":"en",
        "tl":target,
        "dt":"t",
        "q":text
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        result = r.json()

        return result[0][0][0]

    except:
        return text


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    db = json.load(f)


for i, chem in enumerate(db):

    name_en = chem.get("name_en") or chem.get("name",{}).get("en")

    print(i+1, name_en)

    if not chem.get("name_ko"):
        chem["name_ko"] = translate(name_en, "ko")

    if not chem.get("name_ja"):
        chem["name_ja"] = translate(name_en, "ja")

    if "name" in chem:
        chem["name"]["ko"] = chem["name_ko"]
        chem["name"]["ja"] = chem["name_ja"]

    time.sleep(0.2)


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("번역 완료:", OUTPUT_FILE)