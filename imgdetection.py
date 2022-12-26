import math
import random

import cv2
import imutils
import numpy
import pyautogui
from PIL import ImageGrab

import antiafk
from core import config_yaml, item_yaml, get_runelite_window_size

global screenshot_image, rescale_factor
global bot

save_debug_screenshots = False


def screen_image(save_screenshot=save_debug_screenshots):
    """
    Screenshots the RuneLite client area and updates the global variable
    :param save_screenshot: (Optional) Save screenshot to images/screenshot.png
    """
    global screenshot_image, rescale_factor
    rect = get_runelite_window_size(bot)
    img = ImageGrab.grab(bbox=rect)
    # noinspection PyTypeChecker
    screenshot_image = numpy.array(img)[:, :, ::-1].copy()

    if save_screenshot:
        cv2.imwrite('images/screenshot.png', screenshot_image)


def object_rec_click_closest_single(color_name, save_screenshot=save_debug_screenshots):
    """
    Find the position of an object on screen within the range of the specified color
    Arguments:
    :param color_name: The name of color in config_yaml to detect
    :param save_screenshot: (Optional) Save screenshot to images/screenshot.png
    :return:  The center of the closest object to the player otherwise False
    """

    global screenshot_image
    screen_image()
    img_rbg = screenshot_image
    img_rbg = cv2.rectangle(img_rbg, pt1=(615, 0), pt2=(865, 205), color=(0, 0, 0), thickness=-1)  # hide minimap
    img_rbg = cv2.rectangle(img_rbg, pt1=(490, 0), pt2=(605, 55), color=(0, 0, 0), thickness=-1)  # hide xp bar
    img_rbg = cv2.rectangle(img_rbg, pt1=(625, 480), pt2=(865, 830), color=(0, 0, 0), thickness=-1)  # hide bottom bar
    img_rbg = cv2.rectangle(img_rbg, pt1=(0, 800), pt2=(520, 830), color=(0, 0, 0), thickness=-1)  # hide bottom bar

    boundaries = [config_yaml['detect_colors'][color_name]]
    print("Detecting object (color): ", color_name)
    # loop over the boundaries
    if save_screenshot:
        cv2.imwrite('images/screenshot-blacked.png', screenshot_image)
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = numpy.array(lower, dtype="uint8")
        upper = numpy.array(upper, dtype="uint8")
        # find the colors within the specified boundaries and apply

        mask = cv2.inRange(img_rbg, lower, upper)
        thresh = cv2.threshold(mask, 40, 255, 0)[1]

        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        closest_dist = 9999
        contour_center = None
        for cont in contours:
            if cont is None:
                continue
            moment = cv2.moments(cont)
            if moment is None or moment["m00"] == 0:
                continue
            cX = int(moment["m10"] / moment["m00"])
            cY = int(moment["m01"] / moment["m00"])
            dist = math.dist([cX, cY], [420, 425])
            if dist < closest_dist:
                contour_center = cX, cY
                closest_dist = dist
            else:
                continue
            if save_screenshot:
                cv2.drawContours(mask, [cont], -1, (0, 255, 0), 2)
                cv2.circle(mask, contour_center, 7, (255, 255, 255), -1)
                cv2.putText(mask, str(contour_center), (cX - 20, cY - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        if save_screenshot:
            cv2.imwrite("images/mask.png", mask)

        if contour_center is not None:
            b = random.uniform(0.2, 0.4)
            pyautogui.moveTo(contour_center, duration=b)
            b = random.uniform(0.01, 0.05)
            pyautogui.click(duration=b)

            return contour_center
        else:
            print("No detected contours")
        return False


# OLD SWITCHED TO USING MORG HTTP TO CHECK ITEM COUNTS MIGHT USE FOR SOMETHING THOUGH
# def image_count(image, threshold=0.7):
#     """
#     Detects and counts the given image on the screen
#     :param image: The image to detect
#     :param threshold: Detection threshold [0-1]
#     :return:  The number of instances on screen of the image
#     """
#     global screenshot_image
#     counter = 0
#     screen_image()
#
#     img_rgb = screenshot_image
#     img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
#     template = cv2.imread('images/icons/' + image, 0)
#
#     w, h = template.shape[::-1]
#
#     res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
#     loc = numpy.where(res >= threshold)
#     for pt in zip(*loc[::-1]):
#         cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
#         counter += 1
#     return counter


# OLD MIGHT DELETE MIGHT USE WHO KNOWS AT THIS POINT
# def xp_gain_check_screenshot(image, threshold=0.7):
#     """
#     Checks to see if the player has experience gain on screen
#     :param image: The experience icon to look for
#     :param threshold: Detection threshold [0-1]
#     :return: Was successful
#     """
#     global screenshot_image
#     screen_image()
#     img_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)
#     template = cv2.imread('images/icons/' + image, 0)
#
#     res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
#     print("Checking for XP", numpy.where(res >= threshold))
#     loc = numpy.where(res >= threshold)
#     for _ in zip(*loc[::-1]):
#         return True
#     return False


def image_rec_click_single(item_number, img_height=5, img_width=5, threshold=0.85, clicker='left', img_space=8,
                           inventory_area=False, save_screenshot=save_debug_screenshots):
    global screenshot_image
    screen_image()
    img_rgb = screenshot_image

    cropX, cropY = 0, 0
    if inventory_area:
        img_rgb = img_rgb[475:750, 630:820]
        cropX, cropY = (630, 475)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(item_yaml['icon_path'] + item_yaml['items'][item_number], 0)
    w, h = template.shape[::-1]
    pt = None

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = threshold
    loc = numpy.where(res >= threshold)

    item_pos = 0, 0
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    if pt is None:
        print("No object found: ", item_yaml['items'][item_number])
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
        b = random.uniform(0.1, 0.3)
        pyautogui.moveTo((random.randrange(600, 800), random.randrange(400, 475)),
                         duration=b)  # move mouse out of view
    if save_screenshot:
        cv2.imwrite("images/screenshot_inv.png", img_gray)
    return item_pos


def image_rec_click_all(item_number, img_height=5, img_width=5, threshold=0.85, clicker='left', img_space=8,
                        inventory_area=True, click_interval=0, save_screenshot=save_debug_screenshots):
    """
    Clicks all items on screen based on the item number
    :param item_number: The code of the OSRS item mapped to the icon.png in items_yaml
    :param img_height: Height margin of item image
    :param img_width: Width margin of item image
    :param threshold: The detection threshold 0-1
    :param clicker: Mouse button to click with
    :param img_space: Space between images
    :param inventory_area: Only detect in inventory area: true or false
    :param click_interval: Minimum interval between clicks
    :param save_screenshot: Should debug screenshots?
    :return: Success?
    """
    global screenshot_image
    screen_image()
    img_rgb = screenshot_image

    cropX, cropY = 0, 0
    if inventory_area:
        img_rgb = img_rgb[475:750, 630:820]
        cropX, cropY = (630, 475)

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(item_yaml['icon_path'] + item_yaml['items'][item_number], 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = numpy.where(res >= threshold)

    success = False
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
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
    b = random.uniform(0.1, 0.3)
    pyautogui.moveTo((random.randrange(600, 800), random.randrange(400, 475)),
                     duration=b)  # move mouse out of view
    if not success:
        print("No object found: ", item_yaml['items'][item_number])
    if save_screenshot:
        cv2.imwrite("images/screenshot_inv.png", img_gray)
    return success
