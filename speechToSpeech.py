from tkinter import *

def speechTranslator(parent, backFunction):
    frame = Frame(parent, bg="#001f54")
    
    Label(frame, text="Speech to Speech Translator", font=("Arial",24,"bold"), background="#001f54", fg="white").pack(pady=50)

    Button(frame, text="Back", font=("Helvetica",18, "bold"), bg="#ff5733", fg="white", padx=20, pady=10, command=backFunction).pack(pady=20)
    frame.pack_propagate(False)
    frame.grid_propagate(False)
    return frame