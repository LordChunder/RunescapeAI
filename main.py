import multiprocessing
import os
import random
import time

import pyautogui
from pynput import keyboard

import botfunctions
import core
import gui
from controllers import fishing, woodcutting, combat

modes = {0: woodcutting.start_woodcutting, 1: fishing.start_fishing, 2: combat.start_combat}

global bot_thread
bot_running = False


def start_bot(active_modes):
    global bot_thread, bot_running
    if bot_running:
        return

    bot_thread = multiprocessing.Process(target=bot_loop, args=(active_modes,))
    bot_thread.start()
    bot_running = True


def stop_bot():
    print("Stopping Bot")
    bot_thread.terminate()


def bot_loop(active_modes):
    pyautogui.FAILSAFE = False
    while True:
        run_core(active_modes)


def run_core(active_modes):
    print("Running modes: ", active_modes)
    runTimeSeconds = random.uniform(60 * 60 * 1.5, 60 * 60 * 4.5)
    stopTime = time.time() + runTimeSeconds
    timeTillBreak = stopTime - time.time()

    last_mode = None
    numModeRepeats = 0
    while timeTillBreak > 0:
        timeTillBreak = stopTime - time.time()
        (h, m) = divmod(timeTillBreak / 60, 60)
        print("Stopping in: ", h, m)

        index = active_modes[random.randint(0, len(active_modes) - 1)]
        mode = modes[index]
        if mode == last_mode:
            numModeRepeats += 1
        else:
            numModeRepeats = 0
        if numModeRepeats > 3 and len(active_modes) > 1:
            print("Force switching modes")
            while mode == last_mode:
                mode = modes[random.randint(0, len(modes) - 1)]

        mode()
        last_mode = mode

    botfunctions.sleep()


def on_exit_program():
    pyautogui.press('shift')
    # noinspection PyUnresolvedReferences,PyProtectedMember
    os._exit(0)


if __name__ == '__main__':
    hotkey = keyboard.GlobalHotKeys({'<ctrl>+c': on_exit_program})
    hotkey.start()

    pyautogui.FAILSAFE = False

    core.find_runelite_window()
    gui.build_ui()
