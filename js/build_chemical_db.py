import json
import re

input_file = "cas_list.txt"
output_file = "chemical_db.json"

def is_valid_cas(cas):

    pattern = r'^\d{2,7}-\d{2}-\d$'
    return re.match(pattern, cas)

def clean_cas_list():

    cas_set = set()

    with open(input_file, "r") as f:

        for line in f:

            cas = line.strip()

            if is_valid_cas(cas):
                cas_set.add(cas)

    return sorted(list(cas_set))


def build_db(cas_list):

    chemicals = []

    for cas in cas_list:

        chem = {

            "cas_no": cas,

            "name": {
                "ko": "",
                "en": "",
                "ja": ""
            },

            "synonyms": [],

            "formula": "",
            "molecular_weight": "",

            "physical_state": "",

            "ghs": {
                "physical": [],
                "health": [],
                "environment": []
            },

            "hazard_statements": [],
            "precautionary_statements": [],

            "ppe": [],
            "storage": []

        }

        chemicals.append(chem)

    return chemicals


def main():

    cas_list = clean_cas_list()

    chemicals = build_db(cas_list)

    with open(output_file, "w", encoding="utf-8") as f:

        json.dump(chemicals, f, indent=2, ensure_ascii=False)

    print("화학물질 DB 생성 완료")
    print("총 CAS 수:", len(chemicals))


if __name__ == "__main__":
    main()