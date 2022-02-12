from operator import is_
from unittest.case import DIFF_OMITTED
from input import *
import math

THRESH = 0.5
SCALE_FACTOR = 1.3
SIGMOID_STRETCH = 1
LEFT_KEY = "a"
RIGHT_KEY = "d"
SWIPE_SCALE_FACTOR = 1000
SWIPE_MIN_SENSE = 60
SWIPE_MAX_SENSE = 600
SWIPE_DIST = 0.06

def delta_landmark(previous_landmark, current_landmark):
    return scroll_sens(current_landmark.x - previous_landmark.x), scroll_sens(current_landmark.y - previous_landmark.y), scroll_sens(current_landmark.z - previous_landmark.z)

def is_gesture(vels):
    return any(abs(vels[i]) > THRESH for i in range(2))

def is_scroll_sideways(x, y):
    return abs(x) > abs(y) and abs(x) > THRESH

def is_scroll_vertical(x, y):
    return abs(y) >= abs(x) and abs(y) > THRESH

def is_left_swipe(hand, confidence, landmarks, previous_landmarks):
    pointer_middle_dist = abs(landmarks.landmark[7].y - landmarks.landmark[11].y)
    middle_ring_dist = abs(landmarks.landmark[11].y - landmarks.landmark[15].y)
    ring_pinky_dist = abs(landmarks.landmark[15].y - landmarks.landmark[19].y)
    mean_dist = (pointer_middle_dist + middle_ring_dist + ring_pinky_dist) / 3
    avg_x = (landmarks.landmark[7].x + landmarks.landmark[11].x + landmarks.landmark[15].x + landmarks.landmark[19].x) / 4
    prev_avg = (previous_landmarks.landmark[7].x + previous_landmarks.landmark[11].x + previous_landmarks.landmark[15].x + previous_landmarks.landmark[19].x) / 4
    diff = avg_x - prev_avg
    return (confidence > 0.75 and hand == "Right" and mean_dist < SWIPE_DIST and diff * SWIPE_SCALE_FACTOR < SWIPE_MAX_SENSE and diff * SWIPE_SCALE_FACTOR > SWIPE_MIN_SENSE)

def is_right_swipe(hand, confidence, landmarks, previous_landmarks):
    pointer_middle_dist = abs(landmarks.landmark[7].y - landmarks.landmark[11].y)
    middle_ring_dist = abs(landmarks.landmark[11].y - landmarks.landmark[15].y)
    ring_pinky_dist = abs(landmarks.landmark[15].y - landmarks.landmark[19].y)
    mean_dist = (pointer_middle_dist + middle_ring_dist + ring_pinky_dist) / 3
    avg_x = (landmarks.landmark[7].x + landmarks.landmark[11].x + landmarks.landmark[15].x + landmarks.landmark[19].x) / 4
    prev_avg = (previous_landmarks.landmark[7].x + previous_landmarks.landmark[11].x + previous_landmarks.landmark[15].x + previous_landmarks.landmark[19].x) / 4
    diff = avg_x - prev_avg
    print(diff * SWIPE_SCALE_FACTOR)
    return (confidence > 0.75 and hand == "Right" and mean_dist < SWIPE_DIST and abs(diff * SWIPE_SCALE_FACTOR) > SWIPE_MIN_SENSE and abs(diff * SWIPE_SCALE_FACTOR) < SWIPE_MAX_SENSE)

def gesture_handle(vels, hand, confidence, landmarks, previous_landmarks):
    if is_gesture(vels):
        if is_left_swipe(hand, confidence, landmarks, previous_landmarks):
            swipe_left()
        elif is_right_swipe(hand, confidence, landmarks, previous_landmarks):
            swipe_right()
        #elif is_scroll_sideways(vels[0], vels[1]):
         #   scroll_x(vels[0])
        #elif is_scroll_vertical(vels[0], vels[1]):
         #   scroll_y(vels[1])

def scroll_sens(x):
    sigmoid = (1 / (math.exp(-(tan_shift(abs(x))) * SIGMOID_STRETCH) + 1)) + 1
    if  sigmoid < THRESH:
        return 0
    else:
        return math.copysign(SCALE_FACTOR * sigmoid, x)

def tan_shift(x): 
    return math.tan(((x + (math.pi / 2)) / math.pi))
