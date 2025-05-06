import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk #provides access to themed widgets, such as win11
import music
import pygame
import os
from dotenv import load_dotenv
from google import genai
import voice
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

#initialise pygame
pygame.mixer.init()
isstaring = False
ttsenabled = False
collapseafterid = None #global var to track scheduled collapse
stayactive = False #stay active for window

#fonts and colors
FONT_MAIN = ("Segoe UI", 10)
FONT_AI = ("Comic Sans MS", 12)
COLOR_root = "#353935"
COLOR_BUTTON = "#36454F"
COLOR_FG = "#FEFCFB"

#following function sends text to AI
def getairesponse(text):
    wiseprompt = (
        "You are Binary, a wise old owl who speaks calmly and thoughtfully. You explain things clearly, using gentle and poetic language. Keep responses short but meaningful. At most three sentences. Single word answers are preferred."
    )
    try:
        response = client.models.generate_content(
        model="gemini-2.0-flash", contents = wiseprompt + text
        )
        print(response.text)
        return response.text
    except Exception as e:
        return "Sorry, cannot comprehend this. Me just a pet bro."

#this handles the button click event
def sendmessage():
    input = user_entry.get()
    if input:
        sendbutton.config(state='disabled')
        response_label.grid(row=9, column=0, columnspan=2, sticky="w")
        response_label.config(text="Thinking...")
        response_label.grid(row=9, column=0)
        root.update_idletasks()
        user_entry.delete(0, tk.END)
        threading.Thread(target=handle_ai_response, args=(input,)).start()

def handle_ai_response(input):
    airesponse = getairesponse(input)
    if airesponse:
        def update_ui():
            response_label.config(text=airesponse)
            response_label.grid(row=9, column=0, columnspan=2, sticky="w")
            exitbutton.grid(row=9, column=2, sticky="e")

            sendbutton.config(state='normal')
        root.after(0, update_ui)
        logging.info(input)
        logging.info("AIPP: " + airesponse)
        return airesponse
    else:
        return None

def blinktimer():
    if not music.is_playing and not isstaring:
        eye1_canvas.itemconfig(eye1_id, fill='black' if eye1_canvas.itemcget(eye1_id, "fill") == "#fefcfb" else "#fefcfb")
        eye2_canvas.itemconfig(eye2_id, fill='black' if eye2_canvas.itemcget(eye2_id, "fill") == "#fefcfb" else "#fefcfb")
    elif isstaring:
        eye1_canvas.itemconfig(eye1_id, fill='black')
        eye2_canvas.itemconfig(eye2_id, fill='black')
    root.after(1001, blinktimer)

def blink(event=None):
    if not music.is_playing and not isstaring:
        eye1_canvas.itemconfig(eye1_id, fill='#fefcfb' if eye1_canvas.itemcget(eye1_id, "fill") == "black" else "black")
        eye2_canvas.itemconfig(eye2_id, fill='#fefcfb' if eye2_canvas.itemcget(eye2_id, "fill") == "black" else "black")
    else:
        eye1_canvas.itemconfig(eye1_id, fill='black')
        eye2_canvas.itemconfig(eye2_id, fill='black')

def look():
    global isstaring
    isstaring = True

def voicethread():
    global isstaring, ttsenabled
    while True:
        userinput = voice.waitforbinary()
        if userinput:
            look()
            response = handle_ai_response(userinput)
            if ttsenabled:
                voice.speakresponse(response)
            isstaring = False

def toggletts():
    global ttsenabled
    ttsenabled = not ttsenabled
    tts.config(text="TTS: ON" if ttsenabled else "TTS: OFF")

def clearresponse():
    response_label.grid_forget()
    exitbutton.grid_forget()
    chatframe.grid_forget()
    # chat_box.grid_forget()

def expand_ui(event=None):
    root.overrideredirect(False)
    controlsframe.grid()
    sendframe.grid()
    chatframe.grid()
    root.update_idletasks() #forces layout to update *before* resizing
    root.geometry("")

def collapse_gui(event=None):
    controlsframe.grid_remove()
    sendframe.grid_remove()
    chatframe.grid_remove()
    root.update_idletasks()
    root.overrideredirect(True)
    root.geometry("")

def schedule_collapse():
    global collapseafterid
    if stayactive:
        return
    if collapseafterid is not None:
        root.after_cancel(collapseafterid)
    collapseafterid = root.after(6000, collapse_gui) #3second delay

def cancelscheduledcollapse(event=None):
    global collapseafterid
    if collapseafterid is not None:
        root.after_cancel(collapseafterid)
        collapseafterid = None


def togglestay():
    global stayactive
    stayactive = not stayactive
    staybutton.config(text="Stay: ON" if stayactive else "Stay: OFF",
                      bg="#000000" if stayactive else "#36454f")
    
    if not stayactive:
        # If Stay is turned off, start collapse countdown
        schedule_collapse()

root = tk.Tk(screenName="Binary")
root.bind("<FocusOut>",lambda e: schedule_collapse())
root.bind("<FocusIn>", cancelscheduledcollapse)
root.configure(bg='#f0f0f0')
root.attributes('-topmost', True)
root.overrideredirect(True) #removes window borders

style = ttk.Style()
style.configure('TButton', font=FONT_MAIN, padding=5)
style.configure('TLabel', font=FONT_MAIN)
style.theme_use('clam')

for i in range(3):
    root.columnconfigure(i, weight=1)
for i in range(10):
    root.rowconfigure(i, weight=1)

controlsframe = tk.Frame(root, bg='#36454f')
controlsframe.grid(row=5, column=0, columnspan=3, pady=5)

sendframe = tk.Frame(root, bg='#36454f')
sendframe.grid(row=6, column=0, columnspan=3, pady=5)

chatframe = tk.Frame(root, bg="#36454f")
chatframe.grid(row=2, column=0, columnspan=3)

eyeframe = tk.Frame(root, bg='#7692ff')
eyeframe.grid(row=1, column=0, columnspan=3)

controlsframe.grid_remove()
sendframe.grid_remove()
chatframe.grid_remove()


eye1_canvas = tk.Canvas(eyeframe, width=30, height=30, bg='#36454f', highlightthickness=0)
eye1_canvas.grid(column=0, row=2)
# Outer white ring
eye1_canvas.create_oval(3, 3, 27, 27, fill='#fefcfb', outline='')  # white ring
eye1_id = eye1_canvas.create_oval(5, 5, 25, 25, fill='#fefcfb')

eye2_canvas = tk.Canvas(eyeframe, width=30, height=30, bg='#151b1f', highlightthickness=0)
eye2_canvas.grid(column=2, row=2)
# Outer white ring
eye2_canvas.create_oval(3, 3, 27, 27, fill='#fefcfb', outline='')  # white ring
eye2_id = eye2_canvas.create_oval(5, 5, 25, 25, fill='#fefcfb')

play = tk.Button(controlsframe, text="\u23EF\uFE0F", command=lambda: [music.pausemusic(play)], bg="#36454f", fg="#fefcfb")
next = tk.Button(controlsframe, text="\u23ED\uFE0F", command=lambda: [music.nextmusic(play)], bg="#36454f", fg="#fefcfb")
prev = tk.Button(controlsframe, text="\u23EA", command=lambda: [music.prevmusic(play)], bg="#36454f", fg="#fefcfb")
loop = tk.Button(controlsframe, text="Loop: OFF", command=lambda: [music.toggleloop(loop)], bg="#36454f", fg="#fefcfb")
shuffle = tk.Button(controlsframe, text="Shuffle OFF", command=lambda: [music.toggleshuffle(shuffle)], bg="#36454f", fg="#fefcfb")

play.grid(column=1, row=3)
next.grid(column=2, row=3)
prev.grid(column=0, row=3)
loop.grid(column=1, row=4)
shuffle.grid(column=2, row=4)

volumelabel = tk.Label(controlsframe, text="Volume", bg="#36454f", fg="#fefcfb")
volumeslider = ttk.Scale(controlsframe, from_=0, to=100, orient="horizontal", command=music.setvolume)
volumeslider.set(70)
volumelabel.grid(column=0, row=5)
volumeslider.grid(column=1, row=5, columnspan=2)

user_entry = tk.Entry(sendframe, selectbackground="#36454f", selectforeground="#fefcfb")
user_entry.grid(column=0, row=0, padx=5)
sendbutton = tk.Button(sendframe, text="Send", command=sendmessage, bg="#36454f", fg="#fefcfb")
tts = tk.Button(sendframe, text="TTS: OFF", command=toggletts, bg="#36454f", fg="#fefcfb")

user_entry.bind("<Return>", lambda event: sendmessage())

sendbutton.grid(row=0, column=1)
tts.grid(row=0, column=2)

response_label = tk.Label(chatframe, text="", justify="left", font=FONT_AI, wraplength=250, bg='#36454f', fg="#fefcfb", padx=10, pady=5)

# chat_box.bind("<Button-1>", lambda event: on_chat_click(event))

exitbutton = tk.Button(chatframe, text='x', width=3, command=clearresponse, bg="#36454f", fg="#fefcfb")

staybutton = tk.Button(controlsframe, text="Stay: OFF", command=togglestay, bg="#36454f", fg="#fefcfb")
staybutton.grid(column=0, row=6, columnspan=3, pady=5)

# eyeframe.bind("<B1-Motion>", domove)
eye1_canvas.bind("<Button-1>", expand_ui)
# eye1_canvas.bind("<B1-Motion>", domove)
eye2_canvas.bind("<Button-1>", expand_ui)
# eye2_canvas.bind("<B1-Motion>", domove)

root.columnconfigure(0, weight=1)
root.rowconfigure(7, weight=1)
root.resizable(True, True)

root.configure(bg='#353935')


# chat_box.grid_forget()
blinktimer()
music.check_music_end(root)
threading.Thread(target=voicethread, daemon=True).start()
root.mainloop()
