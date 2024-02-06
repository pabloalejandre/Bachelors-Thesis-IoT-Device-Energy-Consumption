import numpy as np
from matplotlib import pyplot as plt
from dataclass import deviceA, deviceB
from Parameters import Parameters
from PacketEnergy import packetEnergy, packetDelay
from model.EnergyConsumption_4G import energyConsumption1
from model.EnergyConsumption_5G import energyConsumption2

class Simulation:

    def __init__(self, device, energyConsumption):
        self.parameters = Parameters(device)
        self.packetEnergy = packetEnergy(self.parameters)
        self.packetDelay = packetDelay(self.parameters)
        self.energyConsumption = energyConsumption(self.parameters, self.packetEnergy, self.packetDelay)


    def G_Test(self):
        self.energyConsumption.Y.clear()
        for i in range(0, len(self.parameters.R_iterate)):
            self.parameters.G = self.parameters.G_iterate[i]
            self.energyConsumption.Y.append(self.energyConsumption.BatteryLifetime())
        return self.energyConsumption.Y
    
    def REP_Test(self):
        self.energyConsumption.Y.clear()
        for i in range(0, len(self.parameters.R_iterate)):
            self.parameters.R_max = self.parameters.R_iterate[i]
            self.parameters.N_REP_DCI = self.parameters.R_iterate[i]
            self.parameters.NPUSCH_N_REP = self.parameters.R_iterate[i]
            self.parameters.NPDSCH_N_REP = self.parameters.R_iterate[i]
            self.parameters.G = self.parameters.G_rep_iter[i]
            self.energyConsumption.Y.append(self.energyConsumption.BatteryLifetime())
        return self.energyConsumption.Y
    
    def LatencyTest(self):
        self.energyConsumption.L.clear()
        for i in range(0, len(self.parameters.R_iterate)):
            self.parameters.R_max = self.parameters.R_iterate[i]
            self.parameters.N_REP_DCI = self.parameters.R_iterate[i]
            self.parameters.NPUSCH_N_REP = self.parameters.R_iterate[i]
            self.parameters.NPDSCH_N_REP = self.parameters.R_iterate[i]
            self.parameters.G = self.parameters.G_rep_iter[i]
            self.energyConsumption.L.append(self.energyConsumption.Latency())
        return self.energyConsumption.L

    def IATTest_Lifetime(self):
        self.energyConsumption.Y.clear()
        self.parameters.R_max = 8 
        self.parameters.N_REP_DCI = 1
        self.parameters.NPUSCH_N_REP = 1
        self.parameters.NPDSCH_N_REP = 1
        self.parameters.G = 2
        for i in range(0, len(self.parameters.IAT_iter)):
            self.parameters.IAT = self.parameters.IAT_iter[i]*3600000
            self.energyConsumption.Y.append(self.energyConsumption.BatteryLifetime())
        return self.energyConsumption.Y

    def IATTest_Energy(self):
        self.energyConsumption.E.clear()
        self.parameters.R_max = 8 
        self.parameters.N_REP_DCI = 1
        self.parameters.NPUSCH_N_REP = 1
        self.parameters.NPDSCH_N_REP = 1
        self.parameters.G = 2
        for i in range(0, len(self.parameters.IAT_iter)):
            self.parameters.IAT = self.parameters.IAT_iter[i]*3600000
            #self.energyConsumption.E.append(self.energyConsumption.average_energy()/self.energyConsumption.average_delay())
            self.energyConsumption.E.append(self.energyConsumption.average_energy())
        return self.energyConsumption.E


    def Model1_States(self):
        return [self.energyConsumption.Off_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR_List(), self.energyConsumption.Connect_List(), self.energyConsumption.Inactive_List()]

    def Model2_States(self):
        return [self.energyConsumption.Idle_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR1_List(), self.energyConsumption.CR2_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive()]

    
    def Model1_Packet(self):
        self.parameters.R_max = 8 
        self.parameters.N_REP_DCI = 1
        self.parameters.NPUSCH_N_REP = 1
        self.parameters.NPDSCH_N_REP = 1
        self.parameters.G = 2
        E = []
        E.append([0,0])
        for state in [self.energyConsumption.Off_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR_List(), self.energyConsumption.Connect_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.Off_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR_List(), self.energyConsumption.Connect_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.Off_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR_List(), self.energyConsumption.Connect_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.Off_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR_List(), self.energyConsumption.Connect_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.Off_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR_List(), self.energyConsumption.Connect_List(), self.energyConsumption.Inactive_List()]:
            for j in range(len(state)):
                E.append(state[j])
        return E        

    def Model2_StatesLow(self):
        self.parameters.IAT = 100
        self.parameters.R_max = 8 
        self.parameters.N_REP_DCI = 1
        self.parameters.NPUSCH_N_REP = 1
        self.parameters.NPDSCH_N_REP = 1
        self.parameters.G = 2
        E = []
        E.append([0,0])
        for state in [self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List()]:
            for j in range(len(state)):
                E.append(state[j])

        return E

    def Model2_StatesMedium(self):
        self.parameters.IAT = 1000*60
        self.parameters.R_max = 8 
        self.parameters.N_REP_DCI = 1
        self.parameters.NPUSCH_N_REP = 1
        self.parameters.NPDSCH_N_REP = 1
        self.parameters.G = 2
        E = []
        E.append([0,0])
        for state in [self.energyConsumption.RA_List(), self.energyConsumption.CR2_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR2_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR2_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR2_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR2_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive_List()]:
            for j in range(len(state)):
                E.append(state[j])
        return E

    def Model2_StatesHigh(self):
        self.parameters.IAT = 86400000.0
        self.parameters.R_max = 8 
        self.parameters.N_REP_DCI = 1
        self.parameters.NPUSCH_N_REP = 1
        self.parameters.NPDSCH_N_REP = 1
        self.parameters.G = 2
        E = []
        E.append([0,0])
        for state in [self.energyConsumption.Idle_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR1_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.Idle_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR1_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.Idle_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR1_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.Idle_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR1_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive_List(), self.energyConsumption.Idle_List(), self.energyConsumption.RA_List(), self.energyConsumption.CR1_List(), self.energyConsumption.Connected_List(), self.energyConsumption.Connected_DRX_List(), self.energyConsumption.Inactive_List()]:
            for j in range(len(state)):
                E.append(state[j])
        return E
    

    def power_levels(self, list):
        P = []
        for i in range(len(list)):
             P.append(list[i][0])
        return P

    def delays(self, list):
        D = []
        for i in range(len(list)):
            D.append(list[i][1])
        for j in range(len(D)):
            if j == len(D)-1:
                continue
            D[j+1] = D[j] + D[j+1]
        return D

    
if __name__ == "__main__":
  
    simA1 = Simulation(deviceA, energyConsumption1)
    simB1 = Simulation(deviceB, energyConsumption1)

    simA2 = Simulation(deviceA, energyConsumption2)
    simB2 = Simulation(deviceB, energyConsumption2)

    
    #plt.style.use("seaborn")
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()
    fig5, ax5 = plt.subplots()
    fig6, ax6 = plt.subplots()
    fig7, ax7 = plt.subplots()

    """
    ax1.plot(simA1.parameters.G_iterate, simA1.G_Test(), color = "orange", marker = "o", label = "Device A, G Test")
    ax1.plot(simB1.parameters.G_iterate, simB1.G_Test(), color = "green", marker = "o", label = "Device B, G Test")
    ax1.plot(simA1.parameters.R_iterate, simA1.REP_Test(), color = "orange", marker = "x", label = "Device A, REP Test")
    ax1.plot(simB1.parameters.R_iterate, simB1.REP_Test(), color = "green", marker = "x", label = "Device B, REP Test")
    ax2.plot(simA1.parameters.R_iterate, simA1.LatencyTest(), color = "black", marker = "+")
    """
    
    ax1.plot(simA1.parameters.G_iterate, simA1.G_Test(), color = "dodgerblue", marker = "o", label = "NB-IoT Model, G Test")
    ax1.plot(simA2.parameters.G_iterate, simA2.G_Test(), color = "darkorange", marker = "o", label = "Extended Model, G Test")
    ax1.plot(simA1.parameters.R_iterate, simA1.REP_Test(), color = "dodgerblue", marker = "x", label = "NB-IoT Model, REP Test")
    ax1.plot(simA2.parameters.R_iterate, simA2.REP_Test(), color = "darkorange", marker = "x", label = "Extended Model, REP Test")
    
    
    ax2.plot(simA1.parameters.IAT_iter, simA1.IATTest_Lifetime(), color = "red", label = "NB-IoT Model")
    ax2.plot(simA2.parameters.IAT_iter, simA2.IATTest_Lifetime(), color = "blue", label = "Extended Model")

    ax3.plot(simA1.parameters.IAT_iter, simA1.IATTest_Energy(), color = "r", label = "NB-IoT Model")
    ax3.plot(simA2.parameters.IAT_iter, simA2.IATTest_Energy(), color = "blue", label = "Extended Model")
    
    ax4.step(simA1.delays(simA1.Model1_Packet()), simA1.power_levels(simA1.Model1_Packet()))

    ax5.step(simA2.delays(simA2.Model2_StatesLow()), simA2.power_levels(simA2.Model2_StatesLow()))

    ax6.step(simA2.delays(simA2.Model2_StatesMedium()), simA2.power_levels(simA2.Model2_StatesMedium()))

    ax7.step(simA2.delays(simA2.Model2_StatesHigh()), simA2.power_levels(simA2.Model2_StatesHigh()))
    
    
    ax1.legend()
    ax1.set_xlabel("G or number of repetitions")
    ax1.set_ylabel("Years")
    ax1.set_xlim(1, 100)
    ax1.set_ylim(0,25)
    ax1.set_xscale("log", base = 2)
    ax1.grid()
    
    ax2.legend()
    #ax2.set_title("Battery lifetime")
    ax2.set_xlabel("IAT (h)")
    ax2.set_ylabel("Years")
    ax2.grid()
    
    """
    ax2.set_xlabel("Number of repetitions")
    ax2.set_ylabel("Latency (s)")
    ax2.set_xlim(1,100)
    ax2.set_ylim(0,30) 
    ax2.set_xscale("log", base = 2)
    ax2.grid()
    """
    ax3.legend()
    #ax3.set_title("Average energy consumption/ms")
    ax3.set_xlabel("IAT (h)")
    ax3.set_ylabel("uJ/ms")
    ax3.grid()

    #ax4.set_title("Power consumption of one Packet, Model 1")
    ax4.set_xlabel("Time (ms)")
    ax4.set_ylabel("Power (mW)")
    ax4.grid()

    #ax5.set_title("Power consumption of one Packet, Model 2, low IAT")
    ax5.set_xlabel("Time (ms)")
    ax5.set_ylabel("Power (mW)")
    ax5.grid()

    #ax6.set_title("Power consumption of one Packet, Model 2, medium IAT")
    ax6.set_xlabel("Time (ms)")
    ax6.set_ylabel("Power (mW)")
    ax6.grid()

    #ax7.set_title("Power consumption of one Packet, Model 2, high IAT")
    ax7.set_xlabel("Time (ms)")
    ax7.set_ylabel("Power (mW)")
    ax7.grid()


    plt.tight_layout()    
    plt.show()

    