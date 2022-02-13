from pynput.mouse import Button, Controller
from pynput.keyboard import Controller as kb_controller
from pynput.keyboard import Key
import time

keyboard = kb_controller()

mouse = Controller()

def scroll_x(scroll_amount):
    mouse.scroll(scroll_amount, 0)

def scroll_y(scroll_amount):
    mouse.scroll(0, scroll_amount)

def swipe_left():
    keyboard.press(Key.left)
    time.sleep(0.05)
    keyboard.release(Key.left)

def swipe_right():
    keyboard.press(Key.right)
    time.sleep(0.05)
    keyboard.release(Key.right)
