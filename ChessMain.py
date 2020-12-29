from Board import Board
from Config import *
from Craig import *

import random 
import time

import pygame
pygame.init()

screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption('Your turn')

def tileClicked(pos):
    for row in range(8):
        for column in range(8):
            if pygame.Rect(column * 60, row * 60, 60, 60).collidepoint(pos):
                return(row, column)

    return None


whitesTurn = True
selected = None
moves = []

board = Board()

playing = True
while playing:

    if not whitesTurn:  # Craig's turn
        startTime = time.time()

        pygame.display.set_caption('Craig\'s move')
        move = getNextMove(board, DEPTH)
        board.makeMove(move)
        
        endTime = time.time()
        print('\n\nCraig took %.1f seconds to compute his move'%(endTime - startTime))
        print('(r%g, c%g) to (r%g, c%g)'%(move[0][0], move[0][1], move[1][0], move[1][1]))
        print('Board = %.2f'%board.evaluate(True))

        selected = None
        moves = []
        whitesTurn = True
        pygame.display.set_caption('Your move')
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not board.isGameOver():
            pos = pygame.mouse.get_pos()
            clickedPos  = tileClicked(pos)

            if board()[clickedPos[0]][clickedPos[1]] != None and board()[clickedPos[0]][clickedPos[1]].white == whitesTurn and clickedPos != selected:
                selected = (clickedPos[0], clickedPos[1])
                moves = board()[selected[0]][selected[1]].getMoves(board())

            elif selected != None and (selected, clickedPos) in moves:
                board.makeMove((selected, clickedPos))                    
                
                whitesTurn = not whitesTurn
                selected = None
                moves = []

            else:
                selected = None
                moves = []
    
    board.drawBoard(selected, moves, screen)
