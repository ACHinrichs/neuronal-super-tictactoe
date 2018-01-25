import numpy as np

class NeuronalPlayer(Player):
    zuege = []
    
    def __init__(self):
        netz=[]
        netz[0]= np.zeros(9,9)
        super(NeuronalPlayer, self).__init__()

    def won(self)
