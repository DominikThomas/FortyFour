# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use("Qt4Agg", force=True) #Nutno #Qt5Agg způsobuje neplynulost při procházení grafů
import time
import os, sys, matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import random
from PyQt4 import QtCore, QtGui
from numpy import mean
from glob import glob
from platform import system
import rozhrani

class Grafy(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Grafy, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.button)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        
        self.i12=-1

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]
        
        self.i12+=1
        

        # create an axis
        ax = self.figure.add_subplot(111)
        plt.title('jmeno')
        
        # for i12 in range (0,len(soubor)):
            #     plt.ion()
            #     plt.figure(plot_jmeno[i12])
            #     plt.title(plot_jmeno[i12])
            #     plt.xlabel(u'Energie (keV)')
            #     plt.ylabel(u'Četnost (-)')
            #     plt.plot(spektrum['energie'], plot_spektrum[i12], label=u'Spektrum') #vykreslení spektra
            #     plt.plot(spektrum['energie'], plot_pozadi[i12], 'r', label=u'Pozadí') #vykreslení pozadí
            #     plt.legend()
        
            
        # discards the old graph
        ax.hold(False)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
        
        
        if i12==18:
            i12=-1


class Vypocet():
    
    def Vypis(self,s,i): # řetězec, připsat=0/přepsat=1
        if i==0:
            self.textBrowser.append(s)
        if i==1:
            self.textBrowser.setText(s)
            
    def Vstup_konstanty(self):
       
        vyhlazeni=self.checkBox_2.checkState() #zda vyhlazovat samotné spektrum
        vaha=self.vaha1 #váha prostřední hodnoty při vyhlazování spektra
        ampl=self.ampl1 #diskriminace dle plochy píku bez pozadí, píky s plochou menší než 'ampl' nebudou vypsány ve výstupním souboru 
        grafy=self.checkBox.checkState()
        typ_pozadi=self.spinBox.value()
        sirka=int(self.lineEdit.text())
        cykl=int(self.lineEdit_2.text())
        config0=[self.lineEdit_3.text(),self.lineEdit_5.text()]
        config1=[self.lineEdit_4.text(),self.lineEdit_6.text()]
        radit=[self.checkBox_4.checkState(),self.comboBox.currentText().lower().replace('č','c')] #zajištěno, že "klíče" jsou malým písmenem
        self.pocet_kanalu=int(self.comboBox_3.currentText())
        if self.slozka:
            path0=str(self.slozka)
        else:
            self.Vypis('Vyberte prosím složku se soubory FRK nebo CNF',1)
            return
        
        ## Nastavení energetické kalibrace
        
        newconfig=[0,0]
        newconfig[0]=float(config0[1])-float(config0[0])*(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
        newconfig[1]=(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
        
        return(vyhlazeni,vaha,ampl,grafy,typ_pozadi,sirka,cykl,radit,path0,newconfig)

    def xy_txt(self,soubor):

        f=open(soubor)
       # print(soubor)
        a=f.readline()
        while not ('column_1' in a):
            a=f.readline()
            #print(a)
            #time.sleep(1)
            if 'date and time' in a:
                b=a.split()
                date0=b[5].split('-')
                startdate = date0[2]+'.'+date0[1]+'.'+date0[0]
                starttime = b[6]
            if 'live time' in a:
                tlive=float(a.split()[4])
            if 'real time' in a:
                treal=float(a.split()[4])
        f.close()
        tdead=(treal-tlive)/treal*100

        vystup = open(soubor.replace('xy','txt'),'w')
        vystup.write(u"Start:\n")
        vystup.write(u"%s %s\n\n" %(startdate, starttime))
        vystup.write(u"Real time (s):  %5.3f\n" %treal)
        vystup.write(u"Live time (s):  %5.3f\n" %tlive)
        vystup.write(u"Dead time (%s):  %5.3f\n\n" %('%',tdead))        # aneb jak napsat procento...         
        vystup.write(u"Kalibrace:\n")
        vystup.write(u"nedefinováno")
        vystup.close()


        
    def Najdi_nacti(self,path0):
        
        os.chdir(path0)
        if not os.path.exists('out'):
            os.makedirs('out')
        soubor=glob(path0 + '/*.FRK') + glob(path0 + '/*.CNF')
        if glob(path0 + '/*.CNF') != []:
            os.system('xyconv -t canberra_cnf -m %s/*.CNF'%path0)
            for i in range(0,len(soubor)):
                if 'CNF' in soubor[i]:
                    soubor[i]=soubor[i].replace('CNF','xy')
                    self.xy_txt(soubor[i])        
        if (len(soubor)<1):
            self.Vypis('Nebyly nalezeny žádné soubory .FRK ani .CNF',1)
            return
        
        return(soubor)
        
    def Vytvor_spektrum(self,i1,soubor,path0,vyhlazeni,vaha,newconfig):
        
        chyba=0
        if system()=='Windows':
            self.Vypis('%s' %os.path.basename(soubor[i1]),0)
        else:
            self.Vypis('%s' %soubor[i1].replace(path0 + '/', ''),0)
        self.progressBar.setProperty("value", i1/len(soubor)*100)
        Y0=[0]*self.pocet_kanalu #Přidat vstupní proměnnou, za kterou bude možné doplnit počet kanálů
        f1=open(soubor[i1])

        spektrum={}

        if '.FRK' in soubor[i1]:
            for i2 in range(0, self.pocet_kanalu):
                a=f1.readline().split()
                try:
                    Y0[i2]=float(''.join(a))
                except ValueError:
                    print(a)
            spektrum['cetnost']=[]
            if(vyhlazeni==2):
                spektrum['cetnost']=[0]*self.pocet_kanalu
                for i3 in range(1, self.pocet_kanalu-1):
                    spektrum['cetnost'][i3]=(Y0[i3-1]+vaha*Y0[i3]+Y0[i3+1])/(2+vaha)
                del(i3)
            elif(vyhlazeni==0):
                spektrum['cetnost']=Y0

        elif '.xy' in soubor[i1]:
            a=f1.readline().split()
            while a != ['#', 'column_1', 'column_2']:
                a=f1.readline().split()
            spektrum['kanal']=[1] 
            spektrum['energie']=[0] 
            spektrum['cetnost']=[0] 
            spektrum['derivace']=[0] 
            for i in range (1,self.pocet_kanalu):
                a=f1.readline().split()
                spektrum['kanal'].append(i+1)
                spektrum['energie'].append(float(a[0]))
                spektrum['cetnost'].append(float(a[1]))
                spektrum['derivace'].append(spektrum['cetnost'][i]-spektrum['cetnost'][i-1])
        
        return spektrum
        
                                
                
            
    def Najdi_piky(self, spektrum,newconfig,sirka):
        if 'kanal' in spektrum.keys():
            pass
        else:
            spektrum['kanal']=[1] #C=[0]*8192 #kanál
            spektrum['energie']=[newconfig[0]+newconfig[1]] #C2=[0]*8192 #energie
            spektrum['derivace']=[0] #Z=[0]*8192 #derivace spektra
            for i4 in range(1, self.pocet_kanalu):
                spektrum['kanal'].append(i4+1)
                spektrum['energie'].append(newconfig[0]+(i4+1)*newconfig[1])
                spektrum['derivace'].append(spektrum['cetnost'][i4]-spektrum['cetnost'][i4-1])
        
        #print(spektrum)


        piky0={}
        piky0['kanal']=[] #G0=[] #kanál přibližného středu píku (derivace mění znaménko)
        piky0['energie']=[] #G1=[] #energie přibližného středu píku (derivace mění znaménko)
        piky0['levy']=[] #H0=[] #levé okraje píků
        piky0['pravy']=[] #H1=[] #pravé okraje píků
        for i5 in range(0, self.pocet_kanalu-sirka):
            if(spektrum['derivace'][i5+sirka]<0):
                piky0['kanal'].append(spektrum['kanal'][i5])
                piky0['energie'].append(spektrum['energie'][i5])
        for i6 in range(0, len(piky0['kanal'])-sirka):
            if (i6==0):
                l11=piky0['kanal'][i6]
                l12=0
            l1=max(piky0['kanal'][i6],l12+1)
            l2=max(l1+sirka,l11)
            if (l1>self.pocet_kanalu or l2>self.pocet_kanalu):
                break
            while True:
                l1-=1
                if(l1==0 or l1==l12-1 or spektrum['derivace'][max(l1,1)]<-0.1):
                    break
            if l1==0:
                l1=1
            piky0['levy'].append(l1)
            if(l2<self.pocet_kanalu):
                while True:
                    l2+=1
                    if(l2==(self.pocet_kanalu-1) or l2>=self.pocet_kanalu or spektrum['derivace'][l2]>0.1):
                        break
                piky0['pravy'].append(l2-1)
            else:
                piky0['pravy'].append(l2-2)
            l11=l1
            l12=l2

        #print(piky0)

        return piky0
        
    def Uprav_piky(self,piky0,spektrum):
        
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
        piky['vyska']=[] #nové, 3.3.2016
        for i8 in range (0,len(piky1['levy'])):
            maximum, index = max((val, idx) for idx, val in enumerate(spektrum['cetnost'][piky1['levy'][i8]:piky1['pravy'][i8]]))
            piky['energie'].append(spektrum['energie'][piky1['levy'][i8]+index]) #energie maxima píku
            piky['suma'].append(sum(spektrum['cetnost'][piky1['levy'][i8]:piky1['pravy'][i8]])) #suma píku i s pozadím
            piky['levy'].append(piky1['levy'][i8]) #levý okraj píku
            piky['pravy'].append(piky1['pravy'][i8]) #pravý okraj píku
            piky['sirka'].append(len(spektrum['cetnost'][piky1['levy'][i8]:piky1['pravy'][i8]])) #šířka píku v kanálech
            piky['vyska'].append(maximum - spektrum['cetnost'][piky['levy'][i8]] - (spektrum['cetnost'][piky['pravy'][i8]]-spektrum['cetnost'][piky['levy'][i8]])/piky['sirka'][i8]*index ) #výška píku s odečteným pozadím
            
        pozadi=[]
        for i9 in range (0, len(piky['pravy'])):
            pozadi.append(spektrum['cetnost'][piky['pravy'][i9]])
            
        return(piky, pozadi)
        
    def Vyhlad_pozadi(self,typ_pozadi,piky,pozadi,spektrum,cykl,ampl):
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
        
        elif typ_pozadi==4:
            kraje_cet = []
            kraje_cet.extend(pozadi)
            
            kraje_der = [0]
            
            for i in range (1, len(kraje_cet)):
                kraje_der.append(kraje_cet[i]-kraje_cet[i-1])
                
            
            
            pozadi = [0] * len(kraje_cet)
            
            i=1
            
            while i < len(kraje_cet)-2:
                if abs(kraje_der[i]) < 10:
                    
                    pozadi[i] = kraje_cet[i]
                    i+=1
                    
                else:
                    
                    pozadi[i] = kraje_cet[i]
                    pozadi[i+1] = min(kraje_cet[i+1],mean([pozadi[i],kraje_cet[i+4]]))
                    pozadi[i+2] = min(kraje_cet[i+2],mean([pozadi[i+1],kraje_cet[i+5]]))
                    
                    i+=3
                    
            ##
                
            pozadi_vyhlazeno = [0] * len(kraje_cet)
            pozadi_vyhlazeno[0] = kraje_cet[0]
            pozadi_vyhlazeno[len(kraje_cet)-1] = kraje_cet[len(kraje_cet)-1]
            
            cykl = 2
            
            pozadi0 = pozadi
            
            for j in range(cykl):
                for i in range (1, len(pozadi0)-1):
                    pozadi_vyhlazeno[i] = mean([pozadi0[i-1],pozadi0[i],pozadi0[i+1]])
                pozadi0 = pozadi_vyhlazeno
                
            pozadi = pozadi0
        
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
            
        PP=[0.0]*self.pocet_kanalu
        
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
            
            print(P0==PP)
            
            PP=[]
            P1=[0.0]*self.pocet_kanalu
            P1[0:5]=P0[0:5]
            P1[(self.pocet_kanalu-6):(self.pocet_kanalu-1)]=P0[(self.pocet_kanalu-6):(self.pocet_kanalu-1)]
            if typ_pozadi==1:
                for i11 in range (5,self.pocet_kanalu-6):
                    if (i10<(cykl)):
                        P1[i11]=min(Y0[i11],mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]]))
                    else:
                        P1[i11]=mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]])
            elif typ_pozadi==2 or typ_pozadi==3:
                for i11 in range (5,self.pocet_kanalu-6):
                    P1[i11]=mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]])
            elif typ_pozadi == 4:
                P1 = P0
                
            else:
                self.Vypis('Chyba načtení typu pozadí.',1)
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
            
        return(piky,PP)

    def Forty_Three(self):
        t = time.time()
        try:
            self.Gama_data
        except AttributeError:
            self.Gama_data={}
        
        ## Vstupní konstanty
 
        vyhlazeni,vaha,ampl,grafy,typ_pozadi,sirka,cykl,radit,path0,newconfig = self.Vstup_konstanty()
        
        ## Načtení a zpracování souborů FRK ze spektrometru Deimos32
        
        soubor=self.Najdi_nacti(path0)
        
        plot_jmeno=[0]*len(soubor)
        plot_spektrum=[0]*len(soubor)
        plot_pozadi=[0]*len(soubor)
        self.Vypis('Zpracovávám následující soubory:',1)
        
        for i1 in range(0,len(soubor)): # 1): #
            
            spektrum = self.Vytvor_spektrum(i1,soubor,path0,vyhlazeni,vaha,newconfig)
            
            piky0 = self.Najdi_piky(spektrum,newconfig,sirka)
            
            piky, pozadi = self.Uprav_piky(piky0,spektrum)
            
            piky, PP = self.Vyhlad_pozadi(typ_pozadi,piky,pozadi,spektrum,cykl,ampl)
        
                
        ## Uložení spektra a pozadí
            
            if system()=='Windows':
                plot_jmeno[i1]=os.path.basename(soubor[i1]).replace('.FRK','').replace('.xy','')
            else:
                plot_jmeno[i1]=soubor[i1].replace(path0 + '/' , '').replace('.FRK','').replace('.xy','')
            plot_spektrum[i1]=spektrum['cetnost']
            plot_pozadi[i1]=PP
            
        ## Načtení hodnot tlive treal a data ze souboru txt     
            
            if glob(soubor[i1].replace('.FRK','.TXT').replace('.xy','.TXT'))==[] and glob(soubor[i1].replace('.FRK','.txt').replace('.xy','.txt'))==[]:
                Time='Soubor %s nebyl ve složce %s nalezen.' % (soubor[i1].replace('.FRK','.TXT').replace('.xy','.TXT').replace(path0 + '/','') , path0)
                Treal=''
                Tlive=''
            else:
                if glob(soubor[i1].replace('.FRK','.TXT').replace('.xy','.TXT'))==[]:
                    text=glob(soubor[i1].replace('.FRK','.txt').replace('.xy','.txt'))
                    f2=open(text[0])
                    a = f2.readline()
                    while not 'Kalibrace' in a:
                        if 'Start' in a:
                            Time = 'Start date: ' + f2.readline() #skutečně chci načíst další řádek!
                        if 'Real' in a:
                            Treal = 'Real time: ' + a.split()[3] + ' sec\n'
                        if 'Live' in a:       
                            Tlive = 'Live time: ' + a.split()[3] + ' sec\n'
                        a = f2.readline()             
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
        
            if system()=='Windows': prvek0 = os.path.basename(soubor[i1]).replace('.FRK','').replace('.xy','')
            else: prvek0 = (soubor[i1].replace(path0 + '/', '').replace('.FRK','').replace('.xy',''))
            prvek1 = ''.join([i for i in prvek0 if not i.isdigit()])     
                  
                 
            
            if (prvek1[len(prvek1)-1]=='P' or prvek1[len(prvek1)-1]=='p'): #Starý způsob
                prvek1=prvek1[0:len(prvek1)-1]
                
            if 'Pkopie' in prvek1: #Nový způsob
                prvek1=prvek1.replace('Pkopie','')
                
            # print(prvek1) 
            
            piky['reakce']=['  -  ']*len(piky['energie']) #reakce G30
            piky['intensita']=['   -   ']*len(piky['energie']) #intensita G33
            piky['isotop']=['   -   ']*len(piky['energie']) #isotop G31
            piky['polocas']=[' - ']*len(piky['energie']) #poločas G32
            
            if radit[0]==2:
            
                if prvek1 in self.Gama_data.keys(): # Data o gama linkách z internetu jsou ukládány do dictionary self.Gama_data a není tedy potřeba je stahovat pro každý isotop zvlášť.
                    GAMA=self.Gama_data[prvek1]
                else:
                    GAMA=self.get_gamma(prvek1)
                    self.Gama_data[prvek1]=GAMA
                
                if len(GAMA)>1:
                    n3=0
                    for n1 in range (0, len(piky['energie'])):
                        for n2 in range (n3,len(GAMA)):
                            if '≈' in GAMA[n2][9]:
                                GAMA[n2][9]=GAMA[n2][9].strip('≈')
                            if 'stabilní' in GAMA[n2]:
                                # piky['reakce'][n1]=GAMA[n2][1].replace('>',',')
                                # piky['polocas'][n1]='stabilní'
                                # piky['isotop'][n1]=GAMA[n2][3]
                                break
                            if 'neznámo' in GAMA[n2]:
                                # piky['reakce'][n1]=GAMA[n2][1].replace('>',',')
                                # piky['polocas'][n1]='neznámo'
                                # piky['isotop'][n1]=GAMA[n2][3]
                                break
                            if ((float(GAMA[n2][9])-1) <= piky['energie'][n1] <= (float(GAMA[n2][9])+1)):
                                # print(float(GAMA[n2][9])-1,piky['energie'][n1],float(GAMA[n2][9])+1)
                                piky['reakce'][n1]=GAMA[n2][1].replace('>',',')
                                if len(GAMA[n2])>11:
                                    piky['intensita'][n1]=GAMA[n2][11]
                                piky['isotop'][n1]=GAMA[n2][3]
                                piky['polocas'][n1]=float(GAMA[n2][5])
                                # n3=max(3,n2-5)
                                break
        ## Seřazení výstupu dle výběru            
                
                original_list = list(piky[radit[1]])
                sorted_list = sorted(range(len(original_list)), key=lambda k: original_list[k])
                if radit[1] != 'energie':
                    desired_list = list(reversed(sorted_list))
                else:
                    desired_list = sorted_list
                
            else:
                desired_list = range(0,len(piky['energie']))
                
        ## Zapisování dat do souboru
            
            os.chdir('out')
            if system()=='Windows': vystup = open(soubor[i1].replace(os.path.basename(soubor[i1]), 'out\\' + os.path.basename(soubor[i1])).replace('FRK','OUTpy'),'w')
            else: vystup = open(soubor[i1].replace(path0 + '/', '').replace('FRK','OUTpy').replace('xy','OUTpy'),'w')
            vystup.write(u'Vyhodnocováno skriptem: %s \n \n' %(str(os.path.basename(__file__))))
            if system()=='Windows':
                vystup.write(u'Vstupní parametry: \nFaktor šírky píku = %i \n' %(sirka))
                vystup.write(u'Pocet iterací pri vyhlazování pozadí = %i  \n' %(cykl))
            else:
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
            if system()=='Windows':
                vystup.write('Energie (keV)                Plocha (-)                Reakce                   Intenzita(%)                 Isotop                    Polocas (s)\n')
            else:
                vystup.write('Energie (keV)                Plocha (-)                Reakce                   Intenzita(%)                 Isotop                    Poločas (s)\n')

            
            
            for i in desired_list:
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
            self.Vypis(u'Hotovo! Zobrazuji grafy.',0)
            for i12 in range (0,len(soubor)):
                plt.ion()
                plt.figure(plot_jmeno[i12])
                plt.title(plot_jmeno[i12])
                plt.xlabel(u'Energie (keV)')
                plt.ylabel(u'Četnost (-)')
                plt.plot(spektrum['energie'], plot_spektrum[i12], label=u'Spektrum') #vykreslení spektra
                plt.plot(spektrum['energie'], plot_pozadi[i12], 'r', label=u'Pozadí') #vykreslení pozadí
                plt.legend()
            self.progressBar.setProperty("value", 100)
            
            # # app = QtGui.QApplication(sys.argv)
            # # graf = Grafy()
            # # graf.show()
        
            # sys.exit(app.exec_())
            
            
        else:
            self.Vypis(u'Hotovo!',0)
            self.progressBar.setProperty("value", 100)
        print(time.time()-t)
        # print(piky['vyska'])
        # print(self.Gama_data)
