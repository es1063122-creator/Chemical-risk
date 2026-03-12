import json
import time
from google.cloud import translate_v2 as translate

INPUT_FILE = "chemical_db_upgraded.json"
OUTPUT_FILE = "chemical_db_final.json"

translate_client = translate.Client()

def translate_text(text, target):

    if not text:
        return ""

    try:
        result = translate_client.translate(
            text,
            target_language=target
        )

        return result["translatedText"]

    except:
        return text


with open(INPUT_FILE,"r",encoding="utf-8") as f:
    db=json.load(f)

for i,chem in enumerate(db):

    name_en = chem.get("name_en") or chem.get("name",{}).get("en","")

    print(i+1, name_en)

    ko = translate_text(name_en,"ko")
    ja = translate_text(name_en,"ja")

    chem["name_ko"] = ko
    chem["name_ja"] = ja
    chem["name_en"] = name_en

    if "name" in chem:

        chem["name"]["ko"] = ko
        chem["name"]["ja"] = ja

    time.sleep(0.1)


with open(OUTPUT_FILE,"w",encoding="utf-8") as f:
    json.dump(db,f,indent=2,ensure_ascii=False)

print("완료:",OUTPUT_FILE)