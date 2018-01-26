#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import supertictactoe as st
from supertictactoe import Player, Game, Coordinate, Board
LOG_LEVEL = 0


def log(out, level=1):
    if level <= LOG_LEVEL:
        print(out)

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
        self.syn0 = 2*np.random.random((81,90)) - 1
        self.syn1 = 2*np.random.random((81*9,81)) -1
        self.syn2 = 2*np.random.random((81*9,81*9))-1
        self.syn3 = 2*np.random.random((81,81*9)) -1

        pass

    def boardToInput(self, board, playerNumber):
        out = board.field[:] #Copy List!
        out.append([0,0,0,0,0,0,0,0,0])
        outArray =np.zeros(90)
        playerSymb = Board.playerToEntry(playerNumber)
        x=0
        for row in out:
            y=0
            for entry in row:
                if(x<9):
                    outArray[x*9+y]=entry*playerSymb
                else:
                    outArray[x*9+y]=entry
                y=y+1
            x=x+1
        return outArray
        
    
    def nonlin(self, x, deriv=False):
        #return np.arctan(x)
        if(deriv==True):
            return x*(1-x)
        return 1/(1+np.exp(-x))
            
    def move(self, board, playerNumber):
        # Network makes a
        # l0 = board
        # board = board.field
        log("Move")
        l1 = self.nonlin(np.dot(self.syn0,self.boardToInput(board, playerNumber)))
        log(l1.shape)
        l2 = self.nonlin(np.dot(self.syn1, l1))
        log(l2.shape)
        l3 = self.nonlin(np.dot(self.syn2, l2))
        log(l3.shape)
        l4 = self.nonlin(np.dot(self.syn3, l3))
        log(l4.shape)

        x = l4.tolist().index(max(l4.tolist()))
        x1 = x // 9
        x2 = x % 9
        return Coordinate(x1, x2)

    def updateNet(self, lost, moves, playerNumber):
        i=0
        for x,y,board in moves:
            i=i+1
            # forward propagation (has to be recalculated, because we already adapted the network!
            coord = self.move(board,playerNumber)
            log("updateNet")

            penality = (lost*2 - 1) * (i / len(moves)) # Is 1 if move is losing and -1 if move is winning move
            
            #Propagate Backwards to evaluate how much I have to adapt the network

            l4 = np.zeros(81)
            l4[coord.topLevel*9+coord.bottomLevel]=1
            l4_delta = penality * l4 * 0.5

            log(l4.shape)
            #print(self.syn3.shape)
            l3 = self.nonlin(np.dot(l4.T, self.syn3))
            l3_delta = penality * l3 * 0.25
            
            log(l3.shape)
            l2 = self.nonlin(np.dot(l3.T, self.syn2))
            l2_delta = penality * l2 * 0.125
            
            log(l2.shape)
            l1 = self.nonlin(np.dot(l2.T, self.syn1))
            l1_delta = penality * l1 * 0.0625
            #print(l3)
            
            log(l1.shape)
            l0 = self.nonlin(np.dot(l1.T,self.syn0))
            l0_delta = penality * l0 * 0.125
            #print(l3)
            
            log(l0.shape)
            # update weights
            self.syn3 = self.nonlin(self.syn3 - self.nonlin(np.dot(l3, l3_delta)))
            self.syn2 =self.nonlin(self.syn2 - self.nonlin(np.dot(l2, l2_delta)))
            self.syn1 = self.nonlin(self.syn1 - self.nonlin(np.dot(l1, l1_delta)))
            #print(self.syn0.shape)
            #print(l1_delta.shape)
            self.syn0 = self.nonlin(self.syn0 - self.nonlin(np.dot(l0, l0_delta)))
            #self.syn3 += np.dot(l3.T,l3_delta)
            #self.syn2 += np.dot(l2.T,l3_delta)
            #self.syn1 += np.dot(l1.T,l2_delta)
            #self.syn0 += np.dot(l0.T,l1_delta)

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

for i in range(1000):
    p1 = ComputerPlayer(0,lnn)
    p2 = ComputerPlayer(1,lnn)
    game = Game(p1,p2)
    game.play()
    #print(i)

lnn.printNet()

#print (nonlin(np.dot([1,1,0], syn0)))

