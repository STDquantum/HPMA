import json
import re

log_file = "滑动标注日志.txt"
output_json = "annotations.json"

annotations = []
current_points = []

with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()

        # 匹配途径点
        match = re.match(r"\[\+SWIPE\] 添加途径点 (\d+), (\d+)", line)
        if match:
            x, y = int(match.group(1)), int(match.group(2))
            current_points.append([x, y])
            continue

        # 匹配保存路径
        match = re.match(r"\[✔\] 保存滑动路径.+起始帧: (\d+), 结束帧: (\d+)", line)
        if match:
            start_frame = int(match.group(1))
            end_frame = int(match.group(2))
            annotations.append({
                "type": "swipe",
                "start_frame": start_frame,
                "end_frame": end_frame,
                "points": current_points.copy()
            })
            current_points.clear()

# 保存为 JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(annotations, f, indent=2)

print(f"[✔] 已保存 {len(annotations)} 条滑动标注到 {output_json}")
