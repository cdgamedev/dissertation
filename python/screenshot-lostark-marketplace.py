import pyautogui
import keyboard
import time

global counter
counter = 0

def save_screenshot():
    global counter
    counter = counter + 1
    screenshot_dir = r'.\auction-house-screenshots\page_{0}.png'.format(counter)
    pyautogui.screenshot(screenshot_dir, region=(1260, 670, 2930-1260, 1630-670))
    print(r"Screenshot Captured: {0}".format(screenshot_dir))
    
keyboard.add_hotkey('alt', save_screenshot)
    
while True:
    x, y = pyautogui.position()
    posStr = r'({0}, {1})'.format(x, y)
    #print(posStr)