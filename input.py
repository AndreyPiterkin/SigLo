from pynput.mouse import Button, Controller

mouse = Controller()

def scroll_x(scroll_amount):
    mouse.scroll(scroll_amount, 0)

def scroll_y(scroll_amount):
    mouse.scroll(0, scroll_amount)