import os, time
from glob import glob
import matplotlib.pyplot as plt
# from numpy import mean
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp, sqrt, mean

from joblib import Parallel, delayed, cpu_count

t=time.time()

path = '/home/dominik/Dokumenty/Python/FortyFour/FortyFour26/ORTEC'

soubor = glob(path+ '/*.FRK')

list1 = list(range(0,len(soubor)))

def vykresleni_gause(i12):
    print('Vyhodnocuji %i' %i12)
    
    plot_jmeno=[0]*len(soubor)
    plot_spektrum=[0]*len(soubor)
    plot_pozadi=[0]*len(soubor)
    
    FRK1=soubor[i12]
    
    
    
    
    Y0=[0]*8192 
    f1=open(FRK1)
    for i2 in range(0, len(Y0)):
        Y0[i2]=float(''.join(f1.readline().split()))
    
    sirka=3
    cykl = 8
    typ_pozadi=2
    ampl=200
    
    config0 =' 328.0320   88.0730'.strip().split()
    config1='5050.4000 2754.0500'.strip().split()
    
    
    newconfig0=float(config0[1])-float(config0[0])*(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
    newconfig1=(float(config1[1])-float(config0[1]))/(float(config1[0])-float(config0[0]))
    
    
    spektrum={}
    spektrum['cetnost']=[]
    # Y=[0]*8192 == spektrum['cetnost']
    
    spektrum['cetnost']=Y0
    
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
        
    
        
        
        
    for i10 in range (0,cykl):
        # QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
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
        # QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
        PP[piky['pravy'][i9e]]=pozadi[i9e]
        inkrement=(pozadi[i9e+1]-pozadi[i9e])/(piky['pravy'][i9e+1]-piky['pravy'][i9e])
        for i9f in range (0,(piky['pravy'][i9e+1]-piky['pravy'][i9e])):
            PP[piky['pravy'][i9e]+i9f]=PP[piky['pravy'][i9e]]+i9f*inkrement
    
    
    
    for i10 in range (0,int(cykl/4)):
        # QtGui.QApplication.processEvents() #Obnovení okna aplikace na konci každého výpočetního cyklu
        P0=[]
        P0.extend(PP)
        PP=[]
        P1=[0.0]*len(P0)
        P1[0:5]=P0[0:5]
        P1[(len(P0)-6):(len(P0)-1)]=P0[(len(P0)-6):(len(P0)-1)]
        if typ_pozadi==1:
            for i11 in range (5,len(P0)-6):
                if (i10<(cykl)):
                    P1[i11]=min(Y0[i11],mean([P0[i11-5],P0[i11-4],P0[i11-3],P0[i11-2],P0[i11-1],P0[i11],P0[i11+1],P0[i11+2],P0[i11+3],P0[i11+4],P0[i11+5]]))
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
        
        
    # print(piky)
        
        
        
        
    
    plot_spektrum[i12]=spektrum['cetnost']
    plot_pozadi[i12]=PP
    
    BezPozadi=[i - j for i, j in zip(plot_spektrum[i12], plot_pozadi[i12])]
    OkrajL={'energie':[spektrum['energie'][i] for i in piky['levy']],'cetnost':[spektrum['cetnost'][i] for i in piky['levy']]}
    OkrajP={'energie':[spektrum['energie'][i] for i in piky['pravy']],'cetnost':[spektrum['cetnost'][i] for i in piky['pravy']]}
    
    
    # plt.ion()
    # plt.figure(FRK1)
    # plt.title(FRK1)
    # plt.xlabel(u'Energie (keV)')
    # plt.ylabel(u'Četnost (-)')
    # # # plt.plot(Y0) #vykreslení spektra
    # 
    # plt.plot(spektrum['energie'], plot_spektrum[i12], label=u'Spektrum') #vykreslení spektra
    # plt.plot(spektrum['energie'], plot_pozadi[i12], 'r', label=u'Pozadí') #vykreslení pozadí
    # 
    # # plt.plot(spektrum['energie'], BezPozadi, label=u'Spektrum') #vykreslení spektra
    # # plt.plot(spektrum['energie'], [0]*len(spektrum['energie']), 'k', label=u'Nula') #vykreslení pozadí
    # plt.plot(OkrajL['energie'],OkrajL['cetnost'], 'ro:', label=u'Okraje') 
    # plt.plot(OkrajP['energie'],OkrajP['cetnost'], 'bo:', label=u'Okraje') 
    # plt.legend()
    
   
    
    def gaus(x,a,x0,sigma):
        return a*exp(-(x-x0)**2/(2*sigma**2))
    
    pocet=['nic']*35

    pocet0=0
    for j in range(len(piky['levy'])): #range(120,136): #
        
        x = ar(spektrum['energie'][piky['levy'][j]:piky['pravy'][j]])
        y = ar(BezPozadi[piky['levy'][j]:piky['pravy'][j]]) #ar(spektrum['cetnost'][piky['levy'][j]:piky['pravy'][j]])
        
        n = len(x)                          #the number of data
        g_mean = sum(x*y)/n                   #note this correction
        
    
        sigma = sqrt(sum(y*(x-g_mean)**2)/n)/15 #sum(y*(x-mean)**2)/n        #note this correction
        
        
        
        try:
            popt,pcov = curve_fit(gaus,x,y,p0=[max(y),g_mean,sigma])
        except RuntimeError:
            nic=0
        else:
            # print(abs(gaus(x,*popt).max()-gaus(x,*popt).mean()))
            # if True: #abs(gaus(x,*popt).max()-gaus(x,*popt).mean())>1.0e-2:
            #     plt.ion()
            #     plt.figure(j)
            #     plt.plot(x,y,'b+:',label='data')
            #     plt.plot(x,gaus(x,*popt),'ro:',label='fit')
            #     plt.legend()
            #     plt.title(u'Pík %i'%j)
            #     plt.xlabel('Time (s)')
            #     plt.ylabel('Voltage (V)')
            #     plt.show()
            
            if abs(gaus(x,*popt).max()-gaus(x,*popt).mean())>1.0e-2:
                pocet0+=1
    
    
    x1=[]
    y1=[]
    for i25 in range (0,len(pocet)):
        if pocet[i25]!='nic':
            x1.append(pocet[i25][0])
            y1.append(pocet[i25][1])
    
    # plt.ion()
    # plt.figure(i12)
    # plt.plot(x1,y1,'b+:',label='data')
    # plt.title(u'Závislost počtu konvergentních gaussů na koeficientu, kterým je dělena sigma')
    # plt.xlabel('-')
    # plt.ylabel('-')
    # plt.show()
            # nic=input('nic')
        
        
Parallel(n_jobs=cpu_count())(delayed(vykresleni_gause)(input) for input in list1)
    
print(time.time()-t)