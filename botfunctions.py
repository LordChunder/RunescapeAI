import random
import time

import pyautogui
import requests

import antiafk
import imgdetection
from core import config_yaml, options_yaml


def hold_drop_item_button():
    pyautogui.keyUp('shift')
    c = random.uniform(0.1, 0.3)
    d = random.uniform(0.1, 0.2)

    time.sleep(c)
    pyautogui.keyDown('shift')
    time.sleep(d)


def release_drop_item_button():
    e = random.uniform(0.1, 0.3)
    f = random.uniform(0.1, 0.2)

    time.sleep(e)
    pyautogui.keyUp('shift')
    pyautogui.press('shift')
    time.sleep(f)


def get_inv_json():
    r = None
    try:
        r = requests.get(config_yaml['morg_url'] + "/inv")
        json = r.json()
        r.close()
        return json
    except Exception as e:
        print("Morg HTTP Error /inv", e)
        if r is not None:
            r.close()
    return None


def drop_items(item_ids):
    json = get_inv_json()
    if json is None:
        return
    inv_rect = config_yaml['ui']['inv_rect']
    column_offset = (inv_rect[2] - inv_rect[0]) / 4
    row_offset = (inv_rect[3] - inv_rect[1]) / 7
    count = [0, 0]
    b = random.uniform(0.2, 0.5)
    pyautogui.moveTo(inv_rect[0] + random.randint(2, 10), inv_rect[1] + random.randint(2, 10), duration=b)
    hold_drop_item_button()
    for item in json:
        if item['quantity'] > 0 and item_ids.count(item['id']) > 0:
            mouse_pos = inv_rect[0] + column_offset * count[0] + random.randint(5, 15), \
                        inv_rect[1] + row_offset * count[1] + random.randint(5, 15)
            b = random.uniform(0.1, 0.3)
            pyautogui.moveTo(mouse_pos, duration=b)
            b = random.uniform(0.03, 0.05)

            pyautogui.click(duration=b, button='left')

        count[0] += 1
        if count[0] == 4:
            count[0] = 0
            count[1] += 1
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
    json = None
    r = None
    try:
        r = requests.get(config_yaml['morg_url'] + "/events")
        json = r.json()
        r.close()
    except Exception as e:
        print("Morg HTTP Error /events", e)
        if r is not None:
            r.close()
    return json


def get_xp_for_skill(skill_name):
    r = None
    try:
        r = requests.get(config_yaml['morg_url'] + "/stats")
        json = r.json()
        r.close()
        del json[0]
        for skill in json:
            if skill['stat'] == skill_name:
                return skill['xp']
        return 0
    except Exception as e:
        print("Failed to get xp for skill", skill_name, e)
        if r is not None:
            r.close()
        return 0


def inventory_count(item_id=None):
    json = get_inv_json()
    if json is None:
        return 0
    count = 0
    for item in json:
        if item_id is None:
            if item['id'] != -1:
                count += 1
        else:
            if item['id'] == item_id:
                count += 1
    print("Inventory count:", item_id, count)
    return count


def is_inventory_full():
    is_full = False
    if inventory_count() == 28:
        is_full = True
    print("Inventory is full: ", is_full)
    return is_full


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
    if options_yaml['general']['min_time_to_break'] is None:
        return
    print("Logging out and sleeping")
    logout()
    antiafk.random_break(options_yaml['general']['min_sleep_time'] * 60, 1.25 * 60 * 60)
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


def wait_until_idle(timeout=30):
    time_elapsed = 0
    start_time = time.time()
    event_json = get_events()
    if event_json is None:
        return
    start_position = event_json['worldPoint']
    while time_elapsed < timeout:
        event_json = get_events()
        if start_position != event_json['worldPoint'] and \
                event_json['animation pose'] == config_yaml['animation']['idle']:
            break

        time_elapsed = time.time() - start_time
        time.sleep(0.2)
