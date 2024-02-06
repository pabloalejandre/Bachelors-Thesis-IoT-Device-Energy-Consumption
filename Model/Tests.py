from cgi import test
from dataclass import deviceA, deviceB
from model.EnergyConsumption_4G import energyConsumption1
from model.EnergyConsumption_5G import energyConsumption2
from Simulation import Simulation
from matplotlib import pyplot as plt
import numpy as np

class Test:
    def __init__(self, device):
        self.sim1 = Simulation(device, energyConsumption1)
        self.sim2 = Simulation(device, energyConsumption2)
                
    def avg_energy1(self):
        return self.sim1.energyConsumption.average_energy()

    def avg_energy2(self):
        return self.sim2.energyConsumption.average_energy()

    def avg_delay1(self):
        return self.sim1.energyConsumption.average_delay()

    def avg_delay2(self):
        return self.sim2.energyConsumption.average_delay()

    def states1(self):
        print("Off", self.sim1.energyConsumption.Off())
        print("RA", self.sim1.energyConsumption.RA())
        print("CR", self.sim1.energyConsumption.CR())
        print("Connect", self.sim1.energyConsumption.Connect())
        print("ACK", self.sim1.energyConsumption.ACK())
        print("Inactive", self.sim1.energyConsumption.Inactive())
        pass

    def states2(self):
        print("Idle", self.sim2.energyConsumption.Idle())
        print("RA", self.sim2.energyConsumption.RA())
        print("CR1", self.sim2.energyConsumption.CR1())
        print("CR2", self.sim2.energyConsumption.CR2())
        print("Connected", self.sim2.energyConsumption.Connected())
        print("CDRX", self.sim2.energyConsumption.Connected_DRX())
        print("Inactive", self.sim2.energyConsumption.Inactive())
        pass

    def probs1(self):
        print("Off", self.sim1.energyConsumption.b_Off())
        print("RA", self.sim1.energyConsumption.b_RA())
        print("CR", self.sim1.energyConsumption.b_CR())
        print("Connect", self.sim1.energyConsumption.b_Connect())
        print("ACK", self.sim1.energyConsumption.b_ACK())
        print("Inactive", self.sim1.energyConsumption.b_Inactive())
        print("All states 1", self.sim1.energyConsumption.b_Off()+self.sim1.energyConsumption.b_RA()+self.sim1.energyConsumption.b_CR()+self.sim1.energyConsumption.b_Connect()+self.sim1.energyConsumption.b_Inactive())
        pass

    def probs2(self):
        print("Idle", self.sim2.energyConsumption.b_Idle())
        print("RA1", self.sim2.energyConsumption.b_RA1())
        print("RA2", self.sim2.energyConsumption.b_RA2())
        print("CR1", self.sim2.energyConsumption.b_CR1())
        print("CR2", self.sim2.energyConsumption.b_CR2())
        print("Connected", self.sim2.energyConsumption.b_Connected())
        print("CDRX", self.sim2.energyConsumption.b_Connected_DRX())
        print("Inactive", self.sim2.energyConsumption.b_Inactive())
        print("All states 2", self.sim2.energyConsumption.b_Idle()+self.sim2.energyConsumption.b_CR1()+self.sim2.energyConsumption.b_CR2()+self.sim2.energyConsumption.b_Connected()+self.sim2.energyConsumption.b_Connected_DRX()+self.sim2.energyConsumption.b_Inactive())
        pass

    def delays1(self):
        print("Off", self.sim1.energyConsumption.D_Off())
        print("RA", self.sim1.energyConsumption.D_RA())
        print("CR", self.sim1.energyConsumption.D_CR())
        print("Connect", self.sim1.energyConsumption.D_Connect())
        print("ACK", self.sim1.energyConsumption.D_ACK())
        print("Inactive", self.sim1.energyConsumption.D_Inactive())
        pass

    def delays2(self):
        print("Idle", self.sim2.energyConsumption.D_Idle())
        print("RA1", self.sim2.energyConsumption.D_RA1())
        print("RA2", self.sim2.energyConsumption.D_RA2())
        print("CR1", self.sim2.energyConsumption.D_CR1())
        print("CR2", self.sim2.energyConsumption.D_CR2())
        print("Connected", self.sim2.energyConsumption.D_Connected())
        print("CDRX", self.sim2.energyConsumption.D_Connected_DRX())
        print("Inactive", self.sim2.energyConsumption.D_Inactive())
        pass

    def LowIAT(self):
        lis = []
        lis.append(0)
        for i in range(1000):
            if i == 0:
                continue
            else:
                self.sim2.parameters.IAT = i
                lis.append(self.avg_energy2())

        for i in range(1000):
            print(i , lis[i])
          


test1 = Test(deviceA)
test2 = Test(deviceB)

#print(test1.sim1.energyConsumption.BatteryLifetime())
#print(test1.sim2.energyConsumption.p())

#print(test1.avg_energy1())
#print(test1.avg_energy2())

#print(test1.sim1.energyConsumption.p_On())
#print(test1.sim2.energyConsumption.p_OnD())

#print(test1.probs1())
#print(test1.probs2())

#print(test1.avg_energy1())
#print(test1.avg_energy2())

#print(test1.avg_delay1())
#print(test1.avg_delay2())

#print(test1.states1())
#print(test1.states2())


#Energy packet Model 1
#print(test1.sim1.energyConsumption.Off()+ test1.sim1.energyConsumption.RA()+ test1.sim1.energyConsumption.CR() + test1.sim1.energyConsumption.Connect() + test1.sim1.energyConsumption.Inactive())

#Energy packet Model 1, low IAT
#print(test1.sim2.energyConsumption.Connected() + test1.sim2.energyConsumption.Connected_DRX() + test1.sim2.energyConsumption.Inactive() + test1.sim2.energyConsumption.CR1() + test1.sim2.energyConsumption.Idle())

#Energy packet Model 1, medium IAT
#print(test1.sim2.energyConsumption.Connected() + test1.sim2.energyConsumption.Connected_DRX()+ test1.sim2.energyConsumption.Inactive() + test1.sim2.energyConsumption.CR2())

#Energy packet Model 1, high IAT
#test1.sim2.parameters.IAT = 100
#print(test1.sim2.energyConsumption.Connected() + test1.sim2.energyConsumption.Connected_DRX())

#print(test1.sim1.energyConsumption.RA() + test1.sim1.energyConsumption.CR()+ test1.sim1.energyConsumption.Connect())
#print(test1.sim2.energyConsumption.RA() + test1.sim2.energyConsumption.CR1()+test1.sim2.energyConsumption.Connected())

test1.sim1.parameters.IAT = 1000
test1.sim2.parameters.IAT = 1000

print(test1.sim1.energyConsumption.average_energy())
print(test1.sim2.energyConsumption.average_energy())
