import win32com.client
# noinspection PyPackageRequirements
import win32gui
import yaml

global hwnd, item_yaml, config_yaml


def read_config():
    global config_yaml, item_yaml
    with open('config.yaml', 'r') as file:
        config_yaml = yaml.safe_load(file)

    with open('items.yaml', 'r') as file:
        item_yaml = yaml.safe_load(file)


def configure_ui_window():
    window = win32gui.FindWindow(None, "RunescapeAI")

    rect = win32gui.GetWindowRect(window)
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    win32gui.MoveWindow(window, 900, 0, w, h, True)


def find_runelite_window():  # returns PID of runelite app
    global hwnd

    screen_height, screen_width = get_display_size()
    dX, dY = screen_width / 1920, screen_height / 1080

    hwnd = win32gui.FindWindow(None, config_yaml['client_title'] + config_yaml['user']['user_name'])
    print("Found runescape client window as: ", hwnd, dX, dY, screen_height, screen_width)

    win32gui.MoveWindow(hwnd, 0, int(dY), int(865 * dX), int(830 * dY), True)
    win32gui.SetActiveWindow(hwnd)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')

    win32gui.SetForegroundWindow(hwnd)


def get_display_size():
    import tkinter
    root = tkinter.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', False)
    root.state('iconic')
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    root.destroy()
    return height, width


def get_runelite_window_size(bot):
    return win32gui.GetWindowRect(bot.rl_hwnd)


read_config()
