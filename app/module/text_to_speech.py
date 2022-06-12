import pyttsx3
from PyQt5 import QtCore


class TextToSpeech(QtCore.QThread):

    def __init__(self, message=None, silent=False, voice="Female", rate=120):
        super().__init__()
        self.__messages = message
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('rate', rate)
        if voice == "Female":
            self.engine.setProperty('voice', voices[1].id)

    def set_next_message(self, messages):
        self.__messages = messages

    def run(self):
        for msg in self.__messages:
            self.engine.say(msg)
            self.engine.runAndWait()
