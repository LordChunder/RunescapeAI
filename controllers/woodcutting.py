import random
import time
import pyautogui

import antiafk
import botfunctions
import ocr

global running, icon_name

item_numbers = {'yew': 1515}


def start_woodcutting(wood_icon='willow.png', dispose='BANK'):
    global running, icon_name
    icon_name = wood_icon
    running = True

    while running:
        botfunctions.open_inventory()
        inventory_full = botfunctions.is_inventory_full()
        print("Inventory full: ", inventory_full)

        if inventory_full:
            if dispose == "BANK":
                deposit_in_bank()
            else:
                do_fire_making()

            drop_all_wood()
            running = False
        else:
            print("Chopping Wood")
            ocr.find_object(2)
            antiafk.random_break(8, 15)

        antiafk.random_action()
        # antiafk.random_phrase_speak()


def drop_all_wood():
    print("Dropping wood")
    botfunctions.drop_item()
    ocr.image_rec_click_all(icon_name)
    botfunctions.release_drop_item()


def deposit_in_bank():
    antiafk.random_break(1, 3)
    print("Depositing wood in bank")
    ocr.find_object(4)
    antiafk.random_break(15, 19)
    ocr.find_object(4)
    antiafk.random_break(.7, 1.5)
    drop_all_wood()
    antiafk.random_break(1, 3)
    pyautogui.press('esc')
    antiafk.random_break(.4, 1.2)
    botfunctions.move(-1 * random.randint(1, 4), -1 * random.randint(5, 9))
    antiafk.random_break(2, 4)


def do_fire_making(num_per_row=6):
    print("Burning Wood")
    antiafk.random_break(1, 3)

    burnCount = 0
    timeoutCount = 0

    ocr.find_object(4)

    antiafk.random_break(8, 15)

    inventory_count = botfunctions.inventory_count(item_numbers['yew'])
    while inventory_count > 0:
        if timeoutCount > 2:
            drop_all_wood()
            break

        if burnCount > num_per_row:
            antiafk.random_break(2, 4)
            botfunctions.move(num_per_row, -1)
            antiafk.random_break(2, 4)
            burnCount = 0

        # click on tinder and wood
        antiafk.random_break(0.1, 2)
        ocr.image_rec_click_single(icon_name, 5, 5, 0.75, 'left', 8)
        antiafk.random_break(0.1, 1)
        ocr.image_rec_click_single('tinderbox.png', 5, 5, 0.75, 'left', 8)
        timeout = time.time() + random.uniform(10, 15)

        # check for XP gain
        lastXP = botfunctions.get_xp_for_skill('Firemaking')
        while True:
            xp = botfunctions.get_xp_for_skill('Firemaking')
            if 0 < xp > lastXP:
                print("Fire made (XP Gained)", xp, lastXP)
                inventory_count = botfunctions.inventory_count(item_numbers['yew'])
                burnCount += 1
                timeoutCount = 0
                break

            if time.time() > timeout:
                print("Fire making timout")
                botfunctions.move(random.randint(0, 3), -1)
                antiafk.random_break(2, 4)
                burnCount = 0
                timeoutCount += 1
                break
