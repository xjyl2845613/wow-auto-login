import pyautogui, time, random, win32gui, subprocess, win32con

# 监控资源
BATTLE_NET_EXE = r"C:\Program Files (x86)\Battle.net\Battle.net Launcher.exe"
WOW_WINDOW_NAME = "魔兽世界"
BATTLE_NET_WINDOW_NAME = "战网"

# 图像识别图片源
ENTER_GAME_IMAGE = "resources/entergame.png"
ONLINE_IMAGE = "resources/online.png"

# 游戏内部按键
SPACE_KEY = "space"
ENTER_KEY = "enter"
FIRST_KEY = "g"
SECOND_KEY = "v"

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
    time.sleep(random.randint(30, 60))
    val = random.randint(1, 10)
    if val > 6:
        pyautogui.press(FIRST_KEY)
    elif val > 3:
        pyautogui.press(SECOND_KEY)
    else:
        pyautogui.press(SPACE_KEY)
    position = pyautogui.locateCenterOnScreen(ONLINE_IMAGE)
    if position is None:
        print("未找到角色在线标记...")
        retry_count = retry_count + 1
        if retry_count > RETRY_COUNT:
            print("长时间未找到角色标记，即将重启游戏...")
            win32gui.PostMessage(window, win32con.WM_CLOSE, 0, 0)
            open_wow()
            retry_count = 0
