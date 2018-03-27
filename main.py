# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui 
import sys, io, sip, os #, matplotlib
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

import rozhrani, nastaveni, FortyThree, get_gamma_data

class FortyFour(QtGui.QMainWindow, rozhrani.Ui_Dialog, FortyThree.Vypocet, get_gamma_data.Data):
    def __init__(self):
        
        super(self.__class__, self).__init__()
        self.setupUi(self)  
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.start)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.prochazet)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.konfigurace)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.settings)
        self.slozka = None
        self.exepath = os.getcwd()
        
    def prochazet(self):
        self.slozka = QtGui.QFileDialog.getExistingDirectory(None,(u"Vyberte složku s FRK soubory"))
        if self.slozka != '': self.textBrowser.setText('Byla vybrána složka %s' %(self.slozka))
        
    def konfigurace(self):
        self.cfgname = QtGui.QFileDialog.getOpenFileName(None,(u"Vyberte konfigurační soubor cfg"),"./",("Konfigurační soubory (*.CFG *.Cfg *.cfg)"))
        if self.cfgname != '': self.textBrowser.setText('Byl vybrán konfigurační soubor %s' %(self.cfgname))
        f0=io.open(self.cfgname)
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
        
    def settings(self):
        
        nastav = Nastaveni()
        nastav.show()
        QtGui.QApplication.exec_(self)
        
        QtCore.QObject.connect(nastav.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), nastav.zavri)
        
    def start(self):    
        if ('vaha0' in globals()) or ('vaha0' in locals()):
            self.vaha1=vaha0
            self.ampl1=ampl0
        else:
            self.vaha1=50
            self.ampl1=-10000
        self.Forty_Three()
        
class Nastaveni(QtGui.QMainWindow, nastaveni.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
         
        if 'vaha0' in globals():
            print(vaha0)
            self.lineEdit_9.setText(str(vaha0))
            self.lineEdit_8.setText(str(ampl0))
            
    def zavri(self):
        global vaha0
        vaha0=int(self.lineEdit_9.text())
        global ampl0
        ampl0=int(self.lineEdit_8.text())
        self.close()
        
def main():
    app = QtGui.QApplication(sys.argv)  
    form = FortyFour()                
    form.show()
    app.exec_()

if __name__ == '__main__':              
    main()                           