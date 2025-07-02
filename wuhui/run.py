import time
import os
import json
import subprocess

FPS = 24.28880727910546  # 视频帧率

with open("annotation_all_transformed_split_sorted.json", "r", encoding="utf-8") as f:
    all_ops = json.load(f)

first_click = [1787, 898]
video_offset = 37 - 26.928  # 视频开始延迟（可调）

# 执行第一次点击
subprocess.run(f"adb shell input tap {first_click[0]} {first_click[1]}", shell=True)
time.sleep(video_offset - 0.22)

# 记录视频开始时间
video_start = time.time()

for op in all_ops:
    # 计算操作应该发生的时间点
    op_time = op["frame"] / FPS
    
    # 等待到操作时间点
    while True:
        elapsed = time.time() - video_start
        if elapsed >= op_time:
            break
        # 高频检查但避免CPU占用过高
        time.sleep(0.001)  # 1ms精度
    
    if op["type"] == "click":
        x, y = op["pos"]
        subprocess.run(f"adb shell input tap {x} {y}", shell=True)
        
    elif op["type"] == "swipe":
        points = op["points"]
        start_frame = op["start_frame"]
        end_frame = op.get("end_frame", start_frame + len(points) - 1)
        duration_ms = max(10, int((end_frame - start_frame) / FPS * 1000))
        
        # 取首尾点作为滑动
        x1, y1 = points[0]
        x2, y2 = points[-1]
        subprocess.run(f"adb shell input swipe {x1} {y1} {x2} {y2} {duration_ms}", shell=True)

print("所有操作执行完成")