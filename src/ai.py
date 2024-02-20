import random

DEPTH = 4
CHECKMATE = 50000

pieceRedScore = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [5, 5, 5, 5, 5, 5, 5, 5],
                   [10, 10, 10, 10, 10, 10, 10, 10],
                   [13, 13, 13, 13, 130, 13, 13, 13],
                   [15, 15, 15, 1500, 1500, 15, 15, 15],
                   [1250, 1250, 2500, 2500, 25, 25, 25, 25],
                   [3500, 3500, 1500, 500, 50, 50, 50, 50],
                   [10000, 3000, 1500, 50, 50, 50, 50, 50]
                   ]

pieceBlueScore = [[100, 50, 35, 25, 50, 100, 200, 300],
                   [50, 50, 50, 50, 50, 50, 50, 200],
                   [25, 25, 25, 25, 25, 25, 25, 100],
                   [15, 15, 15, 15, 15, 15, 15, 15],
                   [13, 13, 13, 13, 13, 13, 13, 13],
                   [10, 10, 10, 10, 10, 10, 10, 10],
                   [5, 5, 5, 5, 5, 5, 5, 5],
                   [0, 0, 0, 0, 0, 0, 0, 0]
                   ]


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.BlueToMove else -1)
    return nextMove



def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turn):
    global nextMove
    if depth == 0:
        return turn * (pieceAndColumnScore(gs) +
                       manhattanD(gs) * 5000 + numbEnemyPieces(gs)*100)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turn)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def manhattanD(gs):
    minD = 1000.0
    if gs.BlueToMove:
        for i in range(8):
            for j in range(8):
                if "w" in gs.board[i][j]:
                    distance = (abs(0 - i) + abs(7 - j))
                    minD = min(distance, minD)


    else:
        for i in range(8):
            for j in range(8):
                if i not in range(0,4):
                    if "b" in gs.board[i][j]:
                        distance = (abs(7 - i) + abs(0 - j))
                        minD = min(distance, minD)
    score = 1 / (minD + 1)
    return score


def potentialDangerPiece(gs):
    score = 0
    if gs.BlueToMove:
        for i in range(8):
            if gs.board[2][i] == 'ww':
                if i != 0 and i != 7:
                    if gs.board[0][i + 1] != 'bb' or gs.board[0][i - 1] != 'bb' or gs.board[0][i] != 'bb':
                        score -= 1000
                elif i == 7:
                    if gs.board[0][i - 1] != 'bb' or gs.board[0][i] != 'bb':
                        score -= 1000
                elif i == 0:
                    if gs.board[0][i + 1] != 'bb' or gs.board[0][i] != 'bb':
                        score -= 1000


    else:
        for i in range(8):
            if gs.board[5][i] == 'bb':
                if i != 0 and i != 7:
                    if gs.board[7][i + 1] != 'ww' or gs.board[7][i - 1] != 'ww' or gs.board[7][i] != 'ww':
                        score += 1000
                elif i == 7:
                    if "w" not in gs.board[7][i - 1] or "w" not in gs.board[7][i] != 'ww':
                        score += 1000
                elif i == 0:
                    if 'w' not in gs.board[7][i + 1] or 'w' not in gs.board[7][i]:
                        score += 1000


    return score


def numbEnemyPieces(gs):
    if gs.BlueToMove:
        score=(5-gs.existRed)
    else:
        score = (5 - gs.existBlue)
    return score

def pieceAndColumnScore(gs):
    if gs.checkMate:
        if gs.BlueToMove:

            return CHECKMATE
        else:

            return -CHECKMATE
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            sq = gs.board[row][col]
            if 'w' in sq[0]:
                score = score + 1 + pieceBlueScore[row][col]
            elif 'b' in sq[0]:
                score = score - 1 - pieceRedScore[row][col]

    return score