import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
# from openai import OpenAI
from gtts import gTTS
import pygame
import os
import pathlib
import textwrap
import google.generativeai as genai
import time


# pip install speechrecognition 
# pip install pyaudio
# pip install setuptools
# pip install pocketsphinx


engine = pyttsx3.init() 
newsapi = "a8d1fda43b19471893618f98fa5cc63d"
def speak(text):
    engine.say(text)
    engine.runAndWait()
model = genai.GenerativeModel('gemini-pro')
GOOGLE_API_KEY = "AIzaSyDdkHUUHZgbkVCCdUkYDbxDfUhtRNZd168"
genai.configure(api_key=GOOGLE_API_KEY)
# def speak(text):
#     tts = gTTS(text)
#     tts.save('temp.mp3')
#     pygame.mixer.init() #initialize pygame mixer
#     pygame.mixer.music.load("temp.mp3") #load mp3 file
#     pygame.mixer.music.play() # play mp3 file
#     while pygame.mixer.music.get_busy(): #keep the program running untill the music stops playing
#         pygame.time.Clock().tick(10)
#     pygame.mixer.music.unload()
#     os.remove("temp.mp3")
    
# def processai(command):
#     client = OpenAI(
#         api_key="AIzaSyDdkHUUHZgbkVCCdUkYDbxDfUhtRNZd168",
#     )
#     completion = client.chat.completions.create(
#     model = "gpt-3.5-turbo",
#     messages = [
#         {"role": "system","content":"You are a virtual assistant named brother skilled in general task like Alexa and Google Cloud. Give short responses please."},
#         {"role":"user","content":command}
#     ] 
#     )
#     return (completion.choices[0].message.content)

def processgemini(prompt):
    input = prompt
    response = model.generate_content(input+"You are a virtual assistant named Albus skilled in general task like Alexa and Google Cloud. Give short responses please.")
    speak(response.text)
    return response
def processCommand(c):
     if "open google" in c.lower():
          webbrowser.open("https://google.com")
     elif "open facebook" in c.lower():
          webbrowser.open("https://facebook.com")
     elif "open linkedin" in c.lower():
          webbrowser.open("https://linkedin.com")
     elif "open youtube" in c.lower():
          webbrowser.open("https://youtube.com")
     elif c.lower().startswith("play"):
          song = c.lower().split(" ")[1]
          link = musiclibrary.music[song]
          webbrowser.open(link)
     elif "time" in c.lower():
         
         timestamp = time.strftime('%H:%M:%S')
         print("Time is : ",timestamp)
            #speak("Time is : ",timestamp) This is wrong.Explanation in below.
            #  In the first case, we concatenate "Time is: " with the value of timestamp using +.
            # In the second case, if speak() supports multiple arguments, you can just pass them separately without needing to concatenate them.
         timestamp1 = int(time.strftime('%H'))
         speak(timestamp1)
         speak("hours")
         timestamp2 =int(time.strftime('%M'))
         speak(timestamp2)
         speak("minute")
         timestamp3 = int(time.strftime('%S'))
         speak(timestamp3)
         speak("second")
         if(6 <= timestamp1 < 11):
                speak("Good Morning")
         elif(11 <= timestamp1 <17):
                speak("Good-after Noon")
         elif(17<=timestamp1<20):
                speak("Good Evening")
         else:
                speak("Good Night") 
     elif "news" in c.lower():
        url = "https://newsapi.org/v2/top-headlines"
        api_key = "a8d1fda43b19471893618f98fa5cc63d"
        params = {
            'country': 'us',
            'apiKey': api_key
        }
        r = requests.get(url, params=params)
        if r.status_code == 200:
            # Parse the response as JSON
            data = r.json()
            titles = [article['title'] for article in data.get('articles', [])]

            speak(titles)

     else:
        #Let OpenAI handle the request\
        
        processgemini(c)
        # speak(processgemini(c))
        
if __name__ ==  "__main__":
    # speak("Initializing Konver...")
    speak("Hey, I am a talking bot")
    
    r = sr.Recognizer()
    while True:
        #Listen for the wake word Jarvis
        # Obtain audio from the microphone            
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    r.adjust_for_ambient_noise(source)  # Adjust for background noise

                    audio = r.listen(source,timeout=2)
                    print("recognizing...")
                word = r.recognize_google(audio)
                print(word)
                if(word.lower()=="albus"):
                    speak("Welcome back")
                    speak("I am Albus, What can i help you ?")
                    for i in range(1,100):
                        with sr.Microphone() as source:
                            print("Albus Active... Listening for command...")
                            r.adjust_for_ambient_noise(source)  # Adjust for background noise

                            audio = r.listen(source,timeout=5)
                            command = r.recognize_google(audio)
                            print(command)

                            processCommand(command)
                        i += 1
                        if(command == "exit"):
                            break

                if(word=="exit" or word == "stop"):
                    break

            except sr.UnknownValueError:
                speak("Sorry, I could not understand your speech.")
            except Exception as e:
                print("Error; {0}".format(e))
            


    print("Albus, Thank you for using.")
