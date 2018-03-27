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

import matplotlib
matplotlib.use("Qt5Agg", force=True) #Nutno #Qt5Agg způsobuje neplynulost při procházení grafů
import time
import os, sys, matplotlib.pyplot as plt
from PyQt4 import QtCore, QtGui
from numpy import mean
from glob import glob
from platform import system

from joblib import Parallel, delayed
from multiprocessing import cpu_count, freeze_support
# from multiprocessing import Pool, cpu_count


import rozhrani, nastaveni, get_gamma_data

def Multi(self,i1):
    

    if system()=='Windows':
        self.textBrowser.append(u'%s' %os.path.basename(self.soubor[i1]))
    else:
        self.textBrowser.append(u'%s' %self.soubor[i1].replace(self.path0 + '/', ''))
    self.progressBar.setProperty("value", i1/len(self.soubor)*100)
    #print (i1, self.soubor[i1].replace(self.path0 + '/', ''))
    Y0=[0]*8192 #Přidat vstupní proměnnou, za kterou bude možné doplnit počet kanálů
    f1=open(self.soubor[i1])
    for i2 in range(0, len(Y0)):
        Y0[i2]=float(''.join(f1.readline().split()))
    self.spektrum={}
    self.spektrum['cetnost']=[]
    # Y=[0]*8192 == self.spektrum['cetnost']
    if(self.vyhlazeni==2):
        self.spektrum['cetnost']=[0]*len(Y0)
        for i3 in range(1, len(Y0)-1):
            # self.spektrum['cetnost'].append(0)
            self.spektrum['cetnost'][i3]=(Y0[i3-1]+vaha*Y0[i3]+Y0[i3+1])/(2+vaha)
            # self.spektrum['cetnost'].append(0)
        del(i3)
    elif(self.vyhlazeni==0):
        self.spektrum['cetnost']=Y0
    else:
        print(u"Chyba parametru 'vyhlazeni'.")
        # break
    self.spektrum['kanal']=[1] #C=[0]*8192 #kanál
    self.spektrum['energie']=[self.newconfig0+self.newconfig1] #C2=[0]*8192 #energie
    self.spektrum['derivace']=[0] #Z=[0]*8192 #derivace spektra
    for i4 in range(1, 8192):
        self.spektrum['kanal'].append(i4+1)
        self.spektrum['energie'].append(self.newconfig0+(i4+1)*self.newconfig1)
        self.spektrum['derivace'].append(self.spektrum['cetnost'][i4]-self.spektrum['cetnost'][i4-1])
    piky0={}
    piky0['kanal']=[] #G0=[] #kanál přibližného středu píku (derivace mění znaménko)
    piky0['energie']=[] #G1=[] #energie přibližného středu píku (derivace mění znaménko)
    piky0['levy']=[] #H0=[] #levé okraje píků
    piky0['pravy']=[] #H1=[] #pravé okraje píků
    for i5 in range(0, len(self.spektrum['derivace'])-self.sirka):
        if(self.spektrum['derivace'][i5+self.sirka]<0):
            piky0['kanal'].append(self.spektrum['kanal'][i5])
            piky0['energie'].append(self.spektrum['energie'][i5])
    for i6 in range(0, len(piky0['kanal'])-self.sirka):
        if (i6==0):
            l11=piky0['kanal'][i6]
            l12=0
        l1=max(piky0['kanal'][i6],l12+1)
        l2=max(l1+self.sirka,l11)
        if (l1>len(self.spektrum['derivace']) or l2>len(self.spektrum['derivace'])):
            break
        while True:
            l1-=1
            if(l1==0 or l1==l12-1 or self.spektrum['derivace'][max(l1,1)]<-0.1):
                break
        if l1==0:
            l1=1
        piky0['levy'].append(l1)
        if(l2<len(self.spektrum['energie'])):
            while True:
                l2+=1
                if(l2==(len(self.spektrum['energie'])-1) or l2>=len(self.spektrum['energie']) or self.spektrum['derivace'][l2]>0.1):
                    break
            piky0['pravy'].append(l2-1)
        else:
            piky0['pravy'].append(l2-2)
        l11=l1
        l12=l2
    # del l1, l2, l12, l11
    piky1={}
    piky1['levy']=[piky0['levy'][0]] #H01
    piky1['pravy']=[piky0['pravy'][0]] #H11
    for i7 in range (1, len(piky0['levy'])): #odstranění duplicitních píků
        if (piky0['levy'][i7-1],piky0['pravy'][i7-1])!=(piky0['levy'][i7],piky0['pravy'][i7]):
            piky1['levy'].append(piky0['levy'][i7])
            piky1['pravy'].append(piky0['pravy'][i7])
    piky={}
    piky['energie']=[] # G20=[] #energie maxima píku
    piky['suma']=[] #G21=[] #suma píku i s pozadím
    piky['levy']=[] #G22=[] #levý okraj píku
    piky['pravy']=[] #G23=[] #pravý okraj píku
    piky['pozadi']=[] #G24=[] #pozadí
    piky['sirka']=[] #G25=[] #šířka píku v kanálech
    piky['plocha']=[] #G26=[] #plocha píku bez pozadí
    for i8 in range (0,len(piky1['levy'])):
        maximum, index = max((val, idx) for idx, val in enumerate(self.spektrum['cetnost'][piky1['levy'][i8]:piky1['pravy'][i8]]))
        piky['energie'].append(self.spektrum['energie'][piky1['levy'][i8]+index]) #energie maxima píku
        piky['suma'].append(sum(self.spektrum['cetnost'][piky1['levy'][i8]:piky1['pravy'][i8]])) #suma píku i s pozadím
        piky['levy'].append(piky1['levy'][i8]) #levý okraj píku
        piky['pravy'].append(piky1['pravy'][i8]) #pravý okraj píku
        piky['sirka'].append(len(self.spektrum['cetnost'][piky1['levy'][i8]:piky1['pravy'][i8]])) #šířka píku v kanálech
    pozadi=[]
    for i9 in range (0, len(piky['pravy'])):
        pozadi.append(self.spektrum['cetnost'][piky['pravy'][i9]])  

## Vyhlazování pozadí

    if self.typ_pozadi==3:
        for i10 in range (0,self.cykl):
            QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
            P0=[]
            P0.extend(pozadi)
            pozadi=[]
            P1=[0.0]*len(P0)
            P1[0]=P0[0]
            P1[len(P0)-1]=P0[len(P0)-1]
            for i11 in range (1,len(P0)-1):
                P1[i11]=mean([P0[i11-1],P0[i11],P0[i11+1]])
            pozadi.extend(P1) 
    else:
        for i10 in range (0,self.cykl):
            QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
            P0=[]
            P0.extend(pozadi)
            pozadi=[]
            P1=[0.0]*len(P0)
            P1[0]=P0[0]
            P1[len(P0)-1]=P0[len(P0)-1]
            for i11 in range (1,len(P0)-1):
                P1[i11]=min(P0[i11],mean([P0[i11-1],P0[i11],P0[i11+1]]))
            pozadi.extend(P1) 
    
    PP=[0.0]*len(self.spektrum['energie'])
    for i9e in range (0,len(piky['pravy'])-1):
        QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
        PP[piky['pravy'][i9e]]=pozadi[i9e]
        inkrement=(pozadi[i9e+1]-pozadi[i9e])/(piky['pravy'][i9e+1]-piky['pravy'][i9e])
        for i9f in range (0,(piky['pravy'][i9e+1]-piky['pravy'][i9e])):
            PP[piky['pravy'][i9e]+i9f]=PP[piky['pravy'][i9e]]+i9f*inkrement

    for i10 in range (0,int(self.cykl/4)):
        QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
        P0=[]
        P0.extend(PP)
        PP=[]
        P1=[0.0]*len(P0)
        P1[0:5]=P0[0:5]
        P1[(len(P0)-6):(len(P0)-1)]=P0[(len(P0)-6):(len(P0)-1)]
        if self.typ_pozadi==1:
            for i11 in range (5,len(P0)-6):
                if (i10<(self.cykl)):
                    P1[i11]=min(Y0[i11],mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]]))
                else:
                    P1[i11]=mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]])
        elif self.typ_pozadi==2 or self.typ_pozadi==3:
            for i11 in range (5,len(P0)-6):
                P1[i11]=mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]])
        else:
            self.textBrowser.setText('Chyba načtení typu pozadí.')
        PP.extend(P1)    
    for i10a in range (0,len(piky['pravy'])):
        piky['pozadi'].append(PP[piky['pravy'][i10a]])    
    
    piky['plocha'].append(piky['suma'][0]-(self.spektrum['cetnost'][piky['levy'][0]]/2+piky['pozadi'][0]/2)*piky['sirka'][0])
    for i9b in range(1,len(piky['sirka'])):
        piky['plocha'].append(piky['suma'][i9b]-sum(PP[piky['levy'][i9b]:piky['pravy'][i9b]]))
        
    for i9c in range(0,len(piky['plocha'])):
        if piky['plocha'][i9c]<self.ampl:
            piky['energie'][i9c]=[];piky['suma'][i9c]=[];piky['levy'][i9c]=[];piky['pravy'][i9c]=[];piky['pozadi'][i9c]=[];piky['sirka'][i9c]=[];piky['plocha'][i9c]=[]
    for i9d in range(0,piky['energie'].count([])):
        piky['energie'].remove([]);piky['suma'].remove([]);piky['levy'].remove([]);piky['pravy'].remove([]);piky['pozadi'].remove([]);piky['sirka'].remove([]);piky['plocha'].remove([])
        
## Uložení spektra a pozadí
    
    if system()=='Windows':
        self.plot_jmeno[i1]=os.path.basename(self.soubor[i1]).replace('.FRK','')
    else:
        self.plot_jmeno[i1]=self.soubor[i1].replace(self.path0 + '/' , '').replace('.FRK','')
    self.plot_spektrum[i1]=self.spektrum['cetnost']
    self.plot_pozadi[i1]=PP
    
## Načtení hodnot tlive treal a data ze souboru txt     
    
    if glob(self.soubor[i1].replace('.FRK','.TXT'))==[]:
        Time='Soubor %s nebyl ve složce %s nalezen.' % (self.soubor[i1].replace('.FRK','.TXT').replace(self.path0 + '/','') , self.path0)
        Treal=''
        Tlive=''
    else:
        text=glob(self.soubor[i1].replace('.FRK','.TXT'))
        f2=open(text[0])
        for i in range(0,7):
            if i==6:
                Time=f2.readline().replace('                  ','').replace('\r\n', '').replace('/','.')
                Treal=f2.readline().replace('                   ','').replace(' sec\r\n', '')
                Tlive=f2.readline().replace('                   ','').replace(' sec\r\n', '')
            f2.readline()
            
## Určení prvku a odhadnutí produkční reakce pro jednotlivé píky

    if system()=='Windows': prvek0 = os.path.basename(self.soubor[i1]).replace('.FRK','')
    else: prvek0 = (self.soubor[i1].replace(self.path0 + '/', '').replace('.FRK',''))
    prvek1 = ''.join([i for i in prvek0 if not i.isdigit()])           
    if prvek1[len(prvek1)-1]==('P' or 'p'): #Starý způsob
        prvek1=prvek1[0:len(prvek1)-1]
        
    if 'Pkopie' in prvek1: #Nový způsob
        prvek1=prvek1.replace('Pkopie','')
    
    piky['reakce']=['  -  ']*len(piky['energie']) #reakce G30
    piky['intensita']=['   -   ']*len(piky['energie']) #intensita G33
    piky['isotop']=['   -   ']*len(piky['energie']) #isotop G31
    piky['polocas']=[' - ']*len(piky['energie']) #poločas G32
    
    n=0
    # print(type(prvek1))
    
    GAMA=[]
    
    # if prvek1 in self.Gama_data.keys(): # Data o gama linkách z internetu jsou ukládány do dictionary self.Gama_data a není tedy potřeba je stahovat pro každý isotop zvlášť.
    #     GAMA=self.Gama_data[prvek1]
    # else:
    #     GAMA=self.get_gamma(prvek1)
    #     self.Gama_data[prvek1]=GAMA
    
    if len(GAMA)>1:
        n3=3
        for n1 in range (0, len(piky['energie'])):
            for n2 in range (n3,len(GAMA)):
                if ((float(GAMA[n2][9])-1) <= piky['energie'][n1] <= (float(GAMA[n2][9])+1)):
                    piky['reakce'][n1]=GAMA[n2][1].replace('>',',')
                    if len(GAMA[n2])>11:
                        piky['intensita'][n1]=GAMA[n2][11]
                    piky['isotop'][n1]=GAMA[n2][3]
                    piky['polocas'][n1]=float(GAMA[n2][5])
                    n3=max(3,n2-5)
                    break
        
## Zapisování dat do souboru
    
    os.chdir('out')
    if system()=='Windows': vystup = open(self.soubor[i1].replace(os.path.basename(self.soubor[i1]), 'out\\' + os.path.basename(self.soubor[i1])).replace('FRK','OUTpy'),'w')
    else: vystup = open(self.soubor[i1].replace(self.path0 + '/', '').replace('FRK','OUTpy'),'w')
    vystup.write(u'Vyhodnocováno skriptem: %s \n \n' %(str(os.path.basename(__file__))))
    vystup.write(u'Vstupní parametry: \nFaktor šířky píku = %i \n' %(self.sirka))
    vystup.write(u'Pocet iterací při vyhlazování pozadí = %i  \n' %(self.cykl))
    vystup.write(u'Byl použit %i. typ vyhlazování pozadí. \n' %(self.typ_pozadi))
    if self.vyhlazeni==0:
        vystup.write(u'Spektrum nebylo vyhlazováno. \n \n')
    else:
        vystup.write(u'Spektrum bylo vyhlazováno. \n \n')
    if sys.version_info.major<3:
        vystup.write('%s \n%s \n%s \n \n' %(Time, Treal, Tlive)) 
    else:
        vystup.write('%s%s%s \n' %(Time, Treal, Tlive))
    vystup.write('Energie (keV)                Plocha (-)                Reakce                   Intenzita(%)                 Isotop                    Poločas (s)\n')
    for i in range (0,len(piky['energie'])):
        try:
            vystup.write('%13f            %14f     %17s            %17.4f            %14s            %14s \n' % (piky['energie'][i], piky['plocha'][i], piky['reakce'][i], float(piky['intensita'][i]), piky['isotop'][i], str(piky['polocas'][i])) )
        except ValueError:
            vystup.write('%13f            %14f     %17s            %17s            %14s            %14s \n' % (piky['energie'][i], piky['plocha'][i], piky['reakce'][i], piky['intensita'][i], piky['isotop'][i], str(piky['polocas'][i])) )
    vystup.close
    os.chdir(self.path0)
    QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
    # print(len(self.spektrum['kanal']),len(self.spektrum['energie']),len(self.spektrum['derivace']),len(piky0),len(piky1))
    # breakfast=input()
        
        
    
def Forty_Three(self):
    
    t = time.time()
    try:
        self.Gama_data
    except AttributeError:
        self.Gama_data={}
    ## Vstupní konstanty
    
    self.vyhlazeni=self.checkBox_2.checkState() #zda vyhlazovat samotné spektrum
    vaha=self.vaha1 #váha prostřední hodnoty při vyhlazování spektra
    self.ampl=self.ampl1 #diskriminace dle plochy píku bez pozadí, píky s plochou menší než 'ampl' nebudou vypsány ve výstupním souboru 
    grafy=self.checkBox.checkState()
    self.typ_pozadi=self.spinBox.value()
    self.sirka=int(self.lineEdit.text())
    self.cykl=int(self.lineEdit_2.text())
    config0=[self.lineEdit_3.text(),self.lineEdit_5.text()]
    config1=[self.lineEdit_4.text(),self.lineEdit_6.text()]
    if self.slozka:
        self.path0=str(self.slozka)
    else:
        self.textBrowser.setText(u'Vyberte prosím složku se soubory FRK')
        return
    
    # self.textBrowser.append(u'Zpracovávám následující soubory:')
    
    ## Nastavení energetické kalibrace
    
    self.newconfig0=float(config0[1])-float(config0[0])*(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
    self.newconfig1=(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
    
    ## Načtení a zpracování souborů FRK ze spektrometru Deimos32
    
    os.chdir(self.path0)
    if not os.path.exists('out'):
        os.makedirs('out')
    self.soubor=glob(self.path0 + '/*.FRK')
    if (len(self.soubor)<1):
        self.textBrowser.setText(u'Nebyly nalezeny žádné soubory .FRK')
        return
    self.plot_jmeno=[0]*len(self.soubor)
    self.plot_spektrum=[0]*len(self.soubor)
    self.plot_pozadi=[0]*len(self.soubor)
    self.textBrowser.append(u'Zpracovávám následující soubory:')
    
    
    print(len(self.soubor),cpu_count())
    Parallel(n_jobs=2)(delayed(Multi)(self,i1) for i1 in range(0,len(self.soubor)))
    
        
    ## Vykreslování grafů spekter a pozadí 
    
    if (grafy==2):
        self.textBrowser.append(u'Hotovo! Zobrazuji grafy.')
        for i12 in range (0,len(self.soubor)):
            plt.ion()
            plt.figure(self.plot_jmeno[i12])
            plt.title(self.plot_jmeno[i12])
            plt.xlabel(u'Energie (keV)')
            plt.ylabel(u'Četnost (-)')
            plt.plot(self.spektrum['energie'], self.plot_spektrum[i12], label=u'Spektrum') #vykreslení spektra
            plt.plot(self.spektrum['energie'], self.plot_pozadi[i12], 'r', label=u'Pozadí') #vykreslení pozadí
            plt.legend()
        self.progressBar.setProperty("value", 100)
    else:
        self.textBrowser.append(u'Hotovo!')
        self.progressBar.setProperty("value", 100)
    print(time.time()-t)

class FortyFour(QtGui.QMainWindow, rozhrani.Ui_Dialog, get_gamma_data.Data):
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
        if self.slozka != '': self.textBrowser.append('Byla vybrána složka %s' %(self.slozka))
        
    def konfigurace(self):
        self.cfgname = QtGui.QFileDialog.getOpenFileName(None,(u"Vyberte konfigurační soubor cfg"),"./",("Konfigurační soubory (*.CFG *.Cfg *.cfg)"))
        if self.cfgname != '': self.textBrowser.append('Byl vybrán konfigurační soubor %s' %(self.cfgname))
        f0=io.open(self.cfgname)
        if 'J.Frana - OJS UJF Rez' in f0.readline():
            for i0 in range(0, 20):
                if i0==11:
                    config0=(f0.readline().split())
                    config1=(f0.readline().split())
                f0.readline()
        elif 'D.Thomas - OJR UJF Rez' in f0.readline():
            config0=(f0.readline().split())
            config1=(f0.readline().split())
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
        
        Forty_Three(self)
        
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
        
# -*- coding: utf-8 -*-
        

def main():
    app = QtGui.QApplication(sys.argv)  
    form = FortyFour()                
    form.show()
    app.exec_()

if __name__ == '__main__':
    freeze_support()
    main()                           