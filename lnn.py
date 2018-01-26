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
        if board.lastMove == Coordinate(-1,-1):
            log("Rand move",3)
            return Coordinate(np.random.randint(0,9),np.random.randint(0,9))
        c =  self.nw.move(board, self.number);
        self.moves.append([c.topLevel,c.bottomLevel ,board])
        return c;
        

class LayerNeuralNetwork():

    # Number of neurons takes a list with the number of neurons (not connections between them!) including the input and output layer.
    # All layers are vectors!
    def __init__(self,numberOfNeurons):
        self.syn = []
        for i in range(1,len(numberOfNeurons)):
            self.syn.append(2*np.random.rand(numberOfNeurons[i],numberOfNeurons[i-1])-1)
        self.numOut = numberOfNeurons[len(numberOfNeurons)-1]
        self.numIn  = numberOfNeurons[0]

    def boardToInput(self, board, playerNumber):
        out = board.field[:] #Copy List!
        out.append([0,0,0,0,0,0,0,0,0])
        if(board.lastMove == Coordinate(-1,-1)):
            out[9] = [1,1,1,1,1,1,1,1,1]
        else:
            out[9][board.lastMove.bottomLevel] = 1

        outArray =np.zeros((90,1))
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
        
    def neuronActivation(self,x):
        #For sigmoid-Neurons
        return 1/(1+np.exp(-x))
    
    def move(self, board, playerNumber):
        neurons = self.boardToInput(board, playerNumber)
        log("move "+str(neurons.shape),2)
        for layer in self.syn:
            neurons = self.neuronActivation(np.dot(layer, neurons))
            log("move "+str(neurons.shape),2)
        active = neurons.tolist().index(max(neurons))
        return Coordinate( active// 9, active %9)

    def updateNet(self, lost, moves, playerNumber):
        moveNum = 0
        for x,y,board in moves:
            moveNum=moveNum + 1
            # FIrst calculate how the net would move, because it could have been updated
            newMove = self.move(board,playerNumber)
            if not newMove == Coordinate(x,y):
                # If they are not equal, we have already altered the network a lot,
                # so that every new alteration could make it worse
                log("Do not update net, suggesting different move",1)
                return

            # Create idealize move
            neurons = np.zeros((self.numOut,1))
            neurons[x*9+y] = 1
            log("update "+str(neurons.shape),2)
            # Propagate the move backwards
            #Iterate backwards over syns
            newSyn = []
            changeFactor = 0.5  
            penality = (2*lost-1) * moveNum/len(moves)*len(moves)
            for layer in self.syn[::-1]:
                neuronsLower = self.neuronActivation(np.dot(layer.T,neurons))
                
                # Adapt layer network
                log("update n"+str(neurons.shape),2)
                log("update l"+str(neuronsLower.shape),2)
                log(neuronsLower, 3)
                newSyn.append(layer - np.dot(neurons,neuronsLower.T)*changeFactor*lost)
                changeFactor = changeFactor *0.5
                
                neurons = neuronsLower
            self.syn = newSyn[::-1]
            
    def printNet(self):
        for layer in self.syn:
            print(layer)


# seed random numbers to make calculation
# deterministic
np.random.seed(1)


lnn = LayerNeuralNetwork([90, 90*9, 90*9, 90*9, 81*9, 81])
lnn2 = LayerNeuralNetwork([90, 90*9, 90*9, 90*9, 81*9, 81])

# train Network
lnn.printNet()
netStart = lnn.syn[:]
input("ENTER zum starten")
for i in range(1000):
    p1 = ComputerPlayer(0,lnn)
    p2 = ComputerPlayer(1,lnn)
    game = Game(p1,p2)
    game.play()
    log(game.board,2)
    #print(i)

lnn.printNet()

changeLogPrio=0
log("Change of syn:",changeLogPrio)
i=0
for layer in netStart:
    log(lnn.syn[i] - netStart[i],changeLogPrio)
    i=i+1

#print (nonlin(np.dot([1,1,0], syn0)))

