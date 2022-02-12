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
    with keyboard.pressed(Key.alt_l):
        keyboard.press(Key.left)
        time.sleep(0.1)
    keyboard.release(Key.alt_l)
    keyboard.release(Key.left)

def swipe_right():
    with keyboard.pressed(Key.alt_l):
        keyboard.press(Key.right)
        time.sleep(0.1)
    keyboard.release(Key.alt_l)
    keyboard.release(Key.right)

def type_a():
    keyboard.type("a")
    print("a pressed")