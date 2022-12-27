import random
import time

import antiafk
import botfunctions
import imgdetection
from core import options_yaml

global running, bot_instance, items_to_drop


def start_combat(ibot):
    global running, bot_instance, items_to_drop
    bot_instance = ibot
    items_to_drop = options_yaml['combat']['unwanted_items']

    running = True
    while running:
        print("Attacking enemy")
        bot_instance.bot_status.value = 3
        imgdetection.object_rec_click_closest_single('combat_enemy')
        bot_instance.bot_status.value = 0
        no_combat_timer = 0
        interval = random.uniform(4.5, 6.5)
        last_time = time.time()

        last_xp = botfunctions.get_xp_for_skill('Hitpoints')
        combat_started = False
        while True:
            xp = botfunctions.get_xp_for_skill('Hitpoints')
            if 0 < xp > last_xp:
                print("XP Gained", xp, last_xp)
                combat_started = True
                no_combat_timer = 0
                last_xp = xp
            if no_combat_timer > interval:
                print("Out of combat")
                break

            no_combat_timer += time.time() - last_time
            last_time = time.time()

        botfunctions.open_inventory()

        pray = False
        if combat_started:
            pickup_bones()
            pray = botfunctions.is_inventory_full()
            drop_unwanted_items()

        if options_yaml['combat']['pray'] and pray:
            pray_with_bones()

        antiafk.random_action()


def drop_unwanted_items():
    print("Dropping unwanted items")
    bot_instance.bot_status.value = 4
    botfunctions.drop_items(items_to_drop)


def pray_with_bones():
    print("Praying with bones")
    bot_instance.bot_status.value = 5
    imgdetection.image_rec_click_all(options_yaml['combat']['bones_id'], click_interval=.5)
    antiafk.random_break(1.5, 3)


def pickup_bones():
    imgdetection.object_rec_click_closest_single('item_pickup')
    antiafk.random_break(1.7, 3)
    imgdetection.object_rec_click_closest_single('item_pickup')
    antiafk.random_break(.3, .7)
