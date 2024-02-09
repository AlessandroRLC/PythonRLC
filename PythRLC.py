# -*- coding: utf-8 -*-
import pandas as pd #importo modulo per leggere il file excel.xlsx (no csv)
import time
import datetime
import math

#leggo il file 
InfilePath = "./RLC_IO_List.xlsx"
start = time.time()
Data = pd.read_excel(InfilePath, sheet_name= 0)
Df = pd.DataFrame(Data)

#letto il file e il foglio 0 (che sarà elenco utenze), proseguo con la creazione delle liste, definite dalle colonne identificate univocamente dal contenuto della prima cella in capo
try:
    ListaAree = Df['Area'].fillna(' ').tolist()
    ListaTipi = Df['Tipo'].fillna(' ').tolist()
    ListaSigle = Df['Sigla'].fillna(' ').tolist()
    ListaDescrizioni = Df['Descrizione aggiuntiva'].fillna(' ').tolist()
    ListaUsciteA = Df['Uscita A'].fillna(' ').tolist()
    ListaUsciteB = Df['Uscita B'].fillna(' ').tolist()
    ListaIngressiA = Df['Ingresso A'].fillna(' ').tolist()
    ListaIngressiB = Df['Ingresso B'].fillna(' ').tolist()
    ListaIngressiC = Df['Ingresso C'].fillna(' ').tolist()
    ListaAllSpecifico = Df['Allarme Specifico'].fillna(' ').tolist()
    AllarmiVerdePartenza = Df['Allarmi Verde'].fillna(' ').tolist()
    AllarmiTostatoPartenza = Df['Allarmi Tostato'].fillna(' ').tolist()
except:
    print("Errore Durante Lettura della tabella Excel di partenza, le colonne Sono nominate correttamente? Il Primo Foglio del file excel Contiene la Lista I/O?\n Controlla il Log del programma per ulteriori informazioni in merito all'errore verificatosi (LogFile WIP).")
    raise SystemExit
#Ottenute le liste contenenti le informazioni necessari alla creazione dei componenti del progetto finale, procedo inizializzando tutte le liste e 
# le variabili contenenti le informazioni necessari per comporre i db, fc etc...  

VarietaTipi = ['M','INVABB','SOFT','F','SM','SB','DM', 'DB','VMAN', 'VP', 'SENS' ,'SPARE', 'DIN', 'DOUT']
               #1     #2      #3   #4   #5   #6   #7    #8    #9    #10    #11      #12     #13    #14


RobaInizioFileDB = "DATA_BLOCK "

RobaInizioFileDBABB = 'DATA_BLOCK "DRIVES"'

RobaInizioFileDBSINOTTICO = 'DATA_BLOCK "SINOTTICO"'

RobaInMezzoFileDB = "{ S7_Optimized_Access := 'TRUE' }\n VERSION : 0.1\n NON_RETAIN\n " # Data In mezzo file DB

RobaFineFileDB = "BEGIN\n\nEND_DATA_BLOCK\n\n"                                          # Fine DB

RobaFineFileDBABB = "   END_VAR\n\n\nBEGIN\n\nEND_DATA_BLOCK\n\n" #Fine DB (usato anche per il file SINOTTICO)


UDTABB = ': "ABB_DRIVE_semplice";' 

IntVarDB = ': Int;\n'


NomenLivelliMinimo = ['LL','LSL','B1LL','B2LL','B3LL','B4LL']

NomenLivelliMassimo = ['LH','HL','LSH','B1LH','B2LH','B3LH','B4LH']

NomenLivelliMedio = ['LM', 'LSM', 'B1LM', 'B2LM', 'B3LM', 'B4LM']

NomenPrx = ['PRS','PRX']

#Unused NomenValvole = ['YV','SA','VA']



FBmotore = 'MotorCtrl v0.1'

FBInverter = 'InverterCtrl v0.1'

FBFena = ''

FBvalve = 'ValveCtrl v0.2'

FBsensDIG = 'IngressoTipo0 v2.0'

FBFenaDB = "ABB_FENA11_DRIVE_CONTROL_FB"

FPvalveParz = 'ParzCtrl v0.1'

#Parti di IO INT (Utenze HMI)

header_IO_INT_HMI = ":IOInt;Group;Comment;Logged;EventLogged;EventLoggingPriority;RetentiveValue;RetentiveAlarmParameters;AlarmValueDeadband;AlarmDevDeadband;EngUnits;InitialValue;MinEU;MaxEU;Deadband;LogDeadband;LoLoAlarmState;LoLoAlarmValue;LoLoAlarmPri;LoAlarmState;LoAlarmValue;LoAlarmPri;HiAlarmState;HiAlarmValue;HiAlarmPri;HiHiAlarmState;HiHiAlarmValue;HiHiAlarmPri;MinorDevAlarmState;MinorDevAlarmValue;MinorDevAlarmPri;MajorDevAlarmState;MajorDevAlarmValue;MajorDevAlarmPri;DevTarget;ROCAlarmState;ROCAlarmValue;ROCAlarmPri;ROCTimeBase;MinRaw;MaxRaw;Conversion;AccessName;ItemUseTagname;ItemName;ReadOnly;AlarmComment;AlarmAckModel;LoLoAlarmDisable;LoAlarmDisable;HiAlarmDisable;HiHiAlarmDisable;MinDevAlarmDisable;MajDevAlarmDisable;RocAlarmDisable;LoLoAlarmInhibitor;LoAlarmInhibitor;HiAlarmInhibitor;HiHiAlarmInhibitor;MinDevAlarmInhibitor;MajDevAlarmInhibitor;RocAlarmInhibitor;SymbolicName\n"
comune_int_HMI = ";$System;;No;No;0;No;No;0;0;;0;0;65535;0;0;Off;0;1;Off;0;1;Off;0;1;Off;0;1;Off;0;1;Off;0;1;0;Off;0;1;Min;0;65535;Linear;PLC_Symb;No;"
fine_int_HMI = ";No;;0;0;0;0;0;0;0;0;;;;;;;;\n"

comune_IntInv_HMI = ";$System;;No;No;0;No;No;0;0;;0;-32767;32767;0;0;Off;0;1;Off;0;1;Off;0;1;Off;0;1;Off;0;1;Off;0;1;0;Off;0;1;Min;-32767;32767;Linear;PLC_Symb;No;SINOTTICO.vFeedBack"



#Parti di IO DISC (Allarmi HMI)

Header_IO_DISC_HMI = ":IODisc;Group;Comment;Logged;EventLogged;EventLoggingPriority;RetentiveValue;InitialDisc;OffMsg;OnMsg;AlarmState;AlarmPri;DConversion;AccessName;ItemUseTagname;ItemName;ReadOnly;AlarmComment;AlarmAckModel;DSCAlarmDisable;DSCAlarmInhibitor;SymbolicName;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n"
SystemIO_DISC = ";$System;"
Comune_IO_DISC_HMI = ";No;No;0;No;Off;;;On;100;Direct;PLC_Leg;No;"
Dopoindirizzo_IO_DISC = ";No;"
Fine_IO_DISC = ";0;0;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n"

#Commenti per le variabili I/O

CommentoRM = "RISPOSTA MOTORE"
CommentoASS = "ANOMALIA SOFTSTARTER"
CommentoRF = "RISPOSTA FILTRO"
CommentoARF = "ALLARME FILTRO"
CommentoFC = "FINECORSA"
CommentoFCX = "FINECORSA DI SICUREZZA"
CommentoVTX = "VUOTOSTATO DI SICUREZZA"
CommentoTSX = "SONDA EMISSIONI SOGLIA ALLARME"
CommentoTS = "SONDA EMISSIONI SOGLIA PREALLARME"
CommentoVT = "VUOTOSTATO"
CommentoCR = "CONTROLLO DI ROTAZIONE "
CommentoLL = "LIVELLO MINIMO"
CommentoLH = "LIVELLO MASSIMO"
CommentoLM = "LIVELLO MEDIO"
CommentoPRX = "PRESSOSTATO"     
CommentoPR = "PRESSOSTATO"
Commento24VDC = "PRESENZA 24VDC"
CommentoPE = "EMERGENZA "
CommentoPButton = "PULSANTE"
CommentoSele = "SELETTORE"
Commento400V = "RISPOSTA CONTATTORI DI LINEA 400v 50hz"
Commento300V = "RISPOSTA CONTATTORI DI LINEA 300v 50hz"
CommentoTacit = "TACITAZIONE ALLARMI"
CommentoRipr = "RIPRISTINO ALLARMI"
CommentoTERM = "CUMULATIVO RELE' IN BLOCCO"
CommentoPILZ = "PILZ OK EMERGENZA GENERALE"


FineCommentoPRX = "SOGLIA INTERVENTO"
FineCommentoPR = "SOGLIA ALLARME"

CommentoCM = "COMANDO MOTORE"
CommentoCF = "COMANDO FILTRO"
CommentoVM = "COMANDO VALVOLA"

#Parti per Allarmi

AllarmeMotore = " - MANCATA PARTENZA - MOTORE "

AllarmeLetturaInverter = " - ERRORE LETTURA - INVERTER "

AllarmeAnomaliaSS = " - ANOMALIA - SOFTSTARTER "

AllarmeInverter = " - MANCATA PARTENZA - INVERTER "

AllarmeAnomaliaInverter = " - ANOMALIA - INVERTER "

AllarmeFiltro = " - MANCANZA DI ALIMENTAZIONE - FILTRO "

AllarmeFiltroPressione = " - PRESSIONE NON OK - FILTRO "

AllarmeValvola = " - MANCATO POSIZIONAMENTO - VALVOLA "

AllarmeLL = " - LIVELLO MINIMO - SENSORE DI LIVELLO MINIMO "

AllarmeLH = " - LIVELLO MASSIMO - SENSORE DI LIVELLO MASSIMO "

AllarmeLM = " - LIVELLO MEDIO - SENSORE DI LIVELLO MEDIO " #Non usato

AllarmeCR = " - CONTROLLO DI ROTAZIONE - "

AllarmeFCX = " - PILZ - "

AllarmePRX = " - PRESSOSTATO DI SICUREZZA - "

AllarmePR = " - PRESSOSTATO - "

AllarmeVTX = " - VUOTOSTATO DI SICUREZZA - "

AllarmeVT = " - VUOTOSTATO - "

AllarmeTSX = " - EMISSIONI ALTE O SONDA EMISSIONI SCOLLEGATA - SONDA  "

AllarmeTs = " - SOGLIA DI PREALLARME EMISSIONI RAGGIUNTA - SONDA  "

Allarme24VDC = " - MANCANZA DI ALIMENTAZIONE - 24VDC QUADRO ELETTRICO "

AllarmePE = " - PULSANTE DI EMERGENZA - EMERGENZA "

Allarme400V = " - ATTENZIONE! - MANCANZA TENSIONE 400V CONTATTORI DI LINEA "

Allarme300V = " - ATTENZIONE! - MANCANZA TENSIONE 300V CONTATTORI DI LINEA "

AllarmeTERMIC = "- INTERVENTO! - CUMULATIVO TERMICI QUADRO ELETTRICO "

AllarmePILZ = " - INTERVENTO! - EMERGENZA GENERALE PILZ QUADRO ELETTRICO "

PrefIng = "I_"
RobaInMezzoPLCTAGS = ";False;True;True;True;;"
PrefUsc = "U"
PrefAll = "A_"
PrefAllInvL = "A_INV"
PrefAllInvA = "A_ALL"

IntCountAlrm = 1 
ContaRighe = 2


#Inverter allarmi 3
#motori allarmi 1
#valvole allarmi 1 (position failure e basta)

#Ora servono le funzioni che dovranno essere richiamate una volta incominciato ad analizzare il datase

#Area allarmi di partenza ###da fare:renderla Dinamica 
ParteDecimaleIniziale = int(AllarmiVerdePartenza[0])
ParteOttaleIniziale = int(AllarmiVerdePartenza[1])
ParteDecimale = ParteDecimaleIniziale
ParteOttale = ParteOttaleIniziale
StrAllarmiMerker = 'M' + str(ParteDecimale) + '.' + str(ParteOttale)
IndiceAllarme = 1
StrAllarmeIndice = 'A' + str(IndiceAllarme) + ' - '

ParteDecimaleTostato = int(AllarmiTostatoPartenza[0])
ParteOttaleTostato = int(AllarmiTostatoPartenza[1])
StrAllarmiMerkerTostato = 'M' + str(ParteDecimaleTostato) + '.' + str(ParteOttaleTostato)
IndiceAllarmeTostato = ParteDecimaleTostato * 8 + ParteOttaleTostato - (ParteDecimaleIniziale * 8 + ParteOttaleIniziale)
StrAllarmeIndiceTostato = 'A' + str(IndiceAllarmeTostato) + ' - '

SpareINTing = 0
SpareINTusc = 0

def ContaAllarmi(PDEC,POTT,AlarmIndex): #Funzione per creare l'indirizzamento a merker usato per gli allarmi, ogni chiamata della funzione aumenterà di un bit la dimensione dell'area merker
    global IndiceAllarme
    global ParteDecimale 
    global ParteOttale
    global StrAllarmiMerker
    global StrAllarmeIndice

    AlarmIndex = AlarmIndex + 1 
    POTT = POTT + 1
    if POTT > 7: 
        POTT = 0
        PDEC = PDEC + 1
    ParteDecimale = PDEC
    ParteOttale = POTT
    IndiceAllarme = AlarmIndex
    StrAllarmiMerker = 'M' + str(ParteDecimale) + '.' + str(ParteOttale)
    StrAllarmeIndice = 'A' + str(AlarmIndex) + ' - '
    return(PDEC,POTT)
###!!! CHIAMARE SEMPRE DOPO AVER GENERATO UN ALLARME AREA VERDE ###

def ContaAllarmiTostato(PDEC,POTT,AlarmIndex):
    global IndiceAllarmeTostato
    global ParteDecimaleTostato 
    global ParteOttaleTostato
    global StrAllarmiMerkerTostato
    global StrAllarmeIndiceTostato
    global ParteDecimaleIniziale 
    global ParteOttaleIniziale

    #AlarmIndex = AlarmIndex + 1 
    POTT = POTT + 1
    if POTT > 7: 
        POTT = 0
        PDEC = PDEC + 1
    ParteDecimaleTostato = PDEC
    ParteOttaleTostato = POTT
    IndiceAllarmeTostato = AlarmIndex
    StrAllarmiMerkerTostato = 'M' + str(ParteDecimaleTostato) + '.' + str(ParteOttaleTostato)
    StrAllarmeIndiceTostato = 'A' + str((ParteDecimaleTostato * 8 + ParteOttaleTostato - (ParteDecimaleIniziale * 8 + ParteOttaleIniziale))) + ' - '
    return(PDEC,POTT)
###!!! CHIAMARE SEMPRE DOPO AVER GENERATO UN ALLARME AREA TOSTATO ###

### Inizializzazione File di lettura e Scrittura (aka Input ed Output dello script) ###

try: #Sorgente FC FENA TXT
    SorgFenaFC = open('./Sorgenti/FC_FENA01.txt', 'r') #Leggo sorgente FC fena per modificarlo
    FCFENA = SorgFenaFC.read()
except:
    print('Errore In lettura file ./Sorgenti/FC_FENA01.txt, hai permessi adatti? il file è Presente?')
    raise SystemExit

try: #db inverter
    MotoriInvDB = open('./PLC/Motori/Inverter/MotoriInverter.db', 'w', encoding = "utf-8")
except:
    raise SystemExit

try: #ingressi CSV
    IngressiCSV = open("./PLC/IngressiPLC.csv", 'w', encoding = "utf-8")
except:
    print('Errore in creazione file Ingressi.csv, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try:#Utenze HMI CSV
    UtenzeHMICSV = open("./HMI/UtenzeHMI.csv", 'w', encoding = "utf-8")
except:
    print('Errore in creazione file UtenzeHMI.csv, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit
UtenzeHMICSV.write(header_IO_INT_HMI)

try:#Allarmi HMI CSV
    AllarmiUtenzeHMICSV = open("./HMI/AllarmiUtenzeHMI.csv", 'w', encoding = "utf-8")
except:
    print('Errore in creazione file AllarmiUtenzeHMI.csv, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit
AllarmiUtenzeHMICSV.write(Header_IO_DISC_HMI)

try:#FC ABB TXT
    InverterABBTXT = open('./PLC/Motori/Inverter/FCinverterABB.txt', 'w', encoding = "utf-8")
except:
    raise SystemExit

try:#FC inverter TXT
    MotoriInvFCTXT = open('./PLC/Motori/Inverter/MotoriInverterFC.txt','w', encoding = "utf-8")
except:
    print('Errore in creazione file MotoriInverterFC.txt, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try:#FENADB
    MotoriFena = open("./PLC/Motori/Inverter/Motorifena.db", 'w')
except:
    print('Errore in creazione file Motorifena.db, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try:#Motori DB
    Motoridb = open('./PLC/Motori/Motori.db', 'w', encoding = "utf-8")
except: 
    print('Errore in creazione file Motori.db, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try:#Uscite PLC CSV
    UsciteCSV = open('./PLC/UscitePLC.csv', 'w', encoding = "utf-8")
except:
    print('Errore in creazione file Uscite.csv, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try:#Allarmi PLC CSV
    AllarmiPLCCSV = open('./PLC/AllarmiPLC.csv', 'w', encoding = "utf-8")
except:
    print('Errore in creazione file allarmiPLC.csv, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try:#Motore FC TXT
    MotoreFCTXT = open("./PLC/Motori/MotoriFC.txt","w")
except:
     print('Errore in creazione file FCmotori.txt, hai permessi adatti? il file è magari già in uso?')
     raise SystemExit   

try:#Drives DB 
    DRIVESdb = open('./PLC/Motori/Inverter/DRIVES.db', 'w', encoding = "utf-8")
except: 
    print('Errore in creazione file DRIVES.db, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit
DRIVESdb.write(RobaInizioFileDBABB + '\n' + RobaInMezzoFileDB + "   VAR\n" )

try:#DB SINOTTICO (FEEDBACK INVERTER)
    SINOTTICOdb = open('./PLC/Motori/Inverter/SINOTTICO.db', 'w', encoding = "utf-8")
except: 
    print('Errore in creazione file SINOTTICO.db, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit
SINOTTICOdb.write(RobaInizioFileDBSINOTTICO + '\n' + RobaInMezzoFileDB + "   VAR\n" )

try:#FC Filtri TXT
    FiltriFCTXT = open('./PLC/Filtri/FiltriFC.txt', 'w', encoding = "utf-8")
except:
    print('Errore in creazione file FiltriFC.txt, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try: #Valvole Mono DB
    ValvoleMonoDB = open('./PLC/Valvole/Mono/ValvoleMono.db', 'w', encoding = "utf-8")
except:
    print('Errore in creazione file ValvoleMono.db, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try:#Valvole Mono FC TXT
    ValvoleMonoFCTXT = open('./PLC/Valvole/Mono/ValvoleMonoFC.txt', 'w', encoding = "utf-8")
except: 
    print('Errore in creazione file ValvoleMonoFC.txt, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try:#Valvole Bi DB
    ValvoleBiDB = open('./PLC/Valvole/Bistabili/ValvoleBi.db', 'w', encoding = "utf-8")
except:
    print('Errore in creazione file ValvoleBi.db, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try: #Valvole Bi FC TXT
    ValvoleBiFCTXT = open('./PLC/Valvole/Bistabili/ValvoleBiFC.txt', 'w', encoding = "utf-8")
except:
    print('Errore in creazione file ValvoleBi.txt, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try: #Valvole Man DB 
    ValvoleManDB = open('./PLC/Valvole/Manuali/ValvoleMan.db', 'w', encoding = "utf-8")
except: 
    print('Errore in creazione file ValvoleMan.db, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try: #Valvole Man FC TXT
    ValvoleManFCTXT = open('./PLC/Valvole/Manuali/FCValvoleMan.txt', 'w', encoding = "utf-8")
except: 
    print('Errore in creazione file FCValvoleMan.txt, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try: #Valvole Parz DB
    ValvoleParzDB = open('./PLC/Valvole/Parziali/ValvoleParz.db', 'w', encoding = "utf-8")
except: 
    print('Errore in creazione file ValvoleParz.db, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit


try: #Valvole Parz FC TXT 
    ValvoleParzFCTXT = open('./PLC/Valvole/Parziali/ValvoleParzFC.txt', 'w', encoding = "utf-8")
except: 
    print('Errore in creazione file ValvoleParzFC.txt, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try: #Sensori Digitali DB
    SensoriDigitaliDB = open('./PLC/Sensori E Ingressi/Digitali/SensoriDigitali.db', 'w', encoding = "utf-8")
except: 
    print('Errore in creazione file SensoriDigitali.db, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit

try: #Sensori Digitali FC TXT
    SensoriDigitaliFCTXT = open('./PLC/Sensori E Ingressi/Digitali/SensoriDigitaliFC.txt', 'w', encoding = "utf-8")
except:
    print('Errore in creazione file SensoriDigitaliFC.txt, hai permessi adatti? il file è magari già in uso?')
    raise SystemExit


#Mega loop gigante, tutti i dati della tabella sono looppati con un solo indice
for (areaL,tipoL,siglaL,Descr,UscitAL,UscitBL,IngressoAL,IngressoBL,IngressoCL,AllSpecificoL) in zip(ListaAree,ListaTipi,ListaSigle,ListaDescrizioni,ListaUsciteA,ListaUsciteB,ListaIngressiA,ListaIngressiB,ListaIngressiC,ListaAllSpecifico) :
    areaL = areaL.upper()
    tipoL = tipoL.upper()
    siglaL = siglaL.upper()
    Descr = Descr.upper() 
    UscitAL = UscitAL.upper()
    UscitBL = UscitBL.upper()
    IngressoAL = IngressoAL.upper()
    IngressoBL = IngressoBL.upper()
    IngressoCL = IngressoCL.upper()
    AllSpecificoL = AllSpecificoL.upper()
    analizzato = - 1 
    indice = -1
    for i in VarietaTipi:    #funzione che looppa la lista dei tipi (statica) e la confronta con quella del dataset, ritorna l'indice della posizione nella lista in cui il match tra le due liste si è verificato.                            
        indice = indice + 1  #nel caso in cui non si è trovato nulla, il valore inizializzato di ritorno di default è -1 -> il sistema halterà e l'eccezione di uscita viene sollevata
        if tipoL.upper() == i:
            analizzato = indice + 1 
    siglaL = siglaL.replace('.','') #Rimuovo eventuali segni di punteggiatura '.' dalla sigla dell'utenza
    if analizzato == -1: #Caso Riscontro Negativo
        print("Manca Il tipo nella riga o non è tra i possibili scelti, controlla la riga: [" + str(ContaRighe) + ']')
        raise SystemExit
    
    if analizzato == 1: #Caso Motore Diretto 

        Motoridb.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBmotore + '"' + "\n\n" + RobaFineFileDB)
        if Descr != ' ' : #Se ho la descrizione aggiuntiva del motore
            
            
            UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
            
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeMotore + siglaL + ' ' + '('  + Descr + ')'
                
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Motore  
                            
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            elif areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeMotore + siglaL + ' ' + '('  + Descr + ')'
                
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Motore  
                            
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

            if UscitBL != ' ' and UscitAL != ' ': #Se ho sia uscita A che Uscita B --> Due comandi e Due Ingressi

                IngressiCSV.write(PrefIng + 'R'  + siglaL + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoRM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Risposta Motore A

                IngressiCSV.write(PrefIng + 'R'  + siglaL + 'B;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoRM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Risposta Motore B 
                
                UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoCM + ' ' + siglaL + 'A' + ' (' + Descr + ');' + '\n' ) #Uscita Motore A
                
                UsciteCSV.write(PrefUsc + siglaL + 'B;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoCM + ' ' + siglaL + 'B' + ' (' + Descr + ');' + '\n' ) #Uscita Motore B
                
                FCMotore = f"//     {siglaL}    Motore {siglaL}  ({Descr})  \n#TMPalarm := FALSE;\n#TMPblc := FALSE;\n{siglaL}(OO_arisp=> A_{siglaL}, \nII_preset:=#preset, \nI_fbA:= I_R{siglaL}A , \nI_R{siglaL}B, \nI_powerOk:=#Power_OK, \nIO_Alarm:=#TMPalarm, \nI_blocco:=#TMPblc, \nI_man:=ManModeON, \nI_auto:=AutoModeON, \nI_reset:=#rip, \nO_outA:= U{siglaL}A, \nO_outB:=U{siglaL}B);\n\n" #Richiamo FB
                
                MotoreFCTXT.write(FCMotore) #Scrittura Richiamo FB in FC Motore
            elif UscitAL != ' ': #Se ho solo uscita A --> un comando
                
                IngressiCSV.write(PrefIng + 'R'  + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoRM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Risposta Motore

                UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoCM + ' ' + siglaL + ' (' + Descr  + ');' + '\n' ) #Uscita Motore Singola 
                
                FCMotore = f"//     {siglaL}    Motore {siglaL}  ({Descr})   \n#TMPalarm := FALSE;\n#TMPblc := FALSE;\n{siglaL}(OO_arisp=> A_{siglaL}, \nII_preset:=#preset, \nI_fbA:= I_R{siglaL} , \nI_fbB:=#dummy, \nI_powerOk:=#Power_OK, \nIO_Alarm:=#TMPalarm, \nI_blocco:=#TMPblc, \nI_man:=ManModeON, \nI_auto:=AutoModeON, \nI_reset:=#rip, \nO_outA:= U{siglaL}, \nO_outB:=#dummy);\n\n" #Richiamo FB
                
                MotoreFCTXT.write(FCMotore) #Scrittura Richiamo FB in FC Motore
        else: #Se non ho la descrizione aggiuntiva del motore
            IngressiCSV.write(PrefIng + 'R'  + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoRM + ' ' + siglaL + ' ' + ';' + '\n' ) #Ingresso Motore PLC
            
            UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
        
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeMotore + siglaL #Cat Testo Allarme per HMI
        
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)
                
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Motore
            
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI
                
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeMotore + siglaL #Cat Testo Allarme per HMI
        
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)
                
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Motore
            
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI

                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

            if UscitBL != ' ' and UscitAL != ' ': #Se Ho Due Comandi Ho due ingressi

                IngressiCSV.write(PrefIng + 'R'  + siglaL + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoRM + ' ' + siglaL + ' ' + ';' + '\n' ) #Ingresso Motore A

                IngressiCSV.write(PrefIng + 'R'  + siglaL + 'B;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoRM + ' ' + siglaL + ' ' + ';' + '\n' ) #Ingresso Motore B
            
                UsciteCSV.write(PrefUsc + siglaL + 'A' + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoCM + ' ' + siglaL + 'A' + ' ' * ';' + '\n' ) #Uscita Motore A
           
                UsciteCSV.write(PrefUsc + siglaL + 'B' + ';' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoCM + ' ' + siglaL + 'B' + ' ' + ';' + '\n' ) #Uscita Motore B
                                
                FCMotore = f"//     {siglaL}    Motore {siglaL}    \n#TMPalarm := FALSE;\n#TMPblc := FALSE;\n{siglaL}(OO_arisp=> A_{siglaL}, \nII_preset:=#preset, \nI_fbA:= I_R{siglaL}A , \nI_fbB:=I_R{siglaL}B, \nI_powerOk:=#Power_OK, \nIO_Alarm:=#TMPalarm, \nI_blocco:=#TMPblc, \nI_man:=ManModeON, \nI_auto:=AutoModeON, \nI_reset:=#rip, \nO_outA:= U{siglaL}A, \nO_outB:=U{siglaL}B);\n\n" #Richiamo FB
                
                MotoreFCTXT.write(FCMotore) #Scrittura Richiamo FB in FC Motore
            elif UscitAL != ' ': #Altrimenti 

                IngressiCSV.write(PrefIng + 'R'  + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoRM + ' ' + siglaL + ' ' + ';' + '\n' ) #Ingresso Motore PLC

                UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoCM + ' ' + siglaL + ';' + '\n' ) #Uscita Motore Singola
                
                FCMotore = f"//     {siglaL}    Motore {siglaL}    \n#TMPalarm := FALSE;\n#TMPblc := FALSE;\n{siglaL}(OO_arisp=> A_{siglaL}, \nII_preset:=#preset, \nI_fbA:= I_R{siglaL} , \nI_fbB:=#dummy, \nI_powerOk:=#Power_OK, \nIO_Alarm:=#TMPalarm, \nI_blocco:=#TMPblc, \nI_man:=ManModeON, \nI_auto:=AutoModeON, \nI_reset:=#rip, \nO_outA:= U{siglaL}, \nO_outB:=#dummy);\n\n" #Richiamo FB
                
                MotoreFCTXT.write(FCMotore) #Scrittura Richiamo FB in FC Motore
         
    if analizzato == 2: #Caso Motore Sotto Inverter 
        DRIVESdb.write('      ' + siglaL + UDTABB + '\n') #Creazione DB con UDT Inverter

        SINOTTICOdb.write('      vFeedBack' + siglaL + IntVarDB) #Creazione DB feedback per Sinottico

        
        MotoriInvDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBInverter + '"' + "\n\n" + RobaFineFileDB)
        
        UtenzeHMICSV.write(siglaL +comune_int_HMI + siglaL + ".HMI"+ fine_int_HMI) #Scrittura CSV utenza su HMI
        UtenzeHMICSV.write('SINOTTICO_vFeedBack' + siglaL +comune_IntInv_HMI + siglaL + fine_int_HMI) #Scrittura CSV vFeedBack Utenza su HMI
        UtenzeHMICSV.write(siglaL + '_vMan' + comune_int_HMI + siglaL + ".vMan"+ fine_int_HMI) #Scrittura CSV Velocità Manuale su HMI
         
        MotoriFena.write(RobaInizioFileDB + '"' + 'FENA01_' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBFenaDB + '"' + "\n\n" + RobaFineFileDB)

        FCFENAtmp = FCFENA.replace('---',siglaL) 
        
        InverterABBTXT.write(FCFENAtmp + '\n\n\n\n\n')

        if Descr != ' ' : #Se ho la descrizione aggiuntiva del motore
                                                                        ### RICHIAMO FB IN FC MOTORI INVERTER ###
            
            MotoriInvFCTXT.write(f"// {siglaL} - Inverter {siglaL} ({Descr})\n//\n{siglaL}.vAuto := REAL_TO_INT(VELINV.{siglaL}cruise); \n#invall := (NOT DRIVES.{siglaL}.FAULT) OR {siglaL}.pSim; \n#allExt := A_INV{siglaL}L; \n{siglaL}(II_preset := #preset, \nOO_aRisp => A_{siglaL},OO_aInv => A_ALL{siglaL}A, \nI_fbA := DRIVES.{siglaL}.RUNNING, \nI_invAll := #invAll, \nIO_Alarm := #allExt, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA => DRIVES.{siglaL}.START);\n\n") #Richiamo FB

                                                                        ### ALLARME INVERTER MANCATA RISPOSTA ###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeInverter + siglaL + ' ' + '('  + Descr + ')' #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI
                
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Mancata Risposta)

                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeInverter + siglaL + ' ' + '('  + Descr + ')' #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI
                
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Mancata Risposta)

                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker
                

                                                                        ### ALLARME INVERTER LETTURA ###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeLetturaInverter + siglaL + ' ' + '('  + Descr + ')' #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAllInvL + siglaL + 'L' + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI
                
                AllarmiPLCCSV.write(PrefAllInvL + siglaL + 'L;' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Lettura)

                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker
            
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeLetturaInverter + siglaL + ' ' + '('  + Descr + ')' #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAllInvL + siglaL + 'L' + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI
                
                AllarmiPLCCSV.write(PrefAllInvL + siglaL + 'L;' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Lettura)

                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker


                                                                        ### ALLARME INVERTER ANOMALIA ###   

            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeAnomaliaInverter + siglaL + ' ' + '('  + Descr + ')' #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)

                AllarmiUtenzeHMICSV.write(PrefAllInvA + siglaL + 'A' + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI

                AllarmiPLCCSV.write(PrefAllInvA + siglaL + 'A;' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Anomalia)

                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker

            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeAnomaliaInverter + siglaL + ' ' + '('  + Descr + ')' #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)

                AllarmiUtenzeHMICSV.write(PrefAllInvA + siglaL + 'A' + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI

                AllarmiPLCCSV.write(PrefAllInvA + siglaL + 'A;' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Anomalia)

                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker                
        
        else: #Se non ho la descrizione aggiuntiva del motore
                                                                        ### RICHIAMO FB IN FC MOTORI INVERTER ###
            
            MotoriInvFCTXT.write(f"// {siglaL} - Inverter {siglaL}\n//\n{siglaL}.vAuto := REAL_TO_INT(VELINV.{siglaL}cruise); \n#invall := (NOT DRIVES.{siglaL}.FAULT) OR {siglaL}.pSim; \n#allExt := A_INV{siglaL}L; \n{siglaL}(II_preset := #preset, \nOO_aRisp => A_{siglaL},OO_aInv => A_ALL{siglaL}A, \nI_fbA := DRIVES.{siglaL}.RUNNING, \nI_invAll := #invAll, \nIO_Alarm := #allExt, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA => DRIVES.{siglaL}.START);\n\n") #Richiamo FB


                                                                        ### ALLARME INVERTER MANCATA RISPOSTA ###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeInverter + siglaL #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)

                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI
                
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Mancata Risposta)

                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeInverter + siglaL #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)

                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI
                
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Mancata Risposta)

                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker


                                                                        ### ALLARME INVERTER LETTURA ###

            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeLetturaInverter + siglaL #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)

                AllarmiUtenzeHMICSV.write(PrefAllInvL + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI
                
                AllarmiPLCCSV.write(PrefAllInvL + siglaL + 'L;' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Lettura)

                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeLetturaInverter + siglaL #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)

                AllarmiUtenzeHMICSV.write(PrefAllInvL + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI
                
                AllarmiPLCCSV.write(PrefAllInvL + siglaL + 'L;' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Lettura)

                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker

                                                                        ### ALLARME INVERTER ANOMALIA ###   
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeAnomaliaInverter + siglaL  #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)

                AllarmiUtenzeHMICSV.write(PrefAllInvA + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI

                AllarmiPLCCSV.write(PrefAllInvA + siglaL + 'A;' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Anomalia)

                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeAnomaliaInverter + siglaL  #Cat Testo Allarme per HMI
                
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione indirizzo da Siemens a Wonderware (Legacy)

                AllarmiUtenzeHMICSV.write(PrefAllInvA + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi HMI

                AllarmiPLCCSV.write(PrefAllInvA + siglaL + 'A;' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n') #Allarme Inverter (Anomalia)

                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato) #Chiamo la Funzione per incrementare conta allarmi ed Aerea Merker             

    if analizzato == 3: #Caso Motore Soft Starter
        MotoriInvDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBInverter + '"' + "\n\n" + RobaFineFileDB)
        UtenzeHMICSV.write(siglaL +comune_int_HMI + siglaL + ".HMI"+ fine_int_HMI) #Scrittura CSV utenza su HMI
        
        if Descr != ' ': #Se Ho la Descrizione Del SoftStarter
            IngressiCSV.write(PrefIng + 'R'  + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoRM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Risposta Motore
            IngressiCSV.write(PrefIng + 'ALL' + siglaL + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoASS + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Risposta Motore
            UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoCM + ' ' + siglaL + ' (' + Descr  + ');' + '\n' ) #Uscita Motore Singola 
            MotoriInvFCTXT.write(f"// {siglaL} - Softstarter {siglaL} ({Descr})\n{siglaL}(II_preset := #preset, \nOO_aRisp => A_{siglaL},OO_aInv => A_{siglaL}A, \nI_fbA := I_R{siglaL}, \nI_invAll := I_ALL{siglaL}, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA => U{siglaL});\n\n") #Richiamo FB
                                                                                            ###MANCATA RISPOSTA###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeMotore + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeMotore + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
            
                                                                                        ###ANOMALIA SOFTSTARTER###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeAnomaliaSS + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + siglaL + 'A;' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + 'A' + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeAnomaliaSS + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + siglaL + 'A;' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + 'A' + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
        
        else:#Se Non Ho la Descrizione Del Softstarter
            IngressiCSV.write(PrefIng + 'R'  + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoRM + ' ' + siglaL + ';' + '\n' ) #Risposta Motore
            IngressiCSV.write(PrefIng + 'ALL'  + siglaL + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoASS + ' ' + siglaL +';' + '\n' ) #Risposta Motore
            UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoCM + ' ' + siglaL + ';' + '\n' ) #Uscita Motore Singola
            MotoriInvFCTXT.write(f"// {siglaL} - Softstarter {siglaL} \n{siglaL}(II_preset := #preset, \nOO_aRisp => A_{siglaL},OO_aInv => A_{siglaL}A, \nI_fbA := I_R{siglaL}, \nI_invAll := I_ALL{siglaL}A, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA => U{siglaL});\n\n") #Richiamo FB
 
                                                                                            ###MANCATA RISPOSTA###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeMotore + siglaL 
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeMotore + siglaL
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
            
                                                                                        ###ANOMALIA SOFTSTARTER###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeAnomaliaSS + siglaL + ' ' 
                AllarmiPLCCSV.write(PrefAll + siglaL + 'A;' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + 'A' + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeAnomaliaSS + siglaL + ' '
                AllarmiPLCCSV.write(PrefAll + siglaL + 'A;' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + 'A' + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

    if analizzato == 4: #Caso Filtro
     if Descr != ' ' : #Se ho la descrizione aggiuntiva del motore
        UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoCF + ' ' + siglaL + ' (' + Descr  + ');' + '\n' ) #Uscita Filtro
        UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
        Motoridb.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBmotore + '"' + "\n\n" + RobaFineFileDB)
        if IngressoAL != ' ' and IngressoBL != ' ': #Se ho Due Ingressi ho sia La Risposta che La Soglia di Allarme
            IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + 'FILTRO' + ' ' + siglaL + ' (' + Descr + ') IN ALLARME '  + ';' + '\n' ) #Ingresso Filtro in Allarme Ing A
            IngressiCSV.write(PrefIng + 'R' + siglaL + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoRF + ' ' + siglaL + ' ' + Descr + ';' + '\n' ) #Risposta Filtro Ing B
            FCfiltro = f"#Rfiltri := I_R{siglaL} AND U{siglaL};\n//     {siglaL}    Filtro {siglaL} ( {Descr} )     \n{siglaL}(OO_arisp=> A_{siglaL}, \nII_preset:=#preset, \nI_fbA:= #RFiltri, \nI_powerOk:=#Power_OK, \nIO_Alarm:=#dummy, \nI_man:= m_abilMan, \nI_auto:=m_abilAuto, \nI_reset:=#rip, \nO_outA:= U{siglaL});\n\n" #Richiamo FB
            FiltriFCTXT.write(FCfiltro)
                                                                            ### MANCANZA DI ALIMENTAZIONE ###            
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeFiltro + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFiltro + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                                                                    ###  PRESSIONE NON OK ###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeFiltroPressione + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + 'PR' + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + 'PR' + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFiltroPressione + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + 'PR' + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + 'PR' + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

        elif IngressoAL != ' ': #Se Ho solo l'INGRESSO A
            IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + 'FILTRO' + ' ' + siglaL + ' (' + Descr + ') IN ALLARME '  + ';' + '\n' ) #Ingresso Filtro in Allarme Ing A
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeFiltro + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFiltro + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                                                                    ###  PRESSIONE NON OK ###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeFiltroPressione + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + 'PR' + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + 'PR' + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFiltroPressione + siglaL + ' ' + '('  + Descr + ')'
                AllarmiPLCCSV.write(PrefAll + 'PR' + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + 'PR' + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
            FCfiltro = f"#Rfiltri := U{siglaL};\n//     {siglaL}    Filtro {siglaL} ( {Descr} )     \n{siglaL}(OO_arisp=> A_{siglaL}, \nII_preset:=#preset, \nI_fbA:= #RFiltri, \nI_powerOk:=#Power_OK, \nIO_Alarm:=#dummy, \nI_man:= m_abilMan, \nI_auto:=m_abilAuto, \nI_reset:=#rip, \nO_outA:= U{siglaL});\n\n" #Richiamo FB
            FiltriFCTXT.write(FCfiltro)

     else: #Se non ho la descrizione aggiuntiva del filtro 
        UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoCF + ' ' + siglaL + ';' + '\n' ) #Uscita Filtro
        UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
        Motoridb.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBmotore + '"' + "\n\n" + RobaFineFileDB)
        if IngressoAL != ' ' and IngressoBL != ' ': #Se ho Due Ingressi ho sia La Risposta che La Soglia di Allarme
            IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + 'FILTRO' + ' ' + siglaL + ' IN ALLARME '  + ';' + '\n' ) #Ingresso Filtro in Allarme Ing A
            IngressiCSV.write(PrefIng + 'R' + siglaL + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoRF + ' ' + siglaL + ';' + '\n' ) #Risposta Filtro Ing B
            FCfiltro = f"#Rfiltri := I_R{siglaL} AND U{siglaL};\n//     {siglaL}    Filtro {siglaL}     \n{siglaL}(OO_arisp=> A_{siglaL}, \nII_preset:=#preset, \nI_fbA:= #RFiltri, \nI_powerOk:=#Power_OK, \nIO_Alarm:=#dummy, \nI_man:= m_abilMan, \nI_auto:=m_abilAuto, \nI_reset:=#rip, \nO_outA:= U{siglaL});\n\n" #Richiamo FB
            FiltriFCTXT.write(FCfiltro)
                                                                            ### MANCANZA DI ALIMENTAZIONE ###            
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeFiltro + siglaL
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFiltro + siglaL
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                                                                    ###  PRESSIONE NON OK ###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeFiltroPressione + siglaL
                AllarmiPLCCSV.write(PrefAll + 'PR' + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + 'PR' + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFiltroPressione + siglaL
                AllarmiPLCCSV.write(PrefAll + 'PR' + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + 'PR' + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

        elif IngressoAL != ' ': #Se Ho solo l'uscita A
            IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + 'FILTRO' + ' ' + siglaL + ' IN ALLARME '  + ';' + '\n' ) #Ingresso Filtro in Allarme Ing A
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeFiltro + siglaL
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFiltro + siglaL
                AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                                                                    ###  PRESSIONE NON OK ###
            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + areaL + AllarmeFiltroPressione + siglaL
                AllarmiPLCCSV.write(PrefAll + 'PR' + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + 'PR' + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFiltroPressione + siglaL
                AllarmiPLCCSV.write(PrefAll + 'PR' + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                AllarmiUtenzeHMICSV.write(PrefAll + 'PR' + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
            FCfiltro = f"#Rfiltri := U{siglaL};\n//     {siglaL}    Filtro {siglaL}      \n{siglaL}(OO_arisp=> A_{siglaL}, \nII_preset:=#preset, \nI_fbA:= #RFiltri, \nI_powerOk:=#Power_OK, \nIO_Alarm:=#dummy, \nI_man:= m_abilMan, \nI_auto:=m_abilAuto, \nI_reset:=#rip, \nO_outA:= U{siglaL});\n\n" #Richiamo FB
            FiltriFCTXT.write(FCfiltro)

    if analizzato == 5: #Caso Serranda Monostabile
            UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura Valvola Su HMI
            ValvoleMonoDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBvalve + '"' + "\n\n" + RobaFineFileDB)
            if Descr != ' ' : #Se ho la descrizione aggiuntiva della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
                
                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due Finecorsa
                        ValvoleMonoFCTXT.write(f"//     Valvola {siglaL} ({Descr})   \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => A_{siglaL}, \nI_fbA := I_{siglaL}A, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Comando Valvola

                        IngressiCSV.write(PrefIng + siglaL + 'A' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A (' + Descr + ');' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'C' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCC

                    elif (IngressoAL != ' ' and IngressoBL == ' ') or (IngressoAL == ' ' and IngressoBL != ' ') and UscitAL != ' ': #Se solo ingresso A o solo ingresso B --> Un finecorsa
                        if IngressoAL != ' ': #Se entro nel ciclo ed ho solo l'FCA
                            UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Comando Valvola

                            IngressiCSV.write(PrefIng + siglaL  + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Risposta FCA
                            
                            ValvoleMonoFCTXT.write(f"//     Valvola {siglaL} ({Descr})   \n#fbB := NOT  I_{siglaL}A ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := I_{siglaL}A , \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")
                        elif IngressoBL != ' ': #Se entro nel ciclo ed ho solo FCC
                            UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Comando Valvola

                            IngressiCSV.write(PrefIng + siglaL  + 'C;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCC                     

                            ValvoleMonoFCTXT.write(f"//      Valvola {siglaL} ({Descr})  \n#fbA := NOT  I_{siglaL}C ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")
                    elif (IngressoAL and IngressoBL == ' ') and UscitAL != ' ': #Se non ho Input Genero Solo uscita

                        ValvoleMonoFCTXT.write(f"//     Valvola {siglaL} ({Descr}) No Micro  \n#fbB := NOT  U{siglaL} ; \n#fbA :=  U{siglaL}; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Comando Valvola
                        
            else: #Se non ho la descrizione della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL 

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL 

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                
                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due Finecorsa
                        ValvoleMonoFCTXT.write(f"//     Valvola {siglaL}   \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => A_{siglaL}, \nI_fbA := I_{siglaL}A, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola

                        IngressiCSV.write(PrefIng + siglaL + 'A' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A;' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'C' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C;' + '\n' ) #Risposta FCC

                    elif (IngressoAL != ' ' and IngressoBL == ' ') or (IngressoAL == ' ' and IngressoBL != ' ') and UscitAL != ' ': #Se solo ingresso A o solo ingresso B --> Un finecorsa
                        if IngressoAL != ' ': #Se entro nel ciclo ed ho solo l'FCA
                            UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola

                            IngressiCSV.write(PrefIng + siglaL  + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A;' + '\n' ) #Risposta FCA
                            
                            ValvoleMonoFCTXT.write(f"//     Valvola {siglaL}  \n#fbB := NOT  I_{siglaL}A ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := I_{siglaL}A , \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")
                        elif IngressoBL != ' ': #Se entro nel ciclo ed ho solo FCC
                            UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola

                            IngressiCSV.write(PrefIng + siglaL  + 'C;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C;' + '\n' ) #Risposta FCC                     

                            ValvoleMonoFCTXT.write(f"//      Valvola {siglaL} \n#fbA := NOT  I_{siglaL}C ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")
                    elif (IngressoAL and IngressoBL == ' ') and UscitAL != ' ': #Se non ho Input Genero Solo uscita

                        ValvoleMonoFCTXT.write(f"//     Valvola {siglaL} no micro  \n#fbB := NOT  U{siglaL} ; \n#fbA :=  U{siglaL}; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Comando Valvola

    if analizzato == 6: #Caso Serranda Bistabile
            UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura Valvola Su HMI
            ValvoleBiDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBvalve + '"' + "\n\n" + RobaFineFileDB)
            if Descr != ' ' : #Se ho la descrizione aggiuntiva della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                
                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due fc
                        ValvoleBiFCTXT.write(f"//     Valvola {siglaL} ({Descr})   \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => A_{siglaL}, \nI_fbA := I_{siglaL}A, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}C);\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Comando Valvola Aperta 

                        UsciteCSV.write(PrefUsc + siglaL + 'C;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'C (' + Descr + ');' + '\n' ) #Comando Valvola Chiusa

                        IngressiCSV.write(PrefIng + siglaL + 'A' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A (' + Descr + ');' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'C' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCC

                    elif (IngressoAL != ' ' and IngressoBL == ' ') or (IngressoAL == ' ' and IngressoBL != ' ') and UscitAL != ' ': #Se solo ingresso A o solo ingresso B --> Un finecorsa
                        if IngressoAL != ' ': #Se entro nel ciclo ed ho solo l'FCA
                            UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Comando Valvola Aperta 
                        
                            UsciteCSV.write(PrefUsc + siglaL + 'C;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'C (' + Descr + ');' + '\n' ) #Comando Valvola Chiusa

                            IngressiCSV.write(PrefIng + siglaL  + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCA
                            
                            ValvoleBiFCTXT.write(f"//     Valvola {siglaL} ({Descr})   \n#fbB := NOT  I_{siglaL}A ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := I_{siglaL}A , \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}C);\n\n")
                        elif IngressoBL != ' ': #Se entro nel ciclo ed ho solo FCB
                            UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Comando Valvola Aperta 
                        
                            UsciteCSV.write(PrefUsc + siglaL + 'C;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'C (' + Descr + ');' + '\n' ) #Comando Valvola Chiusa

                            IngressiCSV.write(PrefIng + siglaL  + 'C;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCC                     

                            ValvoleBiFCTXT.write(f"//      Valvola {siglaL} ({Descr})  \n#fbA := NOT  I_{siglaL}C ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}C);\n\n")
                    elif (IngressoAL and IngressoBL == ' ') and (UscitAL != ' ' and UscitBL != ' '): #Se non ho Input Genero Solo uscita

                        ValvoleBiFCTXT.write(f"//     Valvola {siglaL} ({Descr}) No Micro  \n#fbB :=  U{siglaL}C ; \n#fbA :=  U{siglaL}A; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}C);\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Comando Valvola Aperta 
                        
                        UsciteCSV.write(PrefUsc + siglaL + 'C;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'C (' + Descr + ');' + '\n' ) #Comando Valvola Chiusa
                        
            else: #Se non ho la descrizione della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL 

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                    
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL 

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due Finecorsa
                        ValvoleBiFCTXT.write(f"//     Valvola {siglaL}   \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => A_{siglaL}, \nI_fbA := I_{siglaL}A, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}C);\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Aperta 
                        
                        UsciteCSV.write(PrefUsc + siglaL + 'C;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Chiusa

                        IngressiCSV.write(PrefIng + siglaL + 'A' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A;' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'C' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C;' + '\n' ) #Risposta FCC

                    elif (IngressoAL != ' ' and IngressoBL == ' ') or (IngressoAL == ' ' and IngressoBL != ' ') and UscitAL != ' ': #Se solo ingresso A o solo ingresso B --> Un finecorsa
                        if IngressoAL != ' ': #Se entro nel ciclo ed ho solo l'FCA
                            UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Aperta 
                            
                            UsciteCSV.write(PrefUsc + siglaL + 'C;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Chiusa

                            IngressiCSV.write(PrefIng + siglaL  + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A;' + '\n' ) #Risposta FCA
                            
                            ValvoleBiFCTXT.write(f"//     Valvola {siglaL}  \n#fbB := NOT  I_{siglaL}A ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := I_{siglaL}A , \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}C);\n\n")
                        elif IngressoBL != ' ': #Se entro nel ciclo ed ho solo FCC
                            UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Aperta 
                            
                            UsciteCSV.write(PrefUsc + siglaL + 'C;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Chiusa

                            IngressiCSV.write(PrefIng + siglaL  + 'C;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C;' + '\n' ) #Risposta FCC                     

                            ValvoleBiFCTXT.write(f"//      Valvola {siglaL} \n#fbA := NOT  I_{siglaL}C ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}, \nO_outB := U{siglaL}C);\n\n")
                    elif (IngressoAL and IngressoBL == ' ') and UscitAL != ' ': #Se non ho Input Genero Solo uscita

                        ValvoleBiFCTXT.write(f"//     Valvola {siglaL} no micro  \n#fbB :=  U{siglaL}C ; \n#fbA :=  U{siglaL}A; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}, \nO_outB := U{siglaL}C);\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Aperta 
                        
                        UsciteCSV.write(PrefUsc + siglaL + 'C;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Chiusa
    
    if analizzato == 7: #Caso Deviatrice Monostabile
            UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura Valvola Su HMI
            ValvoleMonoDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBvalve + '"' + "\n\n" + RobaFineFileDB)
            if Descr != ' ' : #Se ho la descrizione aggiuntiva della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)              

                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due Finecorsa
                        ValvoleMonoFCTXT.write(f"//     Valvola {siglaL} ({Descr})   \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => A_{siglaL}, \nI_fbA := I_{siglaL}A, \nI_fbB := I_{siglaL}B, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Comando Valvola

                        IngressiCSV.write(PrefIng + siglaL + 'A' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A (' + Descr + ');' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'B' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'B (' + Descr + ');' + '\n' ) #Risposta FCC

                    elif (IngressoAL != ' ' and IngressoBL == ' ') or (IngressoAL == ' ' and IngressoBL != ' ') and UscitAL != ' ': #Se solo ingresso A o solo ingresso B --> Un finecorsa
                        if IngressoAL != ' ': #Se entro nel ciclo ed ho solo l'FCA
                            UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Comando Valvola

                            IngressiCSV.write(PrefIng + siglaL  + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Risposta FCA
                            
                            ValvoleMonoFCTXT.write(f"//     Valvola {siglaL} ({Descr})   \n#fbB := NOT  I_{siglaL}A ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := I_{siglaL}A , \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")
                        elif IngressoBL != ' ': #Se entro nel ciclo ed ho solo FCC
                            UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Comando Valvola

                            IngressiCSV.write(PrefIng + siglaL  + 'B;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCC                     

                            ValvoleMonoFCTXT.write(f"//      Valvola {siglaL} ({Descr})  \n#fbA := NOT  I_{siglaL}B ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := I_{siglaL}B, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")
                    elif (IngressoAL and IngressoBL == ' ') and UscitAL != ' ': #Se non ho Input Genero Solo uscita

                        ValvoleMonoFCTXT.write(f"//     Valvola {siglaL} ({Descr}) No Micro  \n#fbB := NOT  U{siglaL} ; \n#fbA :=  U{siglaL}; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Comando Valvola
                        
            else: #Se non ho la descrizione della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL 

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL 

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)


                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due Finecorsa
                        ValvoleMonoFCTXT.write(f"//     Valvola {siglaL}   \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => A_{siglaL}, \nI_fbA := I_{siglaL}A, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola

                        IngressiCSV.write(PrefIng + siglaL + 'A' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A;' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'B' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'B;' + '\n' ) #Risposta FCC

                    elif (IngressoAL != ' ' and IngressoBL == ' ') or (IngressoAL == ' ' and IngressoBL != ' ') and UscitAL != ' ': #Se solo ingresso A o solo ingresso B --> Un finecorsa
                        if IngressoAL != ' ': #Se entro nel ciclo ed ho solo l'FCA
                            UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola

                            IngressiCSV.write(PrefIng + siglaL  + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A;' + '\n' ) #Risposta FCA
                            
                            ValvoleMonoFCTXT.write(f"//     Valvola {siglaL}  \n#fbB := NOT  I_{siglaL}A ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := I_{siglaL}A , \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")
                        elif IngressoBL != ' ': #Se entro nel ciclo ed ho solo FCC
                            UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola

                            IngressiCSV.write(PrefIng + siglaL  + 'C;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C;' + '\n' ) #Risposta FCC                     

                            ValvoleMonoFCTXT.write(f"//      Valvola {siglaL} \n#fbA := NOT  I_{siglaL}C ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")
                    elif (IngressoAL and IngressoBL == ' ') and UscitAL != ' ': #Se non ho Input Genero Solo uscita

                        ValvoleMonoFCTXT.write(f"//     Valvola {siglaL} no micro  \n#fbB := NOT  U{siglaL} ; \n#fbA :=  U{siglaL}; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL});\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Comando Valvola

    if analizzato == 8: #Caso Deviatrice Bistabile
                UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura Valvola Su HMI
                ValvoleBiDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBvalve + '"' + "\n\n" + RobaFineFileDB)
                if Descr != ' ' : #Se ho la descrizione aggiuntiva della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                        

                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due fc
                        ValvoleBiFCTXT.write(f"//     Valvola {siglaL} ({Descr})   \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => A_{siglaL}, \nI_fbA := I_{siglaL}A, \nI_fbB := I_{siglaL}B, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}B);\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Comando Valvola Aperta 

                        UsciteCSV.write(PrefUsc + siglaL + 'B;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'B (' + Descr + ');' + '\n' ) #Comando Valvola Chiusa

                        IngressiCSV.write(PrefIng + siglaL + 'A' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A (' + Descr + ');' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'B' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'B (' + Descr + ');' + '\n' ) #Risposta FCC

                    elif (IngressoAL != ' ' and IngressoBL == ' ') or (IngressoAL == ' ' and IngressoBL != ' ') and UscitAL != ' ': #Se solo ingresso A o solo ingresso B --> Un finecorsa
                        if IngressoAL != ' ': #Se entro nel ciclo ed ho solo l'FCA
                            UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Comando Valvola Aperta 
                        
                            UsciteCSV.write(PrefUsc + siglaL + 'B;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'B (' + Descr + ');' + '\n' ) #Comando Valvola Chiusa

                            IngressiCSV.write(PrefIng + siglaL  + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'B (' + Descr + ');' + '\n' ) #Risposta FCA
                            
                            ValvoleBiFCTXT.write(f"//     Valvola {siglaL} ({Descr})   \n#fbB := NOT  I_{siglaL}A ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := I_{siglaL}A , \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}B);\n\n")
                        elif IngressoBL != ' ': #Se entro nel ciclo ed ho solo FCB
                            UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Comando Valvola Aperta 
                        
                            UsciteCSV.write(PrefUsc + siglaL + 'B;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'B (' + Descr + ');' + '\n' ) #Comando Valvola Chiusa

                            IngressiCSV.write(PrefIng + siglaL  + 'B;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'B (' + Descr + ');' + '\n' ) #Risposta FCC                     

                            ValvoleBiFCTXT.write(f"//      Valvola {siglaL} ({Descr})  \n#fbA := NOT  I_{siglaL}C ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := I_{siglaL}B, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}B);\n\n")
                    elif (IngressoAL and IngressoBL == ' ') and (UscitAL != ' ' and UscitBL != ' '): #Se non ho Input Genero Solo uscita

                        ValvoleBiFCTXT.write(f"//     Valvola {siglaL} ({Descr}) No Micro  \n#fbB :=  U{siglaL}C ; \n#fbA :=  U{siglaL}A; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}B);\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Comando Valvola Aperta 
                        
                        UsciteCSV.write(PrefUsc + siglaL + 'B;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'B (' + Descr + ');' + '\n' ) #Comando Valvola Chiusa
                else: #Se non ho la descrizione della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL 

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL 

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due Finecorsa
                        ValvoleBiFCTXT.write(f"//     Valvola {siglaL}   \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => A_{siglaL}, \nI_fbA := I_{siglaL}A, \nI_fbB := I_{siglaL}B, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}B);\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Aperta 
                        
                        UsciteCSV.write(PrefUsc + siglaL + 'B;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Chiusa

                        IngressiCSV.write(PrefIng + siglaL + 'A' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A;' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'B' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'B;' + '\n' ) #Risposta FCC

                    elif (IngressoAL != ' ' and IngressoBL == ' ') or (IngressoAL == ' ' and IngressoBL != ' ') and UscitAL != ' ': #Se solo ingresso A o solo ingresso B --> Un finecorsa
                        if IngressoAL != ' ': #Se entro nel ciclo ed ho solo l'FCA
                            UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A;' + '\n' ) #Comando Valvola Aperta 
                            
                            UsciteCSV.write(PrefUsc + siglaL + 'B;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'B;' + '\n' ) #Comando Valvola Chiusa

                            IngressiCSV.write(PrefIng + siglaL  + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A;' + '\n' ) #Risposta FCA
                            
                            ValvoleBiFCTXT.write(f"//     Valvola {siglaL}  \n#fbB := NOT  I_{siglaL}A ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := I_{siglaL}A , \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outB := U{siglaL}B);\n\n")
                        elif IngressoBL != ' ': #Se entro nel ciclo ed ho solo FCC
                            UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Aperta 
                            
                            UsciteCSV.write(PrefUsc + siglaL + 'B;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + ';' + '\n' ) #Comando Valvola Chiusa

                            IngressiCSV.write(PrefIng + siglaL  + 'B;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'B;' + '\n' ) #Risposta FCC                     

                            ValvoleBiFCTXT.write(f"//      Valvola {siglaL} \n#fbA := NOT  I_{siglaL}B ; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}, \nO_outB := U{siglaL}B);\n\n")
                    elif (IngressoAL and IngressoBL == ' ') and UscitAL != ' ': #Se non ho Input Genero Solo uscita

                        ValvoleBiFCTXT.write(f"//     Valvola {siglaL} no micro  \n#fbB :=  U{siglaL}B ; \n#fbA :=  U{siglaL}A; \n{siglaL}(II_preset := #preset, \nII_bistabile := #bist, \nOO_arisp => #dummy, \nI_fbA := #fbA, \nI_fbB := #fbB, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}, \nO_outB := U{siglaL}B);\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A;' + '\n' ) #Comando Valvola Aperta 
                        
                        UsciteCSV.write(PrefUsc + siglaL + 'B;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'B;' + '\n' ) #Comando Valvola Chiusa

    if analizzato == 9: #Caso Valvola Manuale
            UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura Valvola Su HMI
            ValvoleManDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBvalve + '"' + "\n\n" + RobaFineFileDB)
            if Descr != ' ' : #Se ho la descrizione aggiuntiva della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due Finecorsa
                        ValvoleManFCTXT.write(f"// Valvola {siglaL} ({Descr})\nIF I_{siglaL}A = TRUE\nTHEN\n    {siglaL}.fbA := True;\n    {siglaL}.fbB := FALSE;\n    {siglaL}.HMI.%X8 := True;\n    {siglaL}.HMI.%X9 := FALSE;\nEND_IF;\n\nIF I_{siglaL}C = TRUE\nTHEN\n    {siglaL}.fbA := FALSE;\n   {siglaL}.fbB := TRUE;\n    {siglaL}.HMI.%X8 := FALSE;\n    {siglaL}.HMI.%X9 := True;\nEND_IF;\n\nIF A_{siglaL} = TRUE \nTHEN \n    {siglaL}.all := TRUE; \n     {siglaL}.HMI.%X15 := TRUE; \nELSE \n    {siglaL}.all := FALSE; \n    {siglaL}.HMI.%X15 := FALSE; \nEND_IF;\n\n\n\n")

                        IngressiCSV.write(PrefIng + siglaL + 'A' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A (' + Descr + ');' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'C' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCC

                    elif (IngressoAL != ' ' and IngressoBL == ' ') or (IngressoAL == ' ' and IngressoBL != ' ') and UscitAL != ' ': #Se solo ingresso A o solo ingresso B --> Un finecorsa
                        if IngressoAL != ' ': #Se entro nel ciclo ed ho solo l'FCA

                            IngressiCSV.write(PrefIng + siglaL  + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A (' + Descr + ');' + '\n' ) #Risposta FCA
                            
                            ValvoleManFCTXT.write(f"// Valvola {siglaL} ({Descr})\n IF I_{siglaL}A = TRUE\nTHEN \n    {siglaL}.fbA := True; \n    {siglaL}.fbB := FALSE; \n    {siglaL}.HMI.%X8 := True; \n    {siglaL}.HMI.%X9 := FALSE; \nELSE \n    {siglaL}.fbA := FALSE; \n    {siglaL}.fbB := TRUE; \n    {siglaL}.HMI.%X8 := False; \n    {siglaL}.HMI.%X9 := True; \nEND_IF; \nIF A_{siglaL} = TRUE \nTHEN \n    {siglaL}.all := TRUE; \n    {siglaL}.HMI.%X15 := TRUE; \nELSE \n    {siglaL}.all := FALSE; \n    {siglaL}.HMI.%X15 := FALSE; \nEND_IF\n\n\n\n;")
                        
                        elif IngressoBL != ' ': #Se entro nel ciclo ed ho solo FCC
                            
                            IngressiCSV.write(PrefIng + siglaL  + 'C;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCC                     

                            ValvoleManFCTXT.write(f"// Valvola {siglaL} ({Descr})\n IF I_{siglaL}C = TRUE \nTHEN \n    {siglaL}.fbB := True; \n    {siglaL}.fbA := FALSE; \n    {siglaL}.HMI.%X9 := True; \n    {siglaL}.HMI.%X8 := FALSE; \nELSE \n    {siglaL}.fbB := FALSE; \n    {siglaL}.fbA := TRUE; \n    {siglaL}.HMI.%X9 := False; \n    {siglaL}.HMI.%X8 := True; \nEND_IF; \nIF A_{siglaL} = TRUE \nTHEN \n    {siglaL}.all := TRUE; \n    {siglaL}.HMI.%X15 := TRUE; \nELSE \n    {siglaL}.all := FALSE; \n    {siglaL}.HMI.%X15 := FALSE; \nEND_IF;\n\n\n\n")
                    
                    ####elif (IngressoAL and IngressoBL == ' ') and UscitAL != ' ': #Se non ho Input Genero Solo uscita            
            else: #Se non ho la descrizione della valvola
                    if areaL.__contains__('VERDE'):                        
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL 

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL 

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                
                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due Finecorsa
                        ValvoleManFCTXT.write(f"// Valvola {siglaL} \nIF I_{siglaL}A = TRUE\nTHEN\n    {siglaL}.fbA := True;\n    {siglaL}.fbB := FALSE;\n    {siglaL}.HMI.%X8 := True;\n    {siglaL}.HMI.%X9 := FALSE;\nEND_IF;\n\nIF I_{siglaL}C = TRUE\nTHEN\n    {siglaL}.fbA := FALSE;\n   {siglaL}.fbB := TRUE;\n    {siglaL}.HMI.%X8 := FALSE;\n    {siglaL}.HMI.%X9 := True;\nEND_IF;\n\nIF A_{siglaL} = TRUE \nTHEN \n    {siglaL}.all := TRUE; \n     {siglaL}.HMI.%X15 := TRUE; \nELSE \n    {siglaL}.all := FALSE; \n    {siglaL}.HMI.%X15 := FALSE; \nEND_IF;\n\n\n\n")

                        IngressiCSV.write(PrefIng + siglaL + 'A' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A (' + Descr + ');' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'C' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCC
                    elif (IngressoAL != ' ' and IngressoBL == ' ') or (IngressoAL == ' ' and IngressoBL != ' ') and UscitAL != ' ': #Se solo ingresso A o solo ingresso B --> Un finecorsa
                        if IngressoAL != ' ': #Se entro nel ciclo ed ho solo l'FCA
                            
                            IngressiCSV.write(PrefIng + siglaL  + 'A;' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'A (' + Descr + ');' + '\n' ) #Risposta FCA
                            
                            ValvoleManFCTXT.write(f"// Valvola {siglaL} \n IF I_{siglaL}A = TRUE\nTHEN \n    {siglaL}.fbA := True; \n    {siglaL}.fbB := FALSE; \n    {siglaL}.HMI.%X8 := True; \n    {siglaL}.HMI.%X9 := FALSE; \nELSE \n    {siglaL}.fbA := FALSE; \n    {siglaL}.fbB := TRUE; \n    {siglaL}.HMI.%X8 := False; \n    {siglaL}.HMI.%X9 := True; \nEND_IF; \nIF A_{siglaL} = TRUE \nTHEN \n    {siglaL}.all := TRUE; \n    {siglaL}.HMI.%X15 := TRUE; \nELSE \n    {siglaL}.all := FALSE; \n    {siglaL}.HMI.%X15 := FALSE; \nEND_IF\n\n\n\n;")
                        
                        elif IngressoBL != ' ': #Se entro nel ciclo ed ho solo FCC
                            
                            IngressiCSV.write(PrefIng + siglaL  + 'C;' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCC                     

                            ValvoleManFCTXT.write(f"// Valvola {siglaL} ({Descr})\n IF I_{siglaL}C = TRUE \nTHEN \n    {siglaL}.fbB := True; \n    {siglaL}.fbA := FALSE; \n    {siglaL}.HMI.%X9 := True; \n    {siglaL}.HMI.%X8 := FALSE; \nELSE \n    {siglaL}.fbB := FALSE; \n    {siglaL}.fbA := TRUE; \n    {siglaL}.HMI.%X9 := False; \n    {siglaL}.HMI.%X8 := True; \nEND_IF; \nIF A{siglaL}A = TRUE \nTHEN \n    {siglaL}.all := TRUE; \n    {siglaL}.HMI.%X15 := TRUE; \nELSE \n    {siglaL}.all := FALSE; \n    {siglaL}.HMI.%X15 := FALSE; \nEND_IF;\n\n\n\n")
                    
    if analizzato == 10: #Caso Valvola Parziale 
                UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura Valvola Su HMI
                ValvoleParzDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FPvalveParz + '"' + "\n\n" + RobaFineFileDB)
                if Descr != ' ' : #Se ho la descrizione aggiuntiva della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)    
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL + ' ' + '('  + Descr + ')'

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due fc
                        ValvoleParzFCTXT.write(f"//     Valvola Parziale {siglaL} ({Descr})   \n{siglaL}(II_preset := #preset, \nOO_arisp => A_{siglaL}, \nI_fbP := I_{siglaL}M, \nI_fbC := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outC := U{siglaL}C, \nIO_unCom:= #unComando);\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A (' + Descr + ');' + '\n' ) #Comando Valvola Aperta 

                        UsciteCSV.write(PrefUsc + siglaL + 'C;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'C (' + Descr + ');' + '\n' ) #Comando Valvola Chiusa

                        IngressiCSV.write(PrefIng + siglaL + 'M' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'M (' + Descr + ');' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'C' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C (' + Descr + ');' + '\n' ) #Risposta FCC
                if Descr == ' ': #Se non ho la Descrizione Aggiuntiva della valvola
                    if areaL.__contains__('VERDE'):
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeValvola + siglaL + ' '

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)    
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeValvola + siglaL + ' '

                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n')

                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC)

                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                    if IngressoBL != ' ' and IngressoAL != ' ': #Se ho sia Ingresso A che Ingresso B --> Due fc
                        ValvoleParzFCTXT.write(f"//     Valvola Parziale {siglaL}   \n{siglaL}(II_preset := #preset, \nOO_arisp => A_{siglaL}, \nI_fbP := I_{siglaL}M, \nI_fbC := I_{siglaL}C, \nI_powerOk := #tmp, \nI_man := m_abilMan, \nI_auto := m_abilAuto, \nI_reset := #rip, \nO_outA := U{siglaL}A, \nO_outC := U{siglaL}C, \nIO_unCom:= #unComando);\n\n")

                        UsciteCSV.write(PrefUsc + siglaL + 'A;' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'A' + ';' + '\n' ) #Comando Valvola Aperta 

                        UsciteCSV.write(PrefUsc + siglaL + 'C;' + 'Bool' + ';' + UscitBL + RobaInMezzoPLCTAGS + CommentoVM + ' ' + siglaL + 'C' + ';' + '\n' ) #Comando Valvola Chiusa

                        IngressiCSV.write(PrefIng + siglaL + 'M' + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'M' + ';' + '\n' ) #Risposta FCA

                        IngressiCSV.write(PrefIng + siglaL + 'C' + ';' + 'Bool' + ';' + IngressoBL + RobaInMezzoPLCTAGS + CommentoFC + ' FC' + siglaL + 'C' + ';' + '\n' ) #Risposta FCC                        
                     
    if analizzato == 11: #Caso Sensore

        DigiAnalog = False #0 = Sens Digitale \ #1 = Sens Analogico

        LvLmin = False #Livello Minimo 

        LvLmax = False #Livello Massimo 

        LvLmed = False #Livello Medio

        CtrlRot = False #Controllo di Rotazione

        FCx = False #Finecorsa Di sicurezza

        FineCorsa = False #Finecorsa
            
        FinecDistr = False #Finecorsa Distributore ad Fc - Triggerato dal finecorsa con il nome della batteria dentro

        PRx = False #Pressostato di Sicurezza

        Pres = False #Pressostato

        VTx = False #Vuotostato di Sicurezza 

        TSx = False #Alte emissioni Soglia di preallarme

        Ts = False #Emissioni alte o sonda non collegata

        Vuot = False #Vuotostato

        PEm = False #Pulsante Di emergenza

        Vdc24 = False  #Aux24V

        PButton = False #Push Button

        Sele = False #Selettore

        Vac400 = False #Ingersso Tensione 400VAC

        Vac300 = False #Ingresso Tensione 300VAC

        Tacit = False #Ingresso Tacitazione

        Ripr = False #Ingresso Ripristino
            
        termic = False #Ingresso Cumulativo Termici

        pilz = False #Ingresso Catena PILZ
        
        if Descr != ' ' : #Se ho la descrizione aggiuntiva del sensore

            if IngressoAL.__contains__('PEW') :
                DigiAnalog = True
            
            ### Looppo le varianti di sensori che si possono incontrare ###
            if DigiAnalog == False: #Caso Sensore Digitale
                for prefxMin in NomenLivelliMinimo:
                    if siglaL.upper().__contains__(prefxMin):
                        LvLmin = True
                for prefxMax in NomenLivelliMassimo:
                    if siglaL.upper().__contains__(prefxMax):
                        LvLmax = True
                for prefMed in NomenLivelliMedio:
                    if siglaL.upper().__contains__(prefMed):
                        LvLmed = True
                if siglaL.upper().__contains__('CR'):
                    CtrlRot = True
                if siglaL.upper().__contains__('FCX'):
                    FCx = True
                if siglaL.upper().__contains__('FC') and not FCx :
                    FineCorsa = True
                if FineCorsa == True and (siglaL.upper().__contains__('B1') or siglaL.upper().__contains__('B2') or siglaL.upper().__contains__('B3') or siglaL.upper().__contains__('B4')):
                    FineCorsa = False
                    FinecDistr = True
                if siglaL.upper().__contains__('RIPRISTINO'):
                    Ripr = True                 
                for prefxPR in NomenPrx:
                    if siglaL.upper().__contains__(prefxPR) and not Ripr:
                        PRx = True
                if siglaL.upper().__contains__('PR') and not PRx and not Ripr:
                    Pres = True
                if siglaL.upper().__contains__('VTX'):
                    VTx = True
                if siglaL.upper().__contains__('VT') and not VTx:
                    Vuot = True
                if siglaL.upper().__contains__('TSX'):
                    TSx = True
                if siglaL.upper().__contains__('TS') and not TSx:
                    Ts = True
                    ###Contatti digitali non sensori
                if siglaL.upper().__contains__('24VDC'):
                    Vdc24 = True
                if siglaL.upper().__contains__('PB_EM') and not Vdc24:
                    PEm = True
                if siglaL.upper().__contains__('PB_') and not PEm: 
                    PButton = True
                if siglaL.upper().__contains__('SEL_'):
                    Sele = True
                if siglaL.upper().__contains__('400V'):
                    Vac400 = True
                if siglaL.upper().__contains__('300V'):
                    Vac300 = True
                if siglaL.upper().__contains__('TACITAZIONE'):
                    Tacit = True                
                if siglaL.upper().__contains__('TERMICO'):
                    termic = True                    
                if siglaL.upper().__contains__('PILZ'):
                    pilz = True     



                ListaVarietàSensori = [LvLmin, LvLmed, LvLmax, CtrlRot, FCx, FineCorsa, FinecDistr, PRx, Pres, VTx, Vuot,TSx,Ts, Vdc24,PEm,PButton,Sele,Vac400,Vac300,Tacit,Ripr,termic,pilz]
                if not any(ListaVarietàSensori):
                    print('Non è stata Identificata la Variante del sensore digitale presente alla seguente riga: ' + str(ContaRighe) + ' [' + siglaL + ']' + '\nChiusura programma...')
                    raise SystemExit
                
                SensoriDigitaliDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBsensDIG + '"' + "\n\n" + RobaFineFileDB)
                
                if LvLmin: #Se il sensore digitale è un Livello Di Minimo
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoLL + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Livello Minimo

                   SensoriDigitaliFCTXT.write(f"// Livello Di Minimo  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")
                   
                   if areaL.__contains__('VERDE'):
                
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeLL + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Livello  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeLL + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Livello  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                    

                if LvLmax: #Se il sensore digitale è un Livello di Massimo
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoLH + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Livello Massimo

                   SensoriDigitaliFCTXT.write(f"// Livello Di Massimo  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")
                   
                   if areaL.__contains__('VERDE'):
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeLH + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Livello  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeLH + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Livello  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
                       
                if LvLmed: #Se il sensore digitale è un Livello di Medio
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoLM + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Livello Massimo

                   SensoriDigitaliFCTXT.write(f"// Livello Di Medio  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")
                   
                   UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI

                   #No allarme, è solo livello "Di processo"

                if CtrlRot: #Se il sensore digitale è un Controllo di Rotazione
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoCR + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Controllo di Rotazione

                   SensoriDigitaliFCTXT.write(f"// Controllo Di Rotazione  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeCR + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Controllo di Rotazione  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeCR + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Controllo di Rotazione  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                    
                
                if FCx: #Se il sensore digitale è un Finecorsa Di Sicurezza

                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFCX + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Finecorsa di Sicurezza
                
                   SensoriDigitaliFCTXT.write(f"// Finecorsa Di Sicurezza  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):     
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeFCX + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Finecorsa di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFCX + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Finecorsa di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if FineCorsa: #Se il sensore digitale è un FineCorsa 
                   
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' ' + AllSpecificoL.upper() + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Finecorsa
                
                   SensoriDigitaliFCTXT.write(f"// Finecorsa  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AllarmeFC = ' - ' + AllSpecificoL.upper() + ' - '

                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeFC + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Finecorsa  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'): 
                    AllarmeFC = ' - ' + AllSpecificoL.upper() + ' - '

                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFC + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Finecorsa  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
                
                if FinecDistr: #Se il sensore digitale è un Finecorsa di un distributore
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' ' + AllSpecificoL.upper() + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Finecorsa
                
                   SensoriDigitaliFCTXT.write(f"// Finecorsa {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")                    

                   UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                
                if PRx: #Se il sensore digitale è un pressostato di sicurezza
                   
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoPRX + ' ' + siglaL  + ' ' + FineCommentoPRX + ' (' + Descr + ');' + '\n' ) #Ingresso Pressostato di Sicurezza
                
                   SensoriDigitaliFCTXT.write(f"// Pressostato Di Sicurezza  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmePRX + siglaL + ' - ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Pressostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmePRX + siglaL + ' - ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Pressostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
                
                if Pres: #Se il sensore digitale è un presosstato                    

                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoPR + ' ' + siglaL  + ' ' + FineCommentoPR + ' (' + Descr + ');' + '\n' ) #Ingresso Pressostato
                
                   SensoriDigitaliFCTXT.write(f"// Pressostato  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmePR + siglaL + ' - ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Pressostato  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmePR + siglaL + ' - ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Pressostato  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                       

                if VTx: #Se il sensore digitale è un Vuotostato di sicurezza
                    
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoVTX + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Vuotostato di Sicurezza
                
                   SensoriDigitaliFCTXT.write(f"// Vuotostato Di Sicurezza  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeVTX + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeVTX + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if Vuot: #Se il sensore digitale è un Vuotostato
                   
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoVT + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Vuotostato
                
                   SensoriDigitaliFCTXT.write(f"// Vuotostato   {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")
                
                   if areaL.__contains__('VERDE'):                     
                        AlarmCMT = StrAllarmeIndice + areaL + AllarmeVT + siglaL + ' ' + '('  + Descr + ')'
                        
                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato  
                                
                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeVT + siglaL + ' ' + '('  + Descr + ')'
                        
                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato  
                                
                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                    

                if TSx: #Se il sensore digitale è una sonda emissioni (Allarme)
                    
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoTSX + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Sonda Emissioni
                
                   SensoriDigitaliFCTXT.write(f"// Sonda Emissioni Soglia Allarme {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeTSX + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Emissioni Alte Sonda Emissioni
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeTSX + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Emissioni Alte Sonda Emissioni
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if Ts: #Se il sensore digitale è una sonda emissioni (Preallarme)
                    
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoTS + ' ' + siglaL + ' (' + Descr + ');' + '\n' ) #Ingresso Emissioni Preallarme
                
                   SensoriDigitaliFCTXT.write(f"// Sonda Emissioni Soglia Preallarme {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeTs + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Soglia di preallarme raggiunta
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeTs + siglaL + ' ' + '('  + Descr + ')'
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Soglia di preallarme raggiunta
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if Vdc24: #Se l'ingresso è un VDC24
                    IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + Commento24VDC + ' (' + Descr.replace('24VDC','') + ');' + '\n' ) #Ingresso AUX 24VDC

                    SensoriDigitaliFCTXT.write(f"// 24VDC  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL.replace('_OK','')});\n\n")

                    if areaL.__contains__('VERDE'):

                        AlarmCMT = StrAllarmeIndice + areaL + Allarme24VDC + ' ('  + Descr + ')'
                    
                        AllarmiPLCCSV.write(PrefAll + siglaL.replace('_OK','') + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 24VDC   
                                
                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL.replace('_OK','') + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  

                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + Allarme24VDC + ' ('  + Descr + ')'
                        
                        AllarmiPLCCSV.write(PrefAll + siglaL.replace('_OK','') + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato  
                                
                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL.replace('_OK','') + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                    

                if PEm: #Se l'ingresso è un Pulsante di emergenza
                    IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoPE + siglaL[6:] + ' (' + Descr.upper() + ') PREMUTA ;' + '\n' ) #Ingresso Pulsante Emergenza

                    SensoriDigitaliFCTXT.write(f"// Emergenza {siglaL[6:]} {AllSpecificoL}  ({Descr}) PREMUTA \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_PEM_{siglaL[6:]}_{areaL});\n\n")

                    if areaL.__contains__('VERDE'):

                        AlarmCMT = StrAllarmeIndice + areaL + AllarmePE + ' '  + siglaL[6:] + ' ' + AllSpecificoL.upper() + ' ('  + Descr + ') PREMUTA'
                    
                        AllarmiPLCCSV.write(PrefAll + 'PEM_' + siglaL[6:] + '_' + areaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 24VDC   
                                
                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + 'PEM_' + siglaL[6:] + '_' + areaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                    if areaL.__contains__('TOSTATO'):

                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmePE + ' '  + siglaL[6:] + ' ' + AllSpecificoL.upper() + ' ('  + Descr + ') PREMUTA'
                    
                        AllarmiPLCCSV.write(PrefAll + 'PEM_' + siglaL[6:] + '_' + areaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 24VDC   
                                
                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + 'PEM_' + siglaL[6:] + '_' + areaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
                
                if PButton: #Se l'ingresso è un Pulsante
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoPButton + ' ' + siglaL[3:] + ' (' + Descr + ');' + '\n' ) #Ingresso Pulsante
                
                   SensoriDigitaliFCTXT.write(f"// Pulsante {siglaL[3:]} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")

                if Sele:#Se l'ingresso è un Selettore

                    IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoSele + ' ' + siglaL[4:] + ' (' + Descr + ');' + '\n' ) #Ingresso Pulsante
                
                    SensoriDigitaliFCTXT.write(f"// Selettore {siglaL[4:]} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")
  
                if Vac400: #Se l'ingresso è un 400Vok
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + Commento400V + ';' + '\n' ) #Ingresso Vuotostato di Sicurezza
                
                   SensoriDigitaliFCTXT.write(f"// Tensione 400V  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + Allarme400V
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'): 

                    AlarmCMT = StrAllarmeIndiceTostato + areaL + Allarme400V
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if Vac300: #Se l'ingresso è un 300Vok
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + Commento300V + ';' + '\n' ) #Ingresso Vuotostato di Sicurezza
                
                   SensoriDigitaliFCTXT.write(f"// Tensione 300V  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + Allarme300V
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):

                    AlarmCMT = StrAllarmeIndiceTostato + areaL + Allarme300V
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                
                
                if Tacit: #Se l'ingresso è una tacitazione
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoTacit + ' (' + Descr + ');' + '\n' ) #Ingresso Ripristino
                
                   SensoriDigitaliFCTXT.write(f"// Tacitazione Allarmi \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")

                if Ripr: #Se l'ingresso è un ripristino
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoTacit + ' (' + Descr + ');' + '\n' ) #Ingresso Tacitazione
                
                   SensoriDigitaliFCTXT.write(f"// Ripristino Allarmi  \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")

                if termic: #Se l'ingresso è un cumulativo termici
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoTERM + ';' + '\n' ) #Ingresso Termici
                
                   SensoriDigitaliFCTXT.write(f"// Cumulativo Termici quadro {areaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL}_{areaL});\n\n")
                   
                   if areaL.__contains__('VERDE'): 

                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeTERMIC
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + '_' + areaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ' ' + areaL + ';\n' ) #Allarme Cumulativo termici
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + '_' + areaL + SystemIO_DISC + AlarmCMT + ' ' + areaL + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + ' ' + areaL + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeTERMIC
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + '_' + areaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ' ' + areaL + ';\n' ) #Allarme Cumulativo termici
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + '_' + areaL + SystemIO_DISC + AlarmCMT + ' ' + areaL + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + ' ' + areaL + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                       

                if pilz: #Se l'ingresso è un PILZ 
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoPILZ + ';' + '\n' ) #Ingresso Termici
                
                   SensoriDigitaliFCTXT.write(f"// Emergenza Generale Pilz {areaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL[:5]}EM_{areaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmePILZ
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL[:5] + 'EM_' + areaL+ ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ' ' + areaL + ';\n' ) #Allarme pilz  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL[:5] + 'EM_' + areaL + SystemIO_DISC + AlarmCMT + ' ' + areaL + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + ' ' + areaL + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmePILZ
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL[:5] + 'EM_' + areaL+ ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ' ' + areaL + ';\n' ) #Allarme pilz  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL[:5] + 'EM_' + areaL + SystemIO_DISC + AlarmCMT + ' ' + areaL + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + ' ' + areaL + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato )                   
                                           
            else:
                print("Sensore Analogico Ancora Non Supportato")
        
        else: #Se Non ho la descrizione del sensore
            if DigiAnalog == False: #Caso Sensore Digitale
                for prefxMin in NomenLivelliMinimo:
                    if siglaL.upper().__contains__(prefxMin):
                        LvLmin = True
                for prefxMax in NomenLivelliMassimo:
                    if siglaL.upper().__contains__(prefxMax):
                        LvLmax = True
                for prefMed in NomenLivelliMedio:
                    if siglaL.upper().__contains__(prefMed):
                        LvLmed = True
                if siglaL.upper().__contains__('CR'):
                    CtrlRot = True
                if siglaL.upper().__contains__('FCX'):
                    FCx = True
                if siglaL.upper().__contains__('FC') and not FCx :
                    FineCorsa = True
                if FineCorsa == True and (siglaL.upper().__contains__('B1') or siglaL.upper().__contains__('B2') or siglaL.upper().__contains__('B3') or siglaL.upper().__contains__('B4')):
                    FineCorsa = False
                    FinecDistr = True
                if siglaL.upper().__contains__('RIPRISTINO'):
                    Ripr = True                 
                for prefxPR in NomenPrx:
                    if siglaL.upper().__contains__(prefxPR) and not Ripr:
                        PRx = True
                if siglaL.upper().__contains__('PR') and not PRx and not Ripr:
                    Pres = True
                if siglaL.upper().__contains__('VTX'):
                    VTx = True
                if siglaL.upper().__contains__('VT') and not VTx:
                    Vuot = True
                if siglaL.upper().__contains__('TSX'):
                    TSx = True
                if siglaL.upper().__contains__('TS') and not TSx:
                    Ts = True
                    ###Contatti digitali non sensori
                if siglaL.upper().__contains__('24VDC'):
                    Vdc24 = True
                if siglaL.upper().__contains__('PB_EM') and not Vdc24:
                    PEm = True
                if siglaL.upper().__contains__('PB_') and not PEm: 
                    PButton = True
                if siglaL.upper().__contains__('SEL_'):
                    Sele = True
                if siglaL.upper().__contains__('400V'):
                    Vac400 = True
                if siglaL.upper().__contains__('300V'):
                    Vac300 = True
                if siglaL.upper().__contains__('TACITAZIONE'):
                    Tacit = True                
                if siglaL.upper().__contains__('TERMICO'):
                    termic = True                    
                if siglaL.upper().__contains__('PILZ'):
                    pilz = True     



                ListaVarietàSensori = [LvLmin, LvLmed, LvLmax, CtrlRot, FCx, FineCorsa, FinecDistr, PRx, Pres, VTx, Vuot,TSx,Ts, Vdc24,PEm,PButton,Sele,Vac400,Vac300,Tacit,Ripr,termic,pilz]
                if not any(ListaVarietàSensori):
                    print('Non è stata Identificata la Variante del sensore digitale presente alla seguente riga: ' + str(ContaRighe) + ' [' + siglaL + ']' + '\nChiusura programma...')
                    raise SystemExit
                
                SensoriDigitaliDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBsensDIG + '"' + "\n\n" + RobaFineFileDB)
                
                if LvLmin: #Se il sensore digitale è un Livello Di Minimo
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoLL + ' ' + siglaL + ';' + '\n' ) #Ingresso Livello Minimo

                   SensoriDigitaliFCTXT.write(f"// Livello Di Minimo  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if  areaL.__contains__('VERDE'):
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeLL + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Livello  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeLL + siglaL
                        
                        AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Livello  
                                
                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                        UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
                
                if LvLmax: #Se il sensore digitale è un Livelli di Massimo
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoLH + ' ' + siglaL +  ';' + '\n' ) #Ingresso Livello Massimo

                   SensoriDigitaliFCTXT.write(f"// Livello Di Massimo  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeLH + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Livello  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeLH + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Livello  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
                                       
                if LvLmed: #Se il sensore digitale è un Livello di Medio
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoLM + ' ' + siglaL + ';' + '\n' ) #Ingresso Livello Massimo

                   SensoriDigitaliFCTXT.write(f"// Livello Di Medio  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")
                   
                   UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI

                   #No allarme, è solo livello "Di processo"

                if CtrlRot: #Se il sensore digitale è un Controllo di Rotazione
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoCR + ' ' + siglaL + ';' + '\n' ) #Ingresso Controllo di Rotazione

                   SensoriDigitaliFCTXT.write(f"// Controllo Di Rotazione  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeCR + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Controllo di Rotazione  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeCR + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Controllo di Rotazione  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)   

                if FCx: #Se il sensore digitale è un Finecorsa Di Sicurezza

                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFCX + ' ' + siglaL + ';' + '\n' ) #Ingresso Finecorsa di Sicurezza
                
                   SensoriDigitaliFCTXT.write(f"// Finecorsa Di Sicurezza  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeFCX + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Finecorsa di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFCX + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Finecorsa di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                       

                if FineCorsa: #Se il sensore digitale è un FineCorsa 
                   
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' ' + AllSpecificoL + ' ' + siglaL + ';' + '\n' ) #Ingresso Finecorsa
                
                   SensoriDigitaliFCTXT.write(f"// Finecorsa  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AllarmeFC = ' - ' + AllSpecificoL + ' - '

                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeFC + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Finecorsa  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'):
                    AllarmeFC = ' - ' + AllSpecificoL + ' - '

                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeFC + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Finecorsa  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if FinecDistr: #Se il sensore digitale è un Finecorsa di un distributore
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoFC + ' ' + AllSpecificoL.upper() + ' ' + siglaL + ';' + '\n' ) #Ingresso Finecorsa
                
                   SensoriDigitaliFCTXT.write(f"// Finecorsa {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")                    

                   UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                
                if PRx: #Se il sensore digitale è un pressostato di sicurezza
                   
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoPRX + ' ' + siglaL  + ' ' + FineCommentoPRX + ';' + '\n' ) #Ingresso Pressostato di Sicurezza
                
                   SensoriDigitaliFCTXT.write(f"// Pressostato Di Sicurezza  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):

                    AlarmCMT = StrAllarmeIndice + areaL + AllarmePRX + siglaL 
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Pressostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmePRX + siglaL 
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Pressostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if Pres: #Se il sensore digitale è un presosstato                    

                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoPR + ' ' + siglaL  + ' ' + FineCommentoPR + ';' + '\n' ) #Ingresso Pressostato
                
                   SensoriDigitaliFCTXT.write(f"// Pressostato  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmePR + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Pressostato  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmePR + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Pressostato  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)                     
                
                if VTx: #Se il sensore digitale è un Vuotostato di sicurezza
                    
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoVTX + ' ' + siglaL + ';' + '\n' ) #Ingresso Vuotostato di Sicurezza
                
                   SensoriDigitaliFCTXT.write(f"// Vuotostato Di Sicurezza  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")
                   
                   if areaL.__contains__('VERDE'):

                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeVTX + siglaL 
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   
                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeVTX + siglaL 
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                       
                                      
                if Vuot: #Se il sensore digitale è un Vuotostato
                   
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoVT + ' ' + siglaL + ';' + '\n' ) #Ingresso Vuotostato
                
                   SensoriDigitaliFCTXT.write(f"// Vuotostato   {siglaL}  \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")


                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeVT + siglaL 
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeVT + siglaL 
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)                    

                if TSx: #Se il sensore digitale è una sonda emissioni (Allarme)
                    
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoTSX + ' ' + siglaL + ';' + '\n' ) #Ingresso Sonda Emissioni
                
                   SensoriDigitaliFCTXT.write(f"// Sonda Emissioni Soglia Allarme {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeTSX + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Emissioni Alte Sonda Emissioni
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeTSX + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Emissioni Alte Sonda Emissioni
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if Ts: #Se il sensore digitale è una sonda emissioni (Preallarme)
                    
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoTS + ' ' + siglaL + ';' + '\n' ) #Ingresso Emissioni Preallarme
                
                   SensoriDigitaliFCTXT.write(f"// Sonda Emissioni Soglia Preallarme {siglaL}  \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeTs + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Soglia di preallarme raggiunta
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeTs + siglaL
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Soglia di preallarme raggiunta
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)

                    UtenzeHMICSV.write(siglaL+comune_int_HMI+siglaL+".HMI"+fine_int_HMI) #Scrittura CSV utenza su HMI
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if Vdc24: #Se l'ingresso è un VDC24
                    IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + Commento24VDC + ';' + '\n' ) #Ingresso AUX 24VDC

                    SensoriDigitaliFCTXT.write(f"// Ausiliari 24VDC  {siglaL}  \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_V{siglaL[3:8]}_{areaL});\n\n")

                    if areaL.__contains__('VERDE'):

                        AlarmCMT = StrAllarmeIndice + areaL + Allarme24VDC
                    
                        AllarmiPLCCSV.write(PrefAll + siglaL[3:8] + '_' + areaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 24VDC   
                                
                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + 'V' + siglaL[3:8] + '_' + areaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + Allarme24VDC
                    
                        AllarmiPLCCSV.write(PrefAll + siglaL[3:8] + '_' + areaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 24VDC   
                                
                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + 'V' + siglaL[3:8] + '_' + areaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
                        
                if PEm: #Se l'ingresso è un Pulsante di emergenza
                    IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoPE + siglaL[6:] + ' PREMUTA ;' + '\n' ) #Ingresso Pulsante Emergenza

                    SensoriDigitaliFCTXT.write(f"// Emergenza {siglaL[6:]} {AllSpecificoL} PREMUTA \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_PEM_{siglaL[6:]}_{areaL});\n\n")

                    if areaL.__contains__('VERDE'):

                        AlarmCMT = StrAllarmeIndice + areaL + AllarmePE + ' '  + siglaL[6:] + ' ' + AllSpecificoL.upper() + ' PREMUTA'
                    
                        AllarmiPLCCSV.write(PrefAll + 'PEM_' + siglaL[6:] + '_' + areaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 24VDC   
                                
                        InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + 'PEM_' + siglaL[6:] + '_' + areaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                        ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                    
                    if areaL.__contains__('TOSTATO'):
                        AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmePE + ' '  + siglaL[6:] + ' ' + AllSpecificoL.upper() + ' PREMUTA'
                    
                        AllarmiPLCCSV.write(PrefAll + 'PEM_' + siglaL[6:] + '_' + areaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme 24VDC   
                                
                        InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                            
                        AllarmiUtenzeHMICSV.write(PrefAll + 'PEM_' + siglaL[6:] + '_' + areaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                        ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if PButton: #Se l'ingresso è un Pulsante
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoPButton + ' ' + siglaL[3:] + ';' + '\n' ) #Ingresso Pulsante
                
                   SensoriDigitaliFCTXT.write(f"// Pulsante {siglaL[3:]} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")

                if Sele:#Se l'ingresso è un Selettore

                    IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoSele + ' ' + siglaL[4:] + ';' + '\n' ) #Ingresso Pulsante
                
                    SensoriDigitaliFCTXT.write(f"// Selettore {siglaL[4:]} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")
  
                if Vac400: #Se l'ingresso è un 400Vok
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + Commento400V + ';' + '\n' ) #Ingresso Vuotostato di Sicurezza
                
                   SensoriDigitaliFCTXT.write(f"// Tensione 400V  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + Allarme400V
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'): 

                    AlarmCMT = StrAllarmeIndiceTostato + areaL + Allarme400V
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if Vac300: #Se l'ingresso è un 300Vok
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + Commento300V + ';' + '\n' ) #Ingresso Vuotostato di Sicurezza
                
                   SensoriDigitaliFCTXT.write(f"// Tensione 300V  {siglaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL});\n\n")
                   
                   if areaL.__contains__('VERDE'):

                    AlarmCMT = StrAllarmeIndice + areaL + Allarme300V
                        
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                                
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                            
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)

                   if areaL.__contains__('TOSTATO'):                 
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + Allarme300V
                        
                    AllarmiPLCCSV.write(PrefAll + siglaL + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Vuotostato di Sicurezza  
                                
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                            
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                            
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)
                
                if Tacit: #Se l'ingresso è una tacitazione
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoTacit + ';' + '\n' ) #Ingresso Ripristino
                
                   SensoriDigitaliFCTXT.write(f"// Tacitazione Allarmi \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")

                if Ripr: #Se l'ingresso è un ripristino
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoTacit + ';' + '\n' ) #Ingresso Tacitazione
                
                   SensoriDigitaliFCTXT.write(f"// Ripristino Allarmi  \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")

                if termic: #Se l'ingresso è un cumulativo termici
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoTERM + ';' + '\n' ) #Ingresso Termici
                
                   SensoriDigitaliFCTXT.write(f"// Cumulativo Termici quadro {areaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL}_{areaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmeTERMIC
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + '_' + areaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ' ' + areaL + ';\n' ) #Allarme Cumulativo termici
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + '_' + areaL + SystemIO_DISC + AlarmCMT + ' ' + areaL + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + ' ' + areaL + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
                   
                   if areaL.__contains__('TOSTATO'): 
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmeTERMIC
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL + '_' + areaL + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ' ' + areaL + ';\n' ) #Allarme Cumulativo termici
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL + '_' + areaL + SystemIO_DISC + AlarmCMT + ' ' + areaL + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + ' ' + areaL + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

                if pilz: #Se l'ingresso è un PILZ 
                   IngressiCSV.write(PrefIng + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + CommentoPILZ + ';' + '\n' ) #Ingresso Termici
                
                   SensoriDigitaliFCTXT.write(f"// Emergenza Generale Pilz {areaL} \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc, \n         allarme := A_{siglaL[:5]}EM_{areaL});\n\n")

                   if areaL.__contains__('VERDE'):
                   
                    AlarmCMT = StrAllarmeIndice + areaL + AllarmePILZ
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL[:5] + 'EM_' + areaL+ ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ' ' + areaL + ';\n' ) #Allarme pilz  
                            
                    InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL[:5] + 'EM_' + areaL + SystemIO_DISC + AlarmCMT + ' ' + areaL + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + ' ' + areaL + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)   

                   if areaL.__contains__('TOSTATO'):
                    AlarmCMT = StrAllarmeIndiceTostato + areaL + AllarmePILZ
                    
                    AllarmiPLCCSV.write(PrefAll + siglaL[:5] + 'EM_' + areaL+ ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ' ' + areaL + ';\n' ) #Allarme pilz  
                            
                    InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                        
                    AllarmiUtenzeHMICSV.write(PrefAll + siglaL[:5] + 'EM_' + areaL + SystemIO_DISC + AlarmCMT + ' ' + areaL + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + ' ' + areaL + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                        
                    ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)   
                       
    if analizzato == 12: #Caso SPARE
        if IngressoAL != ' ':
            SpareINTing = SpareINTing + 1 
            IngressiCSV.write(PrefIng + 'SPARE'  + str(SpareINTing) + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + 'INGRESSO SPARE ;' + '\n' ) #Ingresso Spare 
        if UscitAL != ' ':
            SpareINTusc = SpareINTusc + 1
            UsciteCSV.write(PrefUsc + 'SPARE'  + str(SpareINTusc) + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + 'USCITA SPARE ;' + '\n' ) #Uscita Spare 
        
        if UscitAL == ' ' and IngressoAL == ' ' :

            if areaL.__contains__('VERDE'):
                AlarmCMT = StrAllarmeIndice + "ALLARME SPARE " + str(IndiceAllarme)
            
                AllarmiPLCCSV.write(PrefAll + "SPARE" + str(IndiceAllarme) + ';' + 'Bool' + ';' + StrAllarmiMerker + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Motore  
                            
                InTouchAddress = StrAllarmiMerker.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                
                AllarmiUtenzeHMICSV.write(PrefAll + 'SPARE' + str(IndiceAllarme) + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                
                ContaAllarmi(ParteDecimale,ParteOttale,IndiceAllarme)
            if areaL.__contains__('TOSTATO'):
                AlarmCMT = StrAllarmeIndiceTostato + "ALLARME SPARE " + str(IndiceAllarmeTostato)
            
                AllarmiPLCCSV.write(PrefAll + "SPARE" + str(IndiceAllarmeTostato) + ';' + 'Bool' + ';' + StrAllarmiMerkerTostato + RobaInMezzoPLCTAGS + AlarmCMT + ';\n' ) #Allarme Motore  
                            
                InTouchAddress = StrAllarmiMerkerTostato.replace('M','MX') #Conversione Indirizzo da Siemens a Wonderware (Legacy)
                
                AllarmiUtenzeHMICSV.write(PrefAll + 'SPARE' + str(IndiceAllarmeTostato) + SystemIO_DISC + AlarmCMT + Comune_IO_DISC_HMI + InTouchAddress + Dopoindirizzo_IO_DISC + AlarmCMT + Fine_IO_DISC) #Scrittura CSV Allarmi su Hmi  
                
                ContaAllarmiTostato(ParteDecimaleTostato,ParteOttaleTostato,IndiceAllarmeTostato)

    if analizzato == 13: #Caso DIN
        if Descr != ' ':
            if IngressoAL != ' ' : 

                IngressiCSV.write(PrefIng  + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + 'Ingresso Digitale' + '(' + Descr + ')' + ';' + '\n' ) #Ingresso Digitale 
                
                SensoriDigitaliDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBsensDIG + '"' + "\n\n" + RobaFineFileDB) #DB utenza digitale
                
                SensoriDigitaliFCTXT.write(f"// Ingresso Digitale  {siglaL} ({Descr}) \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")
        if Descr == ' ':
            if IngressoAL != ' ' : 

                IngressiCSV.write(PrefIng  + siglaL + ';' + 'Bool' + ';' + IngressoAL + RobaInMezzoPLCTAGS + 'Ingresso Digitale;' + '\n' ) #Ingresso Digitale 
                
                SensoriDigitaliDB.write(RobaInizioFileDB + '"' + siglaL + '"' + "\n" + RobaInMezzoFileDB + '"' + FBsensDIG + '"' + "\n\n" + RobaFineFileDB) #DB utenza digitale
                
                SensoriDigitaliFCTXT.write(f"// Ingresso Digitale  {siglaL}  \n{siglaL}(ingresso := I_{siglaL}, \n         nc := #nc);\n\n")

    if analizzato == 14: #Caso DOUT
        if UscitAL != ' ': 
            UsciteCSV.write(PrefUsc  + siglaL + ';' + 'Bool' + ';' + UscitAL + RobaInMezzoPLCTAGS + 'Uscita Digitale;' + '\n' ) #Uscita Digitale
                    

    ContaRighe = ContaRighe + 1


InverterABBTXT.close() #Chiusura Handle File FCInverterABB.txt

IngressiCSV.close() #Chiusura handle file Ingressi.csv

Motoridb.close() #Chiusura handle file motori.db

UsciteCSV.close() #Chiusura handle file Uscite.csv

AllarmiUtenzeHMICSV.close() #Chiusura handle file AllarmiUtenze.csv

UtenzeHMICSV.close() #Chiusura handle file UtenzeHMI.csv

AllarmiPLCCSV.close() #Chiusura handle file Allarmi.csv

SINOTTICOdb.write(RobaFineFileDBABB) #Appendo footer file DB per MotoriInvFC.db
SINOTTICOdb.close() #Chiusura handle file SINOTTICO.db

FiltriFCTXT.close() #Chiusura handle file FiltriFC.txt

MotoreFCTXT.close() #Chiusura handle file FCMotori.txt

MotoriInvFCTXT.close() #Chiusura handle file MotoriInvFC.txt

DRIVESdb.write(RobaFineFileDBABB) #Appendo footer file DB per ABB
DRIVESdb.close() #Chiusura handle file DRIVES.db

MotoriInvDB.close() #Chiusura handle file MotoriInvFC.txt

ValvoleMonoDB.close() #Chiusura handle file ValvoleMono.db

ValvoleMonoFCTXT.close() #Chiusura handle file ValvoleMonoFC.txt

ValvoleBiDB.close() #Chiusura handle ValvoleBi.db 

ValvoleBiFCTXT.close() #Chiusura handle ValvoleBiFC.txt

ValvoleManDB.close() #Chiusura Handle ValvoleMan.db

ValvoleManFCTXT.close() #Chiusura Handle FCValvoleMan.txt

ValvoleParzDB.close() #Chiusura Handle ValvoleParz.DB

ValvoleParzFCTXT.close() #Chiusura Handle ValvoleParzFC.txt

SensoriDigitaliDB.close() #Chiusura Handle SensoriDigitali.db

SensoriDigitaliFCTXT.close() #Chiusura Handle SensoriDigitaliFC.txt

MotoriFena.close() #Chiusura Handle db MotoriFena.db

end = time.time() #Prendo unix timestamp da epoch in sec alla fine dello script

print(f"Tempo Impiegato: {(end-start)*10**3:.03f}ms") #calcolo la differenza di tempo, ms 


