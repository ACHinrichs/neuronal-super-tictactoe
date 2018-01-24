import numpy as np
import supertictactoe as st
from supertictactoe import Player
import main

class ConmputerPlayer(Player):
    pass
    def __init__(self, aNumber):
        self.number = aNumber

    def won(self):
        #pass
        lnn.updateNet(0)

    def lost(self):
        lnn.updateNet(1)

    def move(self, board):
        move = lnn.move();
        return Coordinate(move[0], move[1])

class LayerNeuralNetwork():
    move_count = 0
    moves = []
    def nonlin(x, deriv=False):
        if(deriv==True):
            return x*(1-x)
        return 1/(1+np.exp(-x))
   

    def trainNetwork(self):
        p1 = ComputerPlayer(1)
        p2 = ComputerPlayer(2)
        
        for i in range(100):
            print(i)
            game = Game(p1,p2)
            
    def move(self, board):
        # Network makes a
        # l0 = board
        l1 = nonlin(np.dot(board, syn0))
        l2 = nonlin(np.dot(l1, syn1))
        l3 = nonlin(np.dot(l2, syn2))
        l4 = nonlin(np.dot(l3, syn3))
        
        x = m.index(max(l4))
        
        x1 = x // 9
        x2 = x % 9
        moves.append((x1,x2, board))
        move_count += 1
        return Coordinate(x1, x2)

    def updateNet(self, lost):


        move = 0
        for x,y,board in moves:
            # forward propagation
            l0 = board
            l1 = nonlin(np.dot(l0, syn0))
            l2 = nonlin(np.dot(l1, syn1))
            l3 = nonlin(np.dot(l2, syn2))
            l4 = nonlin(np.dot(l3, syn3))
            
            # how much did we miss?
            l4_error = lost - l4
            
            # multiply how much we missed by the 
            # slope of the sigmoid at the values in l1
            l4_delta = l4_error * nonlin(l1,True)

            l3_error = l4_delta.dot(syn3.T)
            l3_delta = l3_error * nonlin(l3, deriv=True)

            l2_error = l3_delta.dot(syn2.T)
            l2_delta = l2_error * nonlin(l2, deriv=True)

            l1_error = l2_delta.dot(syn1.T)
            l1_delta = l1_error * nonlin(l1, deriv=True)
            
            # update weights
            syn3 += np.dot(l4.T,l4_delta)
            syn2 += np.dot(l3.T,l3_delta)
            syn1 += np.dot(l2.T,l2_delta)
            syn0 += np.dot(l1.T,l1_delta)
            
            
# seed random numbers to make calculation
# deterministic
np.random.seed(1)

# initialize weights randomly with mean 0
syn0 = 2*np.random.random((9,9)) - 1
syn1 = 2*np.random.random((81,81)) -1
syn2 = 2*np.random.random((81,9)) -1
syn3 = 2*np.random.random((81,1))-1
print(syn0)

lnn = LayerNeuralNetwork()
lnn.trainNetwork()

print ("Neuronales Netz 1: ")
print (syn0)
#print (nonlin(np.dot([1,1,0], syn0)))

