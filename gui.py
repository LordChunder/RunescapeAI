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
        self.text_box.configure(state="normal")
        self.text_box.insert(tkinter.END, text)
        self.text_box.configure(state="disabled")

    def flush(self):
        pass


def copy_to_clip(tk, text):
    tk.clipboard_clear()
    tk.clipboard_append(text)
    pyautogui.alert("Copied to clipboard:\n" + text)


def build_ui(ibot):
    global status_label, start_button, window, console_buffer, console_label, mode_label, bot_instance
    bot_instance = ibot
    window = tkinter.Tk()

    window.title("RunescapeAI")

    checked_modes = Checkbar(window, ['Woodcutting', 'Fishing', 'Combat'])

    checked_modes.grid(row=0, columnspan=2, sticky=W + E)
    checked_modes.config(relief=GROOVE, bd=2)

    start_button = tkinter.Button(window, text="Run", command=lambda: on_run_clicked(checked_modes))
    start_button.grid(row=2, columnspan=2)

    mode_label = tkinter.Label(window)
    mode_label.grid(row=1, columnspan=2)

    status_label = tkinter.Label(window)
    status_label.grid(row=3, columnspan=2)

    help_label = tkinter.Label(window, text="https://github.com/LordChunder/RunescapeAI", fg="blue", cursor="hand2")
    help_label.bind("<Button-1>",
                    lambda e: webbrowser.open_new_tab("https://github.com/LordChunder/RunescapeAI"))
    help_label.grid(row=4, columnspan=2)
    bmac_label = tkinter.Label(window, text="https://www.buymeacoffee.com/awaiteddev", fg="blue", cursor="hand2")
    bmac_label.bind("<Button-1>",
                    lambda e: webbrowser.open_new_tab("https://www.buymeacoffee.com/awaiteddev"))
    bmac_label.grid(row=5, columnspan=2)
    btc_label = tkinter.Label(window, text="btc: bc1qm6hj0vdmrkngjv68xewjlyz58x25eht4232v20", fg="orange",
                              cursor="hand2")
    btc_label.bind("<Button-1>", lambda e: copy_to_clip(window, 'bc1qm6hj0vdmrkngjv68xewjlyz58x25eht4232v20'))
    btc_label.grid(column=0, row=6)
    eth_label = tkinter.Label(window, text="eth: 0x94392A6d1b080A8AE431863F0FCf440ad2DbD10B", fg="orange",
                              cursor="hand2")
    eth_label.bind("<Button-1>", lambda e: copy_to_clip(window, '0x94392A6d1b080A8AE431863F0FCf440ad2DbD10B'))
    eth_label.grid(row=6, column=1)
    tkinter.Label(window, text="Press Ctrl-C to exit").grid(row=7, columnspan=2)

    console_label = tkinter.Text(window, height=15)
    console_label.configure(state="disabled")
    console_label.grid(row=8, columnspan=2)
    console_label.rowconfigure(8, weight=1)
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
