# imports
import pyautogui
import keyboard

# coordinate class
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# information regarding the screenshot region
def get_region_info():
    # set coordinates
    pos1 = Coordinate(1260, 730)
    pos2 = Coordinate(2930, 1585)
    
    # calculate width and height
    width = pos2.x - pos1.x
    height = pos2.y - pos1.y
    return pos1.x, pos1.y, width, height

# counter to name the images
global counter
counter = 0

# function so save screenshots
def save_screenshot():
    global counter
    counter = counter + 1
    
    # set the dir and filename - assumes os.cwd is ~/dissertation-project/
    screenshot_dir = ".\\auction-house-screenshots\\"
    screenshot_name = r'{0}page_{1}.png'.format(screenshot_dir, counter)
    
    # get values for region
    screenshot_region = get_region_info()
    
    # take screenshot of region
    pyautogui.screenshot(screenshot_name, screenshot_region)
    print(r"Screenshot Captured: {0}".format(screenshot_name))

# check for hotkey pressed on keyboard
keyboard.add_hotkey('alt', save_screenshot)

# main loop
while True:
    x, y = pyautogui.position()
    posStr = r'({0}, {1})'.format(x, y)
    #print(posStr) # UNCOMMENT IF POSITIONS NEED TO BE UPDATED