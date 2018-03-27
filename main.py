# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui 
import sys, sip, matplotlib
if sys.version_info.major<3:
    reload(sys)
    sys.setdefaultencoding('UTF8')

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
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.prochazet)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.konfigurace)
        self.slozka = None
        
    def prochazet(self):
        self.slozka = QtGui.QFileDialog.getExistingDirectory(None,(u"Vyberte složku s FRK soubory"))
        if self.slozka != '': self.textBrowser.setText('Byla vybrána složka %s' %(self.slozka))
        
    def konfigurace(self):
        self.cfgname = QtGui.QFileDialog.getOpenFileName(None,(u"Vyberte konfigurační soubor cfg"),"./",("Konfigurační soubory (*.CFG *.Cfg *.cfg)"))
        if self.cfgname != '': self.textBrowser.setText('Byl vybrán konfigurační soubor %s' %(self.cfgname))
        f0=open(self.cfgname)
        for i0 in range(0, 20):
            if i0==12:
                config0=(f0.readline().split())
                config1=(f0.readline().split())
            f0.readline()
        self.lineEdit_3.setText(_translate("Dialog", config0[0], None))
        self.lineEdit_4.setText(_translate("Dialog", config1[0], None))
        self.lineEdit_5.setText(_translate("Dialog", config0[1], None))
        self.lineEdit_6.setText(_translate("Dialog", config1[1], None))
    
    def reject(self):
        sys.exit()
        
def main():
    app = QtGui.QApplication(sys.argv)  
    form = FortyFour()                
    form.show()                       
    app.exec_()                        


if __name__ == '__main__':              
    main()                           