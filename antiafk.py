import random
import time
import pyautogui

nextActionTime = time.time() + random.randint(30, 180)


def random_break(min_sec, max_sec, msg=False):
    length = random.uniform(min_sec, max_sec)
    if msg:
        print("Breaking for (seconds): ", length)
    time.sleep(length)


def random_ui_tab(key):
    b = random.uniform(1.5, 15)
    pyautogui.press(key)
    time.sleep(b)
    pyautogui.press(key)
    b = random.uniform(1.5, 2)
    time.sleep(b)
    pyautogui.press('esc')


actions = {'inventory': 'f4',
           'combat': 'f1',
           'skills': 'f2',
           'quests': 'f3'}


def random_action():
    global nextActionTime

    if time.time() > nextActionTime:
        index = random.randint(0, len(actions) - 1)
        random_ui_tab(list(actions.values())[index])
        nextActionTime = time.time() + random.randint(30, 180)
