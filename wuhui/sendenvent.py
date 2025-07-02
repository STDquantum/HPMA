import json
import time
import os

DEVICE = "/dev/input/event7"  # 修改成你的设备名
FPS = 24.28880727910546  # 用于估算滑动持续时间

def sendevent(code, value):
    os.system(f"adb shell su -c sendevent {DEVICE} {code} {value}")

def sendevent_all(type_code, code, value):
    os.system(f"adb shell su -c sendevent {DEVICE} {type_code} {code} {value}")

def send_touch_point(x, y):
    sendevent_all(3, 57, 0)        # ABS_MT_TRACKING_ID
    sendevent_all(3, 53, x)        # ABS_MT_POSITION_X
    sendevent_all(3, 54, y)        # ABS_MT_POSITION_Y
    sendevent_all(3, 58, 50)       # ABS_MT_PRESSURE
    sendevent_all(0, 2, 0)         # SYN_MT_REPORT
    sendevent_all(0, 0, 0)         # SYN_REPORT

def send_move_point(x, y):
    sendevent_all(3, 53, x)
    sendevent_all(3, 54, y)
    sendevent_all(0, 2, 0)
    sendevent_all(0, 0, 0)

def send_release():
    sendevent_all(3, 57, -1)
    sendevent_all(0, 2, 0)
    sendevent_all(0, 0, 0)

def run_swipe(points, duration_ms):
    delay = duration_ms / (len(points) - 1) / 1000.0  # 秒
    x0, y0 = points[0]
    send_touch_point(x0, y0)
    time.sleep(delay)

    for x, y in points[1:]:
        send_move_point(x, y)
        time.sleep(delay)

    send_release()
    # time.sleep(0.05)