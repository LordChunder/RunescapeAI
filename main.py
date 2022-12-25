import os
from ctypes import windll
import pyautogui
from pynput import keyboard

import core
import gui
from bot import Bot


def on_exit_program():
    pyautogui.press('shift')
    # noinspection PyUnresolvedReferences,PyProtectedMember
    os._exit(0)


def set_dpi_aware():
    try:  # Windows 8.1 and later
        windll.shcore.SetProcessDpiAwareness(2)
    except Exception as e:
        pass
    try:  # Before Windows 8.1
        windll.user32.SetProcessDPIAware()
    except Exception:  # Windows 8 or before
        pass


if __name__ == '__main__':
    #set_dpi_aware()
    hotkey = keyboard.GlobalHotKeys({'<ctrl>+c': on_exit_program})
    hotkey.start()
    pyautogui.FAILSAFE = False
    core.find_runelite_window()
    bot_instance = Bot()
    gui.build_ui(bot_instance)
    gui.update_loop()

    core.configure_ui_window()

    while True:
        gui.update_loop()
