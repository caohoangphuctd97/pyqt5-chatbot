import typing

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
)

from ui_components import settings, birthday_card, login
from ui_components.setting_dialogs import custom_reminders


class BirthdayCard(QDialog):
    on_exit = QtCore.pyqtSignal()
    last_index = 0

    def __init__(
        self,
        parent: typing.Optional[QWidget],
        flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType],
    ) -> None:
        super().__init__(parent=parent, flags=flags)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.bd_window = birthday_card.Ui_Dialog()
        self.bd_window.setupUi(self)
        self.__bd_gif = QtGui.QMovie("image/popup_happybirthday.gif")
        self.__bd_gif = QtGui.QMovie("image/welcome-back.gif")
        self.set_up_window()

    def set_up_window(self):
        self.bd_window.lb_card.setMovie(self.__bd_gif)
        self.__bd_gif.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.on_exit.emit()
        return super().closeEvent(a0)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.on_exit.emit()
        return super().keyPressEvent(a0)


class SettingWindow(QDialog):
    def __init__(
        self,
        parent: typing.Optional[QWidget],
        flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType],
    ) -> None:
        super().__init__(parent=parent, flags=flags)
        self.__offset = None
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setting_window = settings.Ui_Dialog()
        self.setting_window.setupUi(self)
        self.set_up_window()
        self.set_up_draggable_title()

        # set up children dialogs
        self.custom_reminders = CustomReminder(self, Qt.WindowFlags())

        # load images
        self.setting_window.lb_bot_info.setPixmap(QtGui.QPixmap("image/bot_info.png"))
        self.setting_window.lb_custom_reminder.setPixmap(
            QtGui.QPixmap("image/custom_reminder.png")
        )
        self.setting_window.lb_insights.setPixmap(QtGui.QPixmap("image/insights.png"))
        self.setting_window.lb_celebration.setPixmap(
            QtGui.QPixmap("image/celebrations.png")
        )
        self.setting_window.lb_activities.setPixmap(
            QtGui.QPixmap("image/hv_activities.png")
        )
        self.setting_window.lb_fun_meet.setPixmap(QtGui.QPixmap("image/fun_meet.png"))
        self.setting_window.bt_close.setIcon(QtGui.QIcon("image/close_gray.png"))

        # connect signals
        self.setting_window.lb_custom_reminder.mouseReleaseEvent = (
            self.open_reminder_dialog
        )

    def set_up_draggable_title(self):
        self.setting_window.bt_close.pressed.connect(self.exit_window)
        self.setting_window.lb_title.mousePressEvent = self.mousePressX
        self.setting_window.lb_title.mouseMoveEvent = self.mouseMoveX
        self.setting_window.lb_title.mouseReleaseEvent = self.mouseReleaseX

    def mousePressX(self, event):
        if event.button() == Qt.LeftButton:
            self.__offset = event.pos()
        else:
            self.mousePressEvent(event)

    def mouseMoveX(self, event):
        if self.__offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.__offset)
        else:
            self.mouseMoveEvent(event)

    def mouseReleaseX(self, event):
        self.__offset = None
        super().mouseReleaseEvent(event)

    def open_reminder_dialog(self, e: QtGui.QMouseEvent):
        if e.button() == Qt.LeftButton:
            self.custom_reminders.show()

    def set_up_window(self):
        pass

    def exit_window(self):
        self.close()


class CustomReminder(QDialog):
    def __init__(
        self,
        parent: typing.Optional[QWidget],
        flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType],
    ) -> None:
        super().__init__(parent=parent, flags=flags)
        self.__offset = None
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.custom_reminders = custom_reminders.Ui_Dialog()
        self.custom_reminders.setupUi(self)
        self.set_up_window()
        self.set_up_draggable_title()

        # set images
        self.custom_reminders.bt_exit.setIcon(QtGui.QIcon("image/close_gray.png"))

        # connect signals
        self.custom_reminders.chk_all_habits.stateChanged.connect(
            self.__all_habit_changed
        )

    def set_up_draggable_title(self):
        self.custom_reminders.bt_exit.pressed.connect(self.exit_window)
        self.custom_reminders.lb_title.mousePressEvent = self.mousePressX
        self.custom_reminders.lb_title.mouseMoveEvent = self.mouseMoveX
        self.custom_reminders.lb_title.mouseReleaseEvent = self.mouseReleaseX

    def mousePressX(self, event):
        if event.button() == Qt.LeftButton:
            self.__offset = event.pos()
        else:
            self.mousePressEvent(event)

    def mouseMoveX(self, event):
        if self.__offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.__offset)
        else:
            self.mouseMoveEvent(event)

    def mouseReleaseX(self, event):
        self.__offset = None
        super().mouseReleaseEvent(event)

    def set_up_window(self):
        pass

    def exit_window(self):
        self.close()

    def __all_habit_changed(self):
        new_state = self.custom_reminders.chk_all_habits.isChecked()
        self.custom_reminders.chk_0_drink_stand.setChecked(new_state)
        self.custom_reminders.chk_0_eye_relax.setChecked(new_state)
        self.custom_reminders.chk_0_main_meals.setChecked(new_state)


class LoginDialog(QDialog):
    on_exit = QtCore.pyqtSignal()
    def __init__(
        self,
        parent: typing.Optional[QWidget],
        flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType],
    ) -> None:
        super().__init__(parent=parent, flags=flags)
        self.__offset = None
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.login = login.Ui_Dialog()
        self.login.setupUi(self)
        self.set_up_window()
        self.set_up_draggable_title()

        # set images
        self.login.bt_close.setIcon(QtGui.QIcon("image/close_gray.png"))
        self.login.lb_bot_icon.setPixmap(QtGui.QPixmap("image/character_icon.png"))
        # gif_size = QtCore.QSize(
        #     self.login.lb_bot_icon.width(), self.login.lb_bot_icon.height()
        # )
        self.login.lb_bot_icon.setScaledContents(True)
        # connect signals
        self.login.bt_close.pressed.connect(self.exit_window)
        self.login.bt_login.pressed.connect(self.exit_window)

    def set_up_draggable_title(self):
        self.login.bt_close.pressed.connect(self.exit_window)
        self.login.lb_title.mousePressEvent = self.mousePressX
        self.login.lb_title.mouseMoveEvent = self.mouseMoveX
        self.login.lb_title.mouseReleaseEvent = self.mouseReleaseX

    def mousePressX(self, event):
        if event.button() == Qt.LeftButton:
            self.__offset = event.pos()
        else:
            self.mousePressEvent(event)

    def mouseMoveX(self, event):
        if self.__offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.__offset)
        else:
            self.mouseMoveEvent(event)

    def mouseReleaseX(self, event):
        self.__offset = None
        super().mouseReleaseEvent(event)

    def set_up_window(self):
        pass

    def exit_window(self):
        self.on_exit.emit()
        self.close()

