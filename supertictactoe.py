from abc import ABC, abstractmethod

# A single coordinate.
class Coordinate: 
    def __init__(self,tl,bl):
        self.topLevel=tl
        self.bottomLevel=bl

    def __str__(self):
        return "("+str(self.topLevel)+","+str(self.bottomLevel)+")"

# The Board of the game 
class Board:
    won = [0,0,0,0,0,0,0,0,0];
    field = []
    lastMove = Coordinate(-1,-1)
    
    def __init__(self):
        fieldList = []
        for i in range(9):
            fieldList.append([0,0,0,0,0,0,0,0,0])
        self.field=fieldList

    def __str__(self):
        result=""
        for l in range(3):
            for k in range(3):
                for j in range(3):
                    for i in range(3):
                        result=result+self.symbol(self.field[j+l*3][i+k*3])
                    if j < 2: result=result+"│"
                result=result+"\n"
            if l < 2: result=result+"───┼───┼───\n"

        result=result+"\n"
        for j in range(3):
            for i in range(3):
                result=result+self.symbol(self.won[i+j*3])
                if i < 2: result=result+"│"
            if j < 2: result=result+"\n─┼─┼─\n"
        result=result+"\n\nLast Move: "+str(self.lastMove)
        return result
    
    @staticmethod
    def symbol(p):
        if p == 1:
            return "0"
        if p == -1:
            return "X"
        return " "
                    
    @staticmethod
    def validMove(b,m):
        #  Indexes are in [0,9]               
        res = (0<= m.bottomLevel < 9 ) and (0<= m.topLevel < 9 )
        #  TL field has not been won, 
        res = res and (b.won[m.topLevel]==0)
        # last BL is current TL, except for first move and if last bl-tl is taken 
        res = res and (b.lastMove.bottomLevel==m.topLevel or b.lastMove.bottomLevel==-1
                       or b.field[b.lastMove.bottomLevel]!=0)
        # field is unused
        res = res and (b.field[m.topLevel][m.bottomLevel]==0)
        return res
    
    def mark(self,m,p):
        if p==0:
            self.field[m.topLevel][m.bottomLevel]=-1
        else:
            self.field[m.topLevel][m.bottomLevel]=1
        self.lastMove=m

    def hasWinner(self):
        for i in range(9):
            winner = self.tttWinner(self.field[i])
            if winner != -1:
                self.won[i]=self.playerToEntry(winner)
        return self.tttWinner(self.won)

    # converts the entry to the player Number, because of simplicity the entrys are -1 and 1, while the playernumbers are 0 and 1
    @staticmethod
    def entryToPlayer(entry):
            if entry == 1:
                return 0
            if entry ==-1:
                return 1
            return -1
            
    # converts the entry to the player Number, because of simplicity the entrys are -1 and 1, while the playernumbers are 0 and 1
    @staticmethod
    def playerToEntry(playerNum):
            if playerNum == 0:
                return 1
            if playerNum == 1:
                return-1
            
    # Evaluates the winner of a tictactoe field
    @staticmethod
    def tttWinner(tttboard):
        for i in range(3):
            row=Board.entryToPlayer((tttboard[i*3] + tttboard[i*3 + 1] + tttboard[i*3 + 2])/3)
            if row != -1:
                return row
            column=Board.entryToPlayer((tttboard[0+i] + tttboard[3+i] + tttboard[4+i])/3)
            if column != -1:
                return column
        cross = Board.entryToPlayer((tttboard[0] + tttboard[4] + tttboard[8])/3)
        if cross != -1:
            return cross
        cross = Board.entryToPlayer((tttboard[6] + tttboard[4] + tttboard[2])/3)
        return cross
    
# Abstract Base Class for Players
class Player(ABC):
    @abstractmethod
    def move(self, coordinate, board):
        pass

    @abstractmethod
    def won(self):
        pass

    @abstractmethod
    def lost(self):
        pass

class Game:
    
    def __init__(self,p1,p2):
        self.board = Board()
        self.players=[]
        self.players.append(p1)
        self.players.append(p2)
        
    def play(self):
        playing=True
        player=0
        while playing:
            move = self.players[player].move(self.board)

            if self.board.validMove(self.board,move):
                self.board.mark(move,player)
            else:
                self.end((player+1)%2)
            winner = self.board.hasWinner()
            if winner != -1:
                self.end(winner)
                return
            player=(player+1) % 2

    # to alert the players of the end of the match
    def end(self,wonBy):
        self.players[wonBy].won()
        self.players[(wonBy+1)%2].lost()
