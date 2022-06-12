import sys
import copy
import time
from urllib import response

from helper import get_message
from module import speech_to_text, text_to_speech

import chat_ui as chat_ui

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QAbstractListModel, QMargins, QPoint, QRect, QSize, Qt, QModelIndex
from PyQt5.QtGui import QColor, QFont, QPainter, QTextDocument, QTextOption, QIcon, QKeyEvent


from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QListView,
    QMainWindow,
    QPushButton,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
    QStyleOptionViewItem,
    QMessageBox
)

USER_ME = 0
USER_THEM = 1

BUBBLE_COLORS = {USER_ME: "#E9EAEC", USER_THEM: "#CFE5FE"}
USER_TRANSLATE = {USER_ME: QPoint(10, 0), USER_THEM: QPoint(-200, 0)}

FONT_SIZE = 14

MAX_STRING = 48


class MessageDelegate(QStyledItemDelegate):
    """Draws each message.
    """

    _font = "None"
    move_y = []

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex):
        if index.row() == 0 and len(self.move_y) == 0:
            self.move_y.append(0)
        painter.save()
        # Retrieve the user,message uple from our model.data method.
        user, text = index.model().data(index, Qt.DisplayRole)

        text_size: QSize = self.sizeHint(option, index)
        trans = USER_TRANSLATE[user]
        painter.translate(trans)

        text_margins = QMargins(0,12,0,12)
        bubblerect = option.rect.marginsRemoved(text_margins)

        if index.row() != 0:
            bubblerect.setTop(bubblerect.top()+self.move_y[index.row()-1])
         # draw the triangle bubble-pointer, starting from the top left/right.
        if user == USER_ME:
            if text_size.width() <= 260:
                bubblerect.setRect(288-text_size.width(), bubblerect.top(), text_size.width(), text_size.height()-5)
            else:
                bubblerect.setRect(288-text_size.width(), bubblerect.top(), 261, text_size.height()+5)
        else:
            if text_size.width() <= 260:
                bubblerect.setRect(220, bubblerect.top(), text_size.width(), text_size.height()-5)
            else:
                bubblerect.setRect(220, bubblerect.top(), 261, text_size.height()+5)
        if index.row() != 0 and len(self.move_y) <= index.row():
            if text_size.width() > 260:
                self.move_y.append(10+self.move_y[index.row()-1])
            else:
                self.move_y.append(0+self.move_y[index.row()-1])
        # draw the bubble, changing color + arrow position depending on who
        # sent the message. the bubble is a rounded rect, with a triangle in
        # the edge.
        painter.setPen(Qt.NoPen)
        color = QColor(BUBBLE_COLORS[user])
        painter.setBrush(color)
        painter.drawRoundedRect(bubblerect, 10, 10)
        
        text_margins = QMargins(12,12,12,12)
        bubblerect = bubblerect.marginsRemoved(text_margins)
        if user == USER_ME:
            if text_size.width() <= 260:
                bubblerect.setTop(bubblerect.top()-5)
            else:
                pass
        else:
            if text_size.width() <= 260:
                bubblerect.setTop(bubblerect.top()-5)
        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        # draw the text

        doc = QTextDocument(text)
        doc.setTextWidth(bubblerect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)
        d_font = QFont("Roboto")
        d_font.setPixelSize(FONT_SIZE)
        doc.setDefaultFont(d_font)

        painter.translate(bubblerect.left(), bubblerect.top())
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        _, text = index.model().data(index, Qt.DisplayRole)
        d_font = QFont("Roboto")
        d_font.setPixelSize(FONT_SIZE)
        font_size = QtGui.QFontMetrics(d_font) # Calculate the size of the text 
        text_margins = QMargins(12,12,12,12)

        # Remove the margins, get the rectangle for the font, and add the margins back in
        rect = option.rect.marginsRemoved(text_margins) 
        rect = font_size.boundingRect(rect, Qt.TextWordWrap, text)
        rect = rect.marginsAdded(text_margins)
        return rect.size()


class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Here we pass the delegate the user, message tuple.
            return self.messages[index.row()]

    def setData(self, index, role, value):
        self._size[index.row()]

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


class MainWindow(object):
    def __init__(self):
        self.main_window = QMainWindow()
        self.main_window.setWindowIcon(QIcon("image/Avatar-Bot.png"))
        self.chat_ui = chat_ui.Ui_MainWindow()
        self.chat_ui.setupUi(self.main_window)
        self.chat_ui.messsageBrowser.setResizeMode(QListView.Adjust)
        # Use our delegate to draw items in this view.
        self.chat_ui.messsageBrowser.setItemDelegate(MessageDelegate())
        self.model = MessageModel()
        self.chat_ui.messsageBrowser.setModel(self.model) 
        self.chat_ui.messsageBrowser.setStyleSheet("background-color:rgb(255,255,255)")
        self.chat_ui.pushButton.pressed.connect(self.send_message)
        self.chat_ui.mic.pressed.connect(self.speech_to_text)
        self.chat_ui.messageInput.returnPressed.connect(self.send_message)
        self.main_window.setWindowTitle("CareU Bot")
        self.model.add_message(
                USER_THEM,
                "Hello, how are you today?" 
                )
        self.main_window.show()
        self.check_special_day(id="0198dcbe-01a2-474d-bca5-e9c90ef20877")
        # Init text to speech
        self.text_to_speech = text_to_speech.TextToSpeech(self)
        self.text_to_speech.set_next_message(["Hello, how are you today?"])
        self.text_to_speech.start()

    def speech_to_text(self):
        #FIXME: fix not showing of icon when running speech_to_text
        self.chat_ui.stackedWidget.setCurrentIndex(1)
        time.sleep(0.5)
        text = speech_to_text.run()
        self.model.add_message(USER_ME, text)
        self.chat_ui.stackedWidget.setCurrentIndex(0)

    def send_message(self):
        self.model.add_message(USER_ME, self.chat_ui.messageInput.text())

        response = get_message(
            id="0198dcbe-01a2-474d-bca5-e9c90ef20877", text = self.chat_ui.messageInput.text())
        self.text_to_speech.set_next_message(response)
        self.text_to_speech.start()
        for msg in response:
            self.model.add_message(
                USER_THEM,
                msg 
                )
        self.chat_ui.messageInput.setText("")

    def check_special_day(self, id):
        id="b1e3ff15-2d46-4071-bd23-eb7b67ba1896"
        response = get_message(id=id, type="SPECIAL_DAY")
        if "Working Anni" in response:
            print("show popup")
            self.show_popup_happy_birthday()
    
    def show_popup_happy_birthday(self):
        popup = QtWidgets.QDialog()
        popup.ui = chat_ui.PopUp()
        popup.ui.setupUi(popup)
        popup.exec_()
        popup.show()

if __name__=="__main__":
    app = QApplication(sys.argv)
    dir_ = QtCore.QDir("Roboto")
    _id = QtGui.QFontDatabase.addApplicationFont("Roboto/Roboto-Regular.ttf")
    window = MainWindow()
    app.exec_()
