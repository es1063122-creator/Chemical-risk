import requests
import json
import time

chemicals = [
"acetone","toluene","xylene","methanol","ethanol",
"isopropanol","ethyl acetate","butyl acetate","styrene",
"benzene","phenol","aniline","cyclohexane","n-hexane",
"formaldehyde","ammonia","hydrogen peroxide","acetic acid",
"sulfuric acid","hydrochloric acid"
]

db=[]

for name in chemicals:

    url=f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/IUPACName,MolecularFormula/JSON"

    r=requests.get(url)

    try:
        data=r.json()["PropertyTable"]["Properties"][0]

        db.append({
            "name_en":name,
            "iupac":data["IUPACName"],
            "formula":data["MolecularFormula"]
        })

    except:
        pass

    time.sleep(0.2)

with open("chemical-db.json","w",encoding="utf-8") as f:
    json.dump(db,f,ensure_ascii=False,indent=2)

print("DB 생성 완료")