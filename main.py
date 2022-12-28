import os
import time

import pyautogui
from pynput import keyboard
import botfunctions
import core
import gui
from bot import Bot


def hotkey_exit_program():
    pyautogui.press('shift')
    # noinspection PyUnresolvedReferences,PyProtectedMember
    os._exit(0)


if __name__ == '__main__':
    keyboard.GlobalHotKeys({'<ctrl>+c': hotkey_exit_program}).start()

    pyautogui.FAILSAFE = False
    core.find_runelite_window()
    bot_instance = Bot()
    gui.build_ui(bot_instance)
    gui.update_loop()

    core.configure_ui_window()

    while True:
        gui.update_loop()
