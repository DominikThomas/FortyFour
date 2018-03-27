# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests, re, periodic, time
from math import log
from PyQt4 import QtGui

class Data():
    
    def get_gamma(self,prvek): #Toto je dost divné, už jsem to pochopil
        
        # print(prvek,neco)
        
        tercove_jadro0=periodic.element(prvek)
        if tercove_jadro0 == None:
            return {}
        tercove_jadro0hmotnost=str(round(tercove_jadro0.mass))
        
        tercove_jadro=tercove_jadro0hmotnost+prvek
        pocet_nukleonu=int(re.findall('\d+',tercove_jadro)[0])
        terc_prvek=tercove_jadro.replace(re.findall('\d+',tercove_jadro)[0],'')
        # print(pocet_nukleonu,prvek)
        # zkoumane_reakce=['n>2n','n>3n','n>p','n>a']  #'n>4n','n>5n',
        zkoumane_reakce=['n>5n','n>4n','n>3n','n>2n','n>p','n>a']
        m_castice={'n': 1,'p': 1,'d': 2,'t': 3,'3He': 3,'a': 4}
        z_castice={'n': 0,'p': 1,'d': 1,'t': 1,'3He': 2,'a': 2}
        Gamma=[]
        
        switch_url=0
        
        
        while len(zkoumane_reakce)>0:
            
            reakce=zkoumane_reakce.pop()
            
            ##Změna nukleonového a atomového čísla
            
            
            if re.findall('\d+',reakce.split('>')[0])==[]:
                m_in=1*m_castice[reakce.split('>')[0]]
                z_in=1*z_castice[reakce.split('>')[0]]
            else:
                m_in=int(re.findall('\d+',reakce.split('>')[0])[0])*m_castice[reakce.split('>')[0].replace(re.findall('\d+',reakce.split('>')[0])[0],'')]
                z_in=int(re.findall('\d+',reakce.split('>')[0])[0])*z_castice[reakce.split('>')[0].replace(re.findall('\d+',reakce.split('>')[0])[0],'')]
                
            if re.findall('\d+',reakce.split('>')[1])==[]:
                m_out=1*m_castice[reakce.split('>')[1]]
                z_out=1*z_castice[reakce.split('>')[1]]
            else:
                m_out=int(re.findall('\d+',reakce.split('>')[1])[0])*m_castice[reakce.split('>')[1].replace(re.findall('\d+',reakce.split('>')[1])[0],'')]
                z_out=int(re.findall('\d+',reakce.split('>')[1])[0])*z_castice[reakce.split('>')[1].replace(re.findall('\d+',reakce.split('>')[1])[0],'')]
        
            m=-m_in+m_out
            z=-z_in+z_out
            
            prvek = periodic.element(periodic.element(terc_prvek).atomic-z).symbol
            isotop='%i%s' %(pocet_nukleonu-m,prvek)
        
            try:
                del stranka
            except NameError:
                nic='nic'
            
            if switch_url==0:
                self.textBrowser.append(u'Načítám data ze serveru www.nndc.bnl.gov ')
                QtGui.QApplication.processEvents()
                switch_url=1
                
            try:
                url_stranky='http://www.nndc.bnl.gov/nudat2/decaysearchdirect.jsp?nuc=%s' %(isotop)
                stranka=requests.get(url_stranky) #Stáhnutí stránky
                QtGui.QApplication.processEvents()
                # print(url_stranky)
            except requests.exceptions.ConnectionError:
                self.textBrowser.append(u'Nepodařilo se získat data ze serveru www.nndc.bnl.gov ')
                Gamma=[]
                return Gamma
            else:
                if switch_url==1:
                    self.textBrowser.append(u'Hotovo!')
                    switch_url=2
                
            text0 = stranka.text #získání html kódu
            
            if 'No datasets were found since nucleus is stable' in text0:
                polozka=[1,reakce,'Q',isotop,'stabilní','stabilní','stabilní','stabilní',0,'stabilní','stabilní','stabilní','stabilní']
                Gamma.append(polozka)
                print(polozka)
                
            elif 'No datasets were found within the specified search parameters' in text0:
                polozka=[1,reakce,'Q',isotop,'neznámo','neznámo','neznámo','neznámo','neznámo','neznámo','neznámo','neznámo','neznámo']
                Gamma.append(polozka)
                print(polozka)
                
            else:
                text1 = BeautifulSoup(text0, 'html.parser') #částečná extrakce textu z html ku do jednoho řetězce
                
                text2 = text1.get_text().split('\n') #rozdělení tohoto řetězce podle znaku nového řádku
                
                for i in range(0,len(text2)):
                    # print(text2[i])
                    
                    if 'NucleusDecayScheme' in text2[i]: #Hledání klíčového slova, po němž jsou ve vstupu uloženy příslušné informace
                        
                        ### Poločas
                        
                        try:
                            del korekceT_2
                        except NameError:
                            pass
                        
                        if text2[i+1].split()[4] == 'y': # Zjištění, v jakých jednotkách (dny, hodiny, minuty, ...) je zdrojová hodnoty poločasu rozpadu
                            korekceT_2=1*365.25
                        elif text2[i+1].split()[4] == 'd':
                            korekceT_2=1
                        elif text2[i+1].split()[4] == 'h':
                            korekceT_2=1/24
                        elif text2[i+1].split()[4] == 'm':
                            korekceT_2=1/24/60
                        elif text2[i+1].split()[4] == 's':
                            korekceT_2=1/24/60/60
                        elif text2[i+1].split()[4] == 'ms':
                            korekceT_2=1/24/60/60/1000
                        elif text2[i+1].split()[4] == 'µS':
                            korekceT_2=1/24/60/60/1000/1000
                        elif text2[i+1].split()[4] == 'nS':
                            korekceT_2=1/24/60/60/1000/1000/1000    
                        
                        T_2d0=text2[i+1].split()[3] # Načtení poločasu rozpadu
                        T_2d=float(T_2d0)*korekceT_2
                        T_2d_err0=(text2[i+1].split()[5]) #Načtení chyby T1/2
                        if len((T_2d0).strip().split('.')) == 2: #zjištění, zda je poločas uveden s nějakými desetinnými místy:
                            try: T_2d_err=int(T_2d_err0)/(10**len(str(T_2d0).strip().split('.')[1]))*korekceT_2 #Určení, kolik desetinných míst má poločas a podle toho náležitá uprava mantisy? chyby poločasu
                            except ValueError:
                                T_2d_err0=max(T_2d_err0.strip('+').strip('-').split('-'))
                                T_2d_err=int(T_2d_err0)/(10**len(str(T_2d0).strip().split('.')[1]))*korekceT_2
                        elif len((T_2d0).strip().split('.')) == 1:
                            T_2d_err=int(T_2d_err0)*korekceT_2
                        
                    if 'Gamma and X' in text2[i]: #Hledání klíčového slova, po němž jsou ve vstupu uloženy příslušné informace
                        # print(i)
                        poradi=1
                        b=i+13
                        try:
                            while (not 'Gamma' in text2[b]) and (not 'Dataset' in text2[b]):
                                text3=[text2[b].strip(),text2[b+1].strip(),text2[b+2].strip(),text2[b+3].strip()] #Jednotlivé řádky s požadovanými informacemi s chybami zapsanými u hodnot
                                # print(text3)
                                
                                ## Vytvoření výstupu
                                
                                polozka=['poradi','reakce','Q','isotop','T/2(d)','T/2(s)','T/2_err(d)','T/2_err(s)','Lambda','energie','e_err','intensita','i_err']
                                
                                ### Energie
                                
                                if len(text3[1].split())==2 and text3[0]=='':
                                    energie,e_err0=text3[1].split()
                                    if e_err0=='?':
                                        e_err='?'
                                    elif e_err0=='S':
                                        e_err='S'
                                    else:
                                        e_err=int(e_err0)/(10**len(str(energie).strip().split('.')[1]))
                                    # print(energie,chyba)
                                elif len(text3[1].split())==1:
                                    energie=text3[1]
                                    e_err=''
                                    # print(energie)
                                    
                                ### Intenzita
                                
                                intenzita0, intenzita_err0 = text3[2].split('%')
                                intenzita = intenzita0.strip()
                                if len(intenzita.strip().split('.'))==1:
                                    intenzita_err = intenzita_err0 #at už je to rovno '' nebo číslu
                                
                                elif len(intenzita.strip().split('.'))==2:
                                    
                                    if intenzita_err0 != '':
                                        intenzita_err = int(intenzita_err0)/(10**len(str(intenzita).strip().split('.')[1]))
                                    else:
                                        intenzita_err = intenzita_err0
                                
                                
                                polozka[0]=poradi
                                poradi+=1
                                
                                
                                polozka[1]=reakce
                                
                                polozka[3]=isotop
                                polozka[4]=T_2d
                                polozka[5]=T_2d*3600*24
                                polozka[6]=T_2d_err
                                polozka[7]=T_2d_err*3600*24
                                polozka[8]=log(2)/polozka[5]
                                polozka[9]=energie
                                polozka[10]=e_err
                                polozka[11]=intenzita
                                polozka[12]=intenzita_err
                                
                                b+=6
                                # print(polozka)
                                Gamma.append(polozka)
                        except IndexError:
                            nic='nic'
        return Gamma