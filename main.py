from tkinter import *
import speechToSpeech, objectDetection, handGesture, emotionDetection

# ---------------- UI show function --------

def showMainUI():
    speechtospeechUI.pack_forget()
    gotoObjectDetection.pack_forget()
    gotohandGesture.pack_forget()
    gotoEmotionDetection.pack_forget()
    main_frame.pack(fill="both", expand= True)

def speechtospeechUI():
    main_frame.pack_forget()
    speechtospeechUI.pack(fill="both", expand= True)

def gotoObjectDetection():
    main_frame.pack_forget()
    gotoObjectDetection.pack(fill="both", expand= True)
    gotoObjectDetection.start_camera()

def gotohandGesture():
    main_frame.pack_forget()
    gotohandGesture.pack(fill="both", expand= True)
    gotohandGesture.start_camera()

def gotoEmotionDetection():
    main_frame.pack_forget()
    gotoEmotionDetection.pack(fill="both", expand= True)
    gotoEmotionDetection.start_camera()


root = Tk()
root.title("AI Virtual Assistant")
root.state('zoomed')
root.configure(bg="#000814")

#-------------main frame----------------

main_frame = Frame(root, bg="#000814")

heading = Label(main_frame, text="PLEASE MAKE YOUR SELCTION!", font=("Arial",24,"bold"),background="#000814" ,fg="#003566")
heading.pack(pady=50)

button1 = Button(main_frame, text="Speech to Speech", font=("Helvetica",18, "bold"), bg="#ffc300", fg="white", padx=20, pady=10, command=speechtospeechUI)
button2 = Button(main_frame, text="Detect Object", font=("Helvetica",18, "bold"), bg="#ffc300", fg="white", padx=20, pady=10, command=gotoObjectDetection)
button3 = Button(main_frame, text="Hand Gesture", font=("Helvetica",18, "bold"), bg="#ffc300", fg="white", padx=20, pady=10, command=gotohandGesture)
button4 = Button(main_frame, text="Emotion Detection", font=("Helvetica",18, "bold"), bg="#ffc300", fg="white", padx=20, pady=10, command=gotoEmotionDetection)
button1.pack(pady=20)
button2.pack(pady=20)
button3.pack(pady=20)
button4.pack(pady=20)

main_frame.pack(fill="both", expand= True)
main_frame.pack_propagate(False)
main_frame.grid_propagate(False)
# -----speech frame---------------
speechtospeechUI = speechToSpeech.speechTranslator(root, showMainUI)
gotoEmotionDetection = emotionDetection.emotionDetection(root, showMainUI)
gotohandGesture = handGesture.handGesture(root, showMainUI)
gotoObjectDetection = objectDetection.objectDetection(root, showMainUI)

root.mainloop()