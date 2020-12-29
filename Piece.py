import pygame

class Piece:
    
    def __init__(self, white, index):
        self.white = white

        self.row = index[0]
        self.col = index[1]

        self.hasMoved = False # No longer used but will be necessary for castling
        self.wasPawn = False  # Used undoing pawn promotions

        if white:
            self.direction = -1
        else:
            self.direction = 1

        self.setValue()
        self.loadImage()

    def drawPiece(self, screen):
        screen.blit(self.image, (self.col * 60, self.row * 60))

    # Dummy functions so I dont have to look at squiggly lines in VS
    def setValue(self): self.value = None
    def loadImage(self): self.image = None



class Pawn(Piece):

    def setValue(self):
        self.value = 1

    def loadImage(self):
        if self.white:
            self.image = pygame.image.load('Images/White/pawn.png')
        else:
            self.image = pygame.image.load('Images/Black/pawn.png')

    def getMoves(self, board):
        moves = []

        if self.white:
            direction = -1
        else:
            direction = 1

        for i in range(1, 3):
            if self.row + (direction * i) not in range(8):
                break
            
            if board[self.row + (direction * i)][self.col] != None:
                break

            moves.append(((self.row, self.col), (self.row + (direction * i), self.col)))    

            if (self.white and self.row != 6) or (not self.white and self.row != 1):
                break    

        
        for i in range(-1, 2, 2):
            if self.col + i not in range(8) or self.row + direction not in range(8):
                continue

            attackPiece = board[self.row + direction][self.col + i]

            if attackPiece != None and attackPiece.white != self.white:
                moves.append(((self.row, self.col), (self.row + direction, self.col + i)))
        
        return moves





class Rook(Piece):

    def setValue(self):
        self.value = 5

    def loadImage(self):
        if self.white:
            self.image = pygame.image.load('Images/White/rook.png')
        else:
            self.image = pygame.image.load('Images/Black/rook.png')

    def getMoves(self, board):
        moves = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for direction in directions:
            for i in range(1, 8):
                location = (self.row + (direction[0] * i), self.col + (direction[1] * i))

                if location[0] not in range(8) or location[1] not in range(8):
                    break

                if board[location[0]][location[1]] != None:
                    if board[location[0]][location[1]].white != self.white:
                        moves.append(((self.row, self.col), location))

                    break

                moves.append(((self.row, self.col), location))

        return moves





class Bishop(Piece):

    def setValue(self):
        self.value = 3

    def loadImage(self):
        if self.white:
            self.image = pygame.image.load('Images/White/bishop.png')
        else:
            self.image = pygame.image.load('Images/Black/bishop.png')

    def getMoves(self, board):
        moves = []

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            for i in range(1, 8):
                location = (self.row + (direction[0] * i), self.col + (direction[1] * i))

                if location[0] not in range(8) or location[1] not in range(8):
                    break

                if board[location[0]][location[1]] != None:
                    if board[location[0]][location[1]].white != self.white:
                        moves.append(((self.row, self.col), location))

                    break

                moves.append(((self.row, self.col), location))

        return moves





class Knight(Piece):

    def setValue(self):
        self.value = 3

    def loadImage(self):
        if self.white:
            self.image = pygame.image.load('Images/White/knight.png')
        else:
            self.image = pygame.image.load('Images/Black/knight.png')

    def getMoves(self, board):
        moves = []

        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for direction in directions:
            location = (self.row + (direction[0]), self.col + (direction[1]))

            if location[0] not in range(8) or location[1] not in range(8):
                continue

            if board[location[0]][location[1]] != None:
                if board[location[0]][location[1]].white != self.white:
                    moves.append(((self.row, self.col), location))

                continue

            moves.append(((self.row, self.col), location))

        return moves





class Queen(Piece):

    def setValue(self):
        self.value = 9

    def loadImage(self):
        if self.white:
            self.image = pygame.image.load('Images/White/queen.png')
        else:
            self.image = pygame.image.load('Images/Black/queen.png')
            
    def getMoves(self, board):
        moves = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            for i in range(1, 8):
                location = (self.row + (direction[0] * i), self.col + (direction[1] * i))

                if location[0] not in range(8) or location[1] not in range(8):
                    break

                if board[location[0]][location[1]] != None:
                    if board[location[0]][location[1]].white != self.white:
                        moves.append(((self.row, self.col), location))

                    break

                moves.append(((self.row, self.col), location))

        return moves





class King(Piece):

    def setValue(self):
        self.value = 999 # KING STRONG

    def loadImage(self):
        if self.white:
            self.image = pygame.image.load('Images/White/king.png')
        else:
            self.image = pygame.image.load('Images/Black/king.png')

    def getMoves(self, board):
        moves = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            location = (self.row + direction[0], self.col + direction[1])

            if location[0] not in range(8) or location[1] not in range(8):
                continue

            if board[location[0]][location[1]] != None:
                if board[location[0]][location[1]].white != self.white:
                    moves.append(((self.row, self.col), location))

                continue

            moves.append(((self.row, self.col), location))

        return moves