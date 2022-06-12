import os
import requests
from time import sleep
from random import randint

from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtCore import QAbstractListModel, QMargins, QPoint, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QStyledItemDelegate,
)

SERVER_HOSTNAME = "172.18.14.213"
SERVER_PORT = 8080
BASE_URL = "be/v1/careu"
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# constants for drawing messages
USER_ME = 0
USER_THEM = 1
BUBBLE_COLORS = {USER_ME: "#BFD5EE", USER_THEM: "#D9DADC"}
BUBBLE_PADDING = {
    USER_ME: QMargins(50, 5, 15, 5),
    USER_THEM: QMargins(15, 5, 50, 5),
}  # (left, top, right, bottom)
TEXT_PADDING = {USER_ME: QMargins(60, 15, 25, 15), USER_THEM: QMargins(25, 15, 60, 15)}

DING_SOUND = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "sounds", "ding-sound-effect.mp3")
)
TANG_SOUND = os.path.abspath(os.path.join(CURRENT_DIR, "..", "sounds", "TANG.WAV"))

TEMPLATE_USER = """<div style="width: 40%;
                               padding: 5px 5px 5px 5px;
                               height: 30px;
                               background-color: #CFE5FE;
                               margin: 5px 10px 5px 50px;
                               border-radius: 8px;
                               ksjdfhksdjfh: srflgkjsdf;
                               text-align: left;">{}</div>"""
TEMPLATE_BOT = """<div style="width: 60%;
                              padding: 50px 50px 50px 50px;
                              background-color: #E9EAEC;
                              margin: 10px 50px 5px 5px;
                              border: 1px solid;
                              border-radius: 8px;">{}</div>"""


class CareUMsgCourier(QtCore.QThread):
    text_received = QtCore.pyqtSignal(list)

    def __init__(self, user_id=None, message=None):
        super().__init__()
        self.__user_id = user_id
        self.__message = message

        self.__player = QtMultimedia.QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile(DING_SOUND)
        self.__player.setMedia(QtMultimedia.QMediaContent(url))

    def set_next_message(self, user_id, message):
        self.__user_id = user_id
        self.__message = message

    def run(self):
        url = f"http://{SERVER_HOSTNAME}:{SERVER_PORT}/{BASE_URL}/{self.__user_id}/comm"
        response = requests.post(url, json={"message": self.__message})
        try:
            ret = response.json()
        except:
            self.text_received.emit("Please check your connection and try again")
        if ret["result"].get("status", None) != "processed":
            self.text_received.emit("Please check your connection and try again")
        else:
            ret_msgs = [i["response"] for i in ret["result"]["responses"]]
            sleep(randint(11, 22) / 10.0)
            self.text_received.emit(ret_msgs)
        # self.play_sound()

    def play_sound(self):
        self.__player.setVolume(50)
        # self.sound.play()
        self.__player.play()


class MessageDelegate(QStyledItemDelegate):
    """
    Draws each message.
    """

    def paint(self, painter, option, index):
        # Retrieve the user,message uple from our model.data method.
        user, text = index.model().data(index, Qt.DisplayRole)

        # option.rect contains our item dimensions. We need to pad it a bit
        # to give us space from the edge to draw our shape.

        bubblerect = option.rect.marginsRemoved(BUBBLE_PADDING[user])
        textrect = option.rect.marginsRemoved(TEXT_PADDING[user])

        # draw the bubble, changing color + arrow position depending on who
        # sent the message. the bubble is a rounded rect, with a triangle in
        # the edge.
        painter.setPen(Qt.NoPen)
        color = QColor(BUBBLE_COLORS[user])
        painter.setBrush(color)
        painter.drawRoundedRect(bubblerect, 10, 10)

        # draw the triangle bubble-pointer, starting from
        if user == USER_ME:
            p1 = bubblerect.topRight()
            painter.drawPolygon(
                p1 + QPoint(1, 0),
                p1 + QPoint(-25, 0),
                p1 + QPoint(0, 25),
            )
        else:
            p1 = bubblerect.topLeft()
            painter.drawPolygon(
                p1 + QPoint(0, 0),
                p1 + QPoint(20, 0),
                p1 + QPoint(0, 20),
            )

        # draw the text
        painter.setPen(Qt.black)
        painter.drawText(textrect, Qt.TextWordWrap, text)

    def sizeHint(self, option, index):
        user, text = index.model().data(index, Qt.DisplayRole)
        # Calculate the dimensions the text will require.
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(TEXT_PADDING[user])
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, text)
        rect = rect.marginsAdded(TEXT_PADDING[user])  # Re add padding for item size.
        return rect.size()


class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Here we pass the delegate the user, message tuple.
            return self.messages[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def add_message(self, who, text):
        """
        Add an message to our message list, getting the text from the QLineEdit
        """
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.messages.append((who, text))
            # Trigger refresh.
            self.layoutChanged.emit()
