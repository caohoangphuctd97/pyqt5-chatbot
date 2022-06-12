import sys

import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from ui_components import main_window
from ui_components.dialogs import SettingWindow, BirthdayCard, LoginDialog
from utils.msg_helper import (
    CareUMsgCourier,
    MessageDelegate,
    MessageModel,
    USER_ME,
    USER_THEM,
)
from modules.speech_to_text import Speech2TextPager
from modules.text_to_speech import TextToSpeech


from PyQt5.QtWidgets import QApplication, QListView, QMainWindow

USER_ID = "f974474d-e761-42bd-a63c-ec0032a75ca7"
MAX_RESPONSE_SIZE_TO_READ = 128


import time
class InactiveWatcher(QtCore.QThread):
    deactived = QtCore.pyqtSignal()

    def __init__(self, duration: int = 3):
        super().__init__()
        # self.__is_active = False
        self.__duration = duration
        # self.__start: float = None

    def run(self):
        self.__last_active = time.time()
        while (time.time() - self.__last_active) < self.__duration:
            time.sleep(1)
        self.deactived.emit()
    
    def record_activity(self):
        # self.__is_active = True
        self.__last_active = time.time()

class MainWindow(object):
    def __init__(self):
        self.__offset = None
        self.master_window = QMainWindow()
        self.master_window.setWindowIcon(QIcon("image/Avatar-Bot.png"))
        self.master_window.setWindowFlag(Qt.FramelessWindowHint)
        # other children dialogs
        self.setting_window = SettingWindow(self.master_window, Qt.WindowFlags())
        self.bd_dialog = BirthdayCard(self.master_window, Qt.WindowFlags())
        self.login = LoginDialog(self.master_window, Qt.WindowFlags())
        # inactivity watcher
        self.inactivity_watcher = InactiveWatcher(45)
        # client for message
        self.__message_courier = CareUMsgCourier()
        self.__voice_listener = Speech2TextPager()
        self.__voice_agent = TextToSpeech()
        self.__is_listening = False
        self.set_up_main_windows()
        self.set_up_draggable_title()

    def set_up_main_windows(self):
        self.main_window = main_window.Ui_MainWindow()
        self.main_window.setupUi(self.master_window)

        # load images
        self.media = {
            "speaker": QtGui.QIcon("image/speaker.png"),
            "no_speaker": QtGui.QIcon("image/no_speaker.png"),
            "px_globe": QtGui.QPixmap("image/globe_icon.png"),
            "mic": QtGui.QIcon("image/micro-01.png"),
            "mic_activate": QtGui.QIcon("image/mic_activate.png"),
            "send_black_color": QtGui.QIcon("image/send_black_24dp 1.png"),
            "close": QtGui.QIcon("image/close.png"),
            "close_gray": QtGui.QIcon("image/close_gray.png"),
            "settings": QtGui.QIcon("image/settings.png"),
            "gif_voice": QtGui.QMovie("image/voice.gif"),
            "icon64": QtGui.QPixmap("image/character_icon_64.png"),
        }
        self.main_window.lb_icon.setPixmap(self.media["icon64"])
        self.main_window.lb_icon.setScaledContents(True)
        self.main_window.lb_globe_icon.setPixmap(self.media["px_globe"])
        self.main_window.bt_mic_mode.setIcon(self.media["mic"])
        self.main_window.bt_mic_activate.setIcon(self.media["mic_activate"])
        self.main_window.bt_send_message.setIcon(self.media["send_black_color"])
        self.main_window.bt_cancel_mic.setIcon(self.media["close"])
        self.main_window.bt_exit.setIcon(self.media["close_gray"])
        self.main_window.bt_config.setIcon(self.media["settings"])
        self.main_window.bt_config.setVisible(False)
        self.main_window.bt_voice_speak_back.setIcon(self.media["speaker"])
        gif_size = QtCore.QSize(
            self.main_window.voice_gif.width(), self.main_window.voice_gif.height()
        )
        self.gif_object = self.media["gif_voice"]
        self.gif_object.setScaledSize(gif_size)
        self.main_window.voice_gif.setMovie(self.gif_object)
        self.gif_object.start()

        # set up chat history
        self.main_window.chat_history.setResizeMode(QListView.Adjust)
        self.main_window.chat_history.setItemDelegate(MessageDelegate())
        self.model = MessageModel()
        self.main_window.chat_history.setModel(self.model)
        self.main_window.chat_history.setStyleSheet("background-color:rgb(255,255,255)")

        # connect signal to slot
        self.main_window.bt_exit.pressed.connect(self.exit_app)
        self.main_window.bt_mic_mode.pressed.connect(self.activate_mic_mode)
        self.main_window.bt_mic_activate.pressed.connect(self.activate_mic)
        self.main_window.bt_cancel_mic.pressed.connect(self.cancel_mic)
        self.main_window.bt_send_message.pressed.connect(self.send_message)
        self.main_window.bt_config.pressed.connect(self.show_settings)
        self.main_window.input_text.returnPressed.connect(self.send_message)
        self.main_window.bt_voice_speak_back.mouseReleaseEvent = (
            self.__voice_feedback_toggled
        )
        self.__message_courier.text_received.connect(self.project_reponses)
        self.__voice_listener.done_running.connect(self.voice_message_recieved)
        self.__voice_listener.error_occurred.connect(self.voice_message_failed)
        self.inactivity_watcher.deactived.connect(self.show_splash_screen)
        self.bd_dialog.bd_window.bt_start_chatting.pressed.connect(self.close_bd_dialog)
        self.bd_dialog.on_exit.connect(self.splash_screen_close)
        self.login.on_exit.connect(self.show_master_windows)

    def set_up_draggable_title(self):
        self.main_window.lb_botname.mousePressEvent = self.mousePressEvent
        self.main_window.lb_botname.mouseMoveEvent = self.mouseMoveEvent
        self.main_window.lb_botname.mouseReleaseEvent = self.mouseReleaseEvent

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__offset = event.pos()
        else:
            self.master_window.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.__offset is not None and event.buttons() == Qt.LeftButton:
            self.master_window.move(
                self.master_window.pos() + event.pos() - self.__offset
            )
        else:
            self.master_window.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.__offset = None
        self.master_window.mouseReleaseEvent(event)

    def exit_app(self):
        self.master_window.close()

    def activate_mic_mode(self):
        self.inactivity_watcher.record_activity() # to delay inactive screen
        self.main_window.stacked_mic.setCurrentIndex(1)
        self.main_window.stacked_input.setCurrentIndex(2)
        self.main_window.stacked_send.setCurrentIndex(1)
    
    def activate_mic(self):
        self.main_window.stacked_mic.setCurrentIndex(1)
        self.main_window.stacked_input.setCurrentIndex(1)
        self.main_window.stacked_send.setCurrentIndex(1)
        self.__voice_listener.start()
        self.__is_listening = True

    def cancel_mic(self):
        self.inactivity_watcher.record_activity() # to delay inactive screen
        if self.__is_listening:
            self.__voice_listener.cancel()
            self.main_window.stacked_mic.setCurrentIndex(1)
            self.main_window.stacked_input.setCurrentIndex(2)
            self.main_window.stacked_send.setCurrentIndex(1)
            self.__is_listening = False
        else:
            self.main_window.stacked_mic.setCurrentIndex(0)
            self.main_window.stacked_input.setCurrentIndex(0)
            self.main_window.stacked_send.setCurrentIndex(0)

    def send_message(self, allow_blank=False, simulate=False):
        self.inactivity_watcher.record_activity() # to delay inactive screen
        msg = self.main_window.input_text.text()
        if msg.strip() == "" and not allow_blank:
            return
        self.main_window.input_text.setText("")
        if msg.strip() != "":
            self.model.add_message(USER_ME, msg)
        if not simulate:
            self.__message_courier.set_next_message(USER_ID, msg)
            self.__message_courier.start()
        self.main_window.chat_history.scrollToBottom()

    def project_reponses(self, texts: typing.List[str]):
        self.inactivity_watcher.record_activity() # to delay inactive screen
        if not texts:
            return

        # pick text to read
        to_read = []
        for text in texts:
            if len(text) <= MAX_RESPONSE_SIZE_TO_READ:
                to_read.append(text)
            self.model.add_message(USER_THEM, text.strip())

        if self.main_window.bt_voice_speak_back.isChecked():
            self._bot_speak(to_read)
        else:
            self.__message_courier.play_sound()
        self.main_window.chat_history.scrollToBottom()

    def _bot_speak(self, messages: typing.List[str]):
        self.inactivity_watcher.record_activity() # to delay inactive screen
        self.__voice_agent.set_next_messages(messages)
        self.__voice_agent.start()

    def show_settings(self):
        self.setting_window.show()

    def set_possition(self, app: QApplication):
        screen_rect = app.primaryScreen().geometry()
        wd_size = self.master_window.size()
        self.master_window.move(
            (screen_rect.width() - wd_size.width()) / 2,
            (screen_rect.height() - wd_size.height()) / 2,
        )

    def voice_message_recieved(self, messages: typing.List[str]):
        self.inactivity_watcher.record_activity() # to delay inactive screen
        self.cancel_mic()
        if len(messages) > 0:
            msg = messages[0]
        if self.main_window.ch_auto_send.isChecked():
            self.main_window.input_text.setText(msg)
            self.send_message()
        else:
            self.main_window.input_text.setText(msg)

    def voice_message_failed(self, message: str):
        self.inactivity_watcher.record_activity() # to delay inactive screen
        self.__is_listening = False
        self.cancel_mic()
        self.model.add_message(USER_THEM, message)

    def __voice_feedback_toggled(self, e: QtGui.QMouseEvent):
        self.inactivity_watcher.record_activity() # to delay inactive screen
        self.main_window.bt_voice_speak_back.setChecked(
            not self.main_window.bt_voice_speak_back.isChecked()
        )
        if (
            e.button() == Qt.LeftButton
            and not self.main_window.bt_voice_speak_back.isChecked()
        ):
            self.main_window.bt_voice_speak_back.setIcon(self.media["no_speaker"])
            self.__voice_agent.stop_speaking()
        else:
            self.main_window.bt_voice_speak_back.setIcon(self.media["speaker"])

    def splash_screen_close(self):
        self.setup_new_chat_model()
        self.send_greeting()
        self.activate_watcher()

    def send_greeting(self):
        self.inactivity_watcher.record_activity() # to delay inactive screen
        self.send_message(True)

    def activate_watcher(self):
        self.inactivity_watcher.start()

    def show_master_windows(self):
        self.master_window.show()
        #self.bd_dialog.show()
    
    def setup_new_chat_model(self):
        self.model = MessageModel()
        self.main_window.chat_history.setModel(self.model)

    def show_splash_screen(self):
        self.bd_dialog.show()

    def close_bd_dialog(self):
        self.bd_dialog.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dir_ = QtCore.QDir("Roboto")
    _id = QtGui.QFontDatabase.addApplicationFont("Roboto/Roboto-Regular.ttf")
    window = MainWindow()
    window.set_possition(app)
    window.bd_dialog.show()
    window.master_window.show()
    # window.send_greeting()
    #window.login.show()
    app.exec_()
