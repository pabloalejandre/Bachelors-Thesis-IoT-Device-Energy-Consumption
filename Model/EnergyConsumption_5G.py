import numpy as np

class energyConsumption2:

    def __init__(self, parameters, packetEnergy, packetDelay):
        self.parameters = parameters
        self.packetEnergy = packetEnergy
        self.packetDelay = packetDelay
        self.p_ACK = 0                                  #assuming no ACKs from server
        self.L = []                                     #Latency
        self.Y = []                                     #Battery Lifetime
        self.E = []                                     #Energy
        self.D = []                                     #Delay
        

    #Transition probabilities
    def p_On(self):                                     #probability of having UL traffic in a ms
        return 1 - np.exp(-1/self.parameters.IAT)

    def p_T(self):                                      #probability of having no traffic in T ms (from Inactive to Idle)
        return 1 - np.exp(-self.parameters.T/self.parameters.IAT)

    def p_OnD(self):                                    #probability of having traffic in a OnDuration timer in a CDRX-cycle
        pp = self.parameters.R_max * self.parameters.G
        T_onD = min((self.parameters.T_LC/pp),self.parameters.NppOnD)*self.parameters.R_max
        return 1 - np.exp(-T_onD/self.parameters.IAT)           

    def p_C(self):                                      #probability of traffic arriving when in CDRX and transitioning back to Connected
        pp = self.parameters.R_max * self.parameters.G
        T_DRXi = 2*pp
        N_CDRX_Cycles = round((self.parameters.T_Inactivity-T_DRXi)/self.parameters.T_LC)
        return 1-(1-self.p_OnD())**(N_CDRX_Cycles)

    def q(self):                                        #probability of transitioning from Connected_DRX to Idle
        return self.parameters.q

    
    #Stationary probabilities of each state
    def b_Connected(self):
        return self.p_On()/(self.q()+(1-self.p_T())*(1-self.q()-self.p_C())+(5-3*self.p_C()-self.q())*self.p_On())

    def b_Idle(self):
        return (self.q()+(1-self.p_T())*(1-self.q()-self.p_C())*self.b_Connected())/self.p_On()

    def b_RA1(self):
        return (self.q()+(1-self.p_T())*(1-self.q()-self.p_C())*self.b_Connected())

    def b_RA2(self):
        return self.p_T()*(1-self.q()-self.p_C())*self.b_Connected()
    
    def b_CR1(self):
        return (self.q()+(1-self.p_T())*(1-self.q()-self.p_C())*self.b_Connected())

    def b_CR2(self):
        return self.p_T()*(1-self.q()-self.p_C())*self.b_Connected()

    def b_Connected_DRX(self):
        return self.b_Connected()

    def b_Inactive(self):
        return (1-self.p_C()-self.q())*self.b_Connected()


    #Energy in each state
    def Idle(self):
        return self.parameters.D.P_s
    
    def RA(self):
        pp = self.parameters.R_max * self.parameters.G
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40
        else: 
            T_RA_GAP = 0
        return self.parameters.D.P_i*(self.parameters.T_RA_Period/2.0+T_RA_GAP)+self.parameters.D.P_TX_RA*self.parameters.N_RA_REP*self.parameters.T_PRE+self.parameters.D.P_i*(pp/2.0+self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US)+self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=256)

    def CR1(self):
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        self.parameters.D.P_i*self.parameters.T_MIB_I+self.parameters.D.P_RX*(self.parameters.T_Sync+self.parameters.T_MIB_RX)
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions
        return self.parameters.D.P_i*self.parameters.T_MIB_I+self.parameters.D.P_RX*(self.parameters.T_Sync+self.parameters.T_MIB_RX)+self.packetEnergy.UL(L_x=72)+self.parameters.D.P_i*(2*self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US+2*self.parameters.T_ACK_k0+3*T_WDC)+2*self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=80)+self.packetEnergy.HARQ_ACK()
    
    def CR2(self):
        return self.packetEnergy.UL(L_x=72) + self.packetEnergy.DL(L_y=72) + self.packetEnergy.UL(L_x=72)
        #RRC resume request UL, RRC connection resume DL, RRC connection resume complete UL

    def Connected(self):
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions
        E_sch_Cmp = self.parameters.D.P_i*(self.parameters.T_Period_BSR*pp+self.parameters.T_RA_Period/2.0+pp/2.0+self.parameters.T_w_DC2DS+2*self.parameters.T_w_DC2US+T_RA_GAP+T_WDC)+2*self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=256)+self.parameters.D.P_TX_RA*self.parameters.N_RA_REP*self.parameters.T_PRE+self.packetEnergy.UL(L_x=72)+self.packetEnergy.UL(L_x=16)
        return self.packetEnergy.UL(L_x=793)+self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=120)+self.packetEnergy.HARQ_ACK()+E_sch_Cmp

    def Connected_DRX(self):
        pp = self.parameters.R_max * self.parameters.G
        T_DRXi = 2#*pp
        N_CDRX_Cycles = round((self.parameters.T_Inactivity-T_DRXi)/self.parameters.T_LC)
        T_onD = min((self.parameters.T_LC/pp),self.parameters.NppOnD)*self.parameters.R_max #OnDuration timer for monitoring control channel
        E_cycle = self.parameters.D.P_i*(self.parameters.T_LC-T_onD) + self.parameters.D.P_RX*T_onD #Energy of one CDRX cycle
        Avg_Cycles = 1/(self.p_OnD())   #Mean of geometric distribution with success probability self.p_OnD()
        Avg_Cycles = np.round(Avg_Cycles)
        if Avg_Cycles > N_CDRX_Cycles:
            Avg_Cycles = N_CDRX_Cycles
        return Avg_Cycles * E_cycle + self.parameters.D.P_RX * T_DRXi

    def Inactive(self):
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        E_IDRX = self.parameters.N_EDRX_Cycles*(self.parameters.D.P_s*(self.parameters.T_eDRX-self.parameters.T_PTW)+self.parameters.N_IDRX_Cycles*(self.parameters.D.P_s*(self.parameters.T_PC-(self.parameters.N_REP_DCI+self.parameters.T_IDRX_sync))+self.parameters.D.P_RX*self.parameters.N_REP_DCI+self.parameters.D.P_IDRX_sync*self.parameters.T_IDRX_sync))+self.parameters.D.P_s*(self.parameters.T_active-self.parameters.N_EDRX_Cycles*self.parameters.T_eDRX)
        E_sch_rel = self.parameters.D.P_i*(self.parameters.T_Period_BSR+self.parameters.T_RA_Period/2.0+pp/2.0+self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US+T_RA_GAP)+self.packetEnergy.DCI()+self.packetEnergy.DL(L_y=256)+self.parameters.D.P_TX_RA*self.parameters.N_RA_REP*self.parameters.T_PRE+self.packetEnergy.DL(L_y=72) 
        return E_IDRX + E_sch_rel

    #Delay for each state
    def D_Idle(self):
        return 1

    def D_RA(self):
        pp = self.parameters.R_max * self.parameters.G
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        return self.parameters.T_RA_Period/2+T_RA_GAP+self.parameters.N_RA_REP*self.parameters.T_PRE+pp/2+self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US+self.packetDelay.DCI()+self.packetDelay.DL(L_y=256)

    def D_CR1(self):
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions 
        return self.parameters.T_Sync+self.parameters.T_MIB_RX+self.parameters.T_MIB_I+self.packetDelay.UL(L_x=72)+2*self.parameters.T_w_DC2DS+self.parameters.T_w_DC2US+2*self.parameters.T_ACK_k0+3*T_WDC+2*self.packetDelay.DCI()+self.packetDelay.DL(L_y=80)+self.packetDelay.HARQ_ACK()

    def D_CR2(self):
        return 2*self.packetDelay.UL(L_x=72) + self.packetDelay.DL(L_y=72)

    def D_Connected(self):
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions 
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40.0
        else: 
            T_RA_GAP = 0.0
        E_sch_Cmp_delay = self.parameters.T_Period_BSR*pp+self.parameters.T_RA_Period/2+pp/2+self.parameters.T_w_DC2DS+2*self.parameters.T_w_DC2US+T_RA_GAP+T_WDC+2*self.packetDelay.DCI()+self.packetDelay.DL(L_y=256)+self.parameters.N_RA_REP*self.parameters.T_PRE+self.packetDelay.UL(L_x=72)+self.packetDelay.UL(L_x=16)
        return 2*self.packetDelay.HARQ_ACK()+self.packetDelay.UL(L_x=864)+self.packetDelay.DL(L_y=120)+(1-self.p_ACK)*E_sch_Cmp_delay

    def D_Connected_DRX(self):
        pp = self.parameters.R_max * self.parameters.G
        T_DRXi = 2*pp
        N_CDRX_Cycles = round((self.parameters.T_Inactivity-T_DRXi)/self.parameters.T_LC)
        D_cycle = self.parameters.T_LC
        Avg_Cycles = 1/(self.p_OnD())
        Avg_Cycles = np.ceil(Avg_Cycles)
        if Avg_Cycles > N_CDRX_Cycles:
            Avg_Cycles = N_CDRX_Cycles
        return Avg_Cycles * D_cycle + T_DRXi
        
    def D_Inactive(self):
        D_IDRX = self.parameters.N_EDRX_Cycles*(self.parameters.T_eDRX-self.parameters.T_PTW)+self.parameters.N_IDRX_Cycles*(self.parameters.T_PC-(self.parameters.N_REP_DCI+self.parameters.T_IDRX_sync))+self.parameters.N_REP_DCI+self.parameters.T_IDRX_sync+(self.parameters.T_active-self.parameters.N_EDRX_Cycles*self.parameters.T_eDRX)
        return D_IDRX
    

    #States as pairs of power levels and delays
    def Idle_List(self):
        return [[self.parameters.D.P_s,1]]
        
    def RA_List(self):
        pp = self.parameters.R_max * self.parameters.G
        if self.parameters.N_RA_REP > 64:
            T_RA_GAP = 40
        else: 
            T_RA_GAP = 0
        RA = [[self.parameters.D.P_i, self.parameters.T_RA_Period/2.0+T_RA_GAP], [self.parameters.D.P_TX, self.parameters.N_RA_REP*self.parameters.T_PRE], [self.parameters.D.P_i, pp/2.0]]
        RA.extend([[self.parameters.D.P_i, self.parameters.T_w_DC2DS]])
        RA.extend(self.packetEnergy.DL_List(L_y=256))        
        return RA

    def CR1_List(self):
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp
        CR1 = [[self.parameters.D.P_i, self.parameters.T_MIB_I], [self.parameters.D.P_RX, self.parameters.T_Sync+self.parameters.T_MIB_RX]]
        
        CR1.extend([[self.parameters.D.P_i, 2*self.parameters.T_ACK_k0+3*T_WDC]])
        CR1.extend(self.packetEnergy.DCI_List())
        CR1.extend([[self.parameters.D.P_i, self.parameters.T_w_DC2US]])
        CR1.extend(self.packetEnergy.UL_List(L_x=72))
        CR1.extend(self.packetEnergy.DCI_List())
        CR1.extend([[self.parameters.D.P_i, self.parameters.T_w_DC2DS]])
        CR1.extend(self.packetEnergy.DL_List(L_y=80))
        CR1.extend(self.packetEnergy.HARQ_ACK_List()) #+setCmp
        return CR1

    def CR2_List(self):    
        CR2 = []
        CR2.extend(self.packetEnergy.DCI_List())
        CR2.extend(self.packetEnergy.UL_List(L_x=72))
        CR2.extend(self.packetEnergy.DCI_List())
        CR2.extend(self.packetEnergy.DL_List(L_y=72))
        return CR2

    def Connected_List(self):
        Connected = []
        Connected.extend(self.packetEnergy.DCI_List())
        Connected.extend([[self.parameters.D.P_i, self.parameters.T_w_DC2US]])
        Connected.extend(self.packetEnergy.UL_List(L_x = 793))
        Connected.extend(self.packetEnergy.DCI_List())
        Connected.extend([[self.parameters.D.P_i, self.parameters.T_w_DC2DS]])
        Connected.extend(self.packetEnergy.DL_List(L_y = 120))
        Connected.extend(self.packetEnergy.HARQ_ACK_List())
        return Connected

    def Connected_DRX_List(self):
        pp = self.parameters.R_max * self.parameters.G
        T_onD = min((self.parameters.T_LC/pp),self.parameters.NppOnD)*self.parameters.R_max
        T_DRXi = 2*pp   
        Cycles = round(1/self.p_OnD())
        N_CDRX_Cycles = round((self.parameters.T_Inactivity-T_DRXi)/self.parameters.T_LC)
        if Cycles > N_CDRX_Cycles:
            Cycles = N_CDRX_Cycles
        Cycles = round(Cycles)
        Connected_DRX = []
        for n in range(Cycles):
            Connected_DRX.extend([[self.parameters.D.P_i, self.parameters.T_LC-T_onD], [self.parameters.D.P_RX, T_onD]])
        return Connected_DRX

    def Inactive_List(self):
        Inactive = [[self.parameters.D.P_s, self.parameters.T_eDRX-self.parameters.T_PTW]]
        for i in range(self.parameters.N_IDRX_Cycles):
            Inactive.extend([[self.parameters.D.P_s, self.parameters.T_PC-(self.parameters.N_REP_DCI+self.parameters.T_IDRX_sync)]])
            Inactive.extend([[self.parameters.D.P_RX, self.parameters.N_REP_DCI]])
            Inactive.extend([[self.parameters.D.P_IDRX_sync, self.parameters.T_IDRX_sync]])
        Inactive.extend([[self.parameters.D.P_s, self.parameters.T_active - self.parameters.T_eDRX]])
        return Inactive

          
    #Battery lifetime estimation
    def average_energy(self):
        return self.b_Idle()*self.Idle()+self.b_CR1()*self.CR1()+self.b_RA1()*self.RA()+self.b_RA2()*self.RA()+self.b_CR2()*self.CR2()+self.b_Connected()*self.Connected()+self.b_Connected_DRX()*self.Connected_DRX()+self.b_Inactive()*self.Inactive()

    def average_delay(self):
        return self.b_Idle()*self.D_Idle()+self.b_CR1()*self.D_CR1()+self.b_RA1()*self.D_RA()+self.b_RA2()*self.D_RA()+self.b_CR2()*self.D_CR2()+self.b_Connected()*self.D_Connected()+self.b_Connected_DRX()*self.D_Connected_DRX()+self.b_Inactive()*self.D_Inactive()

    def EnergyDay(self):
        E_model_day = self.average_energy()*(86400000.0/self.average_delay())/1000000.0   #in J
        return E_model_day/3600.0   #in Wh

    def BatteryLifetime(self):
        return self.parameters.C_bat/(self.EnergyDay()*365.25)

    def Latency(self):
        return (self.D_Idle() + self.D_RA() + self.D_CR1() + self.D_Connected())/1000.0
