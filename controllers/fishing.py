import random

import pyautogui

import antiafk
import botfunctions
import imgdetection

global running, fish_icon


def start_fishing(fish='shrimp.png', dispose='BANK'):
    global running, fish_icon
    fish_icon = fish
    running = True
    while running:
        botfunctions.open_inventory()
        inventory_full = botfunctions.is_inventory_full()
        print("Inventory full: ", inventory_full)

        if inventory_full:
            if dispose == "BANK":
                deposit_in_bank()
            drop_all_fish()

            running = False
        else:
            print("Fishing")
            imgdetection.find_object(0)
            antiafk.random_break(8, 15)

        antiafk.random_action()


def drop_all_fish():
    print("Dropping fish")
    botfunctions.drop_item()
    imgdetection.image_rec_click_all(fish_icon)
    botfunctions.release_drop_item()


def deposit_in_bank():
    antiafk.random_break(1, 3)
    print("Depositing fish in bank")
    antiafk.random_break(.3, .8)
    imgdetection.find_object(4)
    antiafk.random_break(20, 25)
    imgdetection.find_object(4)
    antiafk.random_break(.7, 1.5)
    drop_all_fish()
    antiafk.random_break(1, 3)
    pyautogui.press('esc')
    antiafk.random_break(.4, 1.2)
    botfunctions.move(-1 * random.randint(1, 4), -1 * random.randint(5, 9))
    antiafk.random_break(2, 4)
