import time
import winsound

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import wolframalpha
import requests
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from Class import Command, Response
from kivy.uix.screenmanager import ScreenManager

from gender_predictor.GenderClassifier import classify_gender

recognizer = sr.Recognizer()
Window.size = (470, 650)


class PersonalAssistant(MDApp):
    isSpeech = False
    engine = pyttsx3.init('sapi5')

    # load screen
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("UI/Main.kv"))
        screen_manager.add_widget(Builder.load_file("UI/Chats.kv"))
        return screen_manager

    # text to speech
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    # functions of assistant
    # chao user
    def wishMe(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"

        self.speak(greeting)
        self.speak("How can I help you?")
        print(greeting)

    # mo wikipedia
    def openWiki(self, command):
        self.speak('Searching Wikipedia...')
        statement = command.replace("wikipedia", "")
        try:
            results = wikipedia.summary(statement, sentences=1)
            self.speak("According to Wikipedia")
            return results
        except Exception as ex:
            return ex.__str__()

    # mo youtube
    def openYoutube(self):
        webbrowser.open_new_tab("https://www.youtube.com")
        self.speak("youtube is open now")
        time.sleep(5)

    # mo Google
    def openGoogle(self):
        webbrowser.open_new_tab("https://www.google.com")
        self.speak("Google is open now")
        time.sleep(5)

    # mo Gmail
    def openGmail(self):
        webbrowser.open_new_tab("https://gmail.com")
        self.speak("Google Mail open now")
        time.sleep(5)

    # xem du bao thoi tiet
    def weather(self):
        api_key = "9fc3485628e332e032140d69385f5b94"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.speak("Where do you live?")
        city_name = self.takeCommand()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            try:
                y = x["main"]
                current_temperature = int(y["temp"]) - 273
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                return (f"Temperature in {city_name} is " + str(current_temperature) + " Celsius degrees"
                        + "\nHumidity is " + str(current_humidiy) + "%"
                        + "\nDescription: " + str(weather_description))
            except Exception as ex:
                return "Place not found! Please try again"
        else:
            return "Place not found! Please try again"

    # xem time
    def time(self):
        strTime = datetime.datetime.now().strftime("%H:%M")
        return f"It is {strTime} now."

    # mo stackoverflow
    def openStackoverflow(self):
        webbrowser.open_new_tab("https://stackoverflow.com/")
        self.speak("Here is stackoverflow")

    # doc tin tuc
    def readNews(self):
        webbrowser.open_new_tab("https://vnexpress.net/")
        self.speak('Here are some headlines from vnexpress. Happy reading')
        time.sleep(6)

    # tim kiem thong tin
    def searchInfor(self, command):
        command = command.replace("search", "")
        webbrowser.open_new_tab(command)
        time.sleep(5)

    # hoi dap voi user
    def askAndAnswer(self):
        self.speak('I can answer to computational and geographical questions and what question do you want to ask now')
        question = self.takeCommand()
        app_id = "R2K75H-7ELALHR35X"
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        return next(res.results).text

    # chuyen doi giua main screen va chat screen
    def change_screen(self, name):
        screen_manager.current = name

    # user dat ten cho assistant o main screen va hien thi ten o chat screen
    def bot_name(self):
        name = "G-one"
        if screen_manager.get_screen('main').bot_name.text != "":
            name = screen_manager.get_screen('main').bot_name.text
            screen_manager.get_screen('chats').bot_name.text = "I am " + name + "\nHave a nice day!"
        else:
            screen_manager.get_screen('chats').bot_name.text = "I am G-one.\nHave a nice day!"
        screen_manager.current = "chats"
        if name == "G-one" or classify_gender(name) == 'M':
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
        else:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)

        self.engine = engine
        self.engine.setProperty('rate', 185)
        time.sleep(1)
        return name

    # phan hoi user
    def response(self, *a):
        response = ""
        command = value.lower()
        if "bye" in command or "goodbye" in command or "okay" in command or "stop" in command or "exit" in command:
            self.speak("I'm shutting down. Goodbye")
            exit(0)

        if "hello" in command or "hi" in command or "nice to meet you" in command or 'who are you' in command:
            response = f"I am {self.bot_name()}. Nice to meet you"
        elif 'what can you do' in command:
            response = "I am programmed to minor tasks like opening youtube, google chrome, gmail and stackoverflow, " \
                       "predict time, search wikipedia, predict weather in different cities, " \
                       "get top headline news and you can ask me computational or geographical questions too!"
        elif "how are you" in command:
            response = "I'm fine, thank you. And you?"
        elif "who made you" in command or "who created you" in command or "who discovered you" in value.lower():
            response = "While I can't give details, let me assure you, Cong Le is involved."
        elif "wikipedia" in command:
            response = self.openWiki(command)
        elif "open youtube" in command:
            self.openYoutube()
        elif "open google" in command:
            self.openGoogle()
        elif "open gmail" in command:
            self.openGmail()
        elif "weather" in command:
            response = self.weather()

        elif "time" in command:
            response = self.time()
        elif "open stackoverflow" in command or "open stack overflow" in command:
            self.openStackoverflow()
        elif "news" in command:
            self.readNews()
        elif "tìm kiếm" in command or "search" in command:
            self.searchInfor(command)
        elif "ask" in command:
            response = self.askAndAnswer()
        else:
            response = "Sorry, but I can't answer that"

        if response != "":
            s = self.text_size(response)
            screen_manager.get_screen('chats').chat_list.add_widget(Response(text=response, size_hint_x=s))
            self.speak(response)

    # adjust command/response size
    def text_size(self, text):
        if len(text) < 5:
            return .20
        elif len(text) < 10:
            return .28
        elif len(text) < 15:
            return .40
        elif len(text) < 20:
            return .53
        elif len(text) < 25:
            return .65
        else:
            return .73

    def send(self):
        global size, halign, value
        halign = "center"
        if screen_manager.get_screen('chats').text_input != "":
            value = screen_manager.get_screen('chats').text_input.text
            if value != "":
                winsound.PlaySound("SFX/messageSent.wav", winsound.SND_FILENAME)
                size = self.text_size(value)
                screen_manager.get_screen('chats').chat_list.add_widget(
                    Command(text=value, size_hint_x=size, halign=halign))
                Clock.schedule_once(self.response, 1)
                screen_manager.get_screen('chats').text_input.text = ""

    def takeCommand(self):
        self.isSpeech = True
        global size, halign, value
        halign = "center"
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Adjusting noise...")
            winsound.Beep(500, 500)
            print("Recording for 3 seconds...")
            recorded_audio = recognizer.listen(source, timeout=3)

        try:
            text = recognizer.recognize_google(recorded_audio, language="en-US")
            value = format(text)
            if value != "":
                print(value)
                size = self.text_size(value)
        except Exception as ex:
            value = ex.__str__()
            size = self.text_size(value)

        winsound.PlaySound("SFX/messageSent.wav", winsound.SND_FILENAME)
        screen_manager.get_screen('chats').chat_list.add_widget(
            Command(text=value, size_hint_x=size, halign=halign))
        self.isSpeech = False
        return value

    def speech_to_text(self):
        Clock.schedule_once(self.response, 1)
        self.takeCommand()


if __name__ == '__main__':
    LabelBase.register(name="Poppins", fn_regular="Poppins/Poppins-Regular.ttf")
    PersonalAssistant().run()
