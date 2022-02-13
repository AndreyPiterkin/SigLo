import math
from input import *

SCROLL_THRESH = 0.001 # Recommended between 0.005 and 0.001
SCALE_FACTOR = 40
SIGMOID_STRETCH = 10
OFFSET = 0

SCROLL_CONFIDENCE_THRESH = 0.9

SWIPE_THRESH = 0.001
SWIPE_UPPER_BOUND = 100

def delta_landmark(previous_landmark, current_landmark):
    return scroll_sens(current_landmark.x - previous_landmark.x), scroll_sens(current_landmark.y - previous_landmark.y), scroll_sens(current_landmark.z - previous_landmark.z)

def is_scroll(hand_data):
    return (2 * (hand_data.index) - 1) * hand_data.score < - SCROLL_CONFIDENCE_THRESH

def is_scroll_sideways(x, y):
    return abs(x) > abs(y)

def is_swipe(hand_data, x):
    return (2 * (hand_data.index) - 1) * hand_data.score > SCROLL_CONFIDENCE_THRESH and sigmoid(x) > SWIPE_THRESH

def swipe_sideways(x):
    if x > 0:
        swipe_left()
    else:
        swipe_right()

def gesture_handle(vels, hand_data):
    if is_scroll(hand_data):
        if is_scroll_sideways(vels[0], vels[1]):
            scroll_x(vels[0])
        else:
            scroll_y(vels[1])

    elif is_swipe(hand_data, vels[0]):
        swipe_sideways(vels[0])
                

def scroll_sens(x):
    return 0 if sigmoid(x) < SCROLL_THRESH else math.copysign(SCALE_FACTOR * sigmoid(x), x)

def sigmoid(x, factor=1): 
    x_new = 2 * abs(x)-1
    expo = -(SIGMOID_STRETCH * factor * (x_new + OFFSET))
    denom = math.e ** expo + 1
    return 1 / (denom + 1)
