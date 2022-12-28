import random
import time

import pyautogui
import requests

import antiafk
import imgdetection
from core import config_yaml, options_yaml


def hold_drop_item_button():
    pyautogui.keyUp('shift')
    c = random.uniform(0.1, 0.2)
    d = random.uniform(0.2, 0.23)

    time.sleep(c)
    pyautogui.keyDown('shift')
    time.sleep(d)


def release_drop_item_button():
    e = random.uniform(0.2, 0.3)
    f = random.uniform(0.1, 0.2)

    time.sleep(e)
    pyautogui.keyUp('shift')
    pyautogui.press('shift')
    time.sleep(f)


def drop_items(item_ids):
    hold_drop_item_button()
    for item in item_ids:
        print("Dropping: ", item)
        imgdetection.image_rec_click_all(item)
    release_drop_item_button()


def open_inventory():
    e = random.uniform(0.2, 0.3)
    f = random.uniform(0.1, 0.2)

    time.sleep(e)
    pyautogui.press("f1")
    time.sleep(f)
    pyautogui.press("f4")


def do_banking(item_ids):
    for movement in options_yaml['general']['walk_before_bank']:
        move(movement)

    num_tries = 0
    while not imgdetection.contains_item_on_screen('bank_hud') and num_tries < 3:
        imgdetection.object_rec_click_closest_single('bank_highlight')
        wait_until_idle()
        num_tries += 1

    drop_items(item_ids)
    pyautogui.press('esc')
    antiafk.random_break(.4, 1.2)
    for movement in options_yaml['general']['walk_after_bank']:
        move(movement)

    antiafk.random_break(1.5, 2.7)


def get_events():
    r = requests.get(config_yaml['morg_url'] + "/events")

    if r.encoding is None:
        r.encoding = 'utf-8'
    print(r.json())
    return r.json()


def get_xp_for_skill(skill_name):
    try:
        r = requests.get(config_yaml['morg_url'] + "/stats")
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
        r = requests.get(config_yaml['morg_url'] + "/inv")
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
        r = requests.get(config_yaml['morg_url'] + "/inv")
        arr = []
        for item in r.json():
            if item['id'] != -1:
                arr.insert(0, item)
        is_full = len(arr) == 28
        print("Inventory is full: ", is_full)
        return is_full
    except Exception:
        print("Failed to get inventory count")
        return False


def logout():
    b = random.uniform(0.2, 0.7)
    coord = 803 + random.randint(0, 8), 30 + random.randint(0, 8),
    pyautogui.moveTo(coord, duration=b)
    b = random.uniform(0.1, 0.3)
    pyautogui.click(coord, duration=b, button='left')
    antiafk.random_break(.6, 1.5)
    imgdetection.image_rec_click_single('logout_button')


def login():
    antiafk.random_break(.7, 1.6)
    pyautogui.press('enter')
    antiafk.random_break(.8, 1.8)
    pyautogui.typewrite(config_yaml['user']['password'], interval=random.uniform(.2, .5))
    antiafk.random_break(.8, 1.8)
    pyautogui.press('enter')
    antiafk.random_break(5, 8)
    imgdetection.image_rec_click_single('play_button')
    antiafk.random_break(3, 8)


def sleep():
    print("Logging out and sleeping")
    logout()
    antiafk.random_break(30 * 60, 1.25 * 60 * 60)
    print("Logging in and restarting")
    login()


def move(position):
    print("Moving spaces: ", position[0], position[1])
    x, y = 420 + 25 * position[0], 425 - 20 * position[1]
    # add a random offset in px
    x += random.randrange(-3, 3)
    y += random.randrange(-3, 3)
    b = random.uniform(0.2, 0.7)
    pyautogui.moveTo([x, y], duration=b)
    antiafk.random_break(0.1, 0.3)
    pyautogui.click(button='left')
    wait_until_idle()


def wait_until_idle(timeout=10):
    time_elapsed = 0
    last_time = time.time()
    event_json = get_events()
    start_position = event_json['worldPoint']
    while time_elapsed < timeout:
        event_json = get_events()
        if start_position != event_json['worldPoint'] and \
                event_json['animation pose'] == config_yaml['animation']['idle']:
            break

        time_elapsed = time.time() - last_time
        last_time = time.time()
        time.sleep(0.2)
