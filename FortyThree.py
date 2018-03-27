# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use("Qt4Agg", force=True) #Nutno #Qt5Agg způsobuje neplynulost při procházení grafů
import time
import os, sys, matplotlib.pyplot as plt
from PyQt4 import QtCore, QtGui
from numpy import mean
from glob import glob
from platform import system
import rozhrani, nastaveni

class Vypocet():
   
    def Forty_Three(self):
        t = time.time()
        ## Vstupní konstanty
        
        vyhlazeni=self.checkBox_2.checkState() #zda vyhlazovat samotné spektrum
        vaha=self.vaha1 #váha prostřední hodnoty při vyhlazování spektra
        ampl=self.ampl1 #diskriminace dle plochy píku bez pozadí, píky s plochou menší než 'ampl' nebudou vypsány ve výstupním souboru 
        grafy=self.checkBox.checkState()
        typ_pozadi=self.spinBox.value()
        sirka=int(self.lineEdit.text())
        cykl=int(self.lineEdit_2.text())
        config0=[self.lineEdit_3.text(),self.lineEdit_5.text()]
        config1=[self.lineEdit_4.text(),self.lineEdit_6.text()]
        if self.slozka:
            path0=str(self.slozka)
        else:
            self.textBrowser.setText(u'Vyberte prosím složku se soubory FRK')
            return
        
        self.textBrowser.setText(u'Zpracovávám následující soubory:')
        
        ## Nastavení energetické kalibrace
        newconfig0=float(config0[1])-float(config0[0])*(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
        newconfig1=(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
        
        ## Načtení a zpracování souborů FRK ze spektrometru Deimos32
        
        os.chdir(path0)
        if not os.path.exists('out'):
            os.makedirs('out')
        soubor=glob(path0 + '/*.FRK')
        if (len(soubor)<1):
            self.textBrowser.setText(u'Nebyly nalezeny žádné soubory .FRK')
            return
        plot_jmeno=[0]*len(soubor)
        plot_spektrum=[0]*len(soubor)
        plot_pozadi=[0]*len(soubor)
        self.textBrowser.setText(u'Zpracovávám následující soubory: \n ')
        for i1 in range(0,len(soubor)): # 1): #
            if system()=='Windows':
                self.textBrowser.setText(u'Zpracovávám následující soubory: \n%s' %os.path.basename(soubor[i1]))
            else:
                self.textBrowser.setText(u'Zpracovávám následující soubory: \n%s' %soubor[i1].replace(path0 + '/', ''))
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
                print(u"Chyba parametru 'vyhlazeni'.")
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
                G25.append(len(Y[H01[i8]:H11[i8]])) #šířka píku v kanálech
            pozadi=[]
            for i9 in range (0, len(G23)):
                pozadi.append(Y[G23[i9]])  
        
        ## Vyhlazování pozadí
            if typ_pozadi==3:
                for i10 in range (0,cykl):
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
                for i10 in range (0,cykl):
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
            
            PP=[0.0]*len(C2)
            for i9e in range (0,len(G23)-1):
                QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
                PP[G23[i9e]]=pozadi[i9e]
                inkrement=(pozadi[i9e+1]-pozadi[i9e])/(G23[i9e+1]-G23[i9e])
                for i9f in range (0,(G23[i9e+1]-G23[i9e])):
                    PP[G23[i9e]+i9f]=PP[G23[i9e]]+i9f*inkrement
        
            for i10 in range (0,int(cykl/4)):
                QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
                P0=[]
                P0.extend(PP)
                PP=[]
                P1=[0.0]*len(P0)
                P1[0:5]=P0[0:5]
                P1[(len(P0)-6):(len(P0)-1)]=P0[(len(P0)-6):(len(P0)-1)]
                if typ_pozadi==1:
                    for i11 in range (5,len(P0)-6):
                        if (i10<(cykl)):
                            P1[i11]=min(Y[i11],mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]]))
                        else:
                            P1[i11]=mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]])
                elif typ_pozadi==2 or typ_pozadi==3:
                    for i11 in range (5,len(P0)-6):
                        P1[i11]=mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]])
                else:
                    self.textBrowser.setText('Chyba načtení typu pozadí.')
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
            
            if system()=='Windows':
                plot_jmeno[i1]=os.path.basename(soubor[i1]).replace('.FRK','')
            else:
                plot_jmeno[i1]=soubor[i1].replace(path0 + '/' , '').replace('.FRK','')
            plot_spektrum[i1]=Y
            plot_pozadi[i1]=PP
            
        ## Načtení hodnot tlive treal a data ze souboru txt     
            
            if glob(soubor[i1].replace('.FRK','.TXT'))==[]:
                Time='Soubor %s nebyl ve složce %s nalezen.' % (soubor[i1].replace('.FRK','.TXT').replace(path0 + '/','') , path0)
                Treal=''
                Tlive=''
            else:
                text=glob(soubor[i1].replace('.FRK','.TXT'))
                f2=open(text[0])
                for i in range(0,7):
                    if i==6:
                        Time=f2.readline().replace('                  ','').replace('\r\n', '').replace('/','.')
                        Treal=f2.readline().replace('                   ','').replace(' sec\r\n', '')
                        Tlive=f2.readline().replace('                   ','').replace(' sec\r\n', '')
                    f2.readline()
                
        ## Zapisování dat do souboru
            
            os.chdir('out')
            if system()=='Windows': vystup = open(soubor[i1].replace(os.path.basename(soubor[i1]), 'out\\' + os.path.basename(soubor[i1])).replace('FRK','OUTpy'),'w')
            else: vystup = open(soubor[i1].replace(path0 + '/', '').replace('FRK','OUTpy'),'w')
            vystup.write(u'Vyhodnocováno skriptem: %s \n \n' %(str(os.path.basename(__file__))))
            vystup.write(u'Vstupní parametry: \nFaktor šířky píku = %i \n' %(sirka))
            vystup.write(u'Pocet iterací při vyhlazování pozadí = %i  \n' %(cykl))
            vystup.write(u'Byl použit %i. typ vyhlazování pozadí. \n' %(typ_pozadi))
            if vyhlazeni==0:
                vystup.write(u'Spektrum nebylo vyhlazováno. \n \n')
            else:
                vystup.write(u'Spektrum bylo vyhlazováno. \n \n')
            if sys.version_info.major<3:
                vystup.write('%s \n%s \n%s \n \n' %(Time, Treal, Tlive)) 
            else:
                vystup.write('%s%s%s \n' %(Time, Treal, Tlive))
            vystup.write('Energie (keV)                Plocha (-)\n')
            for i in range (0,len(G20)):
                vystup.write('%13f            %14f \n' % (G20[i], G26[i]) )
            vystup.close
            os.chdir(path0)
            QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
            
        ## Vykreslování grafů spekter a pozadí 
        if (grafy==2):
            self.textBrowser.setText(u'Hotovo! Zobrazuji grafy.')
            for i12 in range (0,len(soubor)):
                plt.ion()
                plt.figure(plot_jmeno[i12])
                plt.title(plot_jmeno[i12])
                plt.xlabel(u'Energie (keV)')
                plt.ylabel(u'Četnost (-)')
                plt.plot(C2, plot_spektrum[i12]) #vykreslení spektra
                plt.plot(C2, plot_pozadi[i12], 'r') #vykreslení pozadí
            self.progressBar.setProperty("value", 100)
        else:
            self.textBrowser.setText(u'Hotovo!')
            self.progressBar.setProperty("value", 100)
        print(time.time()-t)