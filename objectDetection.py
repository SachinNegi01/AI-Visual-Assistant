from tkinter import *
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO


# ----------frame display function ---------
def objectDetection(parent, backFunction, cam_index=0):
    frame = Frame(parent, bg="#001f54")

    video_label = Label(frame, bg="#f77f00")
    video_label.pack(pady=20, expand= True)

    Label(frame, text="OBJECT DETECTION", font=("Arial",24,"bold"), background="#001f54", fg="white").pack(pady=50)

    def on_back():
        stop_camera()
        backFunction()
    
    Button(frame, text="Back", font=("Helvetica",18, "bold"), bg="#ff5733", fg="white", padx=20, pady=10, command=on_back).pack(pady=20)
    
    # camera comtrols variabless
    cap = None
    update_job = None

    model = YOLO("yolov8n.pt")     #yolo model loaded........

    def start_camera():
        nonlocal cap, update_job
        if cap is not None and cap.isOpened():
            return # return camera already open....
        cap = cv2.VideoCapture(cam_index)

        if not cap.isOpened():
            video_label.config(text= "Error: couldn't open camera", bg="#fcbf49", fg="white", font=("Arial",18,"bold"))
            cap = None
            return
        video_label.config(text="")
        update_frame()
    
    def update_frame():
        nonlocal cap, update_job
        if cap is None:
            return
        
        ret, frame_bgr = cap.read()

        if not ret:
            update_job = video_label.after(100, update_frame)
            return
        
        
        # YOLO model prediction----------------------------
        frame_bgr = cv2.resize(frame_bgr, (640, 480))
        results = model(frame_bgr, verbose=False)
        annoted_frame = results[0].plot()
        

        frame_rgb = cv2.cvtColor(annoted_frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        video_label.imgtk = imgtk
        video_label.config(image=imgtk)

        update_job = video_label.after(30, update_frame)
    
    def stop_camera():
        nonlocal cap, update_job
        if update_job is not None:
            try:
                video_label.after_cancel(update_job)
            except Exception:
                pass
            update_job = None
        
        if cap is not None:
            try:
                cap.release()
            except Exception:
                pass
            cap = None
        
        video_label.config(image='', text='')

    frame.start_camera = start_camera
    frame.stop_camera = stop_camera
        
    
    frame.pack_propagate(False)
    frame.grid_propagate(False)
    return frame