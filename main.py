import pyautogui
import random
import subprocess
import time
import win32con
import win32gui
import configparser

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8-sig")
# 监控资源
BATTLE_NET_EXE = config['RESOURCES']['BATTLE_NET_EXE']
WOW_WINDOW_NAME = config['RESOURCES']['WOW_WINDOW_NAME']
BATTLE_NET_WINDOW_NAME = config['RESOURCES']['BATTLE_NET_WINDOW_NAME']

# 图像识别图片源
ENTER_GAME_IMAGE = config['IMAGES']['ENTER_GAME_IMAGE']
ONLINE_IMAGE = config['IMAGES']['ONLINE_IMAGE']

# 游戏内部按键
SPACE_KEY = config['KEYS']['SPACE_KEY']
ENTER_KEY = config['KEYS']['ENTER_KEY']
FIRST_KEY = config['KEYS']['FIRST_KEY']
SECOND_KEY = config['KEYS']['SECOND_KEY']

# 未检测在游戏内的重试次数，一次最大60s，总体最好不要超过5min（0~5取值）
RETRY_COUNT = 3


def open_wow():
    try:
        battlenet_window = win32gui.FindWindow(None, BATTLE_NET_WINDOW_NAME)
        win32gui.SetForegroundWindow(battlenet_window)
        print("战网正在运行...")
    except Exception as e:
        print("战网没有运行，即将运行战网...")
        subprocess.Popen(BATTLE_NET_EXE)
        time.sleep(20)
    finally:
        x, y = pyautogui.locateCenterOnScreen(ENTER_GAME_IMAGE)
        pyautogui.click(x, y)
        print("开始游戏...")
        time.sleep(20)
        wow_window = win32gui.FindWindow(None, WOW_WINDOW_NAME)
        win32gui.SetForegroundWindow(wow_window)
        pyautogui.press(ENTER_KEY)
        print("进入魔兽世界...")
        pyautogui.click(x, y)
        time.sleep(30)


if win32gui.FindWindow(None, WOW_WINDOW_NAME) == 0:
    open_wow()
retry_count = 0
while True:
    window = win32gui.FindWindow(None, WOW_WINDOW_NAME)
    win32gui.SetForegroundWindow(window)
    time.sleep(random.randint(3, 10))
    val = random.randint(1, 10)
    if val > 6:
        pyautogui.hotkey(FIRST_KEY)
    elif val > 3:
        pyautogui.keyDown("w")
        time.sleep(1)
        pyautogui.keyUp("w")
    else:
        pyautogui.hotkey("c")
    pyautogui.hotkey(SECOND_KEY)
    # position = pyautogui.locateCenterOnScreen(ONLINE_IMAGE)
    # if position is None:
    #     print("未找到角色在线标记...")
    #     retry_count = retry_count + 1
    #     if retry_count > RETRY_COUNT:
    #         print("长时间未找到角色标记，即将重启游戏...")
    #         win32gui.PostMessage(window, win32con.WM_CLOSE, 0, 0)
    #         open_wow()
    #         retry_count = 0
