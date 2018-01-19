from supertictactoe import Player, Game, Board, Coordinate
import curses
from lnn import LayerNeuralNetwork as lnn

class HumanPlayer(Player):
    pass
    def __init__(self, aNumber, screen):
        super(HumanPlayer, self).__init__()
        self.number = aNumber
        self.out = screen

    def won(self):
        self.out.attron(curses.color_pair(self.number))
        self.out.addstr(1,1,"Du hast Gewonnen!")
        self.out.attroff(curses.color_pair(self.number))
        self.out.refresh()
        
    def lost(self):
        self.out.bkgd(curses.color_pair(self.number))
        self.out.addstr(1,1,"Du hast verloren!")
        self.out.refresh()

    def move(self,board):
        self.out.clear()
        self.out.bkgd(curses.color_pair(self.number))
        self.out.addstr(0,1,"Dein Zug, Spieler "+str(self.number))

        self.out.addstr(3,0,str(board))
        key1=ord('0')
        key2=ord('0')
        while not Board.validMove(board,Coordinate(key1-ord('1'),key2-ord('1'))):
            while not ord('1') <= key1 <= ord('9'):
                key1 = self.out.getch()
            self.out.addstr(14,1,str(key1-ord('1')))
            while not ord('1') <= key2 <= ord('9'):
                key2 = self.out.getch()
            self.out.addstr(14,3,str(key2-ord('1')))
            self.out.refresh()
            if ( not Board.validMove(board,Coordinate(key1-ord('1'),key2-ord('1')))):
                self.out.addstr(14,5,"INVALID MOVE")
                key1=ord('0')
                key2=ord('0')
            else:
                self.out.addstr(14,5,"OK!")
        return Coordinate(key1-ord('1'),key2-ord('1'))

class ConmputerPlayer(Player):
    pass
    def __init__(self, aNumber):
        self.number = aNumber

    def won(self):
        #lnn.updateNet()

    def lost(self):
        lnn.updateNet()

    def move(self, board):
        move = lnn.move();
        return Coordinate(move[0], move[1])

# Init curse
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
curses.start_color()
curses.use_default_colors()

curses.init_pair(1, curses.COLOR_RED, -1)
curses.init_pair(2, curses.COLOR_BLUE, -1)


# Ready game
p1 = HumanPlayer(1,stdscr)
p2 = HumanPlayer(2,stdscr)
game = Game(p1,p2)

# Playe
game.play()
stdscr.getkey()

# End curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
