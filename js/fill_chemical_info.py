import json
import requests
import time

INPUT_FILE = "chemical_db.json"
OUTPUT_FILE = "chemical_db_filled.json"

def get_pubchem_data(cas):

    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/property/MolecularFormula,MolecularWeight,IUPACName/JSON"

        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return None

        data = r.json()

        props = data["PropertyTable"]["Properties"][0]

        return {
            "formula": props.get("MolecularFormula", ""),
            "weight": props.get("MolecularWeight", ""),
            "iupac": props.get("IUPACName", "")
        }

    except:
        return None


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chemicals = json.load(f)

    total = len(chemicals)

    for i, chem in enumerate(chemicals):

        cas = chem["cas_no"]

        print(f"{i+1}/{total} 조회중:", cas)

        info = get_pubchem_data(cas)

        if info:

            chem["formula"] = info["formula"]
            chem["molecular_weight"] = info["weight"]

            if not chem["name"]["en"]:
                chem["name"]["en"] = info["iupac"]

        time.sleep(0.2)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chemicals, f, indent=2, ensure_ascii=False)

    print("완료:", OUTPUT_FILE)


if __name__ == "__main__":
    main()