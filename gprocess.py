from operator import is_
from input import *
import math

THRESH = 0.001 # Reccomended between 0.005 to 0.001
SCALE_FACTOR = 40
SIGMOID_STRETCH = 10
OFFSET = 0
        

def delta_landmark(previous_landmark, current_landmark):
    return scroll_sens(current_landmark.x - previous_landmark.x), scroll_sens(current_landmark.y - previous_landmark.y), scroll_sens(current_landmark.z - previous_landmark.z)

def is_scroll(hand_data, thresh):
    pass

def is_scroll_sideways(x, y):
    return abs(x) > abs(y)

def is_scroll_vertical(x, y):
    return abs(y) >= abs(x)

def gesture_handle(vels, hand_data):
    if is_scroll():
        if is_scroll_sideways(vels[0], vels[1]):
            scroll_x(vels[0])
            # pass
        elif is_scroll_vertical(vels[0], vels[1]):
            scroll_y(vels[1])
            # pass

def scroll_sens(x):
    x_new = 2*abs(x)-1
    expo = -(SIGMOID_STRETCH * (x_new + OFFSET))
    denom = math.e ** expo + 1
    sigmoid = 1/(denom+1)

    return 0 if sigmoid < THRESH else math.copysign(SCALE_FACTOR * sigmoid, x)
