import random

def miniMax(board, depth = 4, whitesTurn = False, alpha = -9999, beta = 9999):
    if depth == 0 or board.isGameOver():
        return (board.evaluate(), None)
    
    if whitesTurn:
        minValue = 9999

        for move in board.getAllMoves(True):
            attackedPiece = board.tryMove(move)

            boardValue = miniMax(board, depth - 1, False)[0]

            board.undoMove(move, attackedPiece)

            if boardValue < minValue:
                moves = [move]
                minValue = boardValue

            elif boardValue == minValue:
                moves.append(move)

            if boardValue < beta:
                beta = boardValue
            
            if beta <= alpha:
                break

        return (minValue, moves)

    else:
        maxValue = -9999

        for move in board.getAllMoves(False):
            attackedPiece = board.tryMove(move)

            boardValue = miniMax(board, depth - 1, True)[0]

            board.undoMove(move, attackedPiece)

            if boardValue > maxValue:
                moves = [move]
                maxValue = boardValue

            elif boardValue == maxValue:
                moves.append(move)

            if boardValue > alpha:
                alpha = boardValue
            
            if beta <= alpha:
                break

        return (maxValue, moves)


def getNextMove(board, depth = 3, whitesTurn = False):
    moves = miniMax(board, depth, whitesTurn)[1]

    return random.choice(moves)

    

