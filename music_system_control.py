import os
import cv2
import mediapipe as mp
import numpy as np
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8888/callback") 

if not CLIENT_ID or not CLIENT_SECRET:
    print("Missing CLIENT_ID or CLIENT_SECRET in .env file.")
    exit()

# Initialize Spotify API
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state"
    ))
    print("Spotify API initialized successfully.")
except Exception as e:
    print(f"Error initializing Spotify API: {e}")
    exit()

# Function to open Spotify on macOS
def open_spotify():
    os.system("open -a Spotify")

# Initialize MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Function to classify hand gestures
def detect_gesture(landmarks):
    try:
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]

        thumb_index_dist = np.linalg.norm(np.array(thumb_tip[:2]) - np.array(index_tip[:2]))
        thumb_middle_dist = np.linalg.norm(np.array(thumb_tip[:2]) - np.array(middle_tip[:2]))
        index_ring_dist = np.linalg.norm(np.array(index_tip[:2]) - np.array(ring_tip[:2]))

        if thumb_index_dist < 0.1 and thumb_middle_dist > 0.15:
            return "play"
        elif thumb_middle_dist < 0.1:
            return "pause"
        elif index_ring_dist > 0.2:
            return "next"
        elif index_ring_dist < 0.1:
            return "previous"
        elif index_tip[1] < middle_tip[1] < ring_tip[1] < pinky_tip[1]:
            return "volume up"
        elif index_tip[1] > middle_tip[1] > ring_tip[1] > pinky_tip[1]:
            return "volume down"
        elif index_tip[0] < thumb_tip[0]:
            return "push"
        elif index_tip[0] > thumb_tip[0]:
            return "pop"
        else:
            return "none"
    except Exception as e:
        print(f"Error in gesture detection: {e}")
        return "none"

# Function to control Spotify playback
def control_spotify(gesture):
    try:
        print(f"Detected gesture: {gesture}")
        current_playback = sp.current_playback()
        if not current_playback:
            print("No active playback session found.")

        if gesture == "play":
            sp.start_playback()
            print("Playing music...")
        elif gesture == "pause":
            if current_playback:
                sp.pause_playback()
                print("Pausing music...")
        elif gesture == "next":
            sp.next_track()
            print("Skipping to the next track...")
        elif gesture == "previous":
            sp.previous_track()
            print("Going back to the previous track...")
        elif gesture == "volume up":
            if current_playback and current_playback.get('device'):
                current_volume = current_playback['device']['volume_percent']
                new_volume = min(current_volume + 10, 100)
                sp.volume(new_volume)
                print(f"Volume increased to {new_volume}%.")
        elif gesture == "volume down":
            if current_playback and current_playback.get('device'):
                current_volume = current_playback['device']['volume_percent']
                new_volume = max(current_volume - 10, 0)
                sp.volume(new_volume)
                print(f"Volume decreased to {new_volume}%.")
        elif gesture == "push":
            print("Push action detected.")
        elif gesture == "pop":
            print("Pop action detected.")
    except spotipy.exceptions.SpotifyException as e:
        if 'Premium required' in str(e):
            print("This feature requires a Spotify Premium account.")
        else:
            print(f"Spotify API Error: {e}")
    except Exception as e:
        print(f"Unexpected error in Spotify control: {e}")

# Webcam video capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    gesture = "none"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
            gesture = detect_gesture(landmarks)

    cv2.putText(frame, f"Gesture: {gesture}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if gesture != "none":
        control_spotify(gesture)

    cv2.imshow("Gesture-Controlled Spotify", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
