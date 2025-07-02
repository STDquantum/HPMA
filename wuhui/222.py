import json
import math

def transform(coord):
    return [math.ceil(coord[0] / 576 * 1080), math.ceil((coord[1] - 72) / 576 * 1080)]

with open('annotation_all.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = []

for item in data:
    if item['type'] == 'swipe' and 'points' in item:
        start = item['start_frame']
        end = item['end_frame']
        points = item['points']
        count = len(points)
        
        if count == 1:
            frames = [start]
        else:
            step = (end - start) / (count - 1)
            frames = [round(start + i * step) for i in range(count)]
        
        for i, pt in enumerate(points):
            new_data.append({
                "type": "click",
                "frame": frames[i],
                "pos": transform(pt)
            })
    elif item['type'] == 'click' and 'pos' in item:
        item['pos'] = transform(item['pos'])
        new_data.append(item)

# 保存变换后的结果
with open('annotation_all_clickified.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
