import json
import requests
import time

CAS_LIST_FILE = "cas_list.txt"

DB = []

def get_pubchem_data(cas):

    try:

        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/property/Title/JSON"

        r = requests.get(url,timeout=10)

        data = r.json()

        name = data["PropertyTable"]["Properties"][0]["Title"]

        return name

    except:

        return None


with open(CAS_LIST_FILE,"r") as f:

    cas_list = [x.strip() for x in f.readlines()]

for cas in cas_list:

    print("검색:",cas)

    name = get_pubchem_data(cas)

    if not name:
        continue

    item = {

        "cas":cas,

        "name_ko":name,
        "name_en":name,
        "name_ja":name,

        "category":"chemical",

        "ghs":[],
        "ppe":["보호장갑","보호안경"],
        "storage":[],

        "hazard_score":3,
        "danger_score":3

    }

    DB.append(item)

    time.sleep(0.2)

print("총:",len(DB))

with open("chemical-db-800.js","w",encoding="utf-8") as f:

    f.write("const CHEMICAL_DB = ")
    json.dump(DB,f,ensure_ascii=False,indent=2)