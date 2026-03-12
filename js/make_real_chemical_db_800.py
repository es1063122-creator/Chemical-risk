import requests
import json
import re
import time

CAS_PATTERN = r"\b\d{2,7}-\d{2}-\d\b"

db=[]
cid=1

while len(db) < 800:

    url=f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON"

    try:
        r=requests.get(url,timeout=10)

        data=r.json()

        synonyms=data["InformationList"]["Information"][0]["Synonym"]

        cas=""
        name=""

        for s in synonyms:

            if re.search(CAS_PATTERN,s):
                cas=s
                break

        name=synonyms[0]

        if cas!="":

            db.append({
                "cas":cas,
                "name_ko":name,
                "name_en":name,
                "name_ja":name,
                "name_vi":name,
                "category":"chemical",
                "ghs":[],
                "ppe":["보호장갑","보호안경"],
                "storage":[],
                "hazard_score":3,
                "danger_score":3
            })

            print("추가:",cas,name)

    except:
        pass

    cid+=1
    time.sleep(0.2)

with open("chemical-db-800.js","w",encoding="utf-8") as f:

    f.write("const CHEMICAL_DB = ")
    json.dump(db,f,ensure_ascii=False,indent=2)

print("완료:",len(db))