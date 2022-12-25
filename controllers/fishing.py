import random

import pyautogui

import antiafk
import botfunctions
import imgdetection

global running, fish_ids, bot_instance


def start_fishing(ibot, fish_selection=[317, 321], dispose='BANK'):
    global running, fish_ids, bot_instance
    bot_instance = ibot
    fish_ids = fish_selection
    running = True
    while running:
        botfunctions.open_inventory()

        if botfunctions.is_inventory_full():
            if dispose == "BANK":
                deposit_in_bank()
            drop_all_fish()

            running = False
        else:
            bot_instance.bot_status.value = 3
            imgdetection.object_rec_click_closest_single('fishing_spot')
            bot_instance.bot_status.value = 0
            antiafk.random_break(8, 15)

        antiafk.random_action()


def drop_all_fish():
    print("Dropping fish")
    bot_instance.bot_status.value = 4
    botfunctions.drop_item()
    for item_id in fish_ids:
        imgdetection.image_rec_click_all(item_id)
    botfunctions.release_drop_item()


def deposit_in_bank():
    antiafk.random_break(1, 3)
    bot_instance.bot_status.value = 2
    print("Depositing fish in bank")
    antiafk.random_break(.3, .8)
    imgdetection.object_rec_click_closest_single('bank_highlight')
    antiafk.random_break(20, 25)
    imgdetection.object_rec_click_closest_single('bank_highlight')
    antiafk.random_break(.7, 1.5)
    drop_all_fish()
    antiafk.random_break(1, 3)
    pyautogui.press('esc')
    antiafk.random_break(.4, 1.2)
    botfunctions.move(-1 * random.randint(1, 4), -1 * random.randint(5, 9))
    antiafk.random_break(2, 4)
