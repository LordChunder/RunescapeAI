import win32com.client
# noinspection PyPackageRequirements
import win32gui
import yaml
import requests

global hwnd, item_yaml, config_yaml, options_yaml


def read_config():
    global config_yaml, item_yaml, options_yaml
    with open('config.yaml', 'r') as file:
        config_yaml = yaml.safe_load(file)
    with open('options.yaml', 'r') as file:
        options_yaml = yaml.safe_load(file)
    with open('items.yaml', 'r') as file:
        item_yaml = yaml.safe_load(file)


def configure_ui_window():
    window = win32gui.FindWindow(None, "RunescapeAI")

    rect = win32gui.GetWindowRect(window)
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]

    win32gui.MoveWindow(window, config_yaml['runelite_size'][0] + 30, 0, w, h, True)


def find_runelite_window():  # returns PID of runelite app
    global hwnd
    hwnd = win32gui.FindWindow(None, config_yaml['client_title'] + config_yaml['user']['user_name'])
    print("Found runescape client window as: ", hwnd)

    win32gui.MoveWindow(hwnd, 0, 0, config_yaml['runelite_size'][0], config_yaml['runelite_size'][1], True)
    win32gui.SetActiveWindow(hwnd)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')

    win32gui.SetForegroundWindow(hwnd)


def get_runelite_window_size(bot):
    return win32gui.GetWindowRect(bot.rl_hwnd)


read_config()
