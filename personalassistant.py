from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
from kivy.core.text import LabelBase
from kivy.clock import Clock
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
Window.size = (450, 650)


class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Poppins"
    font_size = 17


class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Poppins"
    font_size = 17


class PersonalAssistant(MDApp):
    isSpeech = False

    def change_screen(self, name):
        screen_manager.current = name

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("UI/Main.kv"))
        screen_manager.add_widget(Builder.load_file("UI/Chats.kv"))
        return screen_manager

    def bot_name(self):
        name = "^^ Nice to meet you ^^"
        if screen_manager.get_screen('main').bot_name.text != "":
            name = screen_manager.get_screen('main').bot_name.text
            screen_manager.get_screen('chats').bot_name.text = "I am " + name
        else:
            screen_manager.get_screen('chats').bot_name.text = name
        screen_manager.current = "chats"

    def response(self, *a):
        response = ""
        if value.lower() == "hello" or value.lower() == "hi":
            response = f"Hello, I am your virtual PA.\nNice to meet you "
        elif value.lower() == "how are you?" or value.lower() == "how are you":
            response = "I'm fine, thank you. And u?"
        elif value.lower() == "who made you" or value.lower() == "who made you?":
            response = "While I can't give details, let me assure you, humans are involved."
        elif value != "Adjusting noise..." or value.lower() != "Recording for 3 seconds...":
            response = "Sorry, but I can't answer that"

        screen_manager.get_screen('chats').chat_list.add_widget(Response(text=response, size_hint_x=.75))
        self.speak(response)
        return

    def speak(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def text_size(self, text):
        if len(text) < 5:
            s = .22
        elif len(text) < 10:
            s = .32
        elif len(text) < 15:
            s = .45
        elif len(text) < 20:
            s = .58
        elif len(text) < 25:
            s = .71
        else:
            s = .77
        return s

    def send(self):
        global size, halign, value
        halign = "center"
        if screen_manager.get_screen('chats').text_input != "":
            value = screen_manager.get_screen('chats').text_input.text
            size = self.text_size(value)
            screen_manager.get_screen('chats').chat_list.add_widget(
                Command(text=value, size_hint_x=size, halign=halign))

            Clock.schedule_once(self.response, 2)

            screen_manager.get_screen('chats').text_input.text = ""

    def speech_to_text(self, *a):
        global size, halign, value
        halign = "center"
        with sr.Microphone() as source:
            self.isSpeech = True
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Adjusting noise...")
            screen_manager.get_screen('chats').chat_list.add_widget(
                Command(text="Adjusting noise...", size_hint_x=.30, halign=halign))
            recorded_audio = recognizer.listen(source, timeout=3)
            print("Recording for 3 seconds...")
            screen_manager.get_screen('chats').chat_list.add_widget(
                Command(text="Recording for 3 seconds...", size_hint_x=.58, halign=halign))
        try:
            text = recognizer.recognize_google(recorded_audio, language="en-US")
            value = format(text)
            if value != "":
                print(value)
                size = self.text_size(value)
        except Exception as ex:
            value = ex.__str__()
            size = self.text_size(value)

        screen_manager.get_screen('chats').chat_list.add_widget(
            Command(text=value, size_hint_x=size, halign=halign))
        Clock.schedule_once(self.response, 2)
        self.isSpeech = False


if __name__ == '__main__':
    LabelBase.register(name="Poppins", fn_regular="Poppins/Poppins-Regular.ttf")
    PersonalAssistant().run()
