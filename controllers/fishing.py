import antiafk
import botfunctions
import imgdetection

from core import options_yaml

global running, fish_ids, bot_instance


def start_fishing(ibot):
    global running, fish_ids, bot_instance
    fish_ids = options_yaml['fishing']['fish_selection']
    bot_instance = ibot

    running = True
    while running:
        botfunctions.open_inventory()

        if botfunctions.is_inventory_full():
            if options_yaml['fishing']['dispose_method'] == 'Bank':
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
    botfunctions.drop_items(fish_ids)


def deposit_in_bank():
    antiafk.random_break(1, 3)
    bot_instance.bot_status.value = 2
    print("Depositing fish in bank")
    botfunctions.do_banking(fish_ids)
