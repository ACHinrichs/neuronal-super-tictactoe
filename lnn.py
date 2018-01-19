import numpy as np
import supertictactoe as st
from supertictactoe import Player
import main

class ConmputerPlayer(Player):
    pass
    def __init__(self, aNumber):
        self.number = aNumber

    def won(self):
        pass
        #lnn.updateNet()

    def lost(self):
        lnn.updateNet()

    def move(self, board):
        move = lnn.move();
        return Coordinate(move[0], move[1])

class LayerNeuralNetwork():
    move_count = 0
    def nonlin(x, deriv=False):
        moves
        if(deriv==True):
            return x*(1-x)
        return 1/(1+np.exp(-x))
   

    def trainNetwork(self):
        p1 = ComputerPlayer(1)
        p2 = ComputerPlayer(2)
        
        for i in range(100):
            game = Game(p1,p2)
            
    def move(self, board):
        m = nonlin(np.dot(board, syn0))
        x1 = m.index(max(m))
        m[x1] = 0
        x2 = m.index(max(m))
        moves.append((x1,x2, board))
        move_count += 1
        return [x1, x2]

    def updateNet(self):
        move = 0
        for x,y,board in moves:
            move += 1;
            # how much did we miss?
            
            impact = move_count - move
            # multiply how much we missed by the 
            # slope of the sigmoid at the values in l1
            l1_delta = impact * nonlin(l1,True)
            
            # update weights
            syn0 += np.dot(board.T,l1_delta)

            
# seed random numbers to make calculation
# deterministic
np.random.seed(1)

# initialize weights randomly with mean 0
syn0 = 2*np.random.random((81,1)) - 1
print(syn0)

lnn = LayerNeuralNetwork()
lnn.trainNetwork()

print ("Neuronales Netz 1: ")
print (syn0)
print (nonlin(np.dot([1,1,0], syn0)))

