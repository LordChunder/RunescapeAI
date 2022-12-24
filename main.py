import os

import pyautogui
from pynput import keyboard

import core
import gui
from bot import Bot

bot_instance = Bot()


def on_exit_program():
    pyautogui.press('shift')
    # noinspection PyUnresolvedReferences,PyProtectedMember
    os._exit(0)


if __name__ == '__main__':
    hotkey = keyboard.GlobalHotKeys({'<ctrl>+c': on_exit_program})
    hotkey.start()
    pyautogui.FAILSAFE = False

    gui.build_ui()
    gui.update_loop()

    core.configure_ui_window()

    core.find_runelite_window()
    while True:
        gui.update_loop()
