import numpy as np
from matplotlib import pyplot as plt
from dataclass import deviceA, deviceB
from Parameters import Parameters
from PacketEnergy import packetEnergy, packetDelay
from EnergyConsumption1 import energyConsumption1
from EnergyConsumption2 import energyConsumption2


class Probabilities:

    def __init__(self, device, energyConsumption):
        self.parameters = Parameters(device)
        self.packetEnergy = packetEnergy(self.parameters)
        self.packetDelay = packetDelay(self.parameters)
        self.energyConsumption = energyConsumption(self.parameters, self.packetEnergy, self.packetDelay)

    def probs1(self):
        P = []
        P.append(self.energyConsumption.b_Off())
        P.append(self.energyConsumption.b_RA())
        P.append(self.energyConsumption.b_CR())
        P.append(self.energyConsumption.b_Connect())
        P.append(self.energyConsumption.b_ACK())
        P.append(self.energyConsumption.b_Inactive())
        return P

    def probs2(self):
        P = []
        P.append(self.energyConsumption.b_Idle())
        P.append(self.energyConsumption.b_RA1())
        P.append(self.energyConsumption.b_RA2())
        P.append(self.energyConsumption.b_CR1())
        P.append(self.energyConsumption.b_CR2())
        P.append(self.energyConsumption.b_Connected())
        P.append(self.energyConsumption.b_Connected_DRX())
        P.append(self.energyConsumption.b_Inactive())
        return P

    def index1(self):
        I = []
        j = 0
        for i in self.probs1():
            j+=1
            I.append(j)
        return I

    def index2(self):
        I = []
        j = 0
        for i in self.probs2():
            j+=1
            I.append(j)
        return I

#Getting the data
p1 = Probabilities(deviceA, energyConsumption1)
p2 = Probabilities(deviceA, energyConsumption2)

p1.parameters.IAT = 1
p2.parameters.IAT = 1


probs1 = p1.probs1()
probs2 = p2.probs2()

index1 = p1.index1()
index2 = p2.index2()

names1 = ["Off", "RA", "CR", "Connect", "ACK", "Inactive"]
names2 = ["Idle", "RA1", "RA2", "CR1", "CR2", "Connected", "CDRX", "Inactive"]



#Plotting the data
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()


ax1.bar(index1, probs1, tick_label=names1)
ax2.bar(index2, probs2, tick_label=names2)

plt.tight_layout() 
plt.show()
