import re

with open("chemical-db-800.js","r",encoding="utf-8") as f:
    text = f.read()

cas_list = re.findall(r'"cas":\s*"([^"]+)"',text)

with open("cas_list.txt","w") as f:
    for cas in cas_list:
        f.write(cas+"\n")

print("CAS 추출 완료:",len(cas_list))