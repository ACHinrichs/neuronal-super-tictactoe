#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import supertictactoe as st
from supertictactoe import Player, Game, Coordinate, Board

class ComputerPlayer(Player):
    def __init__(self, aNumber, network):
        self.number = aNumber
        self.nw = network
        self.moves = []

    def won(self):
        #pass
        self.nw.updateNet(0, self.moves, self.number)

    def lost(self):
        print(str(len(self.moves))+ " \t"+str(self.number))
        self.nw.updateNet(1, self.moves, self.number)

    def move(self, board):
        c =  self.nw.move(board, self.number);
        self.moves.append([c.topLevel,c.bottomLevel ,board])
        return c;
        

class LayerNeuralNetwork():

    def __init__(self):
        # initialize weights randomly with mean 0
        self.syn0 = 2*np.random.random((9,81)) - 1
        self.syn1 = 2*np.random.random((81,81)) -1
        self.syn2 = 2*np.random.random((81,81))-1
        self.syn3 = 2*np.random.random((81,1)) -1

        pass

    def boardToInput(self, board, playerNumber):
        out = board.field[:] #Copy List!
        out.append([0,0,0,0,0,0,0,0,0])
        outArray = Board.playerToEntry(playerNumber) * np.array(out)
        if(not board.lastMove.bottomLevel == -1):
            outArray[9,board.lastMove.bottomLevel]=1
        return outArray
    
    def nonlin(self, x, deriv=False):
        if(deriv==True):
            return x*(1-x)
        return 1/(1+np.exp(-x))
            
    def move(self, board, playerNumber):
        # Network makes a
        # l0 = board
        # board = board.field
        l1 = self.nonlin(np.dot(self.boardToInput(board, playerNumber), self.syn0))
        l2 = self.nonlin(np.dot(l1, self.syn1))
        l3 = self.nonlin(np.dot(l2, self.syn2))
        l4 = self.nonlin(np.dot(l3, self.syn3))
        
        x = l4.tolist().index(max(l4))
        x1 = x // 9
        x2 = x % 9
        return Coordinate(x1, x2)

    def updateNet(self, lost, moves, playerNumber):
        move = 0
        for x,y,board in moves:
            # forward propagation
            l0 = self.boardToInput(board, playerNumber)
            l1 = self.nonlin(np.dot(l0, self.syn0))
            l2 = self.nonlin(np.dot(l1, self.syn1))
            l3 = self.nonlin(np.dot(l2, self.syn2))
            l4 = self.nonlin(np.dot(l3, self.syn3))
            
            # how much did we miss?
            l4_error = lost - l4
            
            # multiply how much we missed by the 
            # slope of the sigmoid at the values in l1
            l4_delta = l4_error * self.nonlin(l4,deriv=True)

            l3_error = l4_delta.dot(self.syn3.T)
            l3_delta = l3_error * self.nonlin(l3, deriv=True)

            l2_error = l3_delta.dot(self.syn2.T)
            l2_delta = l2_error * self.nonlin(l2, deriv=True)

            l1_error = l2_delta.dot(self.syn1.T)
            l1_delta = l1_error * self.nonlin(l1, deriv=True)
            
            # update weights
            self.syn3 += np.dot(l3.T,l4_delta)
            self.syn2 += np.dot(l2.T,l3_delta)
            self.syn1 += np.dot(l1.T,l2_delta)
            self.syn0 += np.dot(l0.T,l1_delta)

    def printNet(self):
        print ("Synapse 0: ")
        print (self.syn0)
        print ("Synapse 1: ")
        print (self.syn1)
        print ("Synapse 2: ")
        print (self.syn2)
        print ("Synapse 3: ")
        print (self.syn3)


# seed random numbers to make calculation
# deterministic
np.random.seed(1)


lnn = LayerNeuralNetwork()

# train Network

for i in range(10000):
    p1 = ComputerPlayer(0,lnn)
    p2 = ComputerPlayer(1,lnn)
    game = Game(p1,p2)
    game.play()
    #print(i)

lnn.printNet()

#print (nonlin(np.dot([1,1,0], syn0)))

