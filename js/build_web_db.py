import json

INPUT_FILE = "chemical_db_ghs.json"
OUTPUT_FILE = "chemical-db-800.js"

def convert():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chemicals = json.load(f)

    web_db = []

    for chem in chemicals:

        item = {
            "name_ko": chem["name"].get("ko",""),
            "name_ja": chem["name"].get("ja",""),
            "name_en": chem["name"].get("en",""),
            "cas": chem.get("cas_no",""),

            "ghs": (
                chem["ghs"].get("physical",[]) +
                chem["ghs"].get("health",[]) +
                chem["ghs"].get("environment",[])
            ),

            "exposure": ["흡입","피부"],

            "ppe": chem.get("ppe",[]),

            "storage": chem.get("storage",[]),

            "hazardMethod": "컨트롤 밴딩",
            "dangerMethod": "위험성 스크리닝 도구",

            "hazardWeight": len(chem["ghs"].get("health",[])) + 2,
            "dangerWeight": len(chem["ghs"].get("physical",[])) + 2
        }

        web_db.append(item)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        f.write("window.CHEMICAL_DB = ")
        json.dump(web_db, f, ensure_ascii=False, indent=2)
        f.write(";")

    print("웹 DB 생성 완료:", OUTPUT_FILE)
    print("화학물질 수:", len(web_db))


if __name__ == "__main__":
    convert()