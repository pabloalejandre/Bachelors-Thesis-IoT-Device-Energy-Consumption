import numpy as np

class packetEnergy:
    
    def __init__(self, parameters):
        self.parameters = parameters
        
    #The List methods return a list of pairs of power levels and durations, whereas the other modules return the energy as a value
    def DCI_List(self):
        T_RX_DCI = np.ceil(self.parameters.N_REP_DCI*(20.0/14.0 - 1)) + self.parameters.N_REP_DCI
        if self.parameters.R_max > self.parameters.DL_Gap_Thr:
            T_DL_Gap_DCI = np.floor(self.parameters.N_REP_DCI/(self.parameters.T_Gap_Period_DL - self.parameters.T_Gap_Dur_DL)) * self.parameters.T_Gap_Dur_DL
        else:
            T_DL_Gap_DCI = 0
        return [[self.parameters.D.P_RX, T_RX_DCI], [self.parameters.D.P_i, T_DL_Gap_DCI]]

    def DCI(self):
        E = self.DCI_List()
        return E[0][0]*E[0][1] + E[1][0]*E[1][1]

    
    def UL_List(self, L_x):
        #req: RRC connection request (72b)
        #scr: Scheduling request (72b)
        #setCmp: RRC Setup Complete together with the piggybacked IP UL report (864b)
        #rlc_ACK: RLC AM ACK (16b) 
        T_RU = 8
        if L_x == 72:
            N_RU = 4
            TBS = 88
            N_REP = 1
        else:
            N_RU = self.parameters.N_RU
            TBS = 568
            N_REP = self.parameters.NPUSCH_N_REP 
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions
        T_RX_DCI = np.ceil(self.parameters.N_REP_DCI*(20.0/14.0 - 1)) + self.parameters.N_REP_DCI
        N_seg_x = np.ceil(L_x/(TBS - self.parameters.H_RLCMAC))
        
        T_TX = N_REP * N_RU * T_RU * N_seg_x
        T_UL_Gap = np.floor(T_TX/(self.parameters.T_Gap_Period_UL-self.parameters.T_Gap_Dur_UL))*self.parameters.T_Gap_Dur_UL
        if N_seg_x > 0:
            E_seg_x = (N_seg_x - 1) * (self.parameters.D.P_RX * T_RX_DCI + self.parameters.D.P_i * (T_WDC + self.parameters.T_w_DC2US))
        else:
            E_seg_x = 0
        #return [[self.parameters.D.P_TX, T_TX], [self.parameters.D.P_ULGap, T_UL_Gap], E_seg_x]
        E = [[self.parameters.D.P_TX, T_TX], [self.parameters.D.P_ULGap, T_UL_Gap]]
        N_seg_x = int(N_seg_x)
        if N_seg_x > 1:
            for i in np.linspace(start=1, stop=N_seg_x-1, num = N_seg_x-1):
                E.extend([[self.parameters.D.P_RX, T_RX_DCI]])
                E.extend([[self.parameters.D.P_i, T_WDC + self.parameters.T_w_DC2US]])
        return E
    
    def UL(self, L_x):
        T_RU = 8
        if L_x == 72:
            N_RU = 4
            TBS = 88
            N_REP = 1
        else:
            N_RU = self.parameters.N_RU
            TBS = 568
            N_REP = self.parameters.NPUSCH_N_REP 
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions
        T_RX_DCI = np.ceil(self.parameters.N_REP_DCI*(20.0/14.0 - 1)) + self.parameters.N_REP_DCI
        N_seg_x = np.ceil(L_x/(TBS - self.parameters.H_RLCMAC))
        
        T_TX = N_REP * N_RU * T_RU * N_seg_x
        T_UL_Gap = np.floor(T_TX/(self.parameters.T_Gap_Period_UL-self.parameters.T_Gap_Dur_UL))*self.parameters.T_Gap_Dur_UL
        if N_seg_x > 0:
            E_seg_x = (N_seg_x - 1) * (self.parameters.D.P_RX * T_RX_DCI + self.parameters.D.P_i * (T_WDC + self.parameters.T_w_DC2US))
        else:
            E_seg_x = 0
        return self.parameters.D.P_TX*T_TX + self.parameters.D.P_ULGap*T_UL_Gap + E_seg_x
        

    
    def DL_List(self, L_y):
        #rar: RAR (256b)
        #set: RRC Connection Setup (80b)
        #accept: Non-Access Stratum (NAS) Service Accept (120b)
        #rel: RRC release (16b)
        TBS = 568
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions
        T_RX_DCI = np.ceil(self.parameters.N_REP_DCI*(20.0/14.0 - 1)) + self.parameters.N_REP_DCI
        N_seg_y = np.ceil(L_y/(TBS-self.parameters.H_RLCMAC))
        T_RX = np.ceil(self.parameters.NPDSCH_N_REP * self.parameters.N_SF * N_seg_y*(20.0/14.0 - 1)) + self.parameters.NPDSCH_N_REP * self.parameters.N_SF * N_seg_y
        if self.parameters.R_max > self.parameters.DL_Gap_Thr:
            T_DL_Gap = np.floor((self.parameters.NPDSCH_N_REP*self.parameters.N_SF*N_seg_y)/(self.parameters.T_Gap_Period_DL-self.parameters.T_Gap_Dur_DL))*self.parameters.T_Gap_Dur_DL
        else:
            T_DL_Gap = 0
        if N_seg_y > 0:
            E_seg_y = (N_seg_y - 1) * (self.parameters.D.P_RX * T_RX_DCI + self.parameters.D.P_i * (T_WDC + self.parameters.T_w_DC2DS))
        else:
            E_seg_y = 0
        E = [[self.parameters.D.P_RX, T_RX], [self.parameters.D.P_i, T_DL_Gap]]
        N_seg_y = int(N_seg_y)
        if N_seg_y > 1:
            for i in np.linspace(start=1, stop=N_seg_y-1, num = N_seg_y-1):
                E.extend([[self.parameters.D.P_RX, T_RX_DCI]])
                E.extend([[self.parameters.D.P_i, T_WDC + self.parameters.T_w_DC2DS]])
        return E
        

    def DL(self, L_y):
        TBS = 568
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions
        T_RX_DCI = np.ceil(self.parameters.N_REP_DCI*(20.0/14.0 - 1)) + self.parameters.N_REP_DCI
        N_seg_y = np.ceil(L_y/(TBS-self.parameters.H_RLCMAC))
        T_RX = np.ceil(self.parameters.NPDSCH_N_REP * self.parameters.N_SF * N_seg_y*(20.0/14.0 - 1)) + self.parameters.NPDSCH_N_REP * self.parameters.N_SF * N_seg_y
        if self.parameters.R_max > self.parameters.DL_Gap_Thr:
            T_DL_Gap = np.floor((self.parameters.NPDSCH_N_REP*self.parameters.N_SF*N_seg_y)/(self.parameters.T_Gap_Period_DL-self.parameters.T_Gap_Dur_DL))*self.parameters.T_Gap_Dur_DL
        else:
            T_DL_Gap = 0
        if N_seg_y > 0:
            E_seg_y = (N_seg_y - 1) * (self.parameters.D.P_RX * T_RX_DCI + self.parameters.D.P_i * (T_WDC + self.parameters.T_w_DC2DS))
        else:
            E_seg_y = 0
        return self.parameters.D.P_RX*T_RX + self.parameters.D.P_i*T_DL_Gap + E_seg_y


    def HARQ_ACK_List(self):
        T_RU = 2
        T_TXF2 = self.parameters.NPUSCH_N_REP * T_RU
        T_UL_Gap = np.floor(T_TXF2/(self.parameters.T_Gap_Period_UL - self.parameters.T_Gap_Dur_UL))*self.parameters.T_Gap_Dur_UL
        return [[self.parameters.D.P_TX, T_TXF2], [self.parameters.D.P_ULGap, T_UL_Gap]]

    def HARQ_ACK(self):
        E = self.HARQ_ACK_List()
        return E[0][0]*E[0][1] + E[1][0]*E[1][1]

class packetDelay:

    def __init__(self, parameters):
        self.parameters = parameters
        self.packetEnergy = packetEnergy(parameters)

    def DCI(self):
        T_RX_DCI = np.ceil(self.parameters.N_REP_DCI*(20/14 - 1)) + self.parameters.N_REP_DCI
        if self.parameters.R_max > self.parameters.DL_Gap_Thr:
            T_DL_Gap_DCI = np.floor(self.parameters.N_REP_DCI/(self.parameters.T_Gap_Period_DL - self.parameters.T_Gap_Dur_DL)) * self.parameters.T_Gap_Dur_DL
        else:
            T_DL_Gap_DCI = 0
        return T_RX_DCI + T_DL_Gap_DCI

    def UL(self, L_x):
        T_RU = 8
        if L_x == 72:
            N_RU = 4
            TBS = 88
            N_REP = 1
        else:
            N_RU = self.parameters.N_RU
            TBS = 568
            N_REP = self.parameters.NPUSCH_N_REP 
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions
        T_RX_DCI = np.ceil(self.parameters.N_REP_DCI*(20/14 - 1)) + self.parameters.N_REP_DCI
        N_seg_x = np.ceil(L_x/(TBS - self.parameters.H_RLCMAC))
        T_TX = N_REP * N_RU * T_RU * N_seg_x
        T_UL_Gap = np.floor(T_TX/(self.parameters.T_Gap_Period_UL-self.parameters.T_Gap_Dur_UL))*self.parameters.T_Gap_Dur_UL
        if N_seg_x > 0:
            return T_TX + T_UL_Gap + (N_seg_x - 1)*(T_RX_DCI + T_WDC + self.parameters.T_w_DC2US)
        else: 
            return T_TX + T_UL_Gap

    def DL(self, L_y):
        TBS = 568
        pp = self.parameters.R_max * self.parameters.G
        T_WDC = pp #- mod(T_x1 + T_x2 + ... T_xn, pp) where x1, x2, ..., xn are the considered steps occurred between NPDCCH occasions      
        T_RX_DCI = np.ceil(self.parameters.N_REP_DCI*(20/14 - 1)) + self.parameters.N_REP_DCI
        N_seg_y = np.ceil(L_y/(TBS-self.parameters.H_RLCMAC))
        T_RX = np.ceil(self.parameters.NPDSCH_N_REP * self.parameters.N_SF * N_seg_y*(20/14 - 1)) + self.parameters.NPDSCH_N_REP * self.parameters.N_SF * N_seg_y
        if self.parameters.R_max > self.parameters.DL_Gap_Thr:
            T_DL_Gap = np.floor((self.parameters.NPDSCH_N_REP*self.parameters.N_SF*N_seg_y)/(self.parameters.T_Gap_Period_DL-self.parameters.T_Gap_Dur_DL))*self.parameters.T_Gap_Dur_DL
        else:
            T_DL_Gap = 0
        if N_seg_y > 0:
            return T_RX + T_DL_Gap + (N_seg_y-1)*(T_RX_DCI + T_WDC + self.parameters.T_w_DC2DS)
        else: 
            return T_RX + T_DL_Gap

    def HARQ_ACK(self):
        T_RU = 2
        T_TXF2 = self.parameters.NPUSCH_N_REP * T_RU
        T_UL_Gap = np.floor(T_TXF2/(self.parameters.T_Gap_Period_UL - self.parameters.T_Gap_Dur_UL))*self.parameters.T_Gap_Dur_UL
        return T_TXF2 + T_UL_Gap