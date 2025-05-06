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

#fonts and colors
FONT_MAIN = ("Segoe UI", 10)
FONT_AI = ("Comic Sans MS", 12)
COLOR_BG = "#fff8dc"
COLOR_FG = "#444"

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
            # chat_box.config(state='normal')
            # chat_box.insert(tk.END, f"You: {input}\n")
            # chat_box.insert(tk.END, f"Binary: {airesponse}\n\n")
            # chat_box.config(state='disabled')
            # chat_box.see(tk.END)
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
        eye1_canvas.itemconfig(eye1_id, fill='black' if eye1_canvas.itemcget(eye1_id, "fill") == "white" else "white")
        eye2_canvas.itemconfig(eye2_id, fill='black' if eye2_canvas.itemcget(eye2_id, "fill") == "white" else "white")
    elif isstaring:
        eye1_canvas.itemconfig(eye1_id, fill='black')
        eye2_canvas.itemconfig(eye2_id, fill='black')
    root.after(1001, blinktimer)

def blink(event=None):
    if not music.is_playing and not isstaring:
        eye1_canvas.itemconfig(eye1_id, fill='white' if eye1_canvas.itemcget(eye1_id, "fill") == "black" else "black")
        eye2_canvas.itemconfig(eye2_id, fill='white' if eye2_canvas.itemcget(eye2_id, "fill") == "black" else "black")
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
    # chat_box.grid_forget()

root = tk.Tk(screenName="Binary")
root.configure(bg='#f0f0f0')
root.attributes('-topmost', True)

style = ttk.Style()
style.configure('TButton', font=FONT_MAIN, padding=5)
style.configure('TLabel', font=FONT_MAIN)
style.theme_use('clam')

for i in range(3):
    root.columnconfigure(i, weight=1)
for i in range(10):
    root.rowconfigure(i, weight=1)

controlsframe = ttk.Frame(root)
controlsframe.grid(row=5, column=0, columnspan=3, pady=5)

sendframe = ttk.Frame(root)
sendframe.grid(row=6, column=0, columnspan=3, pady=5)

chatframe = ttk.Frame(root)
chatframe.grid(row=2, column=0, columnspan=3)

eyeframe = ttk.Frame(root)
eyeframe.grid(row=0, column=0, columnspan=3)

eye1_canvas = tk.Canvas(eyeframe, width=30, height=30, bg='#f0f0f0', highlightthickness=0)
eye1_canvas.grid(column=0, row=2)
eye1_id = eye1_canvas.create_oval(5, 5, 25, 25, fill='black')

eye2_canvas = tk.Canvas(eyeframe, width=30, height=30, bg='#f0f0f0', highlightthickness=0)
eye2_canvas.grid(column=2, row=2)
eye2_id = eye2_canvas.create_oval(5, 5, 25, 25, fill='black')

play = ttk.Button(controlsframe, text="\u23EF\uFE0F", command=lambda: [music.pausemusic(play)])
next = ttk.Button(controlsframe, text="\u23ED\uFE0F", command=lambda: [music.nextmusic(play)])
prev = ttk.Button(controlsframe, text="\u23EA", command=lambda: [music.prevmusic(play)])
loop = ttk.Button(controlsframe, text="Loop: OFF", command=lambda: [music.toggleloop(loop)])
shuffle = ttk.Button(controlsframe, text="Shuffle OFF", command=lambda: [music.toggleshuffle(shuffle)])

play.grid(column=1, row=3)
next.grid(column=2, row=3)
prev.grid(column=0, row=3)
loop.grid(column=1, row=4)
shuffle.grid(column=2, row=4)

volumelabel = ttk.Label(controlsframe, text="Volume")
volumeslider = ttk.Scale(controlsframe, from_=0, to=100, orient="horizontal", command=music.setvolume)
volumeslider.set(70)
volumelabel.grid(column=0, row=5)
volumeslider.grid(column=1, row=5, columnspan=2)

# chat_box = scrolledtext.ScrolledText(chatframe, wrap=tk.WORD, state='normal', width=40, height=10, font=FONT_MAIN)
# chat_box.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

user_entry = ttk.Entry(sendframe)
user_entry.grid(column=0, row=0, padx=5)
sendbutton = ttk.Button(sendframe, text="Send", command=sendmessage)
tts = ttk.Button(sendframe, text="TTS: OFF", command=toggletts)

user_entry.bind("<Return>", lambda event: sendmessage())

sendbutton.grid(row=0, column=1)
tts.grid(row=0, column=2)

response_label = tk.Label(chatframe, text="", font=FONT_AI, wraplength=250, justify="left", bg=COLOR_BG, fg=COLOR_FG, bd=2, relief="solid", padx=10, pady=5)

# chat_box.bind("<Button-1>", lambda event: on_chat_click(event))

exitbutton = ttk.Button(chatframe, text='x', width=3, command=clearresponse)

# def on_chat_click(event):
#     index = chat_box.index("@%s,%s" % (event.x, event.y))
#     line = chat_box.get(f"{index} linestart", f"{index} lineend")
#     if line.startswith("You: "):
#         user_entry.insert(0, line[5:])

eye1_canvas.bind("<Button-1>", blink)
eye2_canvas.bind("<Button-1>", blink)

root.columnconfigure(0, weight=1)
root.rowconfigure(7, weight=1)
root.resizable(True, True)

# chat_box.grid_forget()
blinktimer()
music.check_music_end(root)
threading.Thread(target=voicethread, daemon=True).start()
root.mainloop()
