import pywhatkit
import speech_recognition as speech
import os
import pyttsx3
import datetime
import wikipedia
import webbrowser
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import string
from bs4 import BeautifulSoup
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

API_KEY = open('API_KEY').read()
SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID').read()
def speak(text):
    engine.setProperty('rate', 120)
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
        print("AI : Good Morning")
    elif hour >= 12 and hour < 16:
        speak("Good Afternoon")
        print("AI : Good Afternoon")
    else:
        speak("Good Evening")
        print("AI : Good Evening")
    speak("Hello, I am Anita, made by Abhinandan Subedi, How can I help you?")
    print("AI : Hello,\n I am Anita, made by Abhinandan Subedi. How can I help you?")

def takeCommand():
    r = speech.Recognizer()
    with speech.Microphone() as source:
        print("AI : Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)
    try:
        print("AI : Recognizing ...")
        query = r.recognize_google(audio, language='en-us')
        print(f"User : {query}\n")
    except speech.UnknownValueError:
        print("AI : Sorry, I did not understand that. Please say that again.")
        return "None"
    except speech.RequestError:
        print("AI : Sorry, I'm having trouble connecting to the recognition service.")
        return "None"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"

    return query

    # English (US): en-US
    # English (UK): en-GB
    # Spanish (Spain): es-ES
    # Spanish (Mexico): es-MX
    # French (France): fr-FR
    # French (Canada): fr-CA
    # German: de-DE
    # Italian: it-IT
    # Portuguese (Portugal): pt-PT
    # Portuguese (Brazil): pt-BR
    # Russian: ru-RU
    # Chinese (Simplified): zh-CN
    # Chinese (Traditional): zh-TW
    # Japanese: ja-JP
    # Korean: ko-KR
    # Hindi: hi-IN




def generate_response(input_text, chat_history_ids=None, max_length=1000):
    new_user_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids],dim=-1) if chat_history_ids is not None else new_user_input_ids
    chat_history_ids = model.generate(bot_input_ids, max_length=max_length,pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response, chat_history_ids

def chat():
    chat_history_ids = None
    user_input = query
    response, chat_history_ids = generate_response(user_input, chat_history_ids)
    text_reponse = replace_punctuation_with_comma(response)
    if 'I\'m not sure what you mean by that.' in response or 'I\'m not sure what that is' in response or 'I\'m not sure if you\'re serious' in response:
        print("AI : That is out of my range")
        speak("That is out of my range")
    else:
        print(f"AI : {response}")
        speak(str(text_reponse))
def replace_punctuation_with_comma(text):
    translation_table = str.maketrans(string.punctuation, ',' * len(string.punctuation))
    return text.translate(translation_table)

if __name__ == '__main__':
    # wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia.com' in query:
            print("AI : Opening Wikipedia")
            speak("Opening Wikipedia")
            webbrowser.open("wikipedia.com")

        elif 'wikipedia' in query:
            try:
                speak('Searching in Wikipedia')
                print('AI : Searching in Wikipedia...')
                query = query.replace("wikipedia","")
                result = wikipedia.summary(query,sentences=2)
                speak("According to Wikipedia...")
                print("AI : According to wikipedia")
                print("AI :",result)
                speak(result)
            except Exception as e:
                continue

        elif 'youtube.com' in query:
            speak("Opening Youtube.com")
            print("AI : Opening Youtube.com")
            webbrowser.open("youtube.com")

        elif 'open' in query and '.com' in query:
            query = query.replace('open','')
            query = query.replace(' ', '')
            query = query.replace('.com', '')
            webbrowser.open(f"{query}.com")
            speak(f"Opening {query}.com")
            print(f" AI : Opening {query}.com")

        elif 'who are you' in query or 'hu r u' in query:
            speak("I am Anita, made by ,Abinandan subedi using python,I am capable to do, what I am programed to do")
        elif 'your name' in query :
            speak("I am Anita")

        elif 'play' in query and 'music' in query or 'song' in query:
            # music_dir = 'G:\\Python Projects\\AI Assistent - Desktop Assistant\\Music'
            # songs = os.listdir(music_dir)
            # index = 0
            # os.startfile(os.path.join(music_dir,songs[index]))
            # speak(f"Playing music")
            # song_name = replace_punctuation_with_comma(songs[index]).replace("mp4","")
            # speak(song_name)
            # print(f"AI : Playing {song_name}")
            song = query.replace('play','').replace('music','')
            print(f"AI : playing {song}")
            speak(f"playing{song}")
            pywhatkit.playonyt(song)
        elif 'play' in query and 'video' in query or 'on youtube' in query:
            # music_dir = 'G:\\Python Projects\\AI Assistent - Desktop Assistant\\Music'
            # songs = os.listdir(music_dir)
            # index = 0
            # os.startfile(os.path.join(music_dir,songs[index]))
            # speak(f"Playing music")
            # song_name = replace_punctuation_with_comma(songs[index]).replace("mp4","")
            # speak(song_name)
            # print(f"AI : Playing {song_name}")
            video = query.replace('play','').replace('video','').replace('on youtube','')
            print(f"AI : playing {video}")
            speak(f"playing{video}")
            pywhatkit.playonyt(video)
        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"sir the time is {strtime}")
            print(f"AI : Sir,The time is {strtime}")
        elif 'you from' in query:
            speak("I am from nepal")
            print("AI : I am from nepal")
        elif 'you belong' in query:
            speak("I belongs to nepal")
            print("AI : I belongs to nepal")
        elif 'feeling happy' in query:
            speak("Its nice to listen")
            print("AI : Its nice to listen")

        elif 'feeling sad' in query:
            speak("You are also making me sad")
            print("AI : You are also making me sad")
        elif 'feeling hungry' in query:
            speak("Its bad for health go and eat something")
            print("AI : Its bad for health go and eat something.")
        elif 'say' in query and 'remember' in query.lower():
            a = 0
            speak("This is the thing which you said to remember")
            try:
                while a <= len(remember):
                    speak(remember[a])
                    a += 1
            except Exception as e:
                continue
        elif 'remember' in query.lower() and 'say':
            remember = []
            text_to_remember = query.replace("remember","")
            remember.append(text_to_remember)
            speak("I remember.")
            print("AI : I Remember")
        else:
            chat()