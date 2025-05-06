"""
🎤 Voice input → text

📜 Display the text (for clarity)

🤖 Send it to the chatbot

🗣️ Speak the chatbot's response
"""

import pyaudio
import speech_recognition as sr

p = pyaudio.PyAudio()

def listentouser():
    recogniser = sr.Recognizer()
    with sr.Microphone() as source: #opens mic stream
        print("Say something...")
        recogniser.adjust_for_ambient_noise(source)
        audio = recogniser.listen(source, timeout=10)

    try:
        print("You said: " + recogniser.recognize_google(audio, language='en-IN'))
        return recogniser.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry. Nahi samjha. ")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        try:
            print("Trying offline: " + recogniser.recornize_sphinx(audio))
            return recogniser.recognize_sphinx(audio)
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that (even offline).")
            return None
        except sr.RequestError as e:
            print("Offline recognition also failed.")
            return None 
    
def waitforhotword(hotword = "Max"):
    recogniser = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for hotword...")
        recogniser.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recogniser.listen(source, phrase_time_limit=3)
                spoken = recogniser.recognize_google(audio, language="en-IN").lower()
                print("Heard:", spoken)
                if hotword in spoken:
                    print("Hotword detected!")
                    return
            except sr.UnknownValueError:
                continue

while True:
    waitforhotword()
    usertext = listentouser()
    if usertext:
        print("You:", usertext)

