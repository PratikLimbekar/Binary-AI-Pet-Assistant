import pyttsx3


text = "Hello there, General Kenobi."
engine = pyttsx3.init()
engine.setProperty('rate', 200)
engine.setProperty('volume', 0.9)
voices = engine.getProperty('voices')
for voice in voices:
    print(f"ID: {voice.id}, Name: {voice.name}")
engine.setProperty('voice', voices[0].id)
engine.say(text)
engine.runAndWait()