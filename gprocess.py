from operator import is_
from input import *
import math

THRESH = 0.02
SCALE_FACTOR = 20
SIGMOID_STRETCH = 100
OFFSET = 0
        

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
            # pass
        elif is_scroll_vertical(vels[0], vels[1]):
            scroll_y(vels[1])
            # pass

def scroll_sens(x):
    x_new = 2*x-1
    expo = -SIGMOID_STRETCH * (abs(x_new) + OFFSET)
    denom = math.e ** expo + 1
    sigmoid = 1/(denom+1)

    if  sigmoid < THRESH:
        return 0
    else:
        return math.copysign(SCALE_FACTOR * sigmoid, x)
    