from PyQt5 import QtCore

import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()


class Speech2TextPager(QtCore.QThread):
    done_running = QtCore.pyqtSignal(list)
    error_occurred = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__cancelled = True

    def cancel(self):
        self.__cancelled = True

    def run(self):
        self.__cancelled = False
        try:
            with sr.Microphone() as mic:
                r.adjust_for_ambient_noise(mic)
                audio2 = r.listen(mic)
        except Exception:
            if not self.__cancelled:
                self.error_occurred.emit(
                    "Sorry, there seems to be an issue with the microphone"
                )
        # Using google to recognize audio
        try:
            my_text = r.recognize_google(audio2, language="en")
            if not self.__cancelled:
                self.done_running.emit([my_text])
        except Exception:
            if not self.__cancelled:
                self.error_occurred.emit("Sorry, I couldn't hear that")
