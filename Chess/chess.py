# 15-112: Principles of Programming and Computer Science
# Project: Chess Program
# Name      : Muhammad Nahin Khan
# AndrewID  : mnk1
# File Created: 07/11/2016
# Modification History:
# Start             End
# 07/11 12:52       07/11 13:20
# 07/11 18:00       07/11 21:06
# 09/11 03:13       09/11 05:49
# 09/11 15:38       09/11 16:19
# 10/11 15:51       10/11 16:31
# 10/11 20:17       10/11 21:34
# 11/11 23:50       12/11 05:19
# 13/11 00:01       13/11 01:34
# 15/11 16:19       15/11 17:00
# 16/11 01:00       16/11 01:49
# 16/11 12:50       16/11 13:31
# 17/11 21:20       17/11 22:21
# 18/11 00:15       18/11 01:15
# 18/11 19:01       19/11 20:20
# 21/11 00:56       21/11 02:01
# 21/11 19:36       21/11 20:30
# 22/11 18:10       22/11 20:02
# 23/11 01:00       23/11 02:30
# 23/11 18:05       23/11 20:03
# 25/11 04:10       25/11 04:50
# 25/11 13:00       25/11 14:35
# 25/11 18:35       25/11 19:25
# 26/11 08:04       26/11 08:31
# 26/11 21:44       26/11 23:31
# 27/11 02:24       27/11 03:08
#
# modified by schreibfaul1
# 27/11/2019 17:09 make it runable in Python3
# 27/11/2019 17:09 new board and new figures (as single png)
# 27/11/2019 20:35 AI schould start after transitioning, new flag: awaitAI
# 28/11/2019 05:30 attribute read is no longer 'r+' is now 'rb" (and 'wb' for write)
# 28/11/2019 05:50 put all shades in an folder
# 28/11/2019 05:50 openingTable.txt is damaged, create new file (make a better one later)
# 28/11/2019 12:00 keep all globals on one place
# 28/11/2019 16:30 soundfiles added
# 29/11/2019 16:00 implement Stockfish AI
# 29/11/2019 18:27 board flips according to a player

# Ensure that Pygame is installed

# GUI inspired by: #https://en.lichess.org/
# AI ideas from: #https://chessprogramming.wikispaces.com/

# An online lecture that helped me understand alpha-beta pruning:
# Winston, P. [MIT OpenCourseWare]. (2010) 6. Search: Games, Minimax, and Alpha-Beta.
# [Video File].Retrieved from https://www.youtube.com/watch?v=STjW3eH0Cik

# Special thanks to professor Saquib for being so amazing.

# This program is a chess game. The user may play against a friend or the computer.
# The game state is mainly stored as a 2D list of strings, and most of the processing is thus done on a list of
# strings. The GUI takes the current state and displays it on the screen. The GUI allows drag and drop movement
# of pieces as well as click-click movement. The AI that plays against the human evaluates all possible moves made by
# either player up to a certain level of depth. The AI evaluates each position by giving it a score. The higher the
# value of the score, the more favourable a position is for white and the lower the value of the score, the more
# favourable the position is for black. Knowing that white will try to get the score to be higher and black will
# try and get the score to be lower, the AI assumes best play from either side as it traverses up the search tree and
# chooses the best move to be played. A problem that may arise is the number of postions that need to be evaulated.
# Even at 3 levels of depth, thousands of positions have to be evaluatd.
# Several methods are used in this program to reduce positions that are searched:
# 1. Alpha-beta pruning: As a result of  evaluating a position it can be found that a portion of the search tree can
#    be ignored as no further evaluations can guarantee better results. This can happen because white and black area
#    against one another. White plays what is best for it and black plays what is best for it, so it would make sense
#    for white to ignore any portion of the tree where black has a clear upperhand that it can choose to play.
# 2. Transposition table: Often, two different pathways in a search tree can result in the same board being evaluated.
#    Instead of evaluating the same board several times, the program stores a table of values in a dictionary where
#    the keys are the positions. This way, repeated positions can have their evaluations looked up fairly quickly,
#    as the board state is hashed.
# 3. Opening Book - The opening book is again a dictionary that stores board positions often seen in the beginning few
#    moves in chess. Appropraite moves that can be played at such positions is stored in the dictionary. A random move
#    is selected and played from the list of suggested moves wihtout searching if the AI finds itself confronting a
#    such a board postion. Note that this opening book was recorded by myself and so it does not have many positions
#    stored in it.
# In order to traverse the search tree as above, the AI needs to know how to evaluate the board at any position to
# decide if white or black has the advantage. My evaluation function currently looks at three main things when
# evaluating the board:
# a) Material for white and black. Each piece has a value and the more pieces you have, the better off your position
#    is likely to be. For example, if white has an extra queen, it has an advantage over black.
# b) Piece-square table values - for each piece, there is a table that stores the best squares that the particular
#    piece should occupy. So if white has a knight at a good square that controls the centre of the board, whereas
#    black has a knight at the corner of the board, the situation is evaluated as being more favourable
#    for white.
# c) Reduction in points for doubled pawns, isolated pawns, and blocked pawns. If any side has a set of pawns with
#    the above features their points are slightly lower to indicate a slight disadvantage in such a position.
# d) A checkmate: a position where this has occured gets a very high point, so that the AI moves towards this if it
#    can. (or avoids it).
# There are also several ways in which this program may be improved:
# 1. Move ordering: Given a certain position and the AI needs to search a few layers deep from it, somehow pre-sorting
#    each move by ranking them in their likelihood of being good moves allows for earlier cut-offs to be made by
#    alpha-beta pruning.
# 2. Iterative Deepening: Instead of going directly to a given depth when searching, the A.I. may evaluate the best
#    move at depth 1, then depth 2, then depth 3, etc. until it reaches the final depth it needed to calculate at
#    depth n. The reason for this is that it may be mathematically shown that this does not dignificantly increase
#    computation and allows the A.I. to make its best move if it needs to abide by a time limit.
# 3. Better data structure - I believe the structure I have used to keep the state of the board (list of a list)
#    may be slowing down accessing its elements or assigning its elements. Improvement in efficiency of my code by
#    changing data structures may potentially improve the speed at which my AI makes its move.
# 4. Import of large opening tables: There are databases available online that store the best moves played by
#    grandmasters at various key opening positions of the chess game. Although my AI does make use of an opening
#    table that I recorded for it myself, it is not able to respond to many opening positions using the table since
#    the table only convers few positions. If an opening table with millions of positions could be imported to this
#    program, the AI's moves would improve in the beginning. It would also give it more variety in terms of the move
#    it plays. Furthermore, using good openings allows the AI to make the best moves in the field it is best at
#    middle game tactics.
# 5. Better evaluation of positions - The current features evaluated by the evaluation function when judging a
#    positoin to give it a score allows for good opening games and tactics that often allow it to gain advantage
#    over the opponents that I have tested itagainst. However, there are many aspects of playing good  chess
#    that it does not consider: like having good mobility of your pieces (eg a trapped bishop should be bad for the
#    AI but it doesn't know that). Other aspects include king safety, pawn structure, etc. It could also use different
#    evaluation for each game phase. For example, a pawn is not worth much at the opening phase of the game but in the
#    endgame it is very important and so should be evaulated as a valuable piece.
# 6. Endgame tables - As good as my AI may be in middle games, given a queen and a king to attempt checkmate against
#    a lone king, it would be unlikely for it to succeed. This is because such checkmates, despite being simple,
#    require a large number of combination of moves to occur, the depth of which my AI would not be able to see.
#    So endgame table allows it to know (for a very large number of endgame positions) the best move to play in order
#    to attempt a win or a draw (or try its best to avoid a loss).
#
# Note about coordinates:
# Normally, algebraic notation is used to specify a box on a chess board. In this program, coordinates will be index
# referecnesto the 2_D array that stores thestate of the board. Thus, e4 in algebraic notation would be expressed
# as (4,3) in this program.

# Import dependencies:


import pygame  # Game library
from pygame.locals import *  # For useful variables
import copy  # Library used to make exact copies of lists.
import pickle  # Library used to store dictionaries in a text file and read them from text files.
import random  # Used for making random selections
from collections import defaultdict  # Used for giving dictionary values default data types.
from collections import Counter  # For counting elements in a list effieciently.
import threading  # To allow for AI to think simultaneously while the GUI is coloring the board.
import os  # To allow path joining with cross-platform support
from stockfish import Engine

# global var
boardSize = 680  # height and width in px
searchDepth = 3  # or 4
player = 0  # This is the player that makes the next move. 0 is white, 1 is black
AIPlayer = -1  # will  be set later; 1 means: AI playes black
winner = ""  # will be 'w' or 'b'
prevMove = [-1, -1, -1, -1]  # stores the last move, to allow drawBoard() to create Shades on the squares.
appPath = os.path.dirname(__file__)
mediaPath = appPath + '/Media'
soundPath = appPath + "/Media/Sounds"
piecesImagePath = appPath + '/Media/Pieces'
shadesImagePath = appPath + '/Media/Shades'
offset = int(boardSize / 34)  # boarderwidth in px
squareSize = int((boardSize - 2 * offset) / 8)  # the size of the individual squares
screen = pygame.display.set_mode((boardSize, boardSize))  # Load the screen x, y with size
gameEnded = False  # keep false until the user wants to quit.
isRecord = False  # Set this to True if you want to record moves to the Opening Book.
awaitAI = False  # let start the AI after transitioning has ended
isClicked = False  # is True after mouse leftclick
isTransition = False  # a piece is moving
isFlip = -1  # initial value, flips the board if True
isDraw = False  # Will store True if the game ended with a draw
isDown = False  # a variable that shows if the mouse is being held down
isMenu = True  # for showing the menu and keeping track of user choices.
listofWhitePieces = []
listofBlackPieces = []
listofShades = []
openings = defaultdict(list)  # Initialize the opening book dictionary,and set its values by default.
isAI = -1
isAIThink = False  # Stores whether or not the AI is calculating the best move to be played.
chessEnded = False  # Will become True once the chess game ends by checkmate, stalemate, etc.
ax, ay = 0, 0  # For animating AI thinking graphics
numm = 0  # AI related
colorsign = 0  # AI related
bestMoveReturn = []  # AI related
searched = {}  # global variable that allows negamax to keep track of nodes that have already been evaluated.
bm = None  # global, stores Stockfish's best move
En_Passant_Target = -1  # stores a coordinate if there is a square that can be en passant captured on.
castling_rights = [[True, True], [True, True]]  # [wQueenside, wKingside],[bQueenside, bKingside]
clock = pygame.time.Clock()  # Helps controlling fps of the game.
half_move_clock = 0  # This variable stores the number of reversible moves that have been played so far.
FMN = 1  # FullMoveNumber, begins with 1, ever

# board in basic position
board = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],  # 8
         ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],  # 7
         [0, 0, 0, 0, 0, 0, 0, 0],  # 6
         [0, 0, 0, 0, 0, 0, 0, 0],  # 5
         [0, 0, 0, 0, 0, 0, 0, 0],  # 4
         [0, 0, 0, 0, 0, 0, 0, 0],  # 3
         ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],  # 2
         ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]  # 1
# a      b     c     d     e     f     g     h

# Load the images:
background = pygame.image.load(os.path.join(mediaPath, 'board.png')).convert()
background_flip = pygame.image.load(os.path.join(mediaPath, 'board_flip.png')).convert()
icon = pygame.image.load(os.path.join(mediaPath, "chess.jpg"))  # shown in windows title and taskbar
circle_image_green = pygame.image.load(os.path.join(shadesImagePath, 'green_circle_small.png')).convert_alpha()
circle_image_capture = pygame.image.load(os.path.join(shadesImagePath, 'green_circle_neg.png')).convert_alpha()
circle_image_red = pygame.image.load(os.path.join(shadesImagePath, 'red_circle_big.png')).convert_alpha()
greenbox_image = pygame.image.load(os.path.join(shadesImagePath, 'green_box.png')).convert_alpha()
circle_image_yellow = pygame.image.load(os.path.join(shadesImagePath, 'yellow_circle_big.png')).convert_alpha()
circle_image_green_big = pygame.image.load(os.path.join(shadesImagePath, 'green_circle_big.png')).convert_alpha()
yellowbox_image = pygame.image.load(os.path.join(shadesImagePath, 'yellow_box.png')).convert_alpha()
withfriend_pic = pygame.image.load(os.path.join(shadesImagePath, 'withfriend.png')).convert_alpha()
withAI_pic = pygame.image.load(os.path.join(shadesImagePath, 'withAI.png')).convert_alpha()
playwhite_pic = pygame.image.load(os.path.join(shadesImagePath, 'playWhite.png')).convert_alpha()
playblack_pic = pygame.image.load(os.path.join(shadesImagePath, 'playBlack.png')).convert_alpha()
flipEnabled_pic = pygame.image.load(os.path.join(shadesImagePath, 'flipEnabled.png')).convert_alpha()
flipDisabled_pic = pygame.image.load(os.path.join(shadesImagePath, 'flipDisabled.png')).convert_alpha()

# Rescale the images so that each piece can fit in a square:
background = pygame.transform.scale(background, (boardSize, boardSize))
background_flip = pygame.transform.scale(background_flip, (boardSize, boardSize))
circle_image_green = pygame.transform.scale(circle_image_green, (squareSize, squareSize))
circle_image_capture = pygame.transform.scale(circle_image_capture, (squareSize, squareSize))
circle_image_red = pygame.transform.scale(circle_image_red, (squareSize, squareSize))
greenbox_image = pygame.transform.scale(greenbox_image, (squareSize, squareSize))
yellowbox_image = pygame.transform.scale(yellowbox_image, (squareSize, squareSize))
circle_image_yellow = pygame.transform.scale(circle_image_yellow, (squareSize, squareSize))
circle_image_green_big = pygame.transform.scale(circle_image_green_big, (squareSize, squareSize))
withfriend_pic = pygame.transform.scale(withfriend_pic, (squareSize * 4, squareSize * 4))
withAI_pic = pygame.transform.scale(withAI_pic, (squareSize * 4, squareSize * 4))
playwhite_pic = pygame.transform.scale(playwhite_pic, (squareSize * 4, squareSize * 4))
playblack_pic = pygame.transform.scale(playblack_pic, (squareSize * 4, squareSize * 4))
flipEnabled_pic = pygame.transform.scale(flipEnabled_pic, (squareSize * 4, squareSize * 4))
flipDisabled_pic = pygame.transform.scale(flipDisabled_pic, (squareSize * 4, squareSize * 4))

# Start pygame
pygame.init()
pygame.display.set_caption('Shallow Green')
pygame.display.set_icon(icon)
screen.blit(background, (0, 0))

# Load the sounds:
snd_mov = pygame.mixer.Sound(soundPath + '/move.wav')
snd_cap = pygame.mixer.Sound(soundPath + '/capture.wav')


# -----------------------------------------------------------------------------------------------------------------------
class GamePosition:
    '''
    GamePosition - This class stores a chess position. A chess position constitutes several features that specify
    the state of the game, such as the the player that has to play next, castling rights of the players, number
    of irreversible moves played so far, the positions of pieces on the board, etc.
    '''

    def __init__(self, board, player, castling_rights, EnP_Target, HMC, FMN, history={}):
        self.board = board  # A 2D array containing information about piece postitions. Check main
        # function to see an example of such a representation.
        self.player = player  # Stores the side to move. If white to play, equals 0. If black to
        # play, stores 1.
        self.castling = castling_rights  # A list that contains castling rights for white and
        # black. Each castling right is a list that contains right to castle kingside and queenside.
        self.EnP = EnP_Target  # Stores the coordinates of a square that can be targeted by en passant capture.
        self.HMC = HMC  # Half move clock. Stores the number of irreversible moves made so far, in order to help
        # detect draw by 50 moves without any capture or pawn movement.
        # Fullmove number: The number of the full move. It starts at 1, and is incremented after Black's move.
        self.FMN = FMN
        self.history = history  # A dictionary that stores as key a position (hashed) and the value of each of
        # these keys represents the number of times each of these positions was repeated in order for this
        # position to be reached.

    def getboard(self):
        return self.board

    def setboard(self, board):
        self.board = board

    def getplayer(self):
        return self.player

    def setplayer(self, player):
        self.player = player

    def getCastleRights(self):
        return self.castling

    def setCastleRights(self, castling_rights):
        self.castling = castling_rights

    def getEnP(self):
        return self.EnP

    def setEnP(self, EnP_Target):
        self.EnP = EnP_Target

    def getHMC(self):
        return self.HMC

    def setHMC(self, HMC):
        self.HMC = HMC

    def getFMN(self):
        return int(self.FMN)

    def setFMN(self, FMN):
        self.FMN = int(FMN)

    def increaseFMN(self):
        self.FMN += 0.5
        return int(self.FMN)

    def checkRepition(self):  # Returns True if any of of the values in the history dictionary is greater than 3. This
        # would mean a position had been repeated at least thrice in order to reach the current position in this game.
        return any(value >= 3 for value in self.history.values())

    def addtoHistory(self, position):  # Generate a unique key out of the current position.
        key = pos2key(position)
        self.history[key] = self.history.get(key, 0) + 1  # Add it to the history dictionary.

    def gethistory(self):
        return self.history

    def clone(self):  # This method returns another instance of the current object with exactly the same parameters
        # but independent of the current object.
        clone = GamePosition(copy.deepcopy(self.board),  # Independent copy
                             self.player,
                             copy.deepcopy(self.castling),  # Independent copy
                             self.EnP,
                             self.HMC,
                             self.FMN)
        return clone


# -----------------------------------------------------------------------------------------------------------------------
class Shades:
    '''
    Shades - This is used for GUI. A shade is a transparent colored image that is displayed on a specific square of the
    chess board, in order to show various things to the user such as the squares to which a piece may move, the square
    that is currently selected, etc. The class stores a reference to the image that the instance of the class should
    display when needed. It also stores the coordinates at which the shade would be applied.
    '''

    def __init__(self, image, coord):
        self.image = image
        self.pos = coord

    def getInfo(self):
        return [self.image, self.pos]


# -----------------------------------------------------------------------------------------------------------------------
class Piece:
    '''
    Piece - This is also used for GUI. A Piece object stores the information about the image that a piece should
    display (pawn, queen, etc.) and the coordinate at which it should be displayed on thee chess board.
    '''

    def __init__(self, pieceInfo, chessCoord):
        # pieceinfo is a string such as 'Qb'. The Q represents Queen and b
        # shows the fact that it is black:
        piece = pieceInfo[0]
        color = pieceInfo[1]
        # Get the information about where the image for this piece is stored
        # on the overall sprite image with all the pieces. Note that
        # square_width and square_height represent the size of a square on the
        # chess board.
        if piece == 'K':
            index = 0
        elif piece == 'Q':
            index = 1
        elif piece == 'B':
            index = 2
        elif piece == 'N':
            index = 3
        elif piece == 'R':
            index = 4
        elif piece == 'P':
            index = 5
        left_x = squareSize * index
        if color == 'w':
            left_y = 0
        else:
            left_y = squareSize
        self.pieceInfo = pieceInfo
        self.chess_coord = chessCoord
        self.pos = (-1, -1)

    def getInfo(self):
        return [self.chess_coord, self.pieceInfo, self.pos]

    def setpos(self, pos):
        self.pos = pos

    def getpos(self):
        return self.pos

    def setcoord(self, coord):
        self.chess_coord = coord

    def __repr__(self):
        # useful for debugging
        return self.pieceInfo + '(' + str(chess_coord[0]) + ',' + str(chess_coord[1]) + ')'


# -----------------------------------------------------------------------------------------------------------------------


# ///////////////////////////////CHESS PROCESSING FUNCTIONS////////////////////
#
# drawText(board) - This function is not called in this program. It is useful for debugging
# purposes, as it allows a board to be printed to the screen in a readable format.
#
# isOccupied(board,x,y) - Returns true if a given coordinate on the board is not empty, and
# false otherwise.
#
# isOccupiedby(board,x,y,color) - Same as above, but only returns true if the square
# specified by the coordinates is of the specifc color inputted.
#
# filterbyColor(board,listofTuples,color) - This function takes the board state, a list
# of coordinates, and a color as input. It will return the same list, but without
# coordinates that are out of bounds of the board and also without those occupied by the
# pieces of the particular color passed to this function as an argument. In other words,
# if 'white' is passed in, it will not return any white occupied square.
#
# lookfor(board,piece) - This functions takes the 2D array that represents a board and finds 
# the indices of all the locations that is occupied by the specified piece. The list of 
# indices is returned.
#
# isAttackedby(position,target_x,target_y,color) - This function checks if the square specified
# by (target_x,target_y) coordinates is being attacked by any of a specific colored set of pieces.
#
# findPossibleSquares(position,x,y,AttackSearch=False) - This function takes as its input the
# current state of the chessboard, and a particular x and y coordinate. It will return for the
# piece on that board a list of possible coordinates it could move to, including captures and 
# excluding illegal moves (eg moves that leave a king under check). AtttackSearch is an
# argument used to ensure infinite recursions do not occur.
#
# makemove(position,x,y,x2,y2) - This function makes a move on the board. The position object
# gets updated here with new information. (x,y) are coordinates of the piece to be moved, and
# (x2,y2) are coordinates of the destination. (x2,y2) being correct destination (ie the move
# a valid one) is not checked for and is assumed to be the case.
#
# opp(color) - Returns the complimentary color to the one passed. So inputting 'black' returns
# 'w', for example.
#
# isCheck(position,color) - This function takes a position as its input and checks if the
# King of the specified color is under attack by the enemy. Returns true if that is the case, 
# and false otherwise.
#
# isCheckmate(position,color=-1) - This function tells you if a position is a checkmate.
# Color is an optional argument that may be passed to specifically check for mate against a
# specific color.
#
# isStalemate(position) - This function checks if a particular position is a stalemate.
# If it is, it returns true, otherwise it returns false.
#
# getallpieces(position,color) - This function returns a list of positions of all the pieces on
# the board of a particular color.
#
# allMoves(position, color) - This function takes as its argument a position and a color/colorsign
# that represents a side. It generates a list of all possible moves for that side and returns it.
#
# pos2key(position) - This function takes a position as input argument. For this particular 
# position, it will generate a unique key that can be used in a dictionary by making it hashable.
#

##/////////////////////////////////////////////GUI FUNCTIONS////////////////////////////////
# chess_coord_to_pixels(chess_coord) - This function takes as input a chess coordinate such as
# (4,7). It returns the top left corner pixel at which a piece of the given size should be
# placed on the board for it to appear at the correct square.
#
# pixel_coord_to_chess(pixel_coord) - Does the exact opposite of above, namely taking the 
# pixel coordinate and giving back the chess coordinate of a particular square.
#
# getPiece(chess_coord) - Gives back the reference to the Piece object that occupies
# a particular chess coordinate.
#
# createPieces(board) - Loops through all the pieces in the inputted board array
# and creates an instance of Piece class for each of them. Returns a list of two
# lists: one that contains all the references to the white pieces, and the other 
# for black.
#
# createShades(listofTuples) - This will modify the global list listofShades. It
# will create instance of class Shade for all the specified coordinates given in
# listofTuples (the input argument). These squares are ones that are attacked by
# a particular piece. Furthermore, it will append other appropriate shades as well,
# such as shades used to show checkmate or stalemate.
#
# drawBoard() - Blits to the screen the board, the pieces, and the shades needed
# to make the game look nice.
#

##################################/////CHESS PROCESSING FUNCTIONS\\\\########################
def drawText(board):
    for i in range(len(board)):
        for k in range(len(board[i])):
            if board[i][k] == 0:
                board[i][k] = 'Oo'
        print(board[i])
    for i in range(len(board)):
        for k in range(len(board[i])):
            if board[i][k] == 'Oo':
                board[i][k] = 0


def isOccupied(board, x, y):
    if board[y][x] == 0:
        # The square has nothing on it.
        return False
    return True


def isOccupiedby(board, x, y, color):
    if board[y][x] == 0:
        # the square has nothing on it.
        return False
    if board[y][x][1] == color[0]:
        # The square has a piece of the color inputted.
        return True
    # The square has a piece of the opposite color.
    return False


def filterbyColor(board, listofTuples, color):
    filtered_list = []
    # Go through each coordinate:
    for pos in listofTuples:
        x = pos[0]
        y = pos[1]
        if x >= 0 and x <= 7 and y >= 0 and y <= 7 and not isOccupiedby(board, x, y, color):
            # coordinates are on-board and no same-color piece is on the square.
            filtered_list.append(pos)
    return filtered_list


def lookfor(board, piece):
    listofLocations = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == piece:
                x = col
                y = row
                listofLocations.append((x, y))
    return listofLocations


def isAttackedby(position, target_x, target_y, color):
    # Get board
    board = position.getboard()
    # Get b from black or w from white
    color = color[0]
    # Get all the squares that are attacked by the particular side:
    listofAttackedSquares = []
    for x in range(8):
        for y in range(8):
            if board[y][x] != 0 and board[y][x][1] == color:
                listofAttackedSquares.extend(
                    findPossibleSquares(position, x, y, True))  # The true argument
                # prevents infinite recursion.
    # Check if the target square falls under the range of attack by the specified
    # side, and return it:
    return (target_x, target_y) in listofAttackedSquares


def findPossibleSquares(position, x, y, AttackSearch=False):
    # Get individual component data from the position object:
    board = position.getboard()
    player = position.getplayer()
    castling_rights = position.getCastleRights()
    EnP_Target = position.getEnP()
    # In case something goes wrong:
    if len(board[y][x]) != 2:  # Unexpected, return empty list.
        return []
    piece = board[y][x][0]  # Pawn, rook, etc.
    color = board[y][x][1]  # w or b.
    # Have the complimentary color stored for convenience:
    enemy_color = opp(color)
    listofTuples = []  # Holds list of attacked squares.

    if piece == 'P':  # The piece is a pawn.
        if color == 'w':  # The piece is white
            if not isOccupied(board, x, y - 1) and not AttackSearch:
                # The piece immediately above is not occupied, append it.
                listofTuples.append((x, y - 1))

                if y == 6 and not isOccupied(board, x, y - 2):
                    # If pawn is at its initial position, it can move two squares.
                    listofTuples.append((x, y - 2))

            if x != 0 and isOccupiedby(board, x - 1, y - 1, 'black'):
                # The piece diagonally up and left of this pawn is a black piece.
                # Also, this is not an 'a' file pawn (left edge pawn)
                listofTuples.append((x - 1, y - 1))
            if x != 7 and isOccupiedby(board, x + 1, y - 1, 'black'):
                # The piece diagonally up and right of this pawn is a black one.
                # Also, this is not an 'h' file pawn.
                listofTuples.append((x + 1, y - 1))
            if EnP_Target != -1:  # There is a possible en pasant target:
                if EnP_Target == (x - 1, y - 1) or EnP_Target == (x + 1, y - 1):
                    # We're at the correct location to potentially perform en
                    # passant:
                    listofTuples.append(EnP_Target)

        elif color == 'b':  # The piece is black, same as above but opposite side.
            if not isOccupied(board, x, y + 1) and not AttackSearch:
                listofTuples.append((x, y + 1))
                if y == 1 and not isOccupied(board, x, y + 2):
                    listofTuples.append((x, y + 2))
            if x != 0 and isOccupiedby(board, x - 1, y + 1, 'white'):
                listofTuples.append((x - 1, y + 1))
            if x != 7 and isOccupiedby(board, x + 1, y + 1, 'white'):
                listofTuples.append((x + 1, y + 1))
            if EnP_Target == (x - 1, y + 1) or EnP_Target == (x + 1, y + 1):
                listofTuples.append(EnP_Target)

    elif piece == 'R':  # The piece is a rook.
        # Get all the horizontal squares:
        for i in [-1, 1]:
            # i is -1 then +1. This allows for searching right and left.
            kx = x  # This variable stores the x coordinate being looked at.
            while True:  # loop till break.
                kx = kx + i  # Searching left or right
                if kx <= 7 and kx >= 0:  # Making sure we're still in board.

                    if not isOccupied(board, kx, y):
                        # The square being looked at it empty. Our rook can move
                        # here.
                        listofTuples.append((kx, y))
                    else:
                        # The sqaure being looked at is occupied. If an enemy
                        # piece is occupying it, it can be captured so its a valid
                        # move.
                        if isOccupiedby(board, kx, y, enemy_color):
                            listofTuples.append((kx, y))
                        # Regardless of the occupying piece color, the rook cannot
                        # jump over. No point continuing search beyond in this
                        # direction:
                        break

                else:  # We have exceeded the limits of the board
                    break
        # Now using the same method, get the vertical squares:
        for i in [-1, 1]:
            ky = y
            while True:
                ky = ky + i
                if 7 >= ky >= 0:
                    if not isOccupied(board, x, ky):
                        listofTuples.append((x, ky))
                    else:
                        if isOccupiedby(board, x, ky, enemy_color):
                            listofTuples.append((x, ky))
                        break
                else:
                    break

    elif piece == 'N':  # The piece is a knight.
        # The knight can jump across a board. It can jump either two or one
        # squares in the x or y direction, but must jump the complimentary amount
        # in the other. In other words, if it jumps 2 sqaures in the x direction,
        # it must jump one square in the y direction and vice versa.
        for dx in [-2, -1, 1, 2]:
            if abs(dx) == 1:
                sy = 2
            else:
                sy = 1
            for dy in [-sy, +sy]:
                listofTuples.append((x + dx, y + dy))
        # Filter the list of tuples so that only valid squares exist.
        listofTuples = filterbyColor(board, listofTuples, color)
    elif piece == 'B':  # A bishop.
        # A bishop moves diagonally. This means a change in x is accompanied by a
        # change in y-coordiante when the piece moves. The changes are exactly the
        # same in magnitude and direction.
        for dx in [-1, 1]:  # Allow two directions in x.
            for dy in [-1, 1]:  # Similarly, up and down for y.
                kx = x  # These varibales store the coordinates of the square being
                # observed.
                ky = y
                while True:  # loop till broken.
                    kx = kx + dx  # change x
                    ky = ky + dy  # change y
                    if kx <= 7 and kx >= 0 and ky <= 7 and ky >= 0:
                        # square is on the board
                        if not isOccupied(board, kx, ky):
                            # The square is empty, so our bishop can go there.
                            listofTuples.append((kx, ky))
                        else:
                            # The square is not empty. If it has a piece of the
                            # enemy,our bishop can capture it:
                            if isOccupiedby(board, kx, ky, enemy_color):
                                listofTuples.append((kx, ky))
                            # Bishops cannot jump over other pieces so terminate
                            # the search here:
                            break
                    else:
                        # Square is not on board. Stop looking for more in this
                        # direction:
                        break

    elif piece == 'Q':  # A queen
        # A queen's possible targets are the union of all targets that a rook and
        # a bishop could have made from the same location
        # Temporarily pretend there is a rook on the spot:
        board[y][x] = 'R' + color
        list_rook = findPossibleSquares(position, x, y, True)
        # Temporarily pretend there is a bishop:
        board[y][x] = 'B' + color
        list_bishop = findPossibleSquares(position, x, y, True)
        # Merge the lists:
        listofTuples = list_rook + list_bishop
        # Change the piece back to a queen:
        board[y][x] = 'Q' + color
    elif piece == 'K':  # A king!
        # A king can make one step in any direction:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                listofTuples.append((x + dx, y + dy))
        # Make sure the targets aren't our own piece or off-board:
        listofTuples = filterbyColor(board, listofTuples, color)
        if not AttackSearch:
            # Kings can potentially castle:
            right = castling_rights[player]
            # Kingside
            if (right[0] and  # has right to castle
                    board[y][7] != 0 and  # The rook square is not empty
                    board[y][7][0] == 'R' and  # There is a rook at the appropriate place
                    not isOccupied(board, x + 1, y) and  # The square on its right is empty
                    not isOccupied(board, x + 2, y) and  # The second square beyond is also empty
                    not isAttackedby(position, x, y, enemy_color) and  # The king isn't under atack
                    not isAttackedby(position, x + 1, y, enemy_color) and  # Or the path through which
                    not isAttackedby(position, x + 2, y, enemy_color)):  # it will move
                listofTuples.append((x + 2, y))
            # Queenside
            if (right[1] and  # has right to castle
                    board[y][0] != 0 and  # The rook square is not empty
                    board[y][0][0] == 'R' and  # The rook square is not empty
                    not isOccupied(board, x - 1, y) and  # The square on its left is empty
                    not isOccupied(board, x - 2, y) and  # The second square beyond is also empty
                    not isOccupied(board, x - 3, y) and  # And the one beyond.
                    not isAttackedby(position, x, y, enemy_color) and  # The king isn't under atack
                    not isAttackedby(position, x - 1, y, enemy_color) and  # Or the path through which
                    not isAttackedby(position, x - 2, y, enemy_color)):  # it will move
                listofTuples.append((x - 2, y))  # Let castling be an option.

    # Make sure the king is not under attack as a result of this move:
    if not AttackSearch:
        new_list = []
        for tupleq in listofTuples:
            x2 = tupleq[0]
            y2 = tupleq[1]
            temp_pos = position.clone()
            makeMove(temp_pos, x, y, x2, y2)
            if not isCheck(temp_pos, color):
                new_list.append(tupleq)
        listofTuples = new_list
    return listofTuples


# -----------------------------------------------------------------------------------------------------------------------
def convert_sf(move):
    # convert Stockfish's notation in board notation  e.g. 'g8f6' -> x1=6, y1=0, x2=5, y2=2
    lst = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    idx = 0
    for x in lst:
        if (move[0] == x):
            x1 = idx
        idx += 1
    y1 = 8 - int(move[1])
    idx = 0
    for x in lst:
        if (move[2] == x):
            x2 = idx
        idx += 1
    y2 = 8 - int(move[3])
    return (x1, y1, x2, y2)


# -----------------------------------------------------------------------------------------------------------------------
def makeMove(position, x, y, x2, y2):
    # Get data from the position:
    board = position.getboard()
    piece = board[y][x][0]
    color = board[y][x][1]
    # Get the individual game components:
    player = position.getplayer()
    castling_rights = position.getCastleRights()
    EnP_Target = position.getEnP()
    half_move_clock = position.getHMC()
    # Update the half move clock:
    if isOccupied(board, x2, y2) or piece == 'P':
        # Either a capture was made or a pawn has moved:
        half_move_clock = 0
    else:
        # An irreversible move was played:
        half_move_clock += 1

    # Make the move:
    board[y2][x2] = board[y][x]
    board[y][x] = 0

    # Special piece requirements:
    # King:
    if piece == 'K':
        # Ensure that since a King is moved, the castling
        # rights are lost:
        castling_rights[player] = [False, False]
        # If castling occured, place the rook at the appropriate location:
        if abs(x2 - x) == 2:
            if color == 'w':
                l = 7
            else:
                l = 0

            if x2 > x:
                board[l][5] = 'R' + color
                board[l][7] = 0
            else:
                board[l][3] = 'R' + color
                board[l][0] = 0
    # Rook:
    if piece == 'R':
        # The rook moved. Castling right for this rook must be removed.
        if x == 0 and y == 0:
            # Black queenside
            castling_rights[1][1] = False
        elif x == 7 and y == 0:
            # Black kingside
            castling_rights[1][0] = False
        elif x == 0 and y == 7:
            # White queenside
            castling_rights[0][1] = False
        elif x == 7 and y == 7:
            # White kingside
            castling_rights[0][0] = False
    # Pawn:
    if piece == 'P':
        # If an en passant kill was made, the target enemy must die:
        if EnP_Target == (x2, y2):
            if color == 'w':
                board[y2 + 1][x2] = 0
            else:
                board[y2 - 1][x2] = 0
        # If a pawn moved two steps, there is a potential en passant
        # target. Otherise, there isn't. Update the variable:
        if abs(y2 - y) == 2:
            EnP_Target = (x, int((y + y2) / 2))
        else:
            EnP_Target = -1
        # If a pawn moves towards the end of the board, it needs to
        # be promoted. Note that in this game a pawn is being promoted
        # to a queen regardless of user choice.
        if y2 == 0:
            board[y2][x2] = 'Qw'
        elif y2 == 7:
            board[y2][x2] = 'Qb'
    else:
        # If a pawn did not move, the en passsant target is gone as well,
        # since a turn has passed:
        EnP_Target = -1

    # Since a move has been made, the other player
    # should be the 'side to move'
    player = 1 - player
    # Update the position data:
    position.setplayer(player)
    position.setCastleRights(castling_rights)
    position.setEnP(EnP_Target)
    position.setHMC(half_move_clock)


# -----------------------------------------------------------------------------------------------------------------------
def opp(color):
    color = color[0]
    if color == 'w':
        oppcolor = 'b'
    else:
        oppcolor = 'w'
    return oppcolor


# -----------------------------------------------------------------------------------------------------------------------
def isCheck(position, color):
    # Get data:
    board = position.getboard()
    color = color[0]
    enemy = opp(color)
    piece = 'K' + color
    # Get the coordinates of the king:
    x, y = lookfor(board, piece)[0]
    # Check if the position of the king is attacked by
    # the enemy and return the result:
    return isAttackedby(position, x, y, enemy)


# -----------------------------------------------------------------------------------------------------------------------
def isCheckmate(position, color=-1):
    if color == -1:
        return isCheckmate(position, 'white') or isCheckmate(position, 'b')
    color = color[0]
    if isCheck(position, color) and allMoves(position, color) == []:
        # The king is under attack, and there are no possible moves for this side to make:
        return True
    # Either the king is not under attack or there are possible moves to be played:
    return False


def isStalemate(position):
    # Get player to move:
    player = position.getplayer()
    # Get color:
    if player == 0:
        color = 'w'
    else:
        color = 'b'
    if not isCheck(position, color) and allMoves(position, color) == []:
        # The player to move is not under check yet cannot make a move.
        # It is a stalemate.
        return True
    return False


def getallpieces(position, color):
    # Get the board:
    board = position.getboard()
    listofpos = []
    for j in range(8):
        for i in range(8):
            if isOccupiedby(board, i, j, color):
                listofpos.append((i, j))
    return listofpos


def allMoves(position, color):
    # Find if it is white to play or black:
    if color == 1:
        color = 'white'
    elif color == -1:
        color = 'black'
    color = color[0]
    # Get all pieces controlled by this side:
    listofpieces = getallpieces(position, color)
    moves = []
    # Loop through each piece:
    for pos in listofpieces:
        # For each piece, find all the targets it can attack:
        targets = findPossibleSquares(position, pos[0], pos[1])
        for target in targets:
            # Save them all as possible moves:
            moves.append([pos, target])
    return moves


def pos2key(position):
    # Get board:
    board = position.getboard()
    # Convert the board into a tuple so it is hashable:
    boardTuple = []
    for row in board:
        boardTuple.append(tuple(row))
    boardTuple = tuple(boardTuple)
    # Get castling rights:
    rights = position.getCastleRights()
    # Convert to a tuple:
    tuplerights = (tuple(rights[0]), tuple(rights[1]))
    # Generate the key, which is a tuple that also takes into account the side to play:
    key = (boardTuple, position.getplayer(),
           tuplerights)
    # Return the key:
    return key


# -----------------------------------------------------------------------------------------------------------------------
#                                 G U I    F U N C T I O N S
# -----------------------------------------------------------------------------------------------------------------------
def coord2pixels(chess_coord):
    x, y = chess_coord
    # There are two sets of coordinates that this function could choose to return.One is the coordinates that would
    # be usually returned, the other is one that would be returned if the board were to be flipped.
    # Note that squareSize are defined in the main function and so are accessible here as global variables.
    if isAI:
        if AIPlayer == 0:  # this means you're playing against the AI and are playing as black.
            return ((7 - x) * squareSize + offset, (7 - y) * squareSize + offset)
        else:
            return (x * squareSize + offset, y * squareSize + offset)
    # Being here means two player game is being played. If the flipping mode is enabled, and the player to play is
    # black, the board should flip, but not until the transition animation for white movement is complete.
    if not isFlip or player == 0 ^ isTransition:
        return (x * squareSize + offset, y * squareSize + offset)
    else:
        return ((7 - x) * squareSize + offset, (7 - y) * squareSize + offset)


# -----------------------------------------------------------------------------------------------------------------------
def pixels2coord(pixel_coord):
    if pixel_coord[0] - offset < 0 or pixel_coord[1] - offset < 0:
        return (8, 8)  # outside the board
    x, y = int((pixel_coord[0] - offset) / squareSize), int((pixel_coord[1] - offset) / squareSize)
    if isAI:
        if AIPlayer == 0:
            return (7 - x, 7 - y)
        else:
            return (x, y)
    if not isFlip or player == 0 ^ isTransition:
        return (x, y)
    else:
        return (7 - x, 7 - y)


# -----------------------------------------------------------------------------------------------------------------------
def getPiece(chess_coord):
    for piece in listofWhitePieces + listofBlackPieces:
        if piece.getInfo()[0] == chess_coord:  # piece.getInfo()[0] represents the chess coordinate occupied by piece.
            return piece


# -----------------------------------------------------------------------------------------------------------------------
def createPieces(board):
    listofWhitePieces = []  # Initialize containers.
    listofBlackPieces = []
    for i in range(8):  # Loop through all squares.
        for k in range(8):
            if board[i][k] != 0:  # The square is not empty, create a piece object.
                p = Piece(board[i][k], (k, i))
                if board[i][k][1] == 'w':  # Append the reference to the object to the appropriate list.
                    listofWhitePieces.append(p)
                else:
                    listofBlackPieces.append(p)
    return [listofWhitePieces, listofBlackPieces]  # Return both.


# -----------------------------------------------------------------------------------------------------------------------
def getFEN(board):  # Forsyth-Edwards Notation
    strFEN = ""
    for row in board:
        count = 0
        for col in row:
            if col == 0:  # is a space
                count += 1
            else:
                if count != 0:
                    strFEN += str(count)
                    count = 0
                if col[1] == 'b':
                    col = col.lower()
                    strFEN += col[0]
                else:
                    strFEN += col[0]
        if count != 0:
            strFEN += str(count)
            count = 0
        strFEN += '/'
    strFEN = strFEN[:-1]  # remove the last '/'
    strFEN += " w " if (position.getplayer() == 0) else " b "
    cr = position.getCastleRights()
    r = 0
    if cr[0][0]: strFEN += 'K'; r = 1
    if cr[0][1]: strFEN += 'Q'; r = 1
    if cr[1][0]: strFEN += 'k'; r = 1
    if cr[1][1]: strFEN += 'q'; r = 1
    if r == 0:   strFEN += '-'
    enp = position.getEnP()
    if enp == -1:
        strFEN += " - "
    else:
        x, y = enp
        hor = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        x = hor[x]
        y = str(8 - y)
        strFEN += (' ' + x + y + ' ')
    strFEN += str(position.getHMC()) + ' '
    strFEN += str(position.getFMN())

    return strFEN


# -----------------------------------------------------------------------------------------------------------------------
def createShades(listofTuples):
    global listofShades
    listofShades = []  # Empty the global var list
    if isTransition:
        return  # Nothing should be shaded when a piece is being animated.
    if isDraw:  # The game ended with a draw. Make yellow circle shades for both the kings to show this is the case.
        coord = lookfor(board, 'Kw')[0]
        shade = Shades(circle_image_yellow, coord)
        listofShades.append(shade)
        coord = lookfor(board, 'Kb')[0]
        shade = Shades(circle_image_yellow, coord)
        listofShades.append(shade)
        return  # There is no need to go further.
    if chessEnded:  # The game has ended, with a checkmate because it cannot be a draw if the code reached here.
        coord = lookfor(board, 'K' + winner)[0]  # Give the winning king a green circle shade.
        shade = Shades(circle_image_green_big, coord)
        listofShades.append(shade)
    if isCheck(position, 'white'):
        coord = lookfor(board, 'Kw')[0]  # If either king is under attack, give them a red circle.
        shade = Shades(circle_image_red, coord)
        listofShades.append(shade)
    if isCheck(position, 'black'):
        coord = lookfor(board, 'Kb')[0]
        shade = Shades(circle_image_red, coord)
        listofShades.append(shade)
    for pos in listofTuples:
        # Go through all the target squares inputted. If the target square is occupied, it can be captured.
        # For a capturable square, there is a different shade.Create the appropriate shade for each target square.
        if isOccupied(board, pos[0], pos[1]):
            img = circle_image_capture
        else:
            img = circle_image_green
        shade = Shades(img, pos)
        listofShades.append(shade)  # append


# -----------------------------------------------------------------------------------------------------------------------
def drawBoard():
    if player == 1:
        screen.blit(background_flip, (0, 0))  # Blit the background.
    else:
        screen.blit(background, (0, 0))  # Blit the background.
    # Choose the order in which to blit the pieces. If black is about to play for example, white pieces
    # should be blitted first, so that when black is capturing, the piece appears above:
    if player == 1:
        order = [listofWhitePieces, listofBlackPieces]
    else:
        order = [listofBlackPieces, listofWhitePieces]
    if isTransition:
        # If a piece is being animated, the player info is changed despite
        # white still capturing over black, for example. Reverse the order:
        order = list(reversed(order))
    # The shades which appear during the following three conditions need to be
    # blitted first to appear under the pieces:
    if isDraw or chessEnded or isAIThink:
        # Shades
        for shade in listofShades:
            img, chess_coord = shade.getInfo()
            pixel_coord = coord2pixels(chess_coord)
            screen.blit(img, pixel_coord)
    # Make shades to show what the previous move played was:
    if prevMove[0] != -1 and not isTransition:
        x, y, x2, y2 = prevMove
        screen.blit(yellowbox_image, coord2pixels((x, y)))
        screen.blit(yellowbox_image, coord2pixels((x2, y2)))

    # Blit the Pieces:
    # Now that one side has to be below the green circular shades to showt hat they are being targeted,
    # and the other side if dragged to such a square should be blitted on top to show that it is capturing:
    for piece in order[0]:
        chess_coord, pieceInfo, pos = piece.getInfo()
        pixel_coord = coord2pixels(chess_coord)
        pieceImage = pygame.image.load(os.path.join(piecesImagePath, pieceInfo + ".png"))
        pieceImage = pygame.transform.scale(pieceImage, (squareSize, squareSize))
        if pos == (-1, -1):
            screen.blit(pieceImage, pixel_coord)
        else:
            screen.blit(pieceImage, pos)

    if not (isDraw or chessEnded or isAIThink):  # Blit the shades in between:
        for shade in listofShades:
            img, chess_coord = shade.getInfo()
            pixel_coord = coord2pixels(chess_coord)
            screen.blit(img, pixel_coord)

    for piece in order[1]:
        chess_coord, pieceInfo, pos = piece.getInfo()
        pixel_coord = coord2pixels(chess_coord)
        pieceImage = pygame.image.load(os.path.join(piecesImagePath, pieceInfo + ".png"))
        pieceImage = pygame.transform.scale(pieceImage, (squareSize, squareSize))
        if pos == (-1, -1):
            screen.blit(pieceImage, pixel_coord)
        else:
            screen.blit(pieceImage, pos)


# -----------------------------------------------------------------------------------------------------------------------
#                             A I     R E L A T E D     F U N C T I O N S
# -----------------------------------------------------------------------------------------------------------------------
def negamax(position, depth, alpha, beta, colorsign, bestMoveReturn, root=True):
    # negamax(position,depth,alpha,beta,colorsign,bestMoveReturn,root=True) - This function takes as its inputs a
    # position, and a depth to which moves should be  analysed. It will generate moves and analyse resulting positions
    # to decide the best move to be played for the AI. Alpha and beta are lower and upper bounds to a position's
    # possible score values and allows for alpha-beta pruning. Colorsign indicates the player to move. bestMoveReturn
    # is a list that will be assigned the move to be played. Returning is not possible in this case because threading
    # is used. root is a  variable that keeps track of whether the original node is processing now or a  lower node.
    # Alpha beta pruning is not explained in detail here so I recommend learning more about it if the code does not
    # make sense. Note that the function does not always traverse a tree to give back the move to be played by the AI.
    # It also checks the opening table to see if there is a prerecorded move that it can play without searching.
    # Scoring of each position is also stored in a global dictionary to allow for time-saving if the same  position
    # occurs elsewhere in the tree. The code used here is adapted from the pseudocode provided at
    # Wikipidea: https://en.wikipedia.org/wiki/Negamax#Negamax_with_alpha_beta_pruning
    if root:
        # Generate key from current position:
        key = pos2key(position)
        if key in openings:  # First check if the position is already stored in the opening database dictionary:
            print("position found in openings")
            # Return the best move to be played:
            bestMoveReturn[:] = random.choice(openings[key])
            return
    # Access global variable that will store scores of positions already evaluated:
    global searched
    # If the depth is zero, we are at a leaf node (no more depth to be analysed):
    if depth == 0:
        return colorsign * evaluate(position)
    # Generate all the moves that can be played:
    moves = allMoves(position, colorsign)
    # If there are no moves to be played, just evaluate the position and return it:
    if moves == []:
        return colorsign * evaluate(position)
    # Initialize a best move for the root node:
    if root:
        bestMove = moves[0]
    bestValue = -100000  # initialize the best move's value
    for move in moves:  # go through each move
        newpos = position.clone()  # make a clone of the current move and perform the move on it
        makeMove(newpos, move[0][0], move[0][1], move[1][0], move[1][1])
        # Generate the key for the new resulting position:
        key = pos2key(newpos)
        # If this position was already searched before, retrieve its node value.
        # Otherwise, calculate its node value and store it in the dictionary:
        if key in searched:
            value = searched[key]
        else:
            value = -negamax(newpos, depth - 1, -beta, -alpha, -colorsign, [], False)
            searched[key] = value
        # If this move is better than the best so far:
        if value > bestValue:
            # Store it
            bestValue = value
            # If we're at root node, store the move as the best move:
            if root:
                bestMove = move
        # Update the lower bound for this node:
        alpha = max(alpha, value)
        if alpha >= beta:
            # If our lower bound is higher than the upper bound for this node, there
            # is no need to look at further moves:
            break
    # If this is the root node, return the best move:
    if root:
        searched = {}
        bestMoveReturn[:] = bestMove
        return
    # Otherwise, return the bestValue (i.e. value for this node.)
    return bestValue


# -----------------------------------------------------------------------------------------------------------------------
def evaluate(position):
    # This function takes as input a position to be analysed. It will look at the positioning of pieces on the board
    # to judge whether white has an advantage or black. If it returns zero, it means it considers the position to be
    # equal for both sides. A positive value is an advantage to the white side and a negative value  is an advantage
    # to the black side.
    if isCheckmate(position, 'white'):
        # Major advantage to black
        return -20000
    if isCheckmate(position, 'black'):
        # Major advantage to white
        return 20000
    board = position.getboard()  # get the board
    flatboard = [x for row in board for x in row]  # flatten the board to a 1D array for faster calculations
    c = Counter(flatboard)  # create a counter object to count number of each pieces:
    Qw = c['Qw']
    Qb = c['Qb']
    Rw = c['Rw']
    Rb = c['Rb']
    Bw = c['Bw']
    Bb = c['Bb']
    Nw = c['Nw']
    Nb = c['Nb']
    Pw = c['Pw']
    Pb = c['Pb']
    # Note: The above choices to flatten the board and to use a library to count pieces were attempts at making the AI
    # more efficient. Perhaps using a 1D board throughout the entire program is one way to make the code more efficient.
    # Calculate amount of material on both sides and the number of moves played so far in order to determine game phase.
    whiteMaterial = 9 * Qw + 5 * Rw + 3 * Nw + 3 * Bw + 1 * Pw
    blackMaterial = 9 * Qb + 5 * Rb + 3 * Nb + 3 * Bb + 1 * Pb
    numofmoves = len(position.gethistory())
    gamephase = 'opening'
    if numofmoves > 40 or (whiteMaterial < 14 and blackMaterial < 14):
        gamephase = 'ending'
    # A note again: Determining game phase is again one the attempts to make the AI smarter when analysing boards and
    # has not been implemented to its full potential. Calculate number of doubled, blocked, and isolated pawns for
    # both sides:
    Dw = doubledPawns(board, 'white')
    Db = doubledPawns(board, 'black')
    Sw = blockedPawns(board, 'white')
    Sb = blockedPawns(board, 'black')
    Iw = isolatedPawns(board, 'white')
    Ib = isolatedPawns(board, 'black')
    # Evaluate position based on above data.
    evaluation1 = 900 * (Qw - Qb) + 500 * (Rw - Rb) + 330 * (Bw - Bb) + 320 * (Nw - Nb) + 100 * (Pw - Pb) + -30 * (
                Dw - Db + Sw - Sb + Iw - Ib)
    evaluation2 = pieceSquareTable(flatboard, gamephase)  # evaluate position based on piece square tables
    evaluation = evaluation1 + evaluation2  # Sum the evaluations
    return evaluation  # return it


# -----------------------------------------------------------------------------------------------------------------------
def pieceSquareTable(flatboard, gamephase):
    # Gives a position a score based solely on tables that define points for each position for each piece type.
    score = 0  # initialize score:
    for i in range(64):  # go through each square
        if flatboard[i] == 0:
            continue  # empty square
        piece = flatboard[i][0]  # get data
        color = flatboard[i][1]
        sign = +1
        if color == 'b':  # adjust index if black piece, since piece sqaure tables were designed for white
            i = int((7 - i / 8) * 8 + i % 8)
            sign = -1
        if piece == 'P':  # adjust score
            score += sign * pawn_table[i]
        elif piece == 'N':
            score += sign * knight_table[i]
        elif piece == 'B':
            score += sign * bishop_table[i]
        elif piece == 'R':
            score += sign * rook_table[i]
        elif piece == 'Q':
            score += sign * queen_table[i]
        elif piece == 'K':  # King has different table values based on phase of the game
            if gamephase == 'opening':
                score += sign * king_table[i]
            else:
                score += sign * king_endgame_table[i]
    return score


# -----------------------------------------------------------------------------------------------------------------------
def doubledPawns(board, color):
    # This function counts the number of doubled pawns for a player and returns it.
    # Doubled pawns are those that are on the same file.
    color = color[0]
    listofpawns = lookfor(board, 'P' + color)  # get indices of pawns
    repeats = 0
    temp = []  # count the number of doubled pawns by counting occurences of repeats in their x-coordinates
    for pawnpos in listofpawns:
        if pawnpos[0] in temp:
            repeats = repeats + 1
        else:
            temp.append(pawnpos[0])
    return repeats


# -----------------------------------------------------------------------------------------------------------------------
def blockedPawns(board, color):
    # This function counts the number of blocked pawns for a player and returns it.
    # Blocked pawns are those that have a piece in front of them and so cannot advance forward.
    color = color[0]
    listofpawns = lookfor(board, 'P' + color)
    blocked = 0
    for pawnpos in listofpawns:
        if ((color == 'w' and isOccupiedby(board, pawnpos[0], pawnpos[1] - 1, 'black'))
                or (color == 'b' and isOccupiedby(board, pawnpos[0], pawnpos[1] + 1, 'white'))):
            blocked = blocked + 1
    return blocked


# -----------------------------------------------------------------------------------------------------------------------
def isolatedPawns(board, color):
    # This function counts the number of isolated pawns for a player.
    # These are pawns that do not have supporting pawns on adjacent files and so are difficult to protect.
    color = color[0]
    listofpawns = lookfor(board, 'P' + color)
    xlist = [x for (x, y) in listofpawns]  # get x coordinates of all the pawns
    isolated = 0
    for x in xlist:
        if x != 0 and x != 7:
            if x - 1 not in xlist and x + 1 not in xlist:  # for non-edge cases
                isolated += 1
        elif x == 0 and 1 not in xlist:
            isolated += 1  # left edge
        elif x == 7 and 6 not in xlist:
            isolated += 1  # right edge:
    return isolated


# -----------------------------------------------------------------------------------------------------------------------

#########MAIN FUNCTION####################################################


pawn_table = [0, 0, 0, 0, 0, 0, 0, 0,
              50, 50, 50, 50, 50, 50, 50, 50,
              10, 10, 20, 30, 30, 20, 10, 10,
              5, 5, 10, 25, 25, 10, 5, 5,
              0, 0, 0, 20, 20, 0, 0, 0,
              5, -5, -10, 0, 0, -10, -5, 5,
              5, 10, 10, -20, -20, 10, 10, 5,
              0, 0, 0, 0, 0, 0, 0, 0]

knight_table = [-50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -90, -30, -30, -30, -30, -90, -50]

bishop_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -90, -10, -10, -90, -10, -20]

rook_table = [0, 0, 0, 0, 0, 0, 0, 0,
              5, 10, 10, 10, 10, 10, 10, 5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              0, 0, 0, 5, 5, 0, 0, 0]

queen_table = [-20, -10, -10, -5, -5, -10, -10, -20,
               -10, 0, 0, 0, 0, 0, 0, -10,
               -10, 0, 5, 5, 5, 5, 0, -10,
               -5, 0, 5, 5, 5, 5, 0, -5,
               0, 0, 5, 5, 5, 5, 0, -5,
               -10, 5, 5, 5, 5, 5, 0, -10,
               -10, 0, 5, 0, 0, 0, 0, -10,
               -20, -10, -10, 70, -5, -10, -10, -20]

king_table = [-30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -20, -30, -30, -40, -40, -30, -30, -20,
              -10, -20, -20, -20, -20, -20, -20, -10,
              20, 20, 0, 0, 0, 0, 20, 20,
              20, 30, 10, 0, 0, 10, 30, 20]

king_endgame_table = [-50, -40, -30, -20, -20, -30, -40, -50,
                      -30, -20, -10, 0, 0, -10, -20, -30,
                      -30, -10, 20, 30, 30, 20, -10, -30,
                      -30, -10, 30, 40, 40, 30, -10, -30,
                      -30, -10, 30, 40, 40, 30, -10, -30,
                      -30, -10, 20, 30, 30, 20, -10, -30,
                      -30, -30, 0, 0, 0, 0, -30, -30,
                      -50, -30, -30, -30, -30, -30, -30, -50]


# -----------------------------------------------------------------------------------------------------------------------
def showMenue():
    global isAI, isFlip, AIPlayer, gameEnded, isAIThink, bestMoveReturn, bm
    screen.blit(background, (0, 0))
    if isAI == -1:
        screen.blit(withfriend_pic, (offset, offset + squareSize * 2))
        screen.blit(withAI_pic, (offset + squareSize * 4, offset + squareSize * 2))
    elif isAI == True:
        screen.blit(playwhite_pic, (offset, offset + squareSize * 2))
        screen.blit(playblack_pic, (offset + squareSize * 4, offset + squareSize * 2))
    elif isAI == False:
        screen.blit(flipDisabled_pic, (offset, offset + squareSize * 2))
        screen.blit(flipEnabled_pic, (offset + squareSize * 4, offset + squareSize * 2))
    if isFlip != -1:
        drawBoard()  # Draw all the pieces onto the board,
        # isMenu = False # Don't let the menu ever appear again.
        if isAI and AIPlayer == 0:  # In case the player chose to play against the AI and decided to
            # colorsign=1          # play as black, call upon the AI to make a move:
            # bestMoveReturn = []
            # move_thread = threading.Thread(target = negamax,
            #             args = (position,3,-1000000,1000000,colorsign,bestMoveReturn))
            # move_thread.start()
            stockfish.setfenposition(getFEN(position.getboard()))
            bm = stockfish.bestmove()
            print(bm['move'])
            isAIThink = True
        return False
    for event in pygame.event.get():  # Handle the events while in menu
        if event.type == QUIT:  # Window was closed.
            gameEnded = True
            return False
        if event.type == MOUSEBUTTONUP:  # The mouse was clicked somewhere.
            pos = pygame.mouse.get_pos()  # Get the coordinates of click
            if (pos[0] < offset + squareSize * 4 and  # Determine if left box was clicked or right box.
                    pos[1] > offset + squareSize * 2 and
                    pos[1] < offset + squareSize * 6):  # LEFT SIDE CLICKED
                if isAI == -1:
                    isAI = False
                elif isAI == True:
                    AIPlayer = 1
                    isFlip = False
                elif isAI == False:
                    isFlip = False
            elif (pos[0] > offset + squareSize * 4 and
                  pos[1] > offset + squareSize * 2 and
                  pos[1] < offset + squareSize * 6):  # RIGHT SIDE CLICKED
                if isAI == -1:
                    isAI = True
                elif isAI == True:
                    AIPlayer = 0
                    isFlip = False
                elif isAI == False:
                    isFlip = True
    return True


# -----------------------------------------------------------------------------------------------------------------------

# objects
position = GamePosition(board, player, castling_rights, En_Passant_Target, half_move_clock, FMN)
stockfish = Engine(depth=10)

listofWhitePieces, listofBlackPieces = createPieces(board)  # A list of pieces that should be drawn on the board.

try:  # If openingTable.txt exists, read from it and load the opening moves to the local dictionary.
    file_handle = open(os.path.dirname(__file__) + '/openingTable.txt', 'rb')
    openings = pickle.loads(file_handle.read())
except:
    print("OpeningTable not found or not readable")

while not gameEnded:  # The program remains in this loop until the user quits the application.
    if isMenu:
        isMenu = showMenue()
        pygame.display.update()
        clock.tick(60)  # Run at specific fps
        continue
    # Menu part was done if this part reached. If the AI is currently thinking the move to play next,
    # show some fancy looking squares to indicate that. Do it every 3 frames so it's not too fast:
    numm += 1
    if isAIThink and numm % 3 == 0:
        ax += 1
        if ax == 8:
            ay += 1
            ax = 0
        if ay == 8:
            ax, ay = 0, 0
        if ax % 4 == 0:
            createShades([])
        if AIPlayer == 0:  # If the AI is white, start from the opposite side (since the board is flipped)
            listofShades.append(Shades(greenbox_image, (7 - ax, 7 - ay)))
        else:
            listofShades.append(Shades(greenbox_image, (ax, ay)))

    for event in pygame.event.get():
        if event.type == QUIT:  # Deal with all the user inputs.
            gameEnded = True  # Window was closed.
            break
        # Under the following conditions, user input should be completely ignored:
        if chessEnded or isTransition or isAIThink:
            continue
        if not isDown and event.type == MOUSEBUTTONDOWN:  # isDown means a piece is being dragged.
            pos = pygame.mouse.get_pos()  # Mouse was pressed down. Get the oordinates of the mouse
            chess_coord = pixels2coord(pos)  # convert to chess coordinates
            x = chess_coord[0]
            y = chess_coord[1]
            # If the piece clicked on is not occupied by your own piece, ignore this mouse click:
            if not isOccupiedby(board, x, y, 'wb'[player]):
                continue
            # Now we're sure the user is holding their mouse on a piecec that is theirs.
            # Get reference to the piece that should be dragged around or selected:
            dragPiece = getPiece(chess_coord)
            listofTuples = findPossibleSquares(position, x,
                                               y)  # Find the possible squares that this piece could attack.
            createShades(listofTuples)  # Highlight all such squares
            # A green box should appear on the square which was selected, unless it's a king under check,
            # in which case it shouldn't because the king has a red color on it in that case.
            if ((dragPiece.pieceInfo[0] == 'K') and (isCheck(position, 'white') or isCheck(position, 'black'))):
                None
            else:
                listofShades.append(Shades(greenbox_image, (x, y)))
            isDown = True  # A piece is being dragged.
        if (isDown or isClicked) and event.type == MOUSEBUTTONUP:  # Mouse was released.
            isDown = False
            dragPiece.setpos((-1, -1))  # Snap the piece back to its coordinate position
            pos = pygame.mouse.get_pos()  # Get coordinates and convert them
            chess_coord = pixels2coord(pos)
            x2 = chess_coord[0]
            y2 = chess_coord[1]
            # Initialize:
            isTransition = False
            if (x, y) == (x2, y2):  # NO dragging occured
                # (ie the mouse was held and released on the same square)
                if not isClicked:  # nothing had been clicked previously
                    # This is the first click
                    isClicked = True
                    prevPos = (x, y)  # Store it so next time we know the origin
                else:  # Something had been clicked previously
                    # Find out location of previous click:
                    x, y = prevPos
                    if (x, y) == (x2, y2):  # User clicked on the same square again.
                        # So
                        isClicked = False
                        # Destroy all shades:
                        createShades([])
                    else:
                        # User clicked elsewhere on this second click:
                        if isOccupiedby(board, x2, y2, 'wb'[player]):
                            # User clicked on a square that is occupied by their
                            # own piece.
                            # This is like making a first click on your own piece:
                            isClicked = True
                            prevPos = (x2, y2)  # Store it
                        else:
                            # The user may or may not have clicked on a valid target square.
                            isClicked = False
                            # Destory all shades
                            createShades([])
                            isTransition = True  # Possibly if the move was valid.
            if not (x2, y2) in listofTuples:
                # Move was invalid
                isTransition = False
                continue
            # Reaching here means a valid move was selected.
            # If the recording option was selected, store the move to the opening dictionary:
            if isRecord:
                key = pos2key(position)
                # Make sure it isn't already in there:
                if [(x, y), (x2, y2)] not in openings[key]:
                    openings[key].append([(x, y), (x2, y2)])

            if isOccupied(board, x2, y2):  # play a sound
                pygame.mixer.Sound.play(snd_cap)
            else:
                pygame.mixer.Sound.play(snd_mov)
            makeMove(position, x, y, x2, y2)  # Make the move.
            position.increaseFMN()
            # Update this move to be the 'previous' move (latest move in fact), so that
            # yellow shades can be shown on it.
            FEN = getFEN(position.getboard())
            stockfish.setfenposition(FEN)
            bm = stockfish.bestmove()
            print(FEN)
            print(bm['move'])
            # print(bm['ponder'])
            prevMove = [x, y, x2, y2]
            # Update which player is next to play:
            player = position.getplayer()
            # Add the new position to the history for it:
            position.addtoHistory(position)
            # Check for possibilty of draw:
            HMC = position.getHMC()
            if HMC >= 100 or isStalemate(position) or position.checkRepition():
                # There is a draw:
                isDraw = True
                chessEnded = True
            # Check for possibilty of checkmate:
            if isCheckmate(position, 'white'):
                winner = 'b'
                chessEnded = True
            if isCheckmate(position, 'black'):
                winner = 'w'
                chessEnded = True
            # If the AI option was selecteed and the game still hasn't finished,
            # let the AI start thinking about its next move:
            if isAI and not chessEnded:
                awaitAI = True
            # Move the piece to its new destination:
            dragPiece.setcoord((x2, y2))
            # There may have been a capture, so the piece list should be regenerated.
            # However, if animation is ocurring, the the captured piece should still remain visible.
            if not isTransition:
                listofWhitePieces, listofBlackPieces = createPieces(board)
            else:
                movingPiece = dragPiece
                origin = coord2pixels((x, y))
                destiny = coord2pixels((x2, y2))
                movingPiece.setpos(origin)
                step = (destiny[0] - origin[0], destiny[1] - origin[1])
            createShades([])  # Either way shades should be deleted now.

    if awaitAI and not isTransition:
        awaitAI = False
        # if player==0:
        #     colorsign = 1
        # else:
        #     colorsign = -1
        # bestMoveReturn = []
        # move_thread = threading.Thread(target = negamax,
        #             args = (position,searchDepth,-1000000,1000000,colorsign,bestMoveReturn))
        # move_thread.start()
        isAIThink = True
    if isTransition:  # If an animation is supposed to happen, make it happen.
        p, q = movingPiece.getpos()
        dx2, dy2 = destiny
        n = 30.0
        if abs(p - dx2) <= abs(step[0] / n) and abs(q - dy2) <= abs(step[1] / n):
            # The moving piece has reached its destination:
            # Snap it back to its grid position:
            movingPiece.setpos((-1, -1))
            # Generate new piece list in case one got captured:
            listofWhitePieces, listofBlackPieces = createPieces(board)
            # No more transitioning:
            isTransition = False
            createShades([])
        else:
            # Move it closer to its destination.
            movingPiece.setpos((p + step[0] / n, q + step[1] / n))
    # If a piece is being dragged let the dragging piece follow the mouse:
    if isDown:
        m, k = pygame.mouse.get_pos()
        dragPiece.setpos((int(m - squareSize / 2), int(k - squareSize / 2)))
    # If the AI is thinking, make sure to check if it isn't done thinking yet.
    # Also, if a piece is currently being animated don't ask the AI if it's
    # done thining, in case it replied in the affirmative and starts moving
    # at the same time as your piece is moving:
    if isAIThink and not isTransition:
        # if True():
        # The AI has made a decision.
        # It's no longer thinking
        isAIThink = False
        # Destroy any shades:
        createShades([])
        # Get the move proposed:
        # [x,y],[x2,y2] = bestMoveReturn
        x, y, x2, y2 = convert_sf(bm['move'])
        # Do everything just as if the user made a move by click-click movement:
        # play a sound
        if isOccupied(board, x2, y2):
            pygame.mixer.Sound.play(snd_cap)
        else:
            pygame.mixer.Sound.play(snd_mov)
        print(getFEN(position.getboard()))
        makeMove(position, x, y, x2, y2)
        position.increaseFMN()
        prevMove = [x, y, x2, y2]
        player = position.getplayer()
        HMC = position.getHMC()
        position.addtoHistory(position)
        if HMC >= 100 or isStalemate(position) or position.checkRepition():
            isDraw = True
            chessEnded = True
        if isCheckmate(position, 'white'):
            winner = 'b'
            chessEnded = True
        if isCheckmate(position, 'black'):
            winner = 'w'
            chessEnded = True
        # Animate the movement:
        isTransition = True
        movingPiece = getPiece((x, y))
        origin = coord2pixels((x, y))
        destiny = coord2pixels((x2, y2))
        movingPiece.setpos(origin)
        step = (destiny[0] - origin[0], destiny[1] - origin[1])

    drawBoard()  # Update positions of all images.
    pygame.display.update()  # Update the display.
    clock.tick(60)  # Run at specific fps.

pygame.quit()  # Out of loop. Quit pygame.
if isRecord:  # In case recording mode was on, save the openings dictionary to a file.
    file_handle = open('openingTable.txt', 'wb')
    pickle.dump(openings, file_handle)
    file_handle.close()
