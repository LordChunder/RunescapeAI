import random
import time

import pyautogui

import antiafk
import botfunctions
import ocr

woodIcon = 'willow.png'
rowCount = 6

global running, inventoryCount


def start_woodcutting(dispose="BANK"):
    global running, inventoryCount
    running = True
    while running:
        botfunctions.open_inventory()
        inventoryCount = ocr.image_count(woodIcon)
        print("Inventory Wood Count: ", inventoryCount)

        if botfunctions.is_inventory_full():
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
    ocr.image_rec_click_all(woodIcon)
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


def do_fire_making():
    global inventoryCount, rowCount
    antiafk.random_break(1, 3)
    print("Burning Wood")
    burnCount = 0
    timeoutCount = 0

    ocr.find_object(4)

    antiafk.random_break(8, 15)
    while inventoryCount > 1:
        if timeoutCount > 2:
            drop_all_wood()
            break

        if burnCount > rowCount:
            antiafk.random_break(2, 4)
            botfunctions.move(rowCount, -1)
            antiafk.random_break(2, 4)
            burnCount = 0

        antiafk.random_break(0.1, 2)
        ocr.image_rec_click_single(woodIcon, 5, 5, 0.75, 'left', 8)
        antiafk.random_break(0.1, 1)
        ocr.image_rec_click_single('tinderbox.png', 5, 5, 0.75, 'left', 8)
        timeout = time.time() + random.uniform(10, 15)

        while True:
            fire = ocr.xp_gain_check('firemaking_xp.png', 0.8)
            if not fire:
                fire = ocr.xp_gain_check('firemaking_xp2.png', 0.8)
            if fire:
                inventoryCount = ocr.image_count(woodIcon)
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
