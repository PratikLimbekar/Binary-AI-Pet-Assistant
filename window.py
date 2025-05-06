"""
tkinter info:
widgets
A Tkinter user interface is made up of individual widgets. Each widget is represented as a Python object, instantiated from classes like ttk.Frame, ttk.Label, and ttk.Button.

widget hierarchy
Widgets are arranged in a hierarchy. The label and button were contained within a frame, which in turn was contained within the root window. When creating each child widget, its parent widget is passed as the first argument to the widget constructor.

configuration options
Widgets have configuration options, which modify their appearance and behavior, such as the text to display in a label or button. Different classes of widgets will have different sets of options.

geometry management
Widgets aren’t automatically added to the user interface when they are created. A geometry manager like grid controls where in the user interface they are placed.

event loop
Tkinter reacts to user input, changes from your program, and even refreshes the display only when actively running an event loop. If your program isn’t running the event loop, your user interface won’t update.
"""

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk #provides access to themed widgets, such as win11
import music
import pygame
import os
from dotenv import load_dotenv
from google import genai

import threading
import logging

logging.basicConfig(
    filename='aipp_chat_log.txt',
    level=logging.INFO,
    format='%(asctime)s - USER: %(message)s',
    datefmt='%d-%m-%Y %H: %M: %S'
)

#gemini
load_dotenv()
apikey = os.getenv('gemini_api_key')
client = genai.Client(api_key=apikey)

#following function sends text to AI
def getairesponse(text):
    try:
        response = client.models.generate_content(
        model="gemini-2.0-flash", contents = text
        )
        print(response.text)
        return response.text
    except Exception as e:
        return "Sorry, cannot comprehend this. Me just a pet bro."

#this handles the button click event
def sendmessage():
    input = user_entry.get()
    if input:
        response_label.config(text="Thinking...")
        response_label.grid(row=9, column=0)
        root.update_idletasks()

        user_entry.delete(0, tk.END)

        #implementing threading
        threading.Thread(target=handle_ai_response, args=(input,)).start()

def handle_ai_response(input):
    airesponse = getairesponse(input)

    def update_ui():
        response_label.config(text=airesponse)
    
    root.after(0, update_ui)

    logging.info(input)
    logging.info("AIPP: " + airesponse)

#initialise pygame
pygame.mixer.init()

#blinking functions
def blinktimer():
    if not music.is_playing:
        eye1.config(text='-' if eye1.cget("text") == "●" else "●")
        eye2.config(text='-' if eye2.cget("text") == "●" else "●")

    root.after(1001, blinktimer)

def blink(event=None):
    if not music.is_playing:
         eye1.config(text="-" if eye1.cget("text") == "●" else "●")
         eye2.config(text="-" if eye2.cget("text") == "●" else "●")
         #cget retrieves current value of widget config
    else:
        eye1.config(text="●")
        eye2.config(text="●")

#create window and initialise widgets
root = tk.Tk(screenName="AIPP")
# root.geometry("240x80")
root.attributes('-topmost', True)

frame = ttk.Frame(root, padding=10)#creates a frame widget inside a root window
frame.grid()

ttk.Label(frame, text="AIPP").grid(column=1, row=0) #label widget
eye1 = ttk.Label(frame, text="●", font=("Arial", 20))
eye1.grid(column=0, row=2)
eye2 = ttk.Label(frame, text="●", font=("Arial", 20))
eye2.grid(column=2, row=2)
play = ttk.Button(frame, text="⏯️",  #button widget
           command = lambda: [music.pausemusic(play)]
           )
next = ttk.Button(frame, text="⏭️",  #button widget
           command = lambda: [music.nextmusic(play)]
           )
prev = ttk.Button(frame, text="⏪",  #button widget
           command = lambda: [music.prevmusic(play)]
           )
play.grid(column=1, row=3)
next.grid(column=2, row=3)
prev.grid(column=0, row=3)

loop = ttk.Button(frame, text="Loop: OFF",  #button widget
           command = lambda: [music.toggleloop(loop)]
           )
shuffle = ttk.Button(frame, text="Shuffle OFF",  #button widget
           command = lambda: [music.toggleshuffle(shuffle)]
           )

loop.grid(column=1, row=4)
shuffle.grid(column=2, row=4)

volumelabel = ttk.Label(frame, text="Volume")
volumeslider = ttk.Scale(frame, from_=0, to=100, 
                         orient="horizontal", command=music.setvolume)
volumeslider.set(70)

volumelabel.grid(column=0, row=5)
volumeslider.grid(column=1, row=5, columnspan=2)

chat_box = scrolledtext.ScrolledText(root,
                                     wrap = tk.WORD, state='normal')
chat_box.grid(row=7, column=0)

user_entry = tk.Entry(root, width=40)
user_entry.grid(column=0, row=7)

sendbutton = tk.Button(root, text="Send", command=sendmessage)
sendbutton.grid(row=8, column=0)

response_label = tk.Label(root, text="", font=("Comic Sans MS", 12), wraplength=250, justify="left", bg="white", bd=2, relief="solid", padx=10, pady=5)


chat_box.grid_remove()

blinktimer()

eye1.bind("<Button-1>", blink)
eye2.bind("<Button-1>", blink)

music.check_music_end(root)


root.mainloop() #puts everything on display