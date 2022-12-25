import random
import time

import antiafk
import botfunctions
import imgdetection

global running, bot_instance

items_to_drop = []


def start_combat(ibot, drop_items=[2132, 1739]):
    global running, bot_instance, items_to_drop
    bot_instance = ibot
    items_to_drop = drop_items

    running = True
    while running:
        print("Attacking enemy")
        bot_instance.bot_status.value = 3
        imgdetection.object_rec_click_closest_single(3)
        bot_instance.bot_status.value = 0
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
    bot_instance.bot_status.value = 4
    for item in items_to_drop:
        print("Dropping: ", item)
        botfunctions.drop_item()
        imgdetection.image_rec_click_all(item)
        botfunctions.release_drop_item()


def pray_with_bones(bones_id=526):
    print("Praying with bones")
    bot_instance.bot_status.value = 5
    imgdetection.image_rec_click_all(bones_id, click_interval=.5)
    antiafk.random_break(1.5, 3)


def pickup_bones():
    imgdetection.object_rec_click_closest_single(4)
    antiafk.random_break(1.7, 3)
    imgdetection.object_rec_click_closest_single(4)
    antiafk.random_break(.3, .7)
