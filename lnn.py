import numpy as np
import supertictactoe as st

class LayerNeuralNetwork():
    
    def nonlin(x, deriv=False):
        moves
        if(deriv==True):
            return x*(1-x)
        return 1/(1+np.exp(-x))
   

    def trainNetwork(self):
        p1 = st.ComputerPlayer(1)
        p2 = st.ComputerPlayer(2)
        
        for i in range(100):
            game = Game(p1,p2)
            
    def move(self, board):
        nonlin(np.dot(board, syn0))

    def updateNet(self):
        move = 0
        for x,y in moves:
            l0 = X
            l1 = nonlin(np.dot(l0,syn0))

            # how much did we miss?
            l1_error = y - l1
            
            # multiply how much we missed by the 
            # slope of the sigmoid at the values in l1
            l1_delta = l1_error * nonlin(l1,True)
            
            # update weights
            syn0 += np.dot(l0.T,l1_delta)
    
# input dataset
X = np.array([  [0,0,1],
                [0,1,1],
                [1,0,1],
                [1,1,1],
                [1,1,0]])
# output dataset            
y = np.array([[0,0,1,1,0]]).T

# seed random numbers to make calculation
# deterministic (just a good practice)
np.random.seed(1)

# initialize weights randomly with mean 0
syn0 = 2*np.random.random((3,1)) - 1
print(syn0)
    
for iter in range(100):

    # forward propagation
    l0 = X
    l1 = nonlin(np.dot(l0,syn0))

    # how much did we miss?
    l1_error = y - l1

    # multiply how much we missed by the 
    # slope of the sigmoid at the values in l1
    l1_delta = l1_error * nonlin(l1,True)

    # update weights
    syn0 += np.dot(l0.T,l1_delta)

X_ = np.array([[1,1,1], [0,1,1], 
               [1,1,0], [1,0,0], 
               [1,0,0], [0,0,1]])

y_ = np.array([[1, 0, 1, 1, 1, 0]]).T

l0 = X_
l1 = nonlin(np.dot(l0,syn0))



print ("Testergebnisse: ")
print (l1)
print ("Neuronales Netz 1: ")
print (syn0)
print (nonlin(np.dot([1,1,0], syn0)))

