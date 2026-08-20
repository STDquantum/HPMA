import cv2
import numpy as np
import subprocess
import time
import os
import requests

# 目标图像路径（你要识别的按钮截图）
ADJUST_PATH = 'button_star8.png'
START_PATH = 'button_start.png'
CONFIRM_PATH = 'button_confirm.png'
SCREENSHOT_PATH = 'screenshot.png'

# 截图手机屏幕并pull到本地
def capture_screenshot():
    subprocess.run(['adb', "-s", "HJS0219110007202", 'shell', 'screencap', '-p', '/sdcard/screenshot.png'])
    subprocess.run(['adb', "-s", "HJS0219110007202", 'pull', '/sdcard/screenshot.png', SCREENSHOT_PATH])

# 找到目标图像在屏幕上的位置
def find_template_on_screen(threshold=0.8, path=START_PATH):
    screen = cv2.imread(SCREENSHOT_PATH)
    template = cv2.imread(path)
    
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(f'Match confidence: {max_val:.2f}')
    if max_val >= threshold:
        # 计算中心点坐标
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return center_x, center_y
    else:
        return None

# 在手机上点击某个坐标
def adb_tap(x, y):
    subprocess.run(['adb', "-s", "HJS0219110007202", 'shell', 'input', 'tap', str(x), str(y)])

DINGWEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=c62419abe952f338c47f2904674cf20b51f9bfdd57b8d92606a615023587adc8"

def sendToDingTalk():
    try:
        requests.post(
            url=DINGWEBHOOK,
            json={
                "msgtype": "markdown",
                "markdown": {
                    "title": "并非考试成绩通知",
                    "text": f"## 考试成绩通知\n\n你的一个卡牌训练度刷完了",
                },
            },
        )
    except:
        print("钉钉成绩发送失败")

# 主程序
def main():
    global succ
    capture_screenshot()
    coord = find_template_on_screen(path=ADJUST_PATH)
    if coord:
        print(f'点击调整按钮: {coord}')
        adb_tap(*coord)
    else:
        print("未找到目标按钮")
        
    time.sleep(1)  # 等待1秒后再截图
    if coord:
        coord_wipe_start = (1524, 236)
        coord_wipe_end = (1524, 774)  # 假设按钮高度为100像素
        # 用 adb shell input wipe 划过这一段
        subprocess.run(['adb', "-s", "HJS0219110007202", 'shell', 'input', 'swipe', str(coord_wipe_start[0]), str(coord_wipe_start[1]),
                        str(coord_wipe_end[0]), str(coord_wipe_end[1]), '1000'])  # 持续时间为1000毫秒
        # 点击 1531 225
        adb_tap(1531, 225)
        time.sleep(1)  # 等待1秒后再截图
    else:
        return
    
    capture_screenshot()
    coord = find_template_on_screen(path=START_PATH)
    if coord:
        print(f'点击开始按钮: {coord}')
        adb_tap(*coord)
    else:
        print("未找到目标按钮")
    time.sleep(1)  # 等待1秒后再截图
    
    capture_screenshot()
    coord1 = find_template_on_screen(path=CONFIRM_PATH)
    if coord1:
        print(f'点击确认按钮坐标: {coord1}')
        adb_tap(*coord1)
    else:
        print("未找到确认按钮")
        
    if coord and coord1:
        succ += 1
        print(f'成功点击次数: {succ}')
        time.sleep(40)
        if succ == 3000:
            sendToDingTalk()
            subprocess.run(['adb', "-s", "HJS0219110007202", 'shell', 'input', 'keyevent', '26'])
            exit()
    else:
        time.sleep(1)  # 等待1秒后再截图

if __name__ == '__main__':
    succ = 0
    while True:
        main()
