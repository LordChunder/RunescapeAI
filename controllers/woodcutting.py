import random
import time
import pyautogui

import antiafk
import botfunctions
import imgdetection

global running, bot_instance, wood_id


def start_woodcutting(ibot, wood_selection=1511, dispose='BANK'):
    global running, bot_instance, wood_id
    bot_instance = ibot
    wood_id = wood_selection
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
            bot_instance.bot_status.value = 3
            imgdetection.object_rec_click_closest_single('woodcutting_trees')
            bot_instance.bot_status.value = 0
            antiafk.random_break(8, 15)

        antiafk.random_action()


def drop_all_wood():
    print("Dropping wood")
    bot_instance.bot_status.value = 4
    botfunctions.drop_item()
    imgdetection.image_rec_click_all(wood_id)
    botfunctions.release_drop_item()


def deposit_in_bank():
    antiafk.random_break(1, 3)
    print("Depositing wood in bank")
    bot_instance.bot_status.value = 2
    imgdetection.object_rec_click_closest_single('bank_highlight')
    antiafk.random_break(15, 19)
    imgdetection.object_rec_click_closest_single('bank_highlight')
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

    bot_instance.bot_status.value = 5
    burnCount = 0
    timeoutCount = 0

    imgdetection.object_rec_click_closest_single('woodcutting_fire_spot')  # Click the starting point on the screen to move there

    antiafk.random_break(8, 15)

    inventory_count = botfunctions.inventory_count(wood_id)
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
        imgdetection.image_rec_click_single(wood_id)
        antiafk.random_break(0.1, 1)
        imgdetection.image_rec_click_single(590)
        timeout = time.time() + random.uniform(10, 15)

        # check for XP gain
        lastXP = botfunctions.get_xp_for_skill('Firemaking')
        while True:
            xp = botfunctions.get_xp_for_skill('Firemaking')
            if 0 < xp > lastXP:
                print("Fire made (XP Gained)", xp, lastXP)
                inventory_count = botfunctions.inventory_count(wood_id)
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
