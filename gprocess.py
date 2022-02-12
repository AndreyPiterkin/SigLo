from operator import is_
from unittest.case import DIFF_OMITTED
from input import *
import math

THRESH = 0.001 # Recommended between 0.005 and 0.001
SCALE_FACTOR = 40
SIGMOID_STRETCH = 10
OFFSET = 0

SCROLL_CONFIDENCE_THRESH = -0.6

SWIPE_SCALE_FACTOR = 1000
SWIPE_MIN_SENSE = 60
SWIPE_MAX_SENSE = 600
SWIPE_DIST = 0.06

def delta_landmark(previous_landmark, current_landmark):
    return scroll_sens(current_landmark.x - previous_landmark.x), scroll_sens(current_landmark.y - previous_landmark.y), scroll_sens(current_landmark.z - previous_landmark.z)

def is_scroll(hand_data):
    return (2 * (hand_data.index) - 1) * hand_data.score < SCROLL_CONFIDENCE_THRESH

def is_scroll_sideways(x, y):
    return abs(x) > abs(y)

def is_scroll_vertical(x, y):
    return abs(y) >= abs(x)

def is_left_swipe(hand_classification, landmarks, previous_landmarks):
    pointer_middle_dist = abs(landmarks.landmark[7].y - landmarks.landmark[11].y)
    middle_ring_dist = abs(landmarks.landmark[11].y - landmarks.landmark[15].y)
    ring_pinky_dist = abs(landmarks.landmark[15].y - landmarks.landmark[19].y)

    mean_dist = (pointer_middle_dist + middle_ring_dist + ring_pinky_dist) / 3
    avg_x = (landmarks.landmark[7].x + landmarks.landmark[11].x + landmarks.landmark[15].x + landmarks.landmark[19].x) / 4
    prev_avg = (previous_landmarks.landmark[7].x + previous_landmarks.landmark[11].x + previous_landmarks.landmark[15].x + previous_landmarks.landmark[19].x) / 4
    
    diff = avg_x - prev_avg

    return (hand_classification.score > 0.75 and hand_classification.index == 1 and mean_dist < SWIPE_DIST and diff * SWIPE_SCALE_FACTOR < SWIPE_MAX_SENSE and diff * SWIPE_SCALE_FACTOR > SWIPE_MIN_SENSE)

def is_right_swipe(hand_classification, landmarks, previous_landmarks):
    pointer_middle_dist = abs(landmarks.landmark[7].y - landmarks.landmark[11].y)
    middle_ring_dist = abs(landmarks.landmark[11].y - landmarks.landmark[15].y)
    ring_pinky_dist = abs(landmarks.landmark[15].y - landmarks.landmark[19].y)

    mean_dist = (pointer_middle_dist + middle_ring_dist + ring_pinky_dist) / 3
    avg_x = (landmarks.landmark[7].x + landmarks.landmark[11].x + landmarks.landmark[15].x + landmarks.landmark[19].x) / 4
    prev_avg = (previous_landmarks.landmark[7].x + previous_landmarks.landmark[11].x + previous_landmarks.landmark[15].x + previous_landmarks.landmark[19].x) / 4
    
    diff = avg_x - prev_avg
    return (hand_classification.score > 0.75 and hand_classification.index == 1 and mean_dist < SWIPE_DIST and abs(diff * SWIPE_SCALE_FACTOR) > SWIPE_MIN_SENSE and abs(diff * SWIPE_SCALE_FACTOR) < SWIPE_MAX_SENSE)

def gesture_handle(vels, hand_classification, landmarks, previous_landmarks):
    if is_scroll(hand_classification):
        if is_scroll_sideways(vels[0], vels[1]):
            scroll_x(vels[0])
        elif is_scroll_vertical(vels[0], vels[1]):
            scroll_y(vels[1])
    elif is_left_swipe(hand_classification, landmarks, previous_landmarks):
        swipe_left()
    elif is_right_swipe(hand_classification, landmarks, previous_landmarks):
        swipe_right()

def scroll_sens(x):
    x_new = 2 * abs(x)-1
    expo = -(SIGMOID_STRETCH * (x_new + OFFSET))
    denom = math.e ** expo + 1
    sigmoid = 1/(denom + 1)

    return 0 if sigmoid < THRESH else math.copysign(SCALE_FACTOR * sigmoid, x)
