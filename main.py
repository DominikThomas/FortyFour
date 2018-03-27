# from joblib import Parallel, delayed, cpu_count
from PyQt4 import QtCore, QtGui 
from glob import glob
# from joblib import Parallel, delayed, cpu_count



import matplotlib
matplotlib.use("Qt4Agg", force=True) #Nutno #Qt5Agg způsobuje neplynulost při procházení grafů
import time
import os, sys, matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from numpy import mean
from platform import system

import _thread


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

import rozhrani, get_gamma_data


class Spektrum():
    def __init__(self,iterator):
        self.vystup = self.soubory[iterator]
        self.pocet_kanalu = int(self.comboBox_3.currentText())
        config0=[self.lineEdit_3.text(),self.lineEdit_5.text()]
        config1=[self.lineEdit_4.text(),self.lineEdit_6.text()]
        self.newconfig=[0,0]
        self.newconfig[0]=float(config0[1])-float(config0[0])*(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
        self.newconfig[1]=(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
        self.sirka = int(self.lineEdit.text())
        self.cykl = int(self.lineEdit_2.text())
        self.ampl = self.ampl1
        self.grafy = self.checkBox.checkState() #aby se vykreslovaly
        
        vyhlazeni=self.checkBox_2.checkState() #zda vyhlazovat samotné spektrum
        vaha=self.vaha1 #váha prostřední hodnoty při vyhlazování spektra
        typ_pozadi=self.spinBox.value()
        radit=[self.checkBox_4.checkState(),self.comboBox.currentText().lower().replace('č','c')] #zajištěno, že "klíče" jsou malým písmenem
        
        
    def Vytvor_spektrum(self):
        
        Y0=[0]*self.pocet_kanalu
        f1=open(self.vystup)

        self.spektrum={}

        for i2 in range(0, self.pocet_kanalu):
            a=f1.readline().split()
            try:
                Y0[i2]=float(''.join(a))
            except ValueError:
                print('Metoda "Vytvoř spektrum", chyba hodnoty a: ',a)
        self.spektrum['cetnost']=[]
        self.spektrum['cetnost']=Y0
        
        return self
        
    def Najdi_piky(self):
        if 'kanal' in self.spektrum.keys():
            pass
        else:
            self.spektrum['kanal']=range(1,self.pocet_kanalu)
            self.spektrum['energie']=tuple((self.newconfig[0]+(i+1)*self.newconfig[1]) for i in range(self.pocet_kanalu))
            self.spektrum['derivace']=(0,)+tuple((self.spektrum['cetnost'][i]-self.spektrum['cetnost'][i-1]) for i in range(self.pocet_kanalu-1))
            # print((self.spektrum['derivace'][0]))
            # print(self.spektrum['kanal'])
        self.piky0={}
        self.piky0['kanal']=[] #G0=[] #kanál přibližného středu píku (derivace mění znaménko)
        self.piky0['energie']=[] #G1=[] #energie přibližného středu píku (derivace mění znaménko)
        self.piky0['levy']=[] #H0=[] #levé okraje píků
        self.piky0['pravy']=[] #H1=[] #pravé okraje píků
        for i5 in range(0, self.pocet_kanalu-self.sirka):
            if(self.spektrum['derivace'][i5+self.sirka]<0):
                self.piky0['kanal'].append(self.spektrum['kanal'][i5])
                self.piky0['energie'].append(self.spektrum['energie'][i5])
        for i6 in range(0, len(self.piky0['kanal'])-self.sirka):
            if (i6==0):
                l11=self.piky0['kanal'][i6]
                l12=0
            l1=max(self.piky0['kanal'][i6],l12+1)
            l2=max(l1+self.sirka,l11)
            if (l1>self.pocet_kanalu or l2>self.pocet_kanalu):
                break
            while True:
                l1-=1
                if(l1==0 or l1==l12-1 or self.spektrum['derivace'][max(l1,1)]<-0.1):
                    break
            if l1==0:
                l1=1
            self.piky0['levy'].append(l1)
            if(l2<self.pocet_kanalu):
                while True:
                    l2+=1
                    if(l2==(self.pocet_kanalu-1) or l2>=self.pocet_kanalu or self.spektrum['derivace'][l2]>0.1):
                        break
                self.piky0['pravy'].append(l2-1)
            else:
                self.piky0['pravy'].append(l2-2)
            l11=l1
            l12=l2
        
        return self
        
    def Uprav_piky(self):
        
        self.piky1={}
        self.piky1['levy']=[self.piky0['levy'][0]] #H01
        self.piky1['pravy']=[self.piky0['pravy'][0]] #H11
        for i7 in range (1, len(self.piky0['levy'])): #odstranění duplicitních píků
            if (self.piky0['levy'][i7-1],self.piky0['pravy'][i7-1])!=(self.piky0['levy'][i7],self.piky0['pravy'][i7]):
                self.piky1['levy'].append(self.piky0['levy'][i7])
                self.piky1['pravy'].append(self.piky0['pravy'][i7])
        self.piky={}
        self.piky['energie']=[] # G20=[] #energie maxima píku
        self.piky['suma']=[] #G21=[] #suma píku i s pozadím
        self.piky['levy']=[] #G22=[] #levý okraj píku
        self.piky['pravy']=[] #G23=[] #pravý okraj píku
        self.piky['pozadi']=[] #G24=[] #pozadí
        self.piky['sirka']=[] #G25=[] #šířka píku v kanálech
        self.piky['plocha']=[] #G26=[] #plocha píku bez pozadí
        self.piky['vyska']=[] #nové, 3.3.2016
        for i8 in range (0,len(self.piky1['levy'])):
            maximum, index = max((val, idx) for idx, val in enumerate(self.spektrum['cetnost'][self.piky1['levy'][i8]:self.piky1['pravy'][i8]]))
            self.piky['energie'].append(self.spektrum['energie'][self.piky1['levy'][i8]+index]) #energie maxima píku
            self.piky['suma'].append(sum(self.spektrum['cetnost'][self.piky1['levy'][i8]:self.piky1['pravy'][i8]])) #suma píku i s pozadím
            self.piky['levy'].append(self.piky1['levy'][i8]) #levý okraj píku
            self.piky['pravy'].append(self.piky1['pravy'][i8]) #pravý okraj píku
            self.piky['sirka'].append(len(self.spektrum['cetnost'][self.piky1['levy'][i8]:self.piky1['pravy'][i8]])) #šířka píku v kanálech
            self.piky['vyska'].append(maximum - self.spektrum['cetnost'][self.piky['levy'][i8]] - (self.spektrum['cetnost'][self.piky['pravy'][i8]]-self.spektrum['cetnost'][self.piky['levy'][i8]])/self.piky['sirka'][i8]*index ) #výška píku s odečteným pozadím
            
        self.pozadi=[]
        for i9 in range (0, len(self.piky['pravy'])):
            self.pozadi.append(self.spektrum['cetnost'][self.piky['pravy'][i9]])
            
        return self
        
    def Vyhlad_pozadi(self):
       
        
        kraje_cet = tuple(self.pozadi)
        # kraje_cet =[]
        # kraje_cet.extend(self.pozadi)
        
        kraje_der = [0]
        
        for i in range (1, len(kraje_cet)):
            kraje_der.append(kraje_cet[i]-kraje_cet[i-1])
            
        pozadi_2 = [0] * len(kraje_cet)
        kraje_der_2 = [0] * len(kraje_der)
        
        i=1
        
        while i < len(kraje_cet)-2:
            if abs(kraje_der[i]) < 50:
                pozadi_2[i] = kraje_cet[i]
                kraje_der_2[i] = kraje_der[i]
                i+=1
            else:
                
                j=i
                try:
                    while (abs(kraje_der[j]) > 40) and (j-i<30):
                    
                        j+=1
                except IndexError: 
                    j-=1
                d=j-i
                if d!=0:
                    kraje_der_2[i:j] = [mean(kraje_der[i:j])]*d
                    pozadi_2[i]=pozadi_2[i-1]+kraje_der_2[i]
                i+=1
                
                for k in range(d):
                    pozadi_2[i+k]=pozadi_2[i+k-1]+kraje_der_2[i+k]
                i+=d
                    
            ##
                
        pozadi_vyhlazeno = [0] * len(kraje_cet)
        pozadi_vyhlazeno[0] = kraje_cet[0]
        pozadi_vyhlazeno[len(kraje_cet)-1] = kraje_cet[len(kraje_cet)-1]
        
        # cykl = 2
        
        pozadi0 = []
        for i in pozadi_2:
            pozadi0.append(i)
        
        for j in range(self.cykl):
            for i in range (1, len(pozadi0)-1):
                pozadi_vyhlazeno[i] = mean([pozadi0[i-1],pozadi0[i],pozadi0[i+1]])
            pozadi0 = pozadi_vyhlazeno
            
        self.pozadi = pozadi0
        
        
        PP=[0.0]*self.pocet_kanalu
        
        for i9e in range (0,len(self.piky['pravy'])-1):
            PP[self.piky['pravy'][i9e]]=self.pozadi[i9e]
            inkrement=(self.pozadi[i9e+1]-self.pozadi[i9e])/(self.piky['pravy'][i9e+1]-self.piky['pravy'][i9e])
            for i9f in range (0,(self.piky['pravy'][i9e+1]-self.piky['pravy'][i9e])):
                PP[self.piky['pravy'][i9e]+i9f]=PP[self.piky['pravy'][i9e]]+i9f*inkrement
    
       
        for i10a in range (0,len(self.piky['pravy'])):
            self.piky['pozadi'].append(PP[self.piky['pravy'][i10a]])    
        
        self.piky['plocha'].append(self.piky['suma'][0]-(self.spektrum['cetnost'][self.piky['levy'][0]]/2+self.piky['pozadi'][0]/2)*self.piky['sirka'][0])
        for i9b in range(1,len(self.piky['sirka'])):
            self.piky['plocha'].append(self.piky['suma'][i9b]-sum(PP[self.piky['levy'][i9b]:self.piky['pravy'][i9b]]))
            
        for i9c in range(0,len(self.piky['plocha'])):
            if self.piky['plocha'][i9c]<self.ampl:
                self.piky['energie'][i9c]=[];self.piky['suma'][i9c]=[];self.piky['levy'][i9c]=[];self.piky['pravy'][i9c]=[];self.piky['pozadi'][i9c]=[];self.piky['sirka'][i9c]=[];self.piky['plocha'][i9c]=[]
        for i9d in range(0,self.piky['energie'].count([])):
            self.piky['energie'].remove([]);self.piky['suma'].remove([]);self.piky['levy'].remove([]);self.piky['pravy'].remove([]);self.piky['pozadi'].remove([]);self.piky['sirka'].remove([]);self.piky['plocha'].remove([])
            
        self.pozadi_konec = PP
            
        return self
        
    def vykresli(self):
        if (self.grafy==2):
            plt.figure(os.path.basename(self.vystup))
            plt.title(os.path.basename(self.vystup))
            plt.xlabel(u'Energie (keV)')
            plt.ylabel(u'Četnost (-)')
            plt.plot(self.spektrum['energie'], self.spektrum['cetnost'], label=u'Spektrum') #vykreslení spektra
            plt.plot(self.spektrum['energie'], self.pozadi_konec, 'r', label=u'Pozadí') #vykreslení pozadí
            plt.legend()
        return self
        
class Zacni():
    def A(self):
        self.inputs = range(len(self.soubory))
        print('OK0')
        Parallel(n_jobs=len(self.inputs))(delayed(self.Multi)(input) for input in self.inputs)
        
    def Multi(self,x):
        print('OK1')
        # import main
        # super(FortyFour, self).__init__()
        # time.sleep(0.1)
        b = Spektrum(x)
        b.Vytvor_spektrum().Najdi_piky().Uprav_piky().Vyhlad_pozadi().vykresli()
        if x == len(self.inputs)-1:
            print(time.time()-self.t)
        plt.show()
    
            
            
class FortyFour(QtGui.QMainWindow, rozhrani.Ui_Dialog, Zacni, get_gamma_data.Data):
  
        
    def initUI(self):
        print('468')
        
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
        
        
        if len(self.soubory)<1:
            self.textBrowser.setText('Nebyly nalezeny žádné soubory .FRK ani .CNF')
        else:
            self.A()
            
            # pool = Pool(processes=len(self.inputs))
            # pool.map(self.Multi, self.inputs)
            # self.Multi()

class Selfish():
    def __init__(self):
        super(self.__class__, self).__init__()
        print(self)
        app = QtGui.QApplication(sys.argv)  
        form = FortyFour() #.initUI            
        form.show()
        app.exec_()


def main():
    Selfish()


if __name__ == '__main__':              
    main()   
