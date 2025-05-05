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
from tkinter import ttk #provides access to themed widgets, such as win11
import music
import pygame

pygame.mixer.init()

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



def blinktimer():
    if not music.is_playing:
        eye1.config(text='-' if eye1.cget("text") == "●" else "●")
        eye2.config(text='-' if eye2.cget("text") == "●" else "●")

    root.after(1001, blinktimer)

blinktimer()

def blink(event=None):
    if not music.is_playing:
         eye1.config(text="-" if eye1.cget("text") == "●" else "●")
         eye2.config(text="-" if eye2.cget("text") == "●" else "●")
         #cget retrieves current value of widget config
    else:
        eye1.config(text="●")
        eye2.config(text="●")

eye1.bind("<Button-1>", blink)
eye2.bind("<Button-1>", blink)

music.check_music_end(root)
root.mainloop() #puts everything on display