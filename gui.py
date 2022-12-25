import logging
import random
import tkinter
import webbrowser
import os
from tkinter import *

import pyautogui

global status_label, start_button, window, console_buffer, console_label, mode_label, bot_instance

mode_string = {99: "Canceled (Error)", 100: "STOPPED", 101: "STARTING",
               0: "WOODCUTTING", 1: "FISHING", 2: "COMBAT"}
status_string = {0: "Training", 1: "Resting", 2: "Banking", 3: "Finding Target", 4: "Dropping Items",
                 5: "Consuming Drops"}


class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        self.checkboxes = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.checkboxes.append(chk)
            self.vars.append(var)

    def disable(self):
        for checkbox in self.checkboxes:
            checkbox.configure(state="disabled")

    def enable(self):
        for checkbox in self.checkboxes:
            checkbox.configure(state="normal")

    def state(self):
        return map((lambda var: var.get()), self.vars)


class LogStream(object):
    def __init__(self, text_box):
        self.text_box = text_box

    def write(self, text):
        self.text_box.insert(tkinter.END, text)

    def flush(self):
        pass


def build_ui(ibot):
    global status_label, start_button, window, console_buffer, console_label, mode_label, bot_instance
    bot_instance = ibot
    window = tkinter.Tk()

    window.title("RunescapeAI")

    checked_modes = Checkbar(window, ['Woodcutting', 'Fishing', 'Combat'])

    checked_modes.pack(side=TOP, fill=X)
    checked_modes.config(relief=GROOVE, bd=2)

    start_button = tkinter.Button(window, text="Run", command=lambda: on_run_clicked(checked_modes))
    start_button.pack()

    mode_label = tkinter.Label(window)
    mode_label.pack()

    status_label = tkinter.Label(window)
    status_label.pack()

    help_label = tkinter.Label(window, text="https://github.com/LordChunder/RunescapeAI", fg="blue", cursor="hand2")
    help_label.bind("<Button-1>",
                    lambda e: webbrowser.open_new_tab("https://github.com/LordChunder/RunescapeAI"))
    help_label.pack()

    tkinter.Label(window, text="Press Ctrl-C to exit").pack()

    console_label = tkinter.Text(window)
    console_label.pack()

    window.protocol("WM_DELETE_WINDOW", on_window_exit_pressed)

    log_stream = LogStream(console_label)
    logging.basicConfig(stream=log_stream, level=logging.INFO)


def update_loop():
    update_status_label(bot_instance.bot_mode.value)
    window.update_idletasks()
    window.update()


def on_window_exit_pressed():
    pyautogui.press('shift')
    # noinspection PyUnresolvedReferences,PyProtectedMember
    os._exit(0)


def update_status_label(status):
    global mode_label
    mode_label.config(text="Status: " + mode_string[status])
    global status_label
    if status == 99 or status == 100:
        status_label.config(text="")
    else:
        status_label.config(text="(" + status_string[bot_instance.bot_status.value] + ")")


def on_run_clicked(checked_modes):
    global status_label, start_button

    if bot_instance.bot_running:
        bot_instance.stop_bot()
        update_status_label(100)
        start_button.config(text="Run")
        checked_modes.enable()
        return

    selected_modes = []
    for index, val in enumerate(checked_modes.vars):
        if val.get() == 1:
            selected_modes.insert(0, index)

    if len(selected_modes) == 0:
        pyautogui.alert("Must select at least one mode")
        return

    checked_modes.disable()
    start_button.config(text="Stop")
    random.shuffle(selected_modes)

    bot_instance.start_bot(selected_modes)
