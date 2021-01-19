import win32gui,win32ui,win32con
import win32com, win32com.client
import win32api
import cv2
import numpy as np
import time
import random
import ctypes
import ctypes.wintypes
import threading

ORIG_SIZE = (450, 850)
AD_PT = (400, 780)
ORDER_PTS = [
    (170, 340),
    (280, 340),
    (370, 340),
    (170, 475),
    (280, 475),
    (370, 475),
]
FISH_PTS = [
    (190, 400),
    (290, 400),
    (390, 400),
    (190, 530),
    (290, 530),
    (390, 530),
]

WND_POS = None
EXIT_MSG = None

def click_on(x, y):
    win32api.SetCursorPos((x,y))
    action = win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_LEFTDOWN
    win32api.mouse_event(action, x, y, 0, 0)
    time.sleep(0.005)
    action = win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_LEFTUP
    win32api.mouse_event(action, x, y, 0, 0)

def click_on_order():
    for x, y in ORDER_PTS:
        x = WND_POS[0] + x
        y = WND_POS[1] + y
        click_on(x, y)
        time.sleep(0.05)

def click_on_fish():
    for x, y in FISH_PTS:
        x = WND_POS[0] + x
        y = WND_POS[1] + y
        click_on(x, y)
        time.sleep(0.05)

def click_on_ad(num):
    for _ in range(num):
        x = WND_POS[0] + AD_PT[0]
        y = WND_POS[1] + AD_PT[1]
        click_on(x, y)
        time.sleep(0.05)

def get_exit_msg():
    global EXIT_MSG
    user32 = ctypes.windll.user32
    if not user32.RegisterHotKey(None, 99, win32con.MOD_WIN, win32con.VK_F2):
        print("Unable to register id", 99)
    msg = ctypes.wintypes.MSG()
    if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
        if msg.message == win32con.WM_HOTKEY:
            if msg.wParam == 99:
                EXIT_MSG = True
                return

def run():
    # 获取窗口句柄
    handle = win32gui.FindWindow(None,"动物餐厅")
    if handle <= 0:
        print('没找到餐厅')
        exit(-1)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(handle)

    # 获取窗口的位置信息
    left, top, right, bottom = win32gui.GetWindowRect(handle)
    print('windows: (%d, %d, %d, %d)' % (left, top, right, bottom))
    # 窗口长宽
    width = right - left
    height = bottom - top

    msg_thread = threading.Thread(target=get_exit_msg)
    msg_thread.start()

    global WND_POS
    WND_POS = (left, top)
    for _ in range(100):
        click_on_ad(random.randint(20, 50))
        click_on_order()
        click_on_fish()
        if EXIT_MSG:
            exit(0)

if __name__=="__main__":
    run()