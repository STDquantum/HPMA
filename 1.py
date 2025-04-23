import requests
import json

a = {}

for i in range(2600, 3200):
    url = f"https://nie.res.netease.com/nie/hlbt/zfj/cards/{i}.png?v=1"
    res = requests.get(url)
    if res.status_code == 200:
        a[i] = {}
        file = f"result\\{i}.png"
        open(file, "wb").write(res.content)

json.dump(a, open("cards.json", "w", encoding="utf-8"), indent=4)
