# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use("Qt5Agg", force=True) #Nutno #Qt5Agg způsobuje neplynulost při procházení grafů
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
        Gama_data={}
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
            Y0=[0]*8192 #Přidat vstupní proměnnou, za kterou bude možné doplnit počet kanálů
            f1=open(soubor[i1])
            for i2 in range(0, len(Y0)):
                Y0[i2]=float(''.join(f1.readline().split()))
            spektrum={}
            spektrum['cetnost']=[]
            # Y=[0]*8192 == spektrum['cetnost']
            if(vyhlazeni==2):
                for i3 in range(1, len(Y0)-1):
                    spektrum['cetnost'].append(0)
                    spektrum['cetnost'][i3]=(Y0[i3-1]+vaha*Y0[i3]+Y0[i3+1])/(2+vaha)
                    spektrum['cetnost'].append(0)
                del(i3)
            elif(vyhlazeni==0):
                spektrum['cetnost']=Y0
            else:
                print(u"Chyba parametru 'vyhlazeni'.")
                break
            spektrum['kanal']=[1] #C=[0]*8192 #kanál
            spektrum['energie']=[newconfig0+newconfig1] #C2=[0]*8192 #energie
            spektrum['derivace']=[0] #Z=[0]*8192 #derivace spektra
            for i4 in range(1, 8192):
                spektrum['kanal'].append(i4+1)
                spektrum['energie'].append(newconfig0+(i4+1)*newconfig1)
                spektrum['derivace'].append(spektrum['cetnost'][i4]-spektrum['cetnost'][i4-1])
            piky0={}
            piky0['kanal']=[] #G0=[] #kanál přibližného středu píku (derivace mění znaménko)
            piky0['energie']=[] #G1=[] #energie přibližného středu píku (derivace mění znaménko)
            piky0['levy']=[] #H0=[] #levé okraje píků
            piky0['pravy']=[] #H1=[] #pravé okraje píků
            for i5 in range(0, len(spektrum['derivace'])-sirka):
                if(spektrum['derivace'][i5+sirka]<0):
                    piky0['kanal'].append(spektrum['kanal'][i5])
                    piky0['energie'].append(spektrum['energie'][i5])
            for i6 in range(0, len(piky0['kanal'])-sirka):
                if (i6==0):
                    l11=piky0['kanal'][i6]
                    l12=0
                l1=max(piky0['kanal'][i6],l12+1)
                l2=max(l1+sirka,l11)
                if (l1>len(spektrum['derivace']) or l2>len(spektrum['derivace'])):
                    break
                while True:
                    l1-=1
                    if(l1==0 or l1==l12-1 or spektrum['derivace'][max(l1,1)]<-0.1):
                        break
                if l1==0:
                    l1=1
                piky0['levy'].append(l1)
                if(l2<len(spektrum['energie'])):
                    while True:
                        l2+=1
                        if(l2==(len(spektrum['energie'])-1) or l2>=len(spektrum['energie']) or spektrum['derivace'][l2]>0.1):
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
                maximum, index = max((val, idx) for idx, val in enumerate(spektrum['cetnost'][piky1['levy'][i8]:piky1['pravy'][i8]]))
                piky['energie'].append(spektrum['energie'][piky1['levy'][i8]+index]) #energie maxima píku
                piky['suma'].append(sum(spektrum['cetnost'][piky1['levy'][i8]:piky1['pravy'][i8]])) #suma píku i s pozadím
                piky['levy'].append(piky1['levy'][i8]) #levý okraj píku
                piky['pravy'].append(piky1['pravy'][i8]) #pravý okraj píku
                piky['sirka'].append(len(spektrum['cetnost'][piky1['levy'][i8]:piky1['pravy'][i8]])) #šířka píku v kanálech
            pozadi=[]
            for i9 in range (0, len(piky['pravy'])):
                pozadi.append(spektrum['cetnost'][piky['pravy'][i9]])  
        
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
            
            PP=[0.0]*len(spektrum['energie'])
            for i9e in range (0,len(piky['pravy'])-1):
                QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
                PP[piky['pravy'][i9e]]=pozadi[i9e]
                inkrement=(pozadi[i9e+1]-pozadi[i9e])/(piky['pravy'][i9e+1]-piky['pravy'][i9e])
                for i9f in range (0,(piky['pravy'][i9e+1]-piky['pravy'][i9e])):
                    PP[piky['pravy'][i9e]+i9f]=PP[piky['pravy'][i9e]]+i9f*inkrement
        
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
            for i10a in range (0,len(piky['pravy'])):
                piky['pozadi'].append(PP[piky['pravy'][i10a]])    
            
            piky['plocha'].append(piky['suma'][0]-(spektrum['cetnost'][piky['levy'][0]]/2+piky['pozadi'][0]/2)*piky['sirka'][0])
            for i9b in range(1,len(piky['sirka'])):
                piky['plocha'].append(piky['suma'][i9b]-sum(PP[piky['levy'][i9b]:piky['pravy'][i9b]]))
                
            for i9c in range(0,len(piky['plocha'])):
                if piky['plocha'][i9c]<ampl:
                    piky['energie'][i9c]=[];piky['suma'][i9c]=[];piky['levy'][i9c]=[];piky['pravy'][i9c]=[];piky['pozadi'][i9c]=[];piky['sirka'][i9c]=[];piky['plocha'][i9c]=[]
            for i9d in range(0,piky['energie'].count([])):
                piky['energie'].remove([]);piky['suma'].remove([]);piky['levy'].remove([]);piky['pravy'].remove([]);piky['pozadi'].remove([]);piky['sirka'].remove([]);piky['plocha'].remove([])
                
        ## Uložení spektra a pozadí
            
            if system()=='Windows':
                plot_jmeno[i1]=os.path.basename(soubor[i1]).replace('.FRK','')
            else:
                plot_jmeno[i1]=soubor[i1].replace(path0 + '/' , '').replace('.FRK','')
            plot_spektrum[i1]=spektrum['cetnost']
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
                    
        ## Určení prvku a odhadnutí produkční reakce pro jednotlivé píky
        
            if system()=='Windows': prvek0 = os.path.basename(soubor[i1]).replace('.FRK','')
            else: prvek0 = (soubor[i1].replace(path0 + '/', '').replace('.FRK',''))
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
            if prvek1 in Gama_data.keys(): # Data o gama linkách z internetu jsou ukládány do dictionary Gama_data a není tedy potřeba je stahovat pro každý isotop zvlášť.
                GAMA=Gama_data[prvek1]
            else:
                GAMA=self.get_gamma(prvek1)
                Gama_data[prvek1]=GAMA
            
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
            vystup.write('Energie (keV)                Plocha (-)                Reakce                   Intenzita(%)                 Isotop                    Poločas (s)\n')
            for i in range (0,len(piky['energie'])):
                try:
                    vystup.write('%13f            %14f     %17s            %17.4f            %14s            %14s \n' % (piky['energie'][i], piky['plocha'][i], piky['reakce'][i], float(piky['intensita'][i]), piky['isotop'][i], str(piky['polocas'][i])) )
                except ValueError:
                    vystup.write('%13f            %14f     %17s            %17s            %14s            %14s \n' % (piky['energie'][i], piky['plocha'][i], piky['reakce'][i], piky['intensita'][i], piky['isotop'][i], str(piky['polocas'][i])) )
            vystup.close
            os.chdir(path0)
            QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
            # print(len(spektrum['kanal']),len(spektrum['energie']),len(spektrum['derivace']),len(piky0),len(piky1))
            # breakfast=input()
            
        ## Vykreslování grafů spekter a pozadí 
        
        if (grafy==2):
            self.textBrowser.setText(u'Hotovo! Zobrazuji grafy.')
            for i12 in range (0,len(soubor)):
                plt.ion()
                plt.figure(plot_jmeno[i12])
                plt.title(plot_jmeno[i12])
                plt.xlabel(u'Energie (keV)')
                plt.ylabel(u'Četnost (-)')
                plt.plot(spektrum['energie'], plot_spektrum[i12]) #vykreslení spektra
                plt.plot(spektrum['energie'], plot_pozadi[i12], 'r') #vykreslení pozadí
            self.progressBar.setProperty("value", 100)
        else:
            self.textBrowser.setText(u'Hotovo!')
            self.progressBar.setProperty("value", 100)
        print(time.time()-t)