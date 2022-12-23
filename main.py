import random
import time

import pyautogui
import pytesseract

import botfunctions
import core
from controllers import fishing, woodcutting, combat

modes = {0: woodcutting.start_woodcutting, 1: fishing.start_fishing, 2: combat.start_combat}

activeModes = [2]  # Set the active modes from above to run


def bot_loop(botMode):
    botMode()


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = core.config_yaml['tesseract_path'] + 'tesseract.exe'
    pyautogui.FAILSAFE = False
    core.find_runelite_window()
    time.sleep(1)

    botfunctions.login()
    lastMode = None
    while True:
        runTimeSeconds = random.uniform(60 * 60 * 1.5, 60 * 60 * 4.5)
        stopTime = time.time() + runTimeSeconds
        timeTillBreak = stopTime - time.time()

        numModeRepeats = 0

        while timeTillBreak > 0:
            timeTillBreak = stopTime - time.time()
            (h, m) = divmod(timeTillBreak / 60, 60)
            print("Stopping in: ", h, m)

            mode = modes[activeModes[random.randint(0, len(activeModes) - 1)]]
            if mode == lastMode:
                numModeRepeats += 1
            else:
                numModeRepeats = 0
            if numModeRepeats > 3 and len(activeModes) > 1:
                print("Force switching modes")
                while mode == lastMode:
                    mode = modes[random.randint(0, len(modes) - 1)]

            bot_loop(mode)
            lastMode = mode

        botfunctions.sleep()
