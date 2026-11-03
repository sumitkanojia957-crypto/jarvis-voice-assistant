import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import urllib.request
import json
from openai import OpenAI
import os
from gtts import gTTS
import pygame
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = "api key"


def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    pygame.mixer.quit()


def aiProcess(command):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Assistant. And give short responses please"
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content


def processCommand(c):

    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():

        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"

        try:
            response = urllib.request.urlopen(url)

            data = json.loads(response.read().decode())

            articles = data.get("articles", [])

            for article in articles:
                title = article.get("title")

                if title:
                    speak(title)

        except Exception as e:
            print("NewsAPI Error:", e)

    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":

    speak("Initializing Jarvis....")

    r = sr.Recognizer()

    print("Recognizing...")

    try:

        with sr.Microphone() as source:
            print("Listening...")

            audio = r.listen(
                source,
                timeout=2,
                phrase_time_limit=5
            )

        word = r.recognize_google(audio)

        if word.lower() == "jarvis":

            speak("Yes sir")

            with sr.Microphone() as source:
                print("Jarvis Active...")

                audio = r.listen(source)

            command = r.recognize_google(audio)

            print("Command:", command)

            processCommand(command)

    except Exception as e:
        print("Error:", e)