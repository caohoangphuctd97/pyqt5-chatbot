import pyttsx3
from PyQt5 import QtCore
from typing import List


class TextToSpeech(QtCore.QThread):
    def __init__(self, voice="Female", rate=125):
        super().__init__()
        self.__messages = None
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("rate", rate)
        if voice == "Female":
            self.engine.setProperty("voice", voices[1].id)

    def set_next_messages(self, messages: List[str]) -> None:
        self.__messages = messages

    def stop_speaking(self):
        try:
            self.engine.stop()
        except RuntimeError:
            pass

    def resume_speak(self):
        self.engine.endLoop()

    def run(self) -> None:
        for msg in self.__messages:
            self.engine.say(msg)
        self.engine.runAndWait()
