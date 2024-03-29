# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_components/designs/settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        # Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(647, 270)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        Dialog.setModal(True)
        self.lb_title = QtWidgets.QLabel(Dialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 0, 641, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName("lb_title")
        self.bt_close = QtWidgets.QPushButton(Dialog)
        self.bt_close.setGeometry(QtCore.QRect(608, 10, 31, 31))
        self.bt_close.setText("")
        self.bt_close.setFlat(True)
        self.bt_close.setObjectName("bt_close")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(0, 50, 651, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 170, 81, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(130, 170, 81, 31))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(230, 170, 81, 31))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(330, 170, 81, 31))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(430, 170, 91, 31))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(530, 170, 81, 31))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.lb_bot_info = QtWidgets.QLabel(Dialog)
        self.lb_bot_info.setGeometry(QtCore.QRect(40, 100, 61, 61))
        self.lb_bot_info.setText("")
        self.lb_bot_info.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_bot_info.setObjectName("lb_bot_info")
        self.lb_custom_reminder = QtWidgets.QLabel(Dialog)
        self.lb_custom_reminder.setGeometry(QtCore.QRect(140, 100, 61, 61))
        self.lb_custom_reminder.setText("")
        self.lb_custom_reminder.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_custom_reminder.setObjectName("lb_custom_reminder")
        self.lb_insights = QtWidgets.QLabel(Dialog)
        self.lb_insights.setGeometry(QtCore.QRect(240, 100, 61, 61))
        self.lb_insights.setText("")
        self.lb_insights.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_insights.setObjectName("lb_insights")
        self.lb_celebration = QtWidgets.QLabel(Dialog)
        self.lb_celebration.setGeometry(QtCore.QRect(340, 100, 61, 61))
        self.lb_celebration.setText("")
        self.lb_celebration.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_celebration.setObjectName("lb_celebration")
        self.lb_activities = QtWidgets.QLabel(Dialog)
        self.lb_activities.setGeometry(QtCore.QRect(440, 100, 61, 61))
        self.lb_activities.setText("")
        self.lb_activities.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_activities.setObjectName("lb_activities")
        self.lb_fun_meet = QtWidgets.QLabel(Dialog)
        self.lb_fun_meet.setGeometry(QtCore.QRect(540, 100, 61, 61))
        self.lb_fun_meet.setText("")
        self.lb_fun_meet.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_fun_meet.setObjectName("lb_fun_meet")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lb_title.setText(_translate("Dialog", "Settings"))
        self.label_2.setText(_translate("Dialog", "Personalize\n" "Bot"))
        self.label_3.setText(_translate("Dialog", "Custom\n" "reminder"))
        self.label_4.setText(_translate("Dialog", "Insights"))
        self.label_5.setText(_translate("Dialog", "Celebration"))
        self.label_6.setText(_translate("Dialog", "HV activities"))
        self.label_7.setText(_translate("Dialog", "Fun Meet"))
