import random
import tkinter
from tkinter import *

import main
from main import start_bot, stop_bot

global status_label, start_button

mode_text = ["WOODCUTTING", "FISHING", "COMBAT"]


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


def build_ui():
    global status_label, start_button
    window = tkinter.Tk()

    window.title("RunescapeAI")
    window.geometry('256x256')

    statusFrame = tkinter.Frame()

    checked_modes = Checkbar(window, ['Woodcutting', 'Fishing', 'Combat'])

    checked_modes.pack(side=TOP, fill=X)
    checked_modes.config(relief=GROOVE, bd=2)
    statusFrame.pack()

    start_button = tkinter.Button(window, text="Run", command=lambda: on_run_clicked(checked_modes))
    start_button.pack()

    status_label = tkinter.Label(master=statusFrame, text="Status: STOPPED")
    status_label.pack()

    statusFrame.mainloop()
    window.protocol("WM_DELETE_WINDOW", main.on_exit_program)
    window.mainloop()


def update_status_label(status):
    global status_label
    status_label.config(text="Status: " + status)


def on_run_clicked(checked_modes):
    global status_label, start_button
    if main.bot_running:
        stop_bot()
        update_status_label("STOPPED")
        start_button.config(text="Run")
        checked_modes.enable()
        return

    checked_modes.disable()

    selected_modes = []
    for index, val in enumerate(checked_modes.vars):
        if val.get() == 1:
            selected_modes.insert(0, index)

    update_status_label("STARTING")
    start_button.config(text="Stop")
    random.shuffle(selected_modes)
    start_bot(selected_modes)
