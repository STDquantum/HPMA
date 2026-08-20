import requests
import json

a = {}

for i in range(1000, 2200):
    url = f"https://nie.res.netease.com/nie/hlbt/zfj/cards/{i}.png?v=1"
    res = requests.get(url)
    if res.status_code == 200:
        a[i] = {}
        file = f"result\\{i}.png"
        open(file, "wb").write(res.content)
        print(f"Downloaded {file}")

json.dump(a, open("下载成功编号.json", "w", encoding="utf-8"), indent=4)
