import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import google.generativeai as genai
import pygame
import time
from gtts import gTTS
import os
import pywhatkit

# Constants & API keys
NEWS_API_KEY = ""
WEATHER_API_KEY = ""
GEMINI_API_KEY = ""

# Flags
stop_reading_news = False
assistant_active = True

# Initialize speech engine and recognizer
recogniser = sr.Recognizer()
engine = pyttsx3.init()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")

# ---------- Speech Functions ----------

def speak(text):
    print("Jarvis:", text)  # ✅ Show text output
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove('temp.mp3')

# ---------- AI Processing ----------

def aiProcess(command):
    try:
        response = model.generate_content(
            f"You are Jarvis, a helpful assistant created by Tony Stark. Be brief and informative.\nUser: {command}"
        )
        # Fix Gemini error by getting proper text part
        parts = response.parts
        if parts:
            return parts[0].text
        else:
            return "Sorry, I couldn't generate a proper response."
    except Exception as e:
        return f"Sorry, Gemini model failed: {e}"

# ---------- Weather ----------

def get_weather_report():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Karnataka,in&units=metric&appid={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"The current temperature in Karnataka is {temp}°C with {desc}."
        else:
            return "Couldn't fetch weather data right now."
    except Exception as e:
        return f"Weather API failed: {e}"

# ---------- Main Command Handler ----------

def processCommand(c):
    global stop_reading_news, assistant_active

    c = c.lower()

    if "google" in c:
        speak("Opening Google.")
        webbrowser.open("https://google.com")
    elif "facebook" in c:
        speak("Opening Facebook.")
        webbrowser.open("https://facebook.com")
    elif "instagram" in c:
        speak("Opening Instagram.")
        webbrowser.open("https://instagram.com")
    elif "youtube" in c:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")
    elif "linkedin" in c:
        speak("Opening LinkedIn.")
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song_name = c.replace("play", "").strip()
        if song_name:
            speak(f"Playing {song_name} on YouTube")
            pywhatkit.playonyt(song_name)
        else:
            speak("Please tell me the song name.")

    elif c.startswith("search"):
        query = c.replace("search", "").strip()
        if query:
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("Please say what you want to search for.")
    elif "news" in c:
        stop_reading_news = False
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
            if r.status_code == 200:
                articles = r.json().get('articles', [])
                for article in articles:
                    if listen_for_stop():
                        speak("News reading stopped.")
                        break
                    speak(article['title'])
            else:
                speak("Sorry, couldn't get news now.")
        except Exception as e:
            speak(f"News error: {e}")
    elif "weather" in c:
        report = get_weather_report()
        speak(report)
    elif "stop" in c:
        speak("Shutting down. Goodbye!")
        assistant_active = False
    else:
        output = aiProcess(c)
        speak(output)

# ---------- Stop Listening ----------

def listen_for_stop():
    global stop_reading_news
    with sr.Microphone() as source:
        recogniser.adjust_for_ambient_noise(source)
        try:
            audio = recogniser.listen(source, timeout=5, phrase_time_limit=3)
            word = recogniser.recognize_google(audio)
            if word.lower() == "stop":
                stop_reading_news = True
                return True
        except:
            pass
    return False

# ---------- Main Program Loop ----------

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            print("Listening for wake word 'Jarvis'...")
            with sr.Microphone() as source:
                recogniser.adjust_for_ambient_noise(source)
                audio = recogniser.listen(source, timeout=5, phrase_time_limit=3)

            wake = recogniser.recognize_google(audio)
            print(f"Wake word heard: {wake}")

            if "jarvis" in wake.lower():
                speak("Yes sir, how can I help?")

                while assistant_active:
                    try:
                        with sr.Microphone() as source:
                            recogniser.adjust_for_ambient_noise(source)
                            print("Listening for command...")
                            audio = recogniser.listen(source, timeout=5, phrase_time_limit=4)

                        command = recogniser.recognize_google(audio)
                        print(f"Command: {command}")
                        processCommand(command)

                    except sr.UnknownValueError:
                        speak("Sorry, I didn't catch that.")
                    except sr.RequestError as e:
                        speak(f"Speech recognition error: {e}")
        except sr.UnknownValueError:
            print("Could not understand wake word.")
        except sr.RequestError as e:
            print(f"Wake word recognition error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
