from chess import board
import os
from colorama import init
from termcolor import colored

UNICODE_PIECES = {
  'r': u'♜', 'n': u'♞', 'b': u'♝', 'q': u'♛',
  'k': u'♚', 'p': u'♟', 'R': u'♖', 'N': u'♘',
  'B': u'♗', 'Q': u'♕', 'K': u'♔', 'P': u'♙',
  None: ' '
}

class BoardGuiConsole(object):
    '''
        Print a text-mode chessboard using the unicode chess pieces
    '''
    error = ''

    def __init__(self, chessboard,color):
        self.color = color
        self.board = chessboard


    def load(self,fen):
        self.board.load(fen)

    def move(self):
        os.system("cls")
        self.unicode_representation()
        print("\n", self.error)
        print("State a move in chess notation (e.g. A2A3). Type \"exit\" to leave:\n", ">>>",)
        self.error = ''
        coord = input()
        if coord == "exit":
            print("Bye.")
            exit(0)
        try:
            if len(coord) != 4: raise board.InvalidCoord
            self.board.move(coord[0:2], coord[2:4])
            os.system("cls")
        except board.ChessError as error:
            self.error = "Error: %s" % error.__class__.__name__



    def unicode_representation(self):
        white_square = True
        if(self.color == self.board.player_turn):
            print("    your turn\n")
        else:
            print("    oponent's turn\n")

        for number in self.board.axis_x[::-1]:
            print( " " + str(number) + " ",end="")
            white_square = not white_square
            for letter in self.board.axis_y:
                white_square = not white_square
                bk = "on_grey"
                if (white_square):
                    bk = "on_white"

                fg = "red"

                piece = self.board[letter+str(number)]
                if piece is not None:
                    if piece.abbriviation.isupper():
                        fg = "green"

                if piece is not None:

                    print(colored(piece.abbriviation + ' ',fg,bk),end="")
                else: print(colored('  ',"red",bk),end="")
            print("\n",end="")
        print("   " + " ".join(self.board.axis_y))


def display(board):
    try:
        gui = BoardGuiConsole(board)
        gui.move()
    except (KeyboardInterrupt, EOFError):
        os.system("cls")
        exit(0)

#display(board.Board())