# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_components/designs/login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(375, 587)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lb_title = QtWidgets.QLabel(Dialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 0, 371, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName("lb_title")
        self.bt_close = QtWidgets.QPushButton(Dialog)
        self.bt_close.setGeometry(QtCore.QRect(340, 10, 31, 31))
        self.bt_close.setText("")
        self.bt_close.setFlat(True)
        self.bt_close.setObjectName("bt_close")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(0, 180, 371, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 220, 331, 17))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 240, 331, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 320, 331, 31))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 300, 331, 17))
        self.label_4.setObjectName("label_4")
        self.bt_login = QtWidgets.QPushButton(Dialog)
        self.bt_login.setGeometry(QtCore.QRect(20, 380, 331, 31))
        self.bt_login.setObjectName("bt_login")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 430, 331, 20))
        self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_5.setStyleSheet("color: blue;")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(20, 470, 331, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 510, 331, 20))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(20, 550, 331, 20))
        self.label_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_7.setStyleSheet("color: blue;")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.lb_bot_icon = QtWidgets.QLabel(Dialog)
        self.lb_bot_icon.setGeometry(QtCore.QRect(120, 60, 121, 121))
        self.lb_bot_icon.setStyleSheet("border-radius: 10px;")
        self.lb_bot_icon.setText("")
        self.lb_bot_icon.setObjectName("lb_bot_icon")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login"))
        self.lb_title.setText(_translate("Dialog", "Login"))
        self.label_2.setText(_translate("Dialog", "Welcome to Care-U Bot"))
        self.label_3.setText(_translate("Dialog", "Email"))
        self.label_4.setText(_translate("Dialog", "Password"))
        self.bt_login.setText(_translate("Dialog", "Login"))
        self.label_5.setText(_translate("Dialog", "Forgot password?"))
        self.label_6.setText(_translate("Dialog", "Don\'t have and account?"))
        self.label_7.setText(_translate("Dialog", "Sign up"))