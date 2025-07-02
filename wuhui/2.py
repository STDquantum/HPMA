import cv2
import json

VIDEO_PATH = 'output.mp4'
OUTPUT_JSON = 'annotations.json'

cap = cv2.VideoCapture(VIDEO_PATH)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

frame_id = 0
annotations = []
swipe_buffer = []
swipe_start_frame = None
mode = "swipe"  # 当前操作模式

# 用于显示模式文字
mode_colors = {
    "click": (255, 0, 255),
    "hold_start": (0, 165, 255),
    "hold_end": (0, 100, 255),
    "swipe": (0, 255, 255)
}


def draw_info(frame, current_mode, fid):
    text = f"Mode: {current_mode} | Frame: {fid}/{total_frames}"
    cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, mode_colors[current_mode], 2)

def on_mouse(event, x, y, flags, param):
    global frame_id, annotations, mode, swipe_buffer, swipe_start_frame

    if mode != "swipe":
        if event == cv2.EVENT_LBUTTONDOWN:
            annotations.append({
                "frame": frame_id,
                "type": mode,
                "pos": [x, y]
            })
            print(f"[+] 添加标注：Frame {frame_id}, Type {mode}, Pos ({x}, {y})")
    else:
        if event == cv2.EVENT_LBUTTONDOWN:
            # 添加路径点
            if not swipe_buffer:
                swipe_start_frame = frame_id
            swipe_buffer.append([x, y])
            print(f"[+SWIPE] 添加途径点 {x}, {y}（当前长度: {len(swipe_buffer)}）")

        elif event == cv2.EVENT_RBUTTONDOWN:
            # 完成路径
            if len(swipe_buffer) >= 2:
                annotations.append({
                    "type": "swipe",
                    "start_frame": swipe_start_frame,
                    "end_frame": frame_id,
                    "points": swipe_buffer.copy()
                })
                print(f"[✔] 保存滑动路径，共 {len(swipe_buffer)} 点，起始帧: {swipe_start_frame}, 结束帧: {frame_id}")
            else:
                print("[!] 滑动路径点太少，至少需要 2 点")
            swipe_buffer.clear()
            swipe_start_frame = None

cv2.namedWindow("Video")
cv2.setMouseCallback("Video", on_mouse)

cnt = 0
while True:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    ret, frame = cap.read()
    cnt = cnt + 1
    if not ret:
        break

    show_frame = frame.copy()
    draw_info(show_frame, mode, frame_id)

    cv2.imshow("Video", show_frame)
    key = cv2.waitKey(0) & 0xFF

    if key == ord('d'):  # 下一帧
        frame_id = min(frame_id + 1, total_frames - 1)
    elif key == ord('a'):  # 上一帧
        frame_id = max(frame_id - 1, 0)
    elif key == ord('w'):  # 切换模式
        modes = list(mode_colors.keys())
        mode = modes[(modes.index(mode) + 1) % len(modes)]
        print(f"[切换模式] 当前模式：{mode}")
    elif key == ord('s'):  # 保存
        print(f"[✔] 已保存 {len(annotations)} 条标注到 {OUTPUT_JSON}")
    elif key == ord('q'):  # 退出
        break
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(annotations, f, indent=2)

cap.release()
cv2.destroyAllWindows()
 