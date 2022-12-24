# noinspection PyPackageRequirements
import win32gui
import yaml

global hwnd


def read_config():
    global config_yaml
    with open('config.yaml', 'r') as file:
        config_yaml = yaml.safe_load(file)


global config_yaml
read_config()


def configure_ui_window():
    window = win32gui.FindWindow(None, "RunescapeAI")

    rect = win32gui.GetWindowRect(window)
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    win32gui.MoveWindow(window, 900, 0, w, h, True)


def find_runelite_window():  # returns PID of runelite app
    global hwnd
    hwnd = win32gui.FindWindow(None, config_yaml['client_title'] + config_yaml['user']['user_name'])
    print("Found runescape client window as: ", hwnd)

    win32gui.MoveWindow(hwnd, 0, -25, 865, 830, True)
    win32gui.SetActiveWindow(hwnd)
    win32gui.SetForegroundWindow(hwnd)


def get_window_size():
    return 0, 0, 865, 830 - 25
