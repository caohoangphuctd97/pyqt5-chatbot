# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_components/designs/birthday_card.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 684)
        Dialog.setModal(False)
        self.lb_card = QtWidgets.QLabel(Dialog)
        self.lb_card.setGeometry(QtCore.QRect(0, 0, 1200, 684))
        self.lb_card.setMinimumSize(QtCore.QSize(1200, 684))
        self.lb_card.setText("")
        self.lb_card.setObjectName("lb_card")
        self.bt_start_chatting = QtWidgets.QPushButton(Dialog)
        self.bt_start_chatting.setGeometry(QtCore.QRect(550, 480, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.bt_start_chatting.setFont(font)
        self.bt_start_chatting.setStyleSheet("background-color: #C00;\n"
"color: white;\n"
"padding: 5px 15px;\n"
"border-radius: 15px;\n"
"outline: 0;\n"
"text-transform: uppercase;\n"
"cursor: pointer;\n"
"box-shadow: 0px 2px 2px gray;\n"
"transition: ease background-color 250ms;\n"
"")
        self.bt_start_chatting.setObjectName("bt_start_chatting")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "birthday_card"))
        self.bt_start_chatting.setText(_translate("Dialog", "Click here to chat with me"))