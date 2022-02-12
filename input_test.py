from pynput.keyboard import Controller as kb_controller
from pynput.keyboard import Key
import time

keyboard = kb_controller()


time.sleep(5)
with keyboard.pressed(Key.alt_l):
    keyboard.press(Key.left)
    time.sleep(0.1)
keyboard.release(Key.alt_l)
keyboard.release(Key.left)