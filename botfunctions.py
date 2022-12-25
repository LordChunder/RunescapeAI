import random
import time

import pyautogui
import requests

import antiafk
import imgdetection
from core import config_yaml


def drop_item():
    pyautogui.keyUp('shift')
    c = random.uniform(0.1, 0.2)
    d = random.uniform(0.2, 0.23)

    time.sleep(c)
    pyautogui.keyDown('shift')
    time.sleep(d)


def release_drop_item():
    e = random.uniform(0.2, 0.3)
    f = random.uniform(0.1, 0.2)

    time.sleep(e)
    pyautogui.keyUp('shift')
    pyautogui.press('shift')
    time.sleep(f)


def open_inventory():
    e = random.uniform(0.2, 0.3)
    f = random.uniform(0.1, 0.2)

    time.sleep(e)
    pyautogui.press("f1")
    time.sleep(f)
    pyautogui.press("f4")


def get_xp_for_skill(skill_name):
    try:
        r = requests.get("http://localhost:8081/stats")
        if r.status_code != 200:
            return 0
        json = r.json()
        del json[0]

        for skill in json:
            if skill['stat'] == skill_name:
                return skill['xp']
        return 0
    except Exception:
        return 0


def inventory_count(item_id=0):
    try:
        r = requests.get("http://localhost:8081/inv")
        count = 0
        for item in r.json():
            if item_id is None:
                if item['id'] != 1:
                    count += 1
            else:
                if item['id'] == item_id:
                    count += 1

        print("Inventory count:", item_id, count)
        return count
    except Exception:
        print("Failed to get inventory count")
        return False


def is_inventory_full():
    try:
        r = requests.get("http://localhost:8081/inv")
        arr = []
        for item in r.json():
            if item['id'] != -1:
                arr.insert(0, item)
        isFull = len(arr) == 28
        print("Inventory is full: ", isFull)
        return isFull
    except Exception:
        print("Failed to get inventory count")
        return False


def logout():
    b = random.uniform(0.2, 0.7)
    coord = 803 + random.randint(0, 8), 3 + random.randint(0, 8),
    pyautogui.moveTo(coord, duration=b)
    b = random.uniform(0.1, 0.3)
    pyautogui.click(coord, duration=b, button='left')
    antiafk.random_break(.6, 1.5)
    imgdetection.image_rec_click_single(config_yaml['images']['logout_button'])


def login():
    antiafk.random_break(.7, 1.6)
    pyautogui.press('enter')
    antiafk.random_break(.8, 1.8)
    pyautogui.typewrite(config_yaml['user']['password'], interval=random.uniform(.2, .5))
    antiafk.random_break(.8, 1.8)
    pyautogui.press('enter')
    antiafk.random_break(5, 8)
    imgdetection.image_rec_click_single(config_yaml['images']['play_button'])
    antiafk.random_break(3, 8)


def sleep():
    print("Logging out and sleeping")
    logout()
    antiafk.random_break(30 * 60, 1.25 * 60 * 60)
    print("Logging in and restarting")
    login()


def move(dX=0, dY=0):
    b = random.uniform(0.2, 0.7)
    antiafk.random_break(0.1, 3)
    coord = 385 + 23 * dX, 400 - 20 * dY
    print(dX, dY)
    pyautogui.moveTo(coord, duration=b)
    antiafk.random_break(0.3, 1)
    pyautogui.click(button='left')
    antiafk.random_break(.8, 1.5)
