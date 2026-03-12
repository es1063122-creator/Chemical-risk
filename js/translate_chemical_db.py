import json
import requests
from deep_translator import GoogleTranslator

INPUT = "chemical-db-800.js"
OUTPUT = "chemical-db-800-final.js"

def load_js():
    with open(INPUT, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace("window.CHEMICAL_DB =", "").strip()

    if text.endswith(";"):
        text = text[:-1]

    return json.loads(text)

def save_js(data):
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("window.CHEMICAL_DB = ")
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_name_from_cas(cas):

    url=f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/property/IUPACName/JSON"

    try:
        r=requests.get(url,timeout=5).json()
        return r["PropertyTable"]["Properties"][0]["IUPACName"]
    except:
        return None


data=load_js()

ko_trans=GoogleTranslator(source="en",target="ko")
ja_trans=GoogleTranslator(source="en",target="ja")

for i,chem in enumerate(data):

    cas=chem.get("cas")

    if not cas:
        continue

    en=chem.get("name_en")

    if en:

        chem["name_ko"]=ko_trans.translate(en)
        chem["name_ja"]=ja_trans.translate(en)

    print(i,"완료")

save_js(data)

print("완료: chemical-db-800-final.js 생성")