import win32gui

import main
global hwnd


def find_runelite_window(userName):  # returns PID of runelite app
    global hwnd
    hwnd = win32gui.FindWindow(None, main.config_yaml['client_title'] + userName)
    print("Found runescape client window as: ", hwnd)

    win32gui.MoveWindow(hwnd, 0, -25, 865, 830, True)
    win32gui.SetActiveWindow(hwnd)
    win32gui.SetForegroundWindow(hwnd)


def get_window_size():
    return 0, 0, 865, 830
