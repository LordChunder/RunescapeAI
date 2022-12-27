import antiafk
import botfunctions
import imgdetection

global running, fish_ids, bot_instance


def start_fishing(ibot, fish_selection=None, dispose='BANK'):
    if fish_selection is None:
        fish_selection = [317, 321]
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
    botfunctions.drop_items(fish_ids)


def deposit_in_bank():
    antiafk.random_break(1, 3)
    bot_instance.bot_status.value = 2
    print("Depositing fish in bank")
    botfunctions.do_banking()
