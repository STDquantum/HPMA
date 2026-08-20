import json

def split_swipe(item):
    """将一个swipe分成多个两点之间的swipe，并平分帧"""
    start_frame = item["start_frame"]
    end_frame = item["end_frame"]
    total_points = item["points"]

    # 分段数量 = 点数 - 1
    segments = []
    num_segments = len(total_points) - 1
    if num_segments <= 0:
        return []

    total_frames = end_frame - start_frame + 1
    frames_per_segment = total_frames / num_segments

    for i in range(num_segments):
        seg_start_frame = int(round(start_frame + i * frames_per_segment))
        seg_end_frame = int(round(start_frame + (i + 1) * frames_per_segment)) - 1
        if seg_end_frame < seg_start_frame:
            seg_end_frame = seg_start_frame

        segments.append({
            "type": "swipe",
            "frame": seg_start_frame,
            "start_frame": seg_start_frame,
            "end_frame": seg_end_frame,
            "points": [total_points[i], total_points[i + 1]]
        })

    return segments

def adjust_swipe_timings(sorted_actions):
    """调整swipe的结束帧，避免重叠下一个操作"""
    for i in range(len(sorted_actions) - 1):
        curr = sorted_actions[i]
        next_ = sorted_actions[i + 1]
        next_start_frame = next_.get("start_frame", None) or next_["frame"]
        if curr["type"] == "swipe":
            if curr["end_frame"] >= next_start_frame:
                # 将结束帧限制在下一操作开始帧之前
                print(curr, next_start_frame)
                curr["end_frame"] = max(curr["start_frame"], next_start_frame - 1)
    return sorted_actions

# === 主流程 ===

with open("annotation_all_transformed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = []

for item in data:
    if item["type"] == "swipe":
        new_data.extend(split_swipe(item))
    else:
        new_data.append(item)

# 按照 frame 排序
new_data.sort(key=lambda x: x.get("frame", x.get("start_frame", 0)))

# 调整swipe的结束帧
new_data = adjust_swipe_timings(new_data)

# 保存结果
with open("annotation_all_transformed_split_sorted.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
