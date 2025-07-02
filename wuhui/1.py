import cv2
import os
import json
import numpy as np

VIDEO = "video.mp4"
FRAME_FOLDER = "frames"
os.makedirs(FRAME_FOLDER, exist_ok=True)

cap = cv2.VideoCapture(VIDEO)
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
# frame_id = -1
# operations = []

# while cap.isOpened():
#     frame_id += 1
#     ret, frame = cap.read()
#     if not ret:
#         break
#     if frame_id < 883:
#         continue


#     timestamp = frame_id / fps
#     display_frame = frame.copy()  # 用于显示的帧

#     # ---- HSV变换并筛选三种颜色区域 ----
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     # 粉色（点击型）
#     lower_pink = np.array([140, 100, 100])
#     upper_pink = np.array([170, 255, 255])
#     mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)
#     contours, _ = cv2.findContours(mask_pink, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # for cnt in contours:
#     #     area = cv2.contourArea(cnt)
#     #     if area > 200:  # 过滤小噪点
#     #         (x, y), r = cv2.minEnclosingCircle(cnt)
#     #         operations.append({"type": "click", "time": timestamp, "pos": [int(x), int(y)]})

#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         if area > 2000:  # 过滤小噪点
#             (x, y), r = cv2.minEnclosingCircle(cnt)
#             operations.append({"type": "click", "time": timestamp, "pos": [int(x), int(y)]})
#             # 在显示帧上绘制检测结果
#             cv2.circle(display_frame, (int(x), int(y)), int(r), (255, 0, 255), 2)  # 粉色圆圈
#             cv2.putText(display_frame, f"Click: ({int(x)},{int(y)})", (int(x), int(y)-10), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#     # 显示信息
#     cv2.putText(display_frame, f"Frame: {frame_id} Time: {timestamp:.2f}s", (10, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


#     # TODO：识别紫色滑动和橙色长按（用历史帧跟踪）

#     # 保存帧（可选）
#     cv2.imwrite(f"{FRAME_FOLDER}/frame_{frame_id:05d}.png", frame)
#     cv2.imwrite(f"{FRAME_FOLDER}/display_{frame_id:05d}.png", display_frame)
#     cv2.imwrite(f"{FRAME_FOLDER}/mask_pink_{frame_id:05d}.png", mask_pink)

# cap.release()

# # 保存操作信息
# with open("ops.json", "w") as f:
#     json.dump(operations, f, indent=2)
