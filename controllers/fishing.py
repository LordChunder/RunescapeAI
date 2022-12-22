import random
import time

import pyautogui

import antiafk
import botfunctions
import ocr

iconName = 'shrimp.png'

global running, inventoryCount


def start_fishing(dispose="BANK"):
    global running, inventoryCount

    running = True
    while running:
        botfunctions.is_inventory_full()
        botfunctions.open_inventory()
        inventoryCount = ocr.image_count(iconName, 0.7)
        print("Inventory fish count: ", inventoryCount)

        if botfunctions.is_inventory_full():
            if dispose == "BANK":
                deposit_in_bank()
            drop_all_fish()

            running = False
        else:
            print("Fishing")
            ocr.find_object(0)
            antiafk.random_break(8, 15)

        antiafk.random_action()
        # antiafk.random_phrase_speak()


def drop_all_fish():
    print("Dropping fish")
    botfunctions.drop_item()
    ocr.image_rec_click_all(iconName)
    botfunctions.release_drop_item()


def deposit_in_bank():
    antiafk.random_break(1, 3)
    print("Depositing fish in bank")
    antiafk.random_break(.3, .8)
    ocr.find_object(4)
    antiafk.random_break(20, 25)
    ocr.find_object(4)
    antiafk.random_break(.7, 1.5)
    drop_all_fish()
    antiafk.random_break(1, 3)
    pyautogui.press('esc')
    antiafk.random_break(.4, 1.2)
    botfunctions.move(-1 * random.randint(1, 4), -1 * random.randint(5, 9))
    antiafk.random_break(2, 4)
