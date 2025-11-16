from tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import tensorflow as tf

# ✅ FIX FOR OLD .h5 MODEL - Use tf.keras instead of keras package
from tensorflow.keras.models import load_model


def emotionDetection(parent, backFunction, cam_index=0):

    # ---------- FRAME ----------
    frame = Frame(parent, bg="#001f54")

    Label(frame, text="EMOTION DETECTION",
          font=("Arial", 24, "bold"),
          bg="#001f54", fg="white").pack(pady=20)

    # Video feed display
    video_label = Label(frame, bg="#003566")
    video_label.pack(pady=20, expand=True)

    # ---------- LOAD EMOTION MODEL ----------
    try:
        model = load_model("emotion_detection_model.h5")
        print("Model loaded successfully!")
    except Exception as e:
        print("Error loading model:", e)
        model = None

    LABELS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    # Face detection model
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # ---------- CAMERA STATE ----------
    cap = None
    update_job = None

    # ---------- PREPROCESS FACE ----------
    def preprocess_face(face):
        face = cv2.resize(face, (48, 48))
        face = face.astype("float32") / 255.0
        face = np.expand_dims(face, axis=-1)
        face = np.expand_dims(face, axis=0)
        return face

    # ---------- UPDATE CAMERA FRAME ----------
    def update_frame():
        nonlocal cap, update_job

        try:
            ret, frame_bgr = cap.read()
            if not ret:
                update_job = video_label.after(20, update_frame)
                return

            # Check if model loaded successfully
            if model is None:
                video_label.config(text="Error: Model failed to load", fg="red")
                return

            gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5
            )

            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                face_input = preprocess_face(roi)

                # Predict emotion
                preds = model.predict(face_input, verbose=0)[0]
                label = LABELS[np.argmax(preds)]
                prob = np.max(preds)

                # Draw bounding box + label
                cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame_bgr,
                    f"{label} ({prob:.2f})",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            # Convert OpenCV frame to Tkinter image
            rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(rgb))
            video_label.imgtk = imgtk
            video_label.config(image=imgtk)

            update_job = video_label.after(20, update_frame)
        except Exception as e:
            print(f"Error in update_frame: {e}")
            update_job = video_label.after(20, update_frame)

    # ---------- START CAMERA ----------
    def start_camera():
        nonlocal cap
        cap = cv2.VideoCapture(cam_index)

        if not cap.isOpened():
            video_label.config(text="Error: Could not open camera", fg="white")
            return

        update_frame()

    # ---------- STOP CAMERA ----------
    def stop_camera():
        nonlocal cap, update_job
        if update_job:
            video_label.after_cancel(update_job)
        if cap:
            cap.release()
        video_label.config(image="", text="")

    # ---------- BACK BUTTON ----------
    def on_back():
        stop_camera()
        backFunction()

    Button(
        frame,
        text="Back",
        font=("Helvetica", 18, "bold"),
        bg="#ff5733",
        fg="white",
        padx=20,
        pady=10,
        command=on_back
    ).pack(pady=20)

    frame.start_camera = start_camera
    frame.stop_camera = stop_camera
    frame.pack_propagate(False)
    frame.grid_propagate(False)

    return frame



# frame = Frame(parent, bg="#001f54")
    
#     Label(
#         frame,
#         text="Speech to Speech Translator",
#         font=("Arial", 24, "bold"),
#         background="#001f54",
#         fg="white"
#     ).pack(pady=50)

#     Button(
#         frame,
#         text="Back",
#         font=("Helvetica", 18, "bold"),
#         bg="#ff5733",
#         fg="white",
#         padx=20,
#         pady=10,
#         command=backFunction
#     ).pack(pady=20)

#     frame.pack_propagate(False)
#     frame.grid_propagate(False)

#     return frame