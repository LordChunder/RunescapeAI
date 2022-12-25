# RunescapeAI

### A bot for Old School RuneScape written in Python

*RunescapeAI is a work in progress and not fully complete*

1. [Requirements](#Requirements)
2. [Set-Up](#Set-Up)
3. [How To Use](#General)
    * [Wood Cutting](#Wood-Cutting)
    * [Fishing](#Fishing)
    * [Combat](#Combat)
4. [Disclaimer](#Disclaimer)

## Requirements

+ Python >= 3.8
  Download Python from: <https://www.python.org/downloads/>
    * For dependencies see [requirements.txt](/requirements.txt)
+ RuneLite Old School RuneScape Client <https://runelite.net/>
    * MorgHTTP <https://runelite.net/plugin-hub/show/morghttpclient>

## Set-Up
***Download and unzip RunescapeAI from:***
    <https://github.com/LordChunder/RunescapeAI/archive/refs/heads/master.zip>

1. Install Python 3.8 or higher <https://www.python.org/downloads/>
2. Install RunescapeAI dependencies [requirements.txt](/requirements.txt)
    * Open a console inside the root RunscapeAI folder.
    * run ```$ pip install -r requirements.txt```
3. Configure RuneLite
    * Ensure `MorgHTTPClient` is
      installed and
      enabled [https://runelite.net/plugin-hub/show/morghttpclient](https://runelite.net/plugin-hub/show/morghttpclient)
        * Ensure the port is configured properly in both the plugin and [config.yaml](config.yaml)
    * Enable hold shift to drop items with in game settings.
    * Enable the `Object Markers`,`Ground Markers`,`Ground Items` and `NPC Indicators` to allow in game object
      highlighting and ensure colors are visible and
      unique
        * The colors will be used with the bots object detection.
        * IMPORTANT: Ensure proper contrast between other in game colors to avoid faulty detection. This does not
          include items in the HUD as this screen area is excluded.
        * Good colors are (BGR): Red (0, 0, 225), Blue (225,0,0), Light Blue (225,225,0), Amber (225,225,0)

4. Configure RunescapeAI's [config.yaml](/config.yaml)
    * Open [config.yaml](/config.yaml) in a text editor.
    * Enter your OSRS username and password. This is used to automatically log out and login during the break period.
    * Configure the colors used for object detection under ```detect_colors:```
        * Format: ```[[B_low,R_low,G_low],[B_high,R_high,G_high]]```
        * IMPORTANT: Do not remove or edit the ```object_name:``` this will cause the program to crash Only edit the
          color range value.
        * The high range BRG values should equal the BRG value set in RuneLite for that color. The low value is used to
          determine the
          threshold for that colors detection.
        * If not cycling multiple bot modes it is okay for colors to overlap if they are not part of the same mode.
    * By default ```image_paths``` should contain the correct paths. If you edit the location of the menu images, update
      their path here.
5. OPTIONAL: Configure RunescapeAI's [items.yaml](/items.yaml)
    * Open [config.yaml](/config.yaml) in a text editor.
    * Configure ```icon_path:``` to the path of the icons folder
    * To configure the items that RunescapeAI can interact/detect edit ```items:```
        * Format: ```item_id: image_file_name```
        * Use Snipping Tool or any other method to obtain an image of the item. Ensure the background is plain and
          perferably the OSRS inventory background.
        * To find the id for OSRS items visit: <https://www.osrsbox.com/tools/item-search/>

## How To Use

### General

***This document is a work in progress as features are rapidly updating.
Current use can be demonstrated within the controller python files and ran with the GUI.***

RunescapeAI uses OpenCV image recognition and color based object detection to determine on screen locations of items and
highlighted entities in RuneLite.

* It is crucial that the object plugins in RuneLite are configured properly or the bot
  will not be able to detect positions on screen [(Set-up)](#Set-Up)
* Any in game items that need to interact with the bot (ie pickup, drop, eat, combine) need to be configured
  in [items.yaml](items.yaml) ([Set-Up](#set-up))
* When selected multiple modes to run it is crucial that colors do not overlap between modes. Example:
    * If fishing and woodcutting make sure the highlited trees and fishing spots are not the same color as the bot will
      not be able to distinguish between trees and fishing spots.

To run start and run RunescapeAI:

1. Launch RuneLite and login to your account
2. Open a console inside the RunescapeAI folder and run command `python main.py`
    * RuneLite must be running prior as the name of this window will be used in the bot to find the RuneLite window
3. Select the bot modes and click run
    * If multiple bot modes are selected they will be cycled randomly
4. Stop the bot by:
    * Exiting the bot with hotkey: `ctrl-c`
    * Clicking stop
    * Closing the RunescapeAI window

#### Disclaimer

<sub>*Botting or using macros is against the rules of OSRS and may result in a ban.
This bot does its best to remain unpredictable and random to avoid detection. To minimize your chances of being banned
avoid using the bot for extended periods and cycle through different modes.
This bot is to be used at your own risk under the assumption that your account may be banned.*</sub>
