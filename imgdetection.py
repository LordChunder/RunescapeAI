import math
import random

import cv2
import numpy
import pyautogui
from PIL import ImageGrab

import antiafk
import core

global screenshot_image

# Detectable Colors
# BGR
red = ([0, 0, 160], [20, 20, 255])  # 0 Index
green = ([0, 180, 0], [80, 255, 80])  # 1 Index
amber = ([0, 200, 200], [60, 255, 255])  # 2 Index
enemy_blue = ([170, 170, 0], [255, 255, 50])  # 3 Index
blue = ([170, 0, 0], [255, 50, 50])  # 4 Index

object_list = [red, green, amber, enemy_blue, blue]


def screen_image(save_screenshot=False):
    """
    Screenshots the RuneLite client area and updates the global variable
    :param save_screenshot: (Optional) Save screenshot to images/screenshot.png
    """
    global screenshot_image
    x, y, w, h = core.get_window_size()
    img = ImageGrab.grab(bbox=(x, y, x + w, y + h))

    # noinspection PyTypeChecker
    screenshot_image = numpy.array(img)[:, :, ::-1].copy()

    if save_screenshot:
        img.save('images/screenshot.png', 'png')


def find_object(colorIndex):
    """
    Find the position of an object on screen within the range of the specified color
    Arguments:
    :param colorIndex: The color to detect
    :return:  The center of the closest object to the player otherwise False
    """

    global screenshot_image
    screen_image()
    img_rbg = screenshot_image
    img_rbg = cv2.rectangle(img_rbg, pt1=(562, 0), pt2=(825, 183), color=(0, 0, 0), thickness=-1)  # hide minimap
    img_rbg = cv2.rectangle(img_rbg, pt1=(430, 0), pt2=(460, 23), color=(0, 0, 0), thickness=-1)  # hide xp bar
    img_rbg = cv2.rectangle(img_rbg, pt1=(540, 725), pt2=(770, 770), color=(0, 0, 0), thickness=-1)  # hide xp bar

    boundaries = [object_list[colorIndex]]
    contours = None
    # loop over the boundaries

    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = numpy.array(lower, dtype="uint8")
        upper = numpy.array(upper, dtype="uint8")
        # find the colors within the specified boundaries and apply

        mask = cv2.inRange(img_rbg, lower, upper)
        thresh, dst = cv2.threshold(mask, 40, 255, 0)
        cv2.imwrite("images/mask.png", mask)
        contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        # find the biggest contour (c) by the area
        centers = map(get_contour_center, contours)
        closest = min(centers, key=lambda c: math.dist(c, [385, 400]))
        offset = closest[0] + random.randrange(-2, 2), closest[1] + random.randrange(-2, 2)

        b = random.uniform(0.2, 0.4)
        pyautogui.moveTo(offset, duration=b)
        b = random.uniform(0.01, 0.05)
        pyautogui.click(duration=b)
        return offset
    else:
        print("No detected contours")
        return False


def get_contour_center(c):
    moment = cv2.moments(c)
    if moment['m00'] == 0:
        return 9999999, 9999999
    x = int(moment['m10'] / moment['m00'])
    y = int(moment['m01'] / moment['m00'])

    return x, y


def image_count(image, threshold=0.7):
    """
    Detects and counts the given image on the screen
    :param image: The image to detect
    :param threshold: Detection threshold [0-1]
    :return:  The number of instances on screen of the image
    """
    global screenshot_image
    counter = 0
    screen_image()

    img_rgb = screenshot_image
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/icons/' + image, 0)

    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = numpy.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        counter += 1
    return counter


def xp_gain_check_screenshot(image, threshold=0.7):
    """
    Checks to see if the player has experience gain on screen
    :param image: The experience icon to look for
    :param threshold: Detection threshold [0-1]
    :return: Was successful
    """
    global screenshot_image
    screen_image()
    img_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/icons/' + image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    print("Checking for XP", numpy.where(res >= threshold))
    loc = numpy.where(res >= threshold)
    for _ in zip(*loc[::-1]):
        return True
    return False


def image_rec_click_single(image, img_height=5, img_width=5, threshold=0.70, clicker='left', img_space=20,
                           inventory_area=False):
    global screenshot_image
    screen_image()
    img_rgb = screenshot_image

    cropX, cropY = 0, 0
    if inventory_area:
        img_rgb = img_rgb[455:720, 620:820]
        cropX, cropY = (620, 455)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/icons/' + image, 0)
    w, h = template.shape[::-1]
    pt = None
    # print('getting match requirements')
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = threshold
    loc = numpy.where(res >= threshold)

    item_pos = 0, 0
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    if pt is None:
        print("No object found: ", image)
        return item_pos
    else:
        x = random.randrange(img_width, img_width + img_space) + cropX
        y = random.randrange(img_height, img_height + img_space) + cropY
        item_pos = pt[0] + img_height + x
        item_pos = (item_pos, pt[1] + img_width + y)

        print("Object found: ", item_pos)
        b = random.uniform(0.2, 0.7)
        pyautogui.moveTo(item_pos, duration=b)
        b = random.uniform(0.1, 0.3)
        pyautogui.click(item_pos, duration=b, button=clicker)

    return item_pos


def image_rec_click_all(image, img_height=5, img_width=5, threshold=0.825, clicker='left', img_space=10,
                        inventory_area=True, click_interval=0):
    global screenshot_image
    screen_image()
    img_rgb = screenshot_image

    cropX, cropY = 0, 0
    if inventory_area:
        img_rgb = img_rgb[455:720, 620:820]
        cropX, cropY = (620, 455)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('images/icons/' + image, 0)

    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = numpy.where(res >= threshold)

    success = False
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        if pt is not None:
            success = True
            x = random.randrange(img_width, img_width + img_space) + cropX
            y = random.randrange(img_height, img_height + img_space) + cropY
            item_pos = pt[0] + img_height + x
            item_pos = (item_pos, pt[1] + img_width + y)

            b = random.uniform(0.1, 0.3)
            pyautogui.moveTo(item_pos, duration=b)
            b = random.uniform(0.01, 0.05)
            pyautogui.click(item_pos, duration=b, button=clicker)

            if click_interval > 0:
                antiafk.random_break(click_interval, click_interval + .8)
    return success
