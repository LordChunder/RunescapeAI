import random
import time

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
    botfunctions.drop_items(wood_id)


def deposit_in_bank():
    antiafk.random_break(1, 3)
    print("Depositing wood in bank")
    bot_instance.bot_status.value = 2


def do_fire_making(num_per_row=6):
    print("Burning Wood")
    antiafk.random_break(1, 3)

    bot_instance.bot_status.value = 5
    burn_count = 0
    timeout_count = 0

    imgdetection.object_rec_click_closest_single(
        'woodcutting_fire_spot')  # Click the starting point on the screen to move there

    antiafk.random_break(8, 15)

    inventory_count = botfunctions.inventory_count(wood_id)
    while inventory_count > 0:
        if timeout_count > 2:
            drop_all_wood()
            break

        if burn_count > num_per_row:
            antiafk.random_break(2, 4)
            botfunctions.move(num_per_row, -1)
            antiafk.random_break(2, 4)
            burn_count = 0

        # click on tinder and wood
        antiafk.random_break(0.1, 2)
        imgdetection.image_rec_click_single(wood_id)
        antiafk.random_break(0.1, 1)
        imgdetection.image_rec_click_single(590)
        timeout = time.time() + random.uniform(10, 15)

        # check for XP gain
        last_xp = botfunctions.get_xp_for_skill('Firemaking')
        while True:
            xp = botfunctions.get_xp_for_skill('Firemaking')
            if 0 < xp > last_xp:
                print("Fire made (XP Gained)", xp, last_xp)
                inventory_count = botfunctions.inventory_count(wood_id)
                burn_count += 1
                timeout_count = 0
                break

            if time.time() > timeout:
                print("Fire making timout")
                botfunctions.move(random.randint(0, 3), -1)
                antiafk.random_break(2, 4)
                burn_count = 0
                timeout_count += 1
                break
