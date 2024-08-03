'''
Run These commands to install the dependencies

sudo apt-get install python3-tk python3-dev
pip install Pillow
sudo apt install gnome-screenshot

'''

import pyautogui

# Take a screenshot
screenshot = pyautogui.screenshot()

# Save the screenshot to a file
screenshot.save('screenshot.png')

print("Screenshot saved as screenshot.png")
