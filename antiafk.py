import random
import time

import pyautogui

global nextActionTime, nextPhraseTime, lastPhrase
nextActionTime = time.time() + random.randint(30, 180)
nextPhraseTime = 0
lastPhrase = 0

phrases = ["has anyone else been playing runescape since the early days?", "who knew grinding would be so peaceful lol",
           "ive been doing this for hours and barely leveled up...", "anyone wana buy wood?", "noob",
           "is this even worth it?", "is anyone level 99?", "can someone with members help me?",
           "can you help me get rune?", "i havent played in years can you help me?", "is this still worth grinding on?"]
random.shuffle(phrases)


def random_break(minSec, maxSec):
    length = random.uniform(minSec, maxSec)
    time.sleep(length)


def random_phrase_speak():
    global lastPhrase, nextPhraseTime
    if time.time() > nextPhraseTime:
        pyautogui.press('enter')
        random_break(.1, .4)
        pyautogui.typewrite(phrases[lastPhrase], interval=random.uniform(.2, .5))
        random_break(.3, 1.2)
        pyautogui.press('enter')
        random_break(.5, 1.2)
        lastPhrase += 1
        nextPhraseTime = time.time() + random.randint(600, 1250)
        if lastPhrase >= len(phrases):
            lastPhrase = 0
            random.shuffle(phrases)


def random_camera():
    print("Anti AFK: Random Camera")
    keys = ['left', 'right', 'up', 'down']
    i = 0
    while i < 3:
        key = keys[random.randint(0, 3)]
        pyautogui.keyDown(key)
        interval = random.uniform(.75, 2)
        time.sleep(interval)
        pyautogui.keyUp(key)
        i += 1
    pyautogui.keyDown('up')
    time.sleep(3)
    pyautogui.keyUp('up')


def random_inventory():
    print("Anti AFK: Random Inventory")
    b = random.uniform(1.5, 15)
    pyautogui.press('f4')
    time.sleep(b)
    pyautogui.press('f4')
    b = random.uniform(1.5, 2)
    time.sleep(b)
    pyautogui.press('esc')


def random_skills():
    print("Anti AFK: Random Skill")
    b = random.uniform(1.5, 15)
    pyautogui.press('f2')
    time.sleep(b)
    pyautogui.press('f2')
    b = random.uniform(1.5, 2)
    time.sleep(b)
    pyautogui.press('esc')


def random_combat():
    print("Anti AFK: Random Combat")
    b = random.uniform(1.5, 15)
    pyautogui.press('f1')
    time.sleep(b)
    pyautogui.press('f1')
    b = random.uniform(1.5, 2)
    time.sleep(b)
    pyautogui.press('esc')


def random_quests():
    print("Anti AFK: Random Quest")
    b = random.uniform(1.5, 15)
    pyautogui.press('f3')
    time.sleep(b)
    pyautogui.press('f3')
    b = random.uniform(1.5, 2)
    time.sleep(b)
    pyautogui.press('esc')


actions = {0: random_inventory,
           1: random_combat,
           2: random_skills,
           3: random_quests, }


def random_action():
    global nextActionTime
    if time.time() > nextActionTime:
        actions[random.randint(0, len(actions) - 1)]()
        nextActionTime = time.time() + random.randint(30, 180)
