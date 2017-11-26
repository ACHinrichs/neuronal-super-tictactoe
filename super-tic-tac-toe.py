from abc import ABC, abstractmethod

# A single coordinate.
class Coordinate:
    topLevel
    bottomLevel 
    def __new__(self,tl,bl):
        topLevel=tl
        bottomLevel=bl

# The Board of the game 
class Board:
    won = array([0,0,0,0,0,0,0,0,0]);
    field
    lastMove = Coordinate(-1,-1)
    
    def __new__(self):
        fieldList = list[]
        for i in Range(1,9):
            fieldList.append(array([0,0,0,0,0,0,0,0,0]))
        self.field= array(fieldList)

# Abstract Base Class for Players
class Player(ABC):
    @abstractmethod
    def move(self, coordinate, board):
        pass

    def 
