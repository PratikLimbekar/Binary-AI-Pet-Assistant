"""
🎤 Voice input → text

📜 Display the text (for clarity)

🤖 Send it to the chatbot

🗣️ Speak the chatbot's response
"""

import pyaudio #to interact with the mic
import speech_recognition as sr
from dotenv import load_dotenv
import os
import pvporcupine #hotword detection
import struct #to process the raw audio buffer by converting binary data into something useful
import pyttsx3


load_dotenv()
apikey = os.getenv('porcupine_key')
porcupine = pvporcupine.create(keyword_paths=["Binary.ppn"], access_key=apikey)

engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 0.9)

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
            print("Trying offline: " + recogniser.recognize_sphinx(audio))
            return recogniser.recognize_sphinx(audio)
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that (even offline).")
            return None
        except sr.RequestError as e:
            print("Offline recognition also failed.")
            return None 
    
print("Listening for hotword...")

def waitforbinary():
    p = pyaudio.PyAudio()
    #setting up Pyaudio stream
    stream = p.open(rate=porcupine.sample_rate,#matches sample rate of porcupine
                channels=1, #mono audio stream
                format=pyaudio.paInt16, #16-bit audio format
                input=True,
                frames_per_buffer=porcupine.frame_length #frame size matches as expected by Porcupine
                )
    try:
        while True:
            #read audio buffer from mic
            audiobuffer = stream.read(porcupine.frame_length) 
            #convert audio to int values (bin to readable data)
            audiodata = struct.unpack_from("h" * porcupine.frame_length, audiobuffer)

            #check for hotword
            keywordindex = porcupine.process(audiodata)
            if keywordindex >= 0:
                print("Binary detected! Triggering the chatbot..")
                user_input = listentouser()
                return user_input
                break

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def speakresponse(text):
    engine.say(text)
    engine.runAndWait()