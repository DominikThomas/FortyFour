# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui 
import sys, sip, matplotlib

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

import rozhrani, FortyThree

class FortyFour(QtGui.QMainWindow, rozhrani.Ui_Dialog, FortyThree.Vypocet):
    def __init__(self):
        
        super(self.__class__, self).__init__()
        self.setupUi(self)  
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.Forty_Three)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Prochazet)
        self.slozka = None
        
    def Prochazet(self):
        self.slozka = QtGui.QFileDialog.getExistingDirectory()
        self.textBrowser.setText('Byla vybrána složka %s' %(self.slozka))
    
    def reject(self):
        exit(0)
        
def main():
    app = QtGui.QApplication(sys.argv)  
    form = FortyFour()                
    form.show()                       
    app.exec_()                        


if __name__ == '__main__':              
    main()                           