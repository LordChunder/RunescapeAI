import logging
import multiprocessing
import random
import time
import pyautogui

import botfunctions
import core
import imgdetection
from controllers import fishing, woodcutting, combat


class Bot:
    modes = {0: woodcutting.start_woodcutting, 1: fishing.start_fishing, 2: combat.start_combat}

    def __init__(self):
        self.bot_mode = multiprocessing.Value('I', 100)  # 100 - Stopped, 101 - Starting, 0-99 - Mode Running
        self.bot_status = multiprocessing.Value('I', 0)

        self.bot_running = False
        self.bot_thread = None

        self.rl_hwnd = core.hwnd

    def start_bot(self, active_modes):
        if self.bot_running:
            return
        logging.info("Starting bot with modes: %s", active_modes)
        random.seed = time.time()
        self.bot_mode.value = 101

        self.bot_thread = multiprocessing.Process(target=self.process_loop, args=(active_modes,))
        self.bot_thread.start()
        self.bot_running = True

    def stop_bot(self, error=False):
        logging.info("Stopping Bot")
        self.bot_running = False

        if error:
            self.bot_mode.value = 99
        else:
            self.bot_mode.value = 100

        pyautogui.press('shift')
        if self.bot_thread is not None:
            self.bot_thread.terminate()
            self.bot_thread = None

    def process_loop(self, active_modes):
        pyautogui.FAILSAFE = False
        imgdetection.bot = self
        stop_time = core.options_yaml['general']['max_run_time'] * 60 * 60 + time.time()
        print("Maximum run time will shut off bot at: ", stop_time)
        while True:
            try:
                self.run_core(active_modes)
                if stop_time is not None and time.time() > stop_time:
                    print("Maximum runtime stopping bot")
                    self.stop_bot()
                    return
            except Exception:
                self.stop_bot(error=True)

    def run_core(self, active_modes):
        runtime_seconds = random.uniform(core.options_yaml['general']['min_time_to_break'] * 60 * 60,
                                         core.options_yaml['general']['min_time_to_break'] * 60 * 60 * 1.05)
        stop_time = time.time() + runtime_seconds
        time_till_break = stop_time - time.time()
        print("Running modes for seconds:", runtime_seconds, stop_time)
        last_mode = None
        num_mode_repeats = 0
        while time_till_break > 0:
            time_till_break = stop_time - time.time()
            (h, m) = divmod(time_till_break / 60, 60)
            print("Stopping in (h:m): ", h, m)

            index = active_modes[random.randint(0, len(active_modes) - 1)]
            mode = self.modes[index]
            self.bot_mode.value = index
            if mode == last_mode:
                num_mode_repeats += 1
            else:
                num_mode_repeats = 0
            if num_mode_repeats > 3 and len(active_modes) > 1:
                print("Force switching modes")
                while mode == last_mode:
                    mode = self.modes[random.randint(0, len(self.modes) - 1)]

            mode(self)
            last_mode = mode
        self.bot_mode.value = 102
        self.bot_status.value = 1
        botfunctions.sleep()
