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
        #TODO

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
        #TODO

    def updateNet(self, lost, moves, playerNumber):
        #TODO

    def printNet(self):
        #TODO


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

