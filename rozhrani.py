# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rozhrani.ui'
#
# Created: Thu Oct  8 14:26:40 2015
#      by: PyQt4 UI code generator 4.11.3
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
        Dialog.resize(625, 325)
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QtCore.QRect(300, 150, 131, 22))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(390, 40, 66, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(490, 40, 91, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(310, 60, 51, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(310, 100, 51, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 60, 151, 31))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(370, 10, 171, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(90, 10, 171, 17))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(10, 90, 151, 31))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(170, 60, 113, 30))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 100, 113, 30))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_3 = QtGui.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(360, 60, 113, 30))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.lineEdit_4 = QtGui.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(360, 100, 113, 30))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit_5 = QtGui.QLineEdit(Dialog)
        self.lineEdit_5.setGeometry(QtCore.QRect(480, 60, 113, 30))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.lineEdit_6 = QtGui.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(480, 100, 113, 30))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.line = QtGui.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(280, 40, 20, 91))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(20, 220, 581, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(10, 110, 151, 31))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.checkBox_2 = QtGui.QCheckBox(Dialog)
        self.checkBox_2.setGeometry(QtCore.QRect(440, 150, 171, 22))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.textBrowser = QtGui.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 260, 381, 51))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(420, 270, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(17, 150, 251, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(310, 130, 291, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.spinBox = QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(300, 180, 60, 27))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(3)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(370, 180, 161, 31))
        self.label_10.setObjectName(_fromUtf8("label_10"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Forty Four", None))
        self.checkBox.setText(_translate("Dialog", "Zobrazit grafy", None))
        self.label.setText(_translate("Dialog", "Kanál", None))
        self.label_2.setText(_translate("Dialog", "Energie (keV)", None))
        self.label_3.setText(_translate("Dialog", "1. bod", None))
        self.label_4.setText(_translate("Dialog", "2. bod", None))
        self.label_5.setText(_translate("Dialog", "Faktor šířky píku", None))
        self.label_6.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Energetická kalibrace</span></p></body></html>", None))
        self.label_7.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Vstupní hodnoty</span></p></body></html>", None))
        self.label_8.setText(_translate("Dialog", "Počet cyklů při", None))
        self.lineEdit.setText(_translate("Dialog", "1", None))
        self.lineEdit_2.setText(_translate("Dialog", "8", None))
        self.lineEdit_3.setText(_translate("Dialog", "1085.7", None))
        self.lineEdit_4.setText(_translate("Dialog", "2783.6", None))
        self.lineEdit_5.setText(_translate("Dialog", "510.9989", None))
        self.lineEdit_6.setText(_translate("Dialog", "1460.83", None))
        self.label_9.setText(_translate("Dialog", "vyhlazování pozadí", None))
        self.checkBox_2.setText(_translate("Dialog", "Vyhlazovat spektrum", None))
        self.pushButton.setText(_translate("Dialog", "Vybrat složku se soubory FRK", None))
        self.label_10.setText(_translate("Dialog", "Typ výpočtu pozadí", None))

