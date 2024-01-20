from abc import ABC
from dataclasses import dataclass

@dataclass
class Parameters_EC_Model:
    #Synchronization
    #P_IDRX_sync : float = 0        #Avg power consumption while performing short synchronizations in I-DRX        
    T_IDRX_sync : float = 250       #Avg duration of the short synchronizations during I-DRX (ms)
    T_Sync : float = 547.5          #Avg initial sync time (ms)
    T_MIB_I : float = 103           #MIB waiting time (ms)
    T_MIB_RX : float = 8            #MIB reception time (ms)

    #RA
    T_RA_Period : float = 640       #NPRACH periodicity (ms)
    T_PRE : float = 5.6             #Preamble format 0 duration (ms)
    N_RA_REP : float = 2            #Preamble repetitions

    #Gaps
    T_Gap_Period_UL : float = 296   #Gap periodicity for UL (ms)
    T_Gap_Period_DL : float = 128   #Gap periodicity for DL (ms)
    T_Gap_Dur_UL : float = 40       #Gap duration for UL (ms)
    T_Gap_Dur_DL : float = 32       #Gap duration for DL (ms) 
    DL_Gap_Thr : float = 64         #DL gap threshold

    #Scheduling
    T_w_DC2US : float = 8           #Start of NPUSCH transmission after the end of its associated DCI (ms)
    T_w_DC2DS : float = 5           #Start of NPDSCH transmission after the end of its associated DCI (ms)
    T_ACK_k0 : float = 13           #Delay for the ACK of a DL packet (ms)
    T_Period_BSR : float = 8        #Buffer Status Report (BSR) Timer (pp)

    #NPDCCH
    R_max : float = 8               #Maximum number of repetitions of NPDCCH
    G : float = 2                   #Time offset in search space period
    alpha : float = 1               #Offset of the starting SF in a search period
    #T = R_max * G                  #Seach space period
    #pp = T                         #PDCCH period, the interval between the start of two NPDCCH
    N_REP_DCI : float = 1           #8 for CSS (paging and RA process), 1 for USS (DL or UL UE’s specific scheduling information)

    #NPDSCH
    NPDSCH_MCS : float = 3          #Modulation and Coding scheme for the NPDSCH
    N_SF : float = 10               #Number of Subframes (SFs)
    NPDSCH_N_REP : float = 1        #Number of repetitions for the NPDSCH
    
    #NPUSCH
    N_PUSCH_MCS : float =  3        #Modulation and Coding scheme for the NPUSCH
    N_RU : float = 10               #Number of Resource Units (RUs)
    NPUSCH_N_REP : float = 1        #Number of repetitions for the NPUSCH
    #Number of subcarriers = 1
    #Subcarrier spacing (SCS) = 15 kHz

    #C-DRX & I-DRX
    T_DRXi : float = 2                  #Period the UE should remain monitoring NPDCCH before starting C-DRX (pp)
    T_Inactivity : float = 20*1000      #RRC Inactivity timer (s)->(ms)
    NppOnD : float = 8                  #Number of consecutive NPDCCH periods to monitor at the start of C-DRX (pp)
    T_LC : float = 2.048*1000           #C-DRX Long Cycle (s)->(ms)
    T_w_IDRX : float = 1.1*1000         #Wait before entering I-DRX after sending the RRC Release ACK (s)->(ms)
    T_PC : float = 2.56*1000            #I-DRX Paging Cycle (s)->(ms)
    T_PTW : float = 20.48*1000          #PTW cycle duration (s)->(ms)
    T_eDRX : float = 81.92*1000         #eDRX cycle duration (s)->(ms)
    T_active : int = 120*1000           #Active timer duration (s)->(ms)
    #T_onD : float = min(T_LC/pp,NppOnD)*R_max                  #On duration timer during a C-DRX cycle  
    #N_CDRX_Cycles : float = round((T_Inactivity-T_DRXi)/T_LC)  #Number of CDRX cycles
    N_EDRX_Cycles : float = round(T_active/T_eDRX)              #Number of EDRX cycles
    N_IDRX_Cycles : float = round(T_PTW/T_PC)                   #Number of IDRX cycles

    H_RLCMAC : float = 32               #RLC/MAC headers size (b)


#Device power levels (mW)
@dataclass
class device(ABC):
    P_TX : float = None
    P_TX_RA : float = None
    P_RX : float = None
    P_ULGap : float = None
    P_i : float = None
    P_s : float = None
    P_IDRX_sync : float = None

@dataclass
class deviceA(device):
    P_TX : float = 731
    P_TX_RA : float = 731
    P_RX : float = 215 
    P_ULGap : float = 128.4
    P_i : float = 17.8
    P_s : float = 0.01414
    P_IDRX_sync : float = 34.5

@dataclass
class deviceB(device):
    P_TX : float = 765
    P_TX_RA : float = 765
    P_RX : float = 242
    P_ULGap : float = 160.4
    P_i : float = 29.1
    P_s : float = 0.01113
    P_IDRX_sync : float = 65.6