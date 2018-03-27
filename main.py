# from joblib import Parallel, delayed, cpu_count
from PyQt4 import QtCore, QtGui 
from glob import glob
from multiprocessing import Pool, cpu_count
import os, sys, io

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

import rozhrani, FortyThree, get_gamma_data

class FortyFour(QtGui.QMainWindow, rozhrani.Ui_Dialog, FortyThree.Vypocet, get_gamma_data.Data):
    def __init__(self):
        super(FortyFour, self).__init__()
        # super(self.__class__, self).__init__()
        self.setupUi(self)  
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.start)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.prochazet)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.konfigurace)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ulozit_konfiguraci)
        self.slozka = None
        self.exepath = os.getcwd()
    
    def prochazet(self):
        self.slozka = QtGui.QFileDialog.getExistingDirectory(None,(u"Vyberte složku s FRK soubory"))
        if self.slozka != '': self.textBrowser.append('Byla vybrána složka %s' %(self.slozka))
        
    def konfigurace(self):
        self.cfgname = QtGui.QFileDialog.getOpenFileName(None,(u"Vyberte konfigurační soubor cfg"),"./",("Konfigurační soubory (*.CFG *.Cfg *.cfg)"))
        if self.cfgname != '':
            self.textBrowser.append('Byl vybrán konfigurační soubor %s' %(self.cfgname))
        else:
            return 0
        f0=io.open(self.cfgname)
        hlavicka = f0.readline()
        if 'J.Frana - OJS UJF Rez' in hlavicka:
            for i0 in range(0, 20):
                if i0==11:
                    config0=(f0.readline().split())
                    config1=(f0.readline().split())
                    break
                f0.readline()
        elif 'D.Thomas - OJR UJF Rez' in hlavicka:
            config0=(f0.readline().split())
            config1=(f0.readline().split())
        else:
            for i0 in range(0, 20):
                if i0==11:
                    config0=(f0.readline().split())
                    config1=(f0.readline().split())
                    break
                f0.readline()
            
        self.lineEdit_3.setText(_translate("Dialog", config0[0], None))
        self.lineEdit_4.setText(_translate("Dialog", config1[0], None))
        self.lineEdit_5.setText(_translate("Dialog", config0[1], None))
        self.lineEdit_6.setText(_translate("Dialog", config1[1], None))
        
    def ulozit_konfiguraci(self):
        self.save_filename = QtGui.QFileDialog.getSaveFileName(self, "Uložit konfigurační soubor", "", ".cfg")
        vystup = open(self.save_filename + '.cfg','w')
        vystup.write('D.Thomas - OJR UJF Rez \n')
        vystup.write('%4.4f %4.4f\n' %(float(self.lineEdit_3.text()), float(self.lineEdit_5.text())))
        vystup.write('%4.4f %4.4f\n' %(float(self.lineEdit_4.text()), float(self.lineEdit_6.text())))
        vystup.write('Inspirovano programy a formaty pana J.Frani - OJS UJF Rez')
        vystup.close
        
    def reject(self):
        sys.exit()
    
    # def pokus(x):
    #     y=x*x
    #     print(y)
        
    def start(self):    
        if ('vaha0' in globals()) or ('vaha0' in locals()):
            self.vaha1=vaha0
            self.ampl1=ampl0
        else:
            self.vaha1=50
            self.ampl1=-10000
        
        self.soubory = glob(self.slozka + '/*.FRK') + glob(self.slozka + '/*.CNF')
        
        self.inputs = range(len(self.soubory))
        if len(self.soubory)<1:
            self.textBrowser.setText('Nebyly nalezeny žádné soubory .FRK ani .CNF')
        else:
            
            print('OK0')
            pool = Pool(processes=len(self.inputs))
            pool.map(self.Forty_Three, self.inputs)
            # self.Multi()

def main():
    app = QtGui.QApplication(sys.argv)  
    form = FortyFour()                
    form.show()
    app.exec_()


if __name__ == '__main__':              
    main()   
