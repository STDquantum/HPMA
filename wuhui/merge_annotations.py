import json

with open("annotation_click.json", "r", encoding="utf-8") as f:
    clicks = json.load(f)

with open("annotation_swipe.json", "r", encoding="utf-8") as f:
    swipes = json.load(f)

# 标准化格式（加入统一的 frame 字段）
clicks_sorted = [{"type": "click", "frame": item["frame"], "pos": item["pos"]} for item in clicks]
swipes_sorted = [{"type": "swipe", "frame": item["start_frame"], **item} for item in swipes]

# 合并 + 排序
all_ops = clicks_sorted + swipes_sorted
all_ops.sort(key=lambda x: x["frame"])

with open("annotation_all.json", "w", encoding="utf-8") as f:
    json.dump(all_ops, f, indent=2)

print(f"[✔] 合并完成，共 {len(all_ops)} 项，已保存到 annotation_all.json")
    