import json
import math

def transform(coord):
    return [math.ceil(coord[0] / 576 * 1080), math.ceil((coord[1] - 72) / 576 * 1080)]

with open('annotation_all.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if item['type'] == 'swipe' and 'points' in item:
        item['points'] = [transform(pt) for pt in item['points']]
    elif item['type'] == 'click' and 'pos' in item:
        item['pos'] = transform(item['pos'])

# 保存到一个新文件
with open('annotation_all_transformed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
