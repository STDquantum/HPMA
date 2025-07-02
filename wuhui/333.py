import json
from collections import defaultdict

# 读入原始 JSON
with open("annotation_all_transformed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 根据类型分类（非 swipe 的直接保留）
others = [op for op in data if op["type"] != "swipe"]
swipes = [op for op in data if op["type"] == "swipe"]

# 按 start_frame 分组 swipe
grouped = defaultdict(list)
for op in swipes:
    grouped[op["start_frame"]].append(op)

merged_ops = []

for start_frame, ops in grouped.items():
    if len(ops) == 1:
        # 只有一个，不需要合并
        merged_ops.append(ops[0])
    else:
        # 合并为 multi_swipe
        multi_op = {
            "type": "multi_swipe",
            "frame": min(op["frame"] for op in ops),
            "start_frame": start_frame,
            "end_frame": max(op["end_frame"] for op in ops),
            "points": [op["points"] for op in ops]
        }
        merged_ops.append(multi_op)

# 合并后再和非 swipe 类型事件合并
all_merged = merged_ops + others

# 按 frame 排序，保持时间顺序
all_merged.sort(key=lambda x: x["frame"])

# 保存为新文件
with open("annotation_all_transformed_merged.json", "w", encoding="utf-8") as f:
    json.dump(all_merged, f, ensure_ascii=False, indent=2)

print("✅ 合并完成，结果已保存为 annotation_all_transformed_merged.json")
