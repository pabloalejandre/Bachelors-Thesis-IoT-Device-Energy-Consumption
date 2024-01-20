from dataclass import Parameters_EC_Model

class Parameters(Parameters_EC_Model):
    def __init__(self, device):
        self.q = 0                                      #Probability of going to Idle from CDRX
        self.T = 1000*120                              #Timer to go to Idle from Inactive in ms
        self.C_bat = 5                                  #Battery capacity   
        self.IAT = 86400000.0                           #Inter arrival time in ms
        self.D = device()                               #Device for simulation
        self.G_iterate = [1.5, 2, 4, 8, 16, 32, 64]     #for G test case
        self.R_iterate = [1, 2, 4, 8, 16, 32, 64]       #for REP test case
        self.G_rep_iter = [8, 4, 2, 2, 2, 2, 2]         #for REP test case
        self.IAT_iter = [1/6,2/6,3/6,4/6,5/6,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]    #in hours
        
