import tkinter as tk

from controllers import woodcutting

global statusLabel


def build_ui():
    global statusLabel

    window = tk.Tk()
    window.title("RunescapeAI")

    statusFrame = tk.Frame()
    buttonFrame = tk.Frame()

    statusLabel = tk.Label(master=statusFrame, text="Status: OFF")
    statusLabel.pack()

    tk.Label(master=buttonFrame, text="Bot Mode").pack()
    buttonWoodCutting = tk.Button(buttonFrame, text="Wood Cutting")

    buttonWoodCutting.bind("<Button-1>", button_click_woodcutting)
    buttonWoodCutting.pack()

    statusFrame.pack()
    buttonFrame.pack()

    statusFrame.mainloop()
    buttonFrame.mainloop()
    window.mainloop()


def button_click_woodcutting():
    statusLabel["text"] = "Status: WOOD CUTTING"
    woodcutting.start_woodcutting()
