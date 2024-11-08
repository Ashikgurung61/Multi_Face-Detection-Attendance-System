from tkinter import *
from tkinter import messagebox

def get_button(window, text, color, command, fg = "white"):
    button = Button(
        window,
        text = text,
        activebackground="black",
        activeforeground="white",
        fg = fg,
        bg = color, 
        command = command,
        height = 2,
        width=20, 
        font=('Helvetica bold', 20)
    )
    return button
def get_img_label(window):
    label = Label(window, background="#132a49")
    label.grid(row = 0, column = 0)
    return label

def get_text_label(window, text):
    label = Label(window, text = text)
    label.config(font=("sans-serif", 21), justify="left")
    return label

def get_entry_text(window):
    inputtext = Text(window, height= 2, width=15, font=("Arial", 32))
    return inputtext