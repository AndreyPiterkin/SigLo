from operator import is_
from input import *
import math

THRESH = 0.5
SCALE_FACTOR = 1.3
SIGMOID_STRETCH = 1

def delta_landmark(previous_landmark, current_landmark):
    return scroll_sens(current_landmark.x - previous_landmark.x), scroll_sens(current_landmark.y - previous_landmark.y), scroll_sens(current_landmark.z - previous_landmark.z)

def is_gesture(vels):
    return any(abs(vels[i]) > THRESH for i in range(2))

def is_scroll_sideways(x, y):
    return abs(x) > abs(y) and abs(x) > THRESH

def is_scroll_vertical(x, y):
    return abs(y) >= abs(x) and abs(y) > THRESH

def gesture_handle(vels):
    if is_gesture(vels):
        if is_scroll_sideways(vels[0], vels[1]):
            scroll_x(vels[0])
        elif is_scroll_vertical(vels[0], vels[1]):
            scroll_y(vels[1])

def scroll_sens(x):
    sigmoid = (1 / (math.exp(-(tan_shift(abs(x))) * SIGMOID_STRETCH) + 1)) + 1
    if  sigmoid < THRESH:
        return 0
    else:
        return math.copysign(SCALE_FACTOR * sigmoid, x)

def tan_shift(x): 
    return math.tan(((x + (math.pi / 2)) / math.pi))
