import numpy as np

class energyConsumption1:

    def __init__(self, parameters, packetEnergy, packetDelay):
        self.parameters = parameters
        self.packetEnergy = packetEnergy
        self.packetDelay = packetDelay
        self.p_ACK = 0                                  #assuming no ACKs from server
        self.L = []                                     #Latency
        self.Y = []                                     #Battery Lifetime
        self.E = []                                     #Energy
        self.D = []                                     #Delay

    #Stationary probabilities of each state and probability of UL traffic
    def p_On(self):
        return 1 - np.exp(-1/self.parameters.IAT)       #probability of having UL traffic in a ms

    def b_Off(self):
        return 1/(1+self.p_On()*(4+self.p_ACK))

    def b_RA(self):
        return self.p_On() * self.b_Off()
    
    def b_CR(self):
        return self.p_On() * self.b_Off()     #b_CR = b_RA
    
    def b_Connect(self):
        return self.p_On() * self.b_Off()     #b_Connect = b_CR
    
    def b_ACK(self):
        return self.p_ACK * self.p_On() * self.b_Off()

    def b_Inactive(self):
        return self.p_On() * self.b_Off()     #b_Inactive = b_Connect
    

    #Energy in each state
    def Off(self):
        return self.parameters.D.P_s*1
    
    def RA(self):
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40
        else: 
            T_RA_GAP = 0
        return self.parameters.D.P_i*(self.parameters.T_MIB_I+self.parameters.T_RA_Period/2.0+T_RA_GAP)+self.parameters.D.P_RX*(self.parameters.T_Sync+self.parameters.T_MIB_RX)+self.parameters.D.P_TX_RA*self.parameters.N_RA_REP*self.parameters.T_PRE

    def CR(self):
        pp = self.parameters.R_max * self.parameters.G
        return self.parameters.D.P_i*(pp/2.0+self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US)+self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=256)+self.packetEnergy.UL(L_x=72)

    def Connect(self):
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions
        E_sch_Cmp = self.parameters.D.P_i*(self.parameters.T_Period_BSR*pp+self.parameters.T_RA_Period/2.0+pp/2.0+self.parameters.T_w_DC2DS+2*self.parameters.T_w_DC2US+T_RA_GAP+T_WDC)+2*self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=256)+self.parameters.D.P_TX_RA*self.parameters.N_RA_REP*self.parameters.T_PRE+self.packetEnergy.UL(L_x=72)+self.packetEnergy.UL(L_x=16)
        return self.parameters.D.P_i*(2*self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US+2*self.parameters.T_ACK_k0+3*T_WDC)+3*self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=80)+2*self.packetEnergy.HARQ_ACK()+self.packetEnergy.UL(L_x=864)+self.packetEnergy.DL(L_y=120) +(1-self.p_ACK)*E_sch_Cmp

    def ACK(self):
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions 
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        E_sch_Cmp = self.parameters.D.P_i*(self.parameters.T_Period_BSR*pp+self.parameters.T_RA_Period/2.0+pp/2.0+self.parameters.T_w_DC2DS+2*self.parameters.T_w_DC2US+T_RA_GAP+T_WDC)+2*self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=256)+self.parameters.D.P_TX_RA*self.parameters.N_RA_REP*self.parameters.T_PRE+self.packetEnergy.UL(L_x=72)+self.packetEnergy.UL(L_x=16)
        return self.parameters.D.P_i*(T_WDC+self.parameters.T_w_DC2DS+self.parameters.T_ACK_k0)+self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=1)+self.packetEnergy.HARQ_ACK()+self.p_ACK*E_sch_Cmp
        
    def Inactive(self):
        pp = self.parameters.R_max * self.parameters.G
        T_DRXi = 2#*pp
        N_CDRX_Cycles = round((self.parameters.T_Inactivity-T_DRXi)/self.parameters.T_LC)
        T_onD = min((self.parameters.T_LC/pp),self.parameters.NppOnD)*self.parameters.R_max 
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        E_CDRX = self.parameters.D.P_i*(N_CDRX_Cycles*(self.parameters.T_LC-T_onD))+self.parameters.D.P_RX*(T_DRXi+N_CDRX_Cycles*T_onD)
        E_IDRX = self.parameters.N_EDRX_Cycles*(self.parameters.D.P_s*(self.parameters.T_eDRX-self.parameters.T_PTW)+self.parameters.N_IDRX_Cycles*(self.parameters.D.P_s*(self.parameters.T_PC-(self.parameters.N_REP_DCI+self.parameters.T_IDRX_sync))+self.parameters.D.P_RX*self.parameters.N_REP_DCI+self.parameters.D.P_IDRX_sync*self.parameters.T_IDRX_sync))+self.parameters.D.P_s*(self.parameters.T_active-self.parameters.N_EDRX_Cycles*self.parameters.T_eDRX)
        E_sch_rel = self.parameters.D.P_i*(self.parameters.T_Period_BSR+self.parameters.T_RA_Period/2.0+pp/2.0+self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US+T_RA_GAP)+self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=256)+self.parameters.D.P_TX_RA*self.parameters.N_RA_REP*self.parameters.T_PRE+self.packetEnergy.DL(L_y=72) 
        E_inactive = E_CDRX+self.parameters.D.P_i*(pp/2+self.parameters.T_w_DC2DS+self.parameters.T_ACK_k0+self.parameters.T_w_IDRX)+self.packetEnergy.DL(L_y=16)+self.packetEnergy.HARQ_ACK()+E_sch_rel+E_IDRX        
        return E_inactive


    #Delay for each state
    def D_Off(self):
        return 1

    def D_RA(self):
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        return self.parameters.T_MIB_I+self.parameters.T_RA_Period/2+T_RA_GAP+self.parameters.T_Sync+self.parameters.T_MIB_RX+self.parameters.N_RA_REP*self.parameters.T_PRE

    def D_CR(self):
        pp = self.parameters.R_max * self.parameters.G
        return pp/2+self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US+self.packetDelay.DCI()+self.packetDelay.DL(L_y=256)+self.packetDelay.UL(L_x=72)

    def D_Connect(self):
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions 
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        E_sch_Cmp_delay = self.parameters.T_Period_BSR*pp+self.parameters.T_RA_Period/2+pp/2+self.parameters.T_w_DC2DS+2*self.parameters.T_w_DC2US+T_RA_GAP+T_WDC+2*self.packetDelay.DCI()+self.packetDelay.DL(L_y=256)+self.parameters.N_RA_REP*self.parameters.T_PRE+self.packetDelay.UL(L_x=72)+self.packetDelay.UL(L_x=16)
        return 2*self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US+2*self.parameters.T_ACK_k0+3*T_WDC+3*self.packetDelay.DCI()+self.packetDelay.DL(L_y=80)+2*self.packetDelay.HARQ_ACK()+self.packetDelay.UL(L_x=864)+self.packetDelay.DL(L_y=120)+(1-self.p_ACK)*E_sch_Cmp_delay

    def D_ACK(self):
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions 
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        E_sch_Cmp_delay = self.parameters.T_Period_BSR*pp+self.parameters.T_RA_Period/2+pp/2+self.parameters.T_w_DC2DS+2*self.parameters.T_w_DC2US+T_RA_GAP+T_WDC+2*self.packetDelay.DCI()+self.packetDelay.DL(L_y=256)+self.parameters.N_RA_REP*self.parameters.T_PRE+self.packetDelay.UL(L_x=72)+self.packetDelay.UL(L_x=16)
        return T_WDC+self.parameters.T_w_DC2DS+self.parameters.T_ACK_k0+self.packetDelay.DCI()+self.packetDelay.DL(L_y=1)+self.packetDelay.HARQ_ACK()+self.p_ACK*E_sch_Cmp_delay  #DLack???

    def D_Inactive(self):
        pp = self.parameters.R_max * self.parameters.G
        T_DRXi = 2*pp
        N_CDRX_Cycles = round((self.parameters.T_Inactivity-T_DRXi)/self.parameters.T_LC)
        T_onD = min((self.parameters.T_LC/pp),self.parameters.NppOnD)*self.parameters.R_max 
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        D_CDRX = N_CDRX_Cycles*(self.parameters.T_LC-T_onD)+T_DRXi+N_CDRX_Cycles*T_onD
        D_IDRX = self.parameters.N_EDRX_Cycles*(self.parameters.T_eDRX-self.parameters.T_PTW)+self.parameters.N_IDRX_Cycles*(self.parameters.T_PC-(self.parameters.N_REP_DCI+self.parameters.T_IDRX_sync))+self.parameters.N_REP_DCI+self.parameters.T_IDRX_sync+(self.parameters.T_active-self.parameters.N_EDRX_Cycles*self.parameters.T_eDRX)
        E_sch_rel_delay = self.parameters.T_Period_BSR+self.parameters.T_RA_Period/2+pp/2+self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US+T_RA_GAP+self.packetDelay.DCI()+self.packetDelay.DL(L_y=256)+self.parameters.N_RA_REP*self.parameters.T_PRE+self.packetDelay.DL(L_y=72) 
        return D_CDRX+(pp/2+self.parameters.T_w_DC2DS+self.parameters.T_ACK_k0+self.parameters.T_w_IDRX)+self.packetDelay.DL(L_y=16)+self.packetDelay.HARQ_ACK()+E_sch_rel_delay+D_IDRX

    
    #States as pairs of power levels and delays
    def Off_List(self):    
        return  [[self.parameters.D.P_s, 1]]

    def RA_List(self):
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40
        else: 
            T_RA_GAP = 0
        return [[self.parameters.D.P_i, self.parameters.T_MIB_I], [self.parameters.D.P_RX, self.parameters.T_Sync + self.parameters.T_MIB_RX], [self.parameters.D.P_i, self.parameters.T_RA_Period/2.0+T_RA_GAP], [self.parameters.D.P_TX, self.parameters.N_RA_REP*self.parameters.T_PRE]]


    def CR_List(self):
        pp = self.parameters.R_max * self.parameters.G
        
        CR = [[self.parameters.D.P_i, pp/2.0]]
        CR.extend([[self.parameters.D.P_i, self.parameters.T_w_DC2DS]])
        CR.extend(self.packetEnergy.DL_List(L_y=256))
        CR.extend(self.packetEnergy.DCI_List())
        CR.extend([[self.parameters.D.P_i, self.parameters.T_w_DC2US]])
        CR.extend(self.packetEnergy.UL_List(L_x=72))
        return CR

    def Connect_List(self):
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp
        Connect = [[self.parameters.D.P_i, 2*self.parameters.T_ACK_k0+3*T_WDC]]
        Connect.extend(self.packetEnergy.DCI_List())
        Connect.extend([[self.parameters.D.P_i, self.parameters.T_w_DC2DS]])
        Connect.extend(self.packetEnergy.DL_List(L_y=80))
        Connect.extend(self.packetEnergy.HARQ_ACK_List())
        Connect.extend(self.packetEnergy.DCI_List())
        Connect.extend([[self.parameters.D.P_i, self.parameters.T_w_DC2US]])
        Connect.extend(self.packetEnergy.UL_List(L_x=864))
        Connect.extend(self.packetEnergy.DCI_List())
        Connect.extend([[self.parameters.D.P_i, self.parameters.T_w_DC2DS]])
        Connect.extend(self.packetEnergy.DL_List(L_y=120))
        Connect.extend(self.packetEnergy.HARQ_ACK_List())
        #Connect.append(E_sch_Cmp)
        return Connect
        
    def Inactive_List(self):
        pp = self.parameters.R_max * self.parameters.G
        T_DRXi = 2*pp
        N_CDRX_Cycles = round((self.parameters.T_Inactivity-T_DRXi)/self.parameters.T_LC)
        T_onD = min((self.parameters.T_LC/pp),self.parameters.NppOnD)*self.parameters.R_max    
        Inactive = []
        for n in range(N_CDRX_Cycles):
            Inactive.extend([[self.parameters.D.P_i, self.parameters.T_LC-T_onD], [self.parameters.D.P_RX, T_onD]])
        Inactive.extend([[self.parameters.D.P_s, self.parameters.T_eDRX-self.parameters.T_PTW]])
        for i in range(self.parameters.N_IDRX_Cycles):
            Inactive.extend([[self.parameters.D.P_s, self.parameters.T_PC-(self.parameters.N_REP_DCI+self.parameters.T_IDRX_sync)]])
            Inactive.extend([[self.parameters.D.P_RX, self.parameters.N_REP_DCI]])
            Inactive.extend([[self.parameters.D.P_IDRX_sync, self.parameters.T_IDRX_sync]])
        Inactive.extend([[self.parameters.D.P_s, self.parameters.T_active - self.parameters.T_eDRX]])
        return Inactive
    
    
    #Battery lifetime estimation
    def average_energy(self):
        return self.b_Off()*self.Off()+self.b_RA()*self.RA()+self.b_CR()*self.CR()+self.b_Connect()*self.Connect()+self.b_ACK()*self.ACK()+self.b_Inactive()*self.Inactive()
    
    def average_delay(self):
        return self.b_Off()*self.D_Off()+self.b_RA()*self.D_RA()+self.b_CR()*self.D_CR()+self.b_Connect()*self.D_Connect()+self.b_ACK()*self.D_ACK()+self.b_Inactive()*self.D_Inactive()

    def EnergyDay(self):
        E_model_day = self.average_energy()*(86400000.0/self.average_delay())/1000000.0   #in J
        return E_model_day/3600.0   #in Wh

    def BatteryLifetime(self):
        return self.parameters.C_bat/(self.EnergyDay()*365.25)

    def Latency(self):
        return (self.D_Off() + self.D_RA() + self.D_CR() + self.D_Connect())/1000.0
