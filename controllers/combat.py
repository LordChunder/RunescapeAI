import random
import time

import antiafk
import botfunctions
import imgdetection

global running

unwantedItems = ["raw_hide.png", "raw_beef.png"]


def start_combat():
    global running

    running = True
    while running:
        print("Attacking enemy")

        imgdetection.find_object(3)
        noCombatTimer = 0
        interval = random.uniform(4.5, 6.5)
        lastTime = time.time()

        lastXP = botfunctions.get_xp_for_skill('Hitpoints')
        combatStarted = False
        while True:
            xp = botfunctions.get_xp_for_skill('Hitpoints')
            if 0 < xp > lastXP:
                print("XP Gained", xp, lastXP)
                combatStarted = True
                noCombatTimer = 0
                lastXP = xp
            if noCombatTimer > interval:
                print("Out of combat")
                break

            noCombatTimer += time.time() - lastTime
            lastTime = time.time()

        botfunctions.open_inventory()

        pray = False
        if combatStarted:
            pickup_bones()
            pray = botfunctions.is_inventory_full()
            drop_unwanted_items()

        if pray:
            pray_with_bones()

        antiafk.random_action()


def drop_unwanted_items():
    for item in unwantedItems:
        print("Dropping: ", item)
        botfunctions.drop_item()
        imgdetection.image_rec_click_all(item)
        botfunctions.release_drop_item()


def pray_with_bones():
    print("Praying to Allah")
    imgdetection.image_rec_click_all('bones.png', click_interval=.5)
    antiafk.random_break(1.5, 3)


def pickup_bones():
    imgdetection.find_object(4)
    antiafk.random_break(1.7, 3)
    imgdetection.find_object(4)
    antiafk.random_break(.3, .7)
