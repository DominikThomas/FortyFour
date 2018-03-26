#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
import matplotlib
matplotlib.use("Qt4Agg", force=True) #Nutno #Qt5Agg způsobuje neplynulost při procházení grafů
import numpy as np, os, glob, sys, matplotlib.pyplot

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
        Dialog.resize(625, 295)
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(300, 150, 131, 22))
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
        self.line.setGeometry(QtCore.QRect(280, 40, 20, 131))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(20, 190, 581, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(10, 110, 151, 31))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.checkBox_2 = QtGui.QCheckBox(Dialog)
        self.checkBox_2.setGeometry(QtCore.QRect(440, 150, 171, 22))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.textBrowser = QtGui.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 230, 381, 51))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(420, 240, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(17, 150, 251, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.Forty_Three)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Prochazet)
        self.slozka = None

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Forty Three", None))
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
        self.textBrowser.setText('Vyberte prosím složku se soubory FRK')
       
    def Prochazet(self):
        self.slozka = QtGui.QFileDialog.getExistingDirectory()
        self.textBrowser.setText('Byla vybrána složka %s' %(self.slozka))
        
    def Forty_Three(self):

        ## Vstupní konstanty
        
        #sirka=1 #*** A kdyby se to celé vypočetlo pro sirka=4 nebo 5 (5 raději ne, dělá to tam bordel...), bylo by pozadí ještě hladší :)
        vyhlazeni=self.checkBox_2.checkState() #zda vyhlazovat samotné spektrum
        vaha=50 #váha prostřední hodnoty při vyhlazování spektra
        ampl=-10000 #diskriminace dle plochy píku bez pozadí, píky s plochou menší než 'ampl' nebudou vypsány ve výstupním souboru 
        grafy=self.checkBox.checkState()
        sirka=int(self.lineEdit.text())
        cykl=int(self.lineEdit_2.text())
        config0=[self.lineEdit_3.text(),self.lineEdit_5.text()]
        config1=[self.lineEdit_4.text(),self.lineEdit_6.text()]
        if self.slozka:
            path0=str(self.slozka)
        else:
            self.textBrowser.setText('Vyberte prosím složku se soubory FRK')
            return
        
        self.textBrowser.setText('Zpracovávám následující soubory:')
        
        ## Nastavení energetické kalibrace
        newconfig0=float(config0[1])-float(config0[0])*(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
        newconfig1=(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
        
        ## Načtení a zpracování souborů FRK ze spektrometru Deimos32
        
        os.chdir(path0)
        soubor=glob.glob(path0 + '/*.FRK')
        if (len(soubor)<1):
            self.textBrowser.setText('Nebyly nalezeny žádné soubory .FRK')
            return
        plot_jmeno=[0]*len(soubor)
        plot_spektrum=[0]*len(soubor)
        plot_pozadi=[0]*len(soubor)
        self.textBrowser.setText('Zpracovávám následující soubory: \n ')
        for i1 in range(0,len(soubor)): # 1): #
            self.textBrowser.setText('Zpracovávám následující soubory: \n %s' %soubor[i1].replace(path0 + '/', ''))
            self.progressBar.setProperty("value", i1/len(soubor)*100)
            #print (i1, soubor[i1].replace(path0 + '/', ''))
            Y0=[0]*8192
            f1=open(soubor[i1])
            for i2 in range(0, len(Y0)):
                Y0[i2]=float(''.join(f1.readline().split()))
            Y=[0]*8192 #spektrum
            if(vyhlazeni==2):
                for i3 in range(1, len(Y0)-1):
                    Y[i3]=(Y0[i3-1]+vaha*Y0[i3]+Y0[i3+1])/(2+vaha)
                del(i3)
            elif(vyhlazeni==0):
                Y=Y0
            else:
                print("Chyba parametru 'vyhlazeni'.")
                break
            C2=[0]*8192 #energie
            C=[0]*8192 #kanál
            Z=[0]*8192 #derivace spektra
            C[0]=1
            C2[0]=newconfig0+newconfig1
            for i4 in range(1, len(C2)):
                C[i4]=i4+1
                C2[i4]=newconfig0+(i4+1)*newconfig1
                Z[i4]=Y[i4]-Y[i4-1]
            G0=[] #kanál přibližného středu píku (derivace mění znaménko)
            G1=[] #energie přibližného středu píku (derivace mění znaménko)
            H0=[] #levé okraje píků
            H1=[] #pravé okraje píků
            for i5 in range(0, len(Z)-sirka):
                if(Z[i5+sirka]<0):
                    G0.append(C[i5])
                    G1.append(C2[i5])
            for i6 in range(0, len(G0)-sirka):
                if (i6==0):
                    l11=G0[i6]
                    l12=0
                l1=max(G0[i6],l12+1)
                l2=max(l1+sirka,l11)
                if (l1>len(Z) or l2>len(Z)):
                    break
                while True:
                    l1-=1
                    if(l1==0 or l1==l12-1 or Z[max(l1,1)]<-0.1):
                        break
                if l1==0:
                    l1=1
                H0.append(l1)
                if(l2<len(C2)):
                    while True:
                        l2+=1
                        if(l2==(len(C2)-1) or l2>=len(C2) or Z[l2]>0.1):
                            break
                    H1.append(l2-1)
                else:
                    H1.append(l2-2)
                l11=l1
                l12=l2
            del l1, l2, l12, l11
            H01=[H0[0]]
            H11=[H1[0]]
            for i7 in range (1, len(H0)): #odstranění duplicitních píků
                if (H0[i7-1],H1[i7-1])!=(H0[i7],H1[i7]):
                    H01.append(H0[i7])
                    H11.append(H1[i7])
            G20=[] #energie maxima píku
            G21=[] #suma píku i s pozadím
            G22=[] #levý okraj píku
            G23=[] #pravý okraj píku
            G24=[] #pozadí
            G25=[] #šířka píku v kanálech
            G26=[] #plocha píku bez pozadí
            for i8 in range (0,len(H01)):
                maximum, index = max((val, idx) for idx, val in enumerate(Y[H01[i8]:H11[i8]]))
                G20.append(C2[H01[i8]+index]) #energie maxima píku
                G21.append(sum(Y[H01[i8]:H11[i8]])) #suma píku i s pozadím
                G22.append(H01[i8]) #levý okraj píku
                G23.append(H11[i8]) #pravý okraj píku
                # # #G24.append(0) #příprava na dosazení pozadí #zde se nesmí dosazovat 0, nutno, aby zůstalo prázdné
                G25.append(len(Y[H01[i8]:H11[i8]])) #šířka píku v kanálech
            pozadi=[]
            for i9 in range (0, len(G23)):
            #if i1==7:
            #	print('Y, G23[i9]', len(Y), G23[i9])
                pozadi.append(Y[G23[i9]])  
        
        ## Vyhlazování pozadí
            
            for i10 in range (0,cykl):
                P0=[]
                P0.extend(pozadi)
                pozadi=[]
                P1=[0.0]*len(P0)
                P1[0]=P0[0]
                P1[len(P0)-1]=P0[len(P0)-1]
                for i11 in range (1,len(P0)-1):
                    P1[i11]=min(P0[i11],np.mean([P0[i11-1],P0[i11],P0[i11+1]]))
                pozadi.extend(P1) 
            
            
            PP=[0.0]*len(C2)
            for i9e in range (0,len(G23)-1):
                PP[G23[i9e]]=pozadi[i9e]
                inkrement=(pozadi[i9e+1]-pozadi[i9e])/(G23[i9e+1]-G23[i9e])
                for i9f in range (0,(G23[i9e+1]-G23[i9e])):
                    PP[G23[i9e]+i9f]=PP[G23[i9e]]+i9f*inkrement
        
            for i10 in range (0,int(cykl/4)):
                P0=[]
                P0.extend(PP)
                PP=[]
                P1=[0.0]*len(P0)
                P1[0:5]=P0[0:5]
                P1[(len(P0)-6):(len(P0)-1)]=P0[(len(P0)-6):(len(P0)-1)]
                for i11 in range (5,len(P0)-6):
                    if (i10<(cykl)):
                        P1[i11]=min(Y[i11],np.mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]]))
                    else:
                        P1[i11]=np.mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]])
                PP.extend(P1)    
            for i10a in range (0,len(G23)):
                G24.append(PP[G23[i10a]])    
            
            G26.append(G21[0]-(Y[G22[0]]/2+G24[0]/2)*G25[0])
            for i9b in range(1,len(G25)):
                G26.append(G21[i9b]-sum(PP[G22[i9b]:G23[i9b]]))
                
            for i9c in range(0,len(G26)):
                if G26[i9c]<ampl:
                    G20[i9c]=[];G21[i9c]=[];G22[i9c]=[];G23[i9c]=[];G24[i9c]=[];G25[i9c]=[];G26[i9c]=[]
            for i9d in range(0,G20.count([])):
                G20.remove([]);G21.remove([]);G22.remove([]);G23.remove([]);G24.remove([]);G25.remove([]);G26.remove([])
                
        ## Uložení spektra a pozadí
            
            plot_jmeno[i1]=soubor[i1].replace(path0 + '/' , '').replace('.FRK','')
            plot_spektrum[i1]=Y
            plot_pozadi[i1]=PP
            
        ## Načtení hodnot tlive treal a data ze souboru txt     
            
            if glob.glob(soubor[i1].replace('.FRK','.TXT'))==[]:
                Time='Soubor %s nebyl ve složce %s nalezen.' % (soubor[i1].replace('.FRK','.TXT').replace(path0 + '/','') , path0)
                Treal=''
                Tlive=''
            else:
                text=glob.glob(soubor[i1].replace('.FRK','.TXT'))
                f2=open(text[0])
                for i in range(0,7):
                    if i==6:
                        Time=f2.readline().replace('                  ','').replace('\r\n', '').replace('/','.')
                        Treal=f2.readline().replace('                   ','').replace(' sec\r\n', '')
                        Tlive=f2.readline().replace('                   ','').replace(' sec\r\n', '')
                    f2.readline()
                
        ## Zapisování dat do souboru
            
            vystup = open(soubor[i1].replace(path0 + '/', '').replace('FRK','OUTpy'),'w')
            vystup.write('Vyhodnocováno skriptem: %s \n \n' %(str(os.path.basename(__file__))))
            vystup.write('Vstupní parametry: \nFaktor šířky píku = %i \n' %(sirka))
            vystup.write('Počet iterací při vyhlazování pozadí = %i  \n' %(cykl))
            if vyhlazeni==0:
                vystup.write('Spektrum nebylo vyhlazováno. \n \n')
            else:
                vystup.write('Spektrum bylo vyhlazováno. \n \n')
            if sys.version_info.major<3:
                vystup.write('%s \n%s \n%s \n \n' %(Time, Treal, Tlive)) 
            else:
                vystup.write('%s%s%s \n' %(Time, Treal, Tlive))
            vystup.write('Energie (keV)                Plocha (-)\n')
            for i in range (0,len(G20)):
                vystup.write('%13f            %14f \n' % (G20[i], G26[i]) )
            vystup.close
            
        ## Vykreslování grafů spekter a pozadí 
        if (grafy==2):
            self.textBrowser.setText('Hotovo! Zobrazuji grafy.')
            for i12 in range (0,len(soubor)):
                matplotlib.pyplot.ion()
                matplotlib.pyplot.figure(i12)
                matplotlib.pyplot.title(plot_jmeno[i12])
                matplotlib.pyplot.xlabel('Energie (keV)')
                matplotlib.pyplot.ylabel('Cetnost (-)')
                matplotlib.pyplot.plot(C2, plot_spektrum[i12]) #vykreslení spektra
                matplotlib.pyplot.plot(C2, plot_pozadi[i12], 'r') #vykreslení pozadí
            self.progressBar.setProperty("value", 100)
        else:
            self.textBrowser.setText('Hotovo!')
            self.progressBar.setProperty("value", 100)
  
      
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())



