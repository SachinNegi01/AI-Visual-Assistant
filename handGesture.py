from tkinter import *
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import pyttsx3
import time


def handGesture(parent, backFunction, cam_index=0):
    frame = Frame(parent, bg="#001f54")

    Label(frame, text="HAND GESTURE DETECTION", font=("Arial",24,"bold"),
          bg="#001f54", fg="white").pack(pady=30)

    video_label = Label(frame, bg="#003566")
    video_label.pack(pady=20, expand=True)

    # ===================== INITIALIZATION =====================
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    last_spoken = ["", 0]  # [text, time]

    cap = None
    update_job = None

    # ===================== SPEAK FUNCTION =====================
    def speak(text):
        if text != last_spoken[0] or time.time() - last_spoken[1] > 4:
            engine.say(text)
            engine.runAndWait()
            last_spoken[0] = text
            last_spoken[1] = time.time()

    # ===================== GESTURE DETECTION =====================
    def detect_gesture(lm):
        thumb = lm[4].y
        index = lm[8].y
        middle = lm[12].y
        ring = lm[16].y
        pinky = lm[20].y

        if thumb < index < middle:
            return "Thumbs Up"
        elif thumb > index > middle:
            return "Thumbs Down"
        elif index < ring and middle < ring:
            return "Peace"
        elif abs(index - middle) < 0.02:
            return "Hello"
        return None

    def detect_sign(lm):
        tips = [4, 8, 12, 16, 20]
        base = [2, 5, 9, 13, 17]

        fingers = []
        for i in range(1, 5):
            fingers.append(1 if lm[tips[i]].y < lm[base[i]].y else 0)

        thumb_open = lm[4].x > lm[2].x

        if fingers == [0,0,0,0] and not thumb_open:
            return "A"
        elif fingers == [1,1,1,1] and not thumb_open:
            return "B"
        elif fingers == [1,1,0,0] and thumb_open:
            return "C"
        return None

    # ===================== CAMERA LOOP =====================
    def update_frame():
        nonlocal update_job, cap

        ret, frame_bgr = cap.read()
        if not ret:
            update_job = video_label.after(30, update_frame)
            return

        frame_bgr = cv2.flip(frame_bgr, 1)
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for handLMS in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame_bgr, handLMS, mp_hands.HAND_CONNECTIONS)

                g = detect_gesture(handLMS.landmark)
                s = detect_sign(handLMS.landmark)

                detected = s if s else g if g else "Hand Detected"
                speak(detected)

                cv2.putText(frame_bgr, f"{detected}", (20, 60),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,0), 2)

        img = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(img))

        video_label.imgtk = img
        video_label.config(image=img)

        update_job = video_label.after(20, update_frame)

    # ===================== START CAMERA =====================
    def start_camera():
        nonlocal cap
        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            video_label.config(text="Failed to open camera")
            return
        update_frame()

    # ===================== STOP CAMERA =====================
    def stop_camera():
        nonlocal cap, update_job
        if update_job:
            video_label.after_cancel(update_job)
        if cap:
            cap.release()
        video_label.config(image='')

    # BACK BUTTON
    def on_back():
        stop_camera()
        backFunction()

    Button(frame, text="Back", font=("Helvetica",18,"bold"),
           bg="#ff5733", fg="white", padx=20, pady=10,
           command=on_back).pack(pady=20)

    frame.start_camera = start_camera
    frame.stop_camera = stop_camera

    return frame
