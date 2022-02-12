import cv2
import mediapipe as mp
from numpy import False_
import gprocess as gp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  previous_landmark = False
  previous_landmarks = False
  while cap.isOpened():
    success, image = cap.read()
    
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape
    if results.multi_hand_landmarks:
      for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
        if not previous_landmark:
         gp.gesture_handle(gp.delta_landmark(hand_landmarks.landmark[7], hand_landmarks.landmark[7]), results.multi_handedness[i].classification[0], hand_landmarks, hand_landmarks)
        else:
         gp.gesture_handle(gp.delta_landmark(previous_landmark, hand_landmarks.landmark[7]), results.multi_handedness[i].classification[0], hand_landmarks, previous_landmarks)
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        previous_landmark = hand_landmarks.landmark[8]
        previous_landmarks = hand_landmarks
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()