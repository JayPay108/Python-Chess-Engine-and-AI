from Piece import *
from Config import *
from PieceSquareTables import squareTables

class Board:
    def __init__(self):
        # Piece declaration:
        # PieceType(isWhite, (rowNum, colNum))

        self.board = [[Rook(False, (0, 0)), Knight(False, (0, 1)), Bishop(False, (0, 2)), Queen(False, (0, 3)), King(False, (0, 4)), Bishop(False, (0, 5)), Knight(False, (0, 6)), Rook(False, (0, 7))],
                      [Pawn(False, (1, 0)), Pawn(False, (1, 1)), Pawn(False, (1, 2)), Pawn(False, (1, 3)), Pawn(False, (1, 4)), Pawn(False, (1, 5)), Pawn(False, (1, 6)), Pawn(False, (1, 7))],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [Pawn(True, (6, 0)), Pawn(True, (6, 1)), Pawn(True, (6, 2)), Pawn(True, (6, 3)), Pawn(True, (6, 4)), Pawn(True, (6, 5)), Pawn(True, (6, 6)), Pawn(True, (6, 7))],
                      [Rook(True, (7, 0)), Knight(True, (7, 1)), Bishop(True, (7, 2)), Queen(True, (7, 3)), King(True, (7, 4)), Bishop(True, (7, 5)), Knight(True, (7, 6)), Rook(True, (7, 7))]]
    
    def __call__(self):
        return self.board

    def drawBoard(self, selected, moves, screen):  #TODO: Highlight the selected piece?
        colors = [LIGHT_COLOR, DARK_COLOR]

        for row in range(8):
            for column in range(8):
                pygame.draw.rect(screen, colors[row % 2 == column % 2], (column * 60, row * 60, 60, 60))

                if self.board[row][column] != None:
                    self.board[row][column].drawPiece(screen)

                if (selected, (row, column)) in moves:
                    if self.board[row][column] == None:
                        pygame.draw.circle(screen, (96, 96, 96), ((column * 60) + 30, (row * 60) + 30), 8)

                    else:
                        pygame.draw.circle(screen, (96, 96, 96), ((column * 60) + 30, (row * 60) + 30), 28, 2)

        pygame.display.update()

    def makeMove(self, move):
        # Move is structured as a tuple of two tuples:
        # ((StartPosRow, StarPosCol), (EndPosRow, EndPosCol))
        startPos = move[0]
        endPos = move[1]

        self.board[endPos[0]][endPos[1]] = self.board[startPos[0]][startPos[1]]
        self.board[startPos[0]][startPos[1]] = None

        self.board[endPos[0]][endPos[1]].row = endPos[0]
        self.board[endPos[0]][endPos[1]].col = endPos[1]

        if type(self.board[endPos[0]][endPos[1]]) == Pawn:
            if endPos[0] == 0 or endPos[0] == 7:
                self.board[endPos[0]][endPos[1]] = Queen(self.board[endPos[0]][endPos[1]].white, (endPos[0], endPos[1]))

        self.board[endPos[0]][endPos[1]].hasMoved = True


    def tryMove(self, move): # Similiar to makeMove but moves only temporarily
        startPos = move[0]
        endPos = move[1]

        attackedPiece = self.board[endPos[0]][endPos[1]]

        self.board[endPos[0]][endPos[1]] = self.board[startPos[0]][startPos[1]]
        self.board[startPos[0]][startPos[1]] = None

        self.board[endPos[0]][endPos[1]].row = endPos[0]
        self.board[endPos[0]][endPos[1]].col = endPos[1]

        if type(self.board[endPos[0]][endPos[1]]) == Pawn:
            if endPos[0] == 0 or endPos[0] == 7:
                self.board[endPos[0]][endPos[1]] = Queen(self.board[endPos[0]][endPos[1]].white, (endPos[0], endPos[1]))
                self.board[endPos[0]][endPos[1]].wasPawn = True

        return attackedPiece

    def undoMove(self, move, attackedPiece):
        self.tryMove(move[::-1])
        self.board[move[1][0]][move[1][1]] = attackedPiece

        if self.board[move[0][0]][move[0][1]].wasPawn:
            self.board[move[0][0]][move[0][1]] = Pawn(self.board[move[0][0]][move[0][1]].white, (move[0][0], move[0][1]))


    def evaluate(self, white = False): # By default, this function evaluates for black
        boardValue = 0

        # Summing up all the different piece values
        pieceValues = 0
        pieceSquareValues = 0
        for row in self.board:
            for piece in row:
                if piece == None:
                    continue

                if piece.white == white:
                    pieceValues += piece.value
                else:
                    pieceValues -= piece.value

                if piece.white:
                    pieceSquareValues += squareTables[type(piece)][piece.row][piece.col]
                else:
                    pieceSquareValues -= squareTables[type(piece)][::-1][piece.row][piece.col]

        pieceValues = pieceValues * DEFENSE
        boardValue += pieceValues

        if not white:
            pieceSquareValues = -pieceSquareValues

        boardValue += pieceSquareValues * POSITIONING            

        # Summing up all valid moves
        allMoves1 = self.getAllMoves(white)
        allMoves2 = self.getAllMoves(not white)

        boardControl = (len(allMoves1) - len(allMoves2)) * AGRESSIVENESS
        boardValue += boardControl

        # Pawn stuff
        cBlocked = 0
        uBlocked = 0

        cPawnsPerRow = [0, 0, 0, 0, 0, 0, 0, 0]
        uPawnsPerRow = [0, 0, 0, 0, 0, 0, 0, 0]
        for col in range(8):
            for row in range(8):
                if type(self.board[row][col]) == Pawn:
                    if self.board[row][col].white == white:
                        cPawnsPerRow[row] += 1
                        if self.board[row + self.board[row][col].direction][col] != None:
                            cBlocked += 1
                    else:
                        uPawnsPerRow[row] += 1
                        if self.board[row + self.board[row][col].direction][col] != None:
                            uBlocked += 1

        cIsolated = 0
        uIsolated = 0

        cDoubled = 0
        uDoubled = 0

        for row in range(8):
            if cPawnsPerRow[row] > 1:
                cDoubled += 1
            if uPawnsPerRow[row] > 1:
                uDoubled += 1

            if (row == 0 or cPawnsPerRow[row - 1] == 0) and (row == 7 or cPawnsPerRow[row + 1] == 0):
                cIsolated += 1

            if (row == 0 or uPawnsPerRow[row - 1] == 0) and (row == 7 or uPawnsPerRow[row + 1] == 0):
                uIsolated += 1        

        boardValue -= ((cIsolated - uIsolated) + (cDoubled - uDoubled) + (cBlocked - uBlocked)) * PAWNLOVE

        return boardValue

    def getAllMoves(self, white):
        # Gets all moves possible from current board
        moves = []

        for row in self.board:
            for piece in row:
                if piece == None or piece.white != white:
                    continue
                
                moves += piece.getMoves(self.board)

        return moves


    def isGameOver(self):
        kings = 0
        for row in self.board:
            for piece in row:
                if type(piece) == King:
                    kings += 1

        return kings != 2

                