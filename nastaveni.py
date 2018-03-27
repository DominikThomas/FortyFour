# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nastaveni.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(305, 159)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(190, 120, 98, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(20, 10, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.lineEdit_8 = QtGui.QLineEdit(Dialog)
        self.lineEdit_8.setGeometry(QtCore.QRect(180, 20, 113, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 80, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_9 = QtGui.QLineEdit(Dialog)
        self.lineEdit_9.setGeometry(QtCore.QRect(180, 70, 113, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setObjectName(_fromUtf8("lineEdit_9"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton.setText(_translate("Dialog", "OK", None))
        self.label_11.setText(_translate("Dialog", "Diskriminace dle", None))
        self.lineEdit_8.setText(_translate("Dialog", "-10000", None))
        self.label_2.setText(_translate("Dialog", "amplitudy píku", None))
        self.label_4.setText(_translate("Dialog", "při vyhlazování pozadí", None))
        self.label_3.setText(_translate("Dialog", "Váha prostřední hodnoty", None))
        self.lineEdit_9.setText(_translate("Dialog", "50", None))

