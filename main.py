import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai  
import pygame
import time
from gtts import gTTS
import os

recogniser = sr.Recognizer()
engine = pyttsx3.init()
newsapi = ""
weather_api = ""  # Your API key
stop_reading_news = False
assistant_active = True  # Flag to keep the assistant active

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()    
    os.remove('temp.mp3')

def aiProcess(command):
    openai.api_key = ""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Lucy skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message['content']


def get_weather_report():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Karnataka,in&units=metric&appid={weather_api}"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        weather_report = f"The current temperature in Karnataka is {temperature} degrees Celsius with {weather_description}."
        return weather_report
    else:
        return "Sorry, I couldn't retrieve the weather information."

def processCommand(c):
    global stop_reading_news, assistant_active
    
    if "google" in c.lower():
        webbrowser.open("https://google.com")
    elif "facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "instagram" in c.lower():
        webbrowser.open("https://instagram.com")    
    elif "youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find the song.")
    elif "news" in c.lower():
        stop_reading_news = False
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            news_data = r.json()
            articles = news_data['articles']
            for article in articles:
                if listen_for_stop():
                    speak("Stopping news reading.")
                    break
                # Print the article title to the console
                print(f"News: {article['title']}")
                # Speak the article title
                speak(article['title'])
        else:
            speak("Sorry, I couldn't retrieve the news.")
    elif "weather" in c.lower():
        weather_report = get_weather_report()
        print(weather_report)
        speak(weather_report)
    elif "stop" in c.lower():
        speak("Okay, stopping the assistant.")
        assistant_active = False
    else:
        output = aiProcess(c)
        speak(output)

def listen_for_stop():
    global stop_reading_news
    with sr.Microphone() as source:
        recogniser.adjust_for_ambient_noise(source)
        audio = recogniser.listen(source, timeout=5, phrase_time_limit=3)
    
    try:
        word = recogniser.recognize_google(audio)
        if word.lower() == "stop":
            stop_reading_news = True
            return True
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    
    return False

if __name__ == "__main__":
    speak("Initializing Lucy...")
    
    while True:
        try:
            print("Listening for the wake word...")
            with sr.Microphone() as source:
                recogniser.adjust_for_ambient_noise(source)
                audio = recogniser.listen(source, timeout=5, phrase_time_limit=3)
            
            word = recogniser.recognize_google(audio)
            print(f"Recognized word: {word}")

            if word.lower() == "lucy":
                speak("Hey user, what can I do for you?")
                
                while assistant_active:
                    try:
                        with sr.Microphone() as source:
                            recogniser.adjust_for_ambient_noise(source)
                            print("Lucy active, listening for command...")
                            audio = recogniser.listen(source, timeout=5, phrase_time_limit=4)
                        
                        try:
                            command = recogniser.recognize_google(audio)
                            print(f"Recognized command: {command}")
                            processCommand(command)
                            if not assistant_active:  # If the "stop" command was issued
                                break
                        except sr.UnknownValueError:
                            speak("Sorry, I didn't catch that. Could you please repeat?")
                        except sr.RequestError as e:
                            speak(f"Could not request results from the service; {e}")
                    except sr.UnknownValueError:
                        print("Could not understand the command.")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.UnknownValueError:
            print("Could not understand the wake word.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")
