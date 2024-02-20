"""
for storing all information and determine the valid move
"""


class GameState():
    def __init__(self):
        # 8x8
        self.board = [
            ["--", "--", "--", "--", "--", "b2", "bb", "bk"],
            ["--", "--", "--", "--", "--", "--", "bb", "bb"],
            ["--", "--", "rock", "--", "--", "--", "--", "b2"],
            ["--", "--", "--", "--", "--", "rock", "--", "--"],
            ["water", "water", "water", "--", "--", "water", "water", "water"],
            ["w2", "--", "--", "--", "--", "--", "--", "rock"],
            ["ww", "ww", "--", "rock", "--", "--", "--", "--"],
            ["wk", "ww", "w2", "--", "--", "--", "--", "--"]

        ]
        self.BlueToMove = True
        self.moveLog = []
        self.check = False
        self.existBlue = 5
        self.existRed = 5
        self.checkMate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"

        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.BlueToMove = not self.BlueToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.BlueToMove = not self.BlueToMove

    def getValidMoves(self):

        moves = self.getPossibleMove()

        self.checkMate = False
        if self.inCheck():
            self.checkMate = True

        return moves

    def getValidMoves2(self):
        return self.getPossibleMove()

    def inCheck(self):
        if self.BlueToMove:
            return self.squareUnderAttack(7)
        else:
            return self.squareUnderAttack(0)

    def squareUnderAttack(self, r):

        self.BlueToMove = not self.BlueToMove
        oppMoves = self.getPossibleMove()
        self.BlueToMove = not self.BlueToMove
        for move in oppMoves:

            if move.endRow == r:
                return True

        return False

    def getPossibleMove(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.BlueToMove) or (turn == "b" and not self.BlueToMove):
                    self.pieceMove(r, c, moves)
        return moves

    def pieceMove(self, r, c, moves):

        if self.BlueToMove:

            if self.board[r][c] == "ww":
                self.add_moves(r, c, moves, "w", [-1, 0, 1])

            elif self.board[r][c] == "w2":
                self.add_moves(r, c, moves, "w", [-2, -1, 0, 1, 2])

        elif not self.BlueToMove:

            if self.board[r][c] == "bb":
                self.add_moves(r, c, moves, "b", [-1, 0, 1])

            elif self.board[r][c] == "b2":
                self.add_moves(r, c, moves, "b", [-2, -1, 0, 1, 2])

    def add_moves(self, r, c, moves, piece_prefix, move_range):
        for dr in move_range:
            for dc in move_range:
                if dr == 0 and dc == 0:
                    continue
                if 0 <= r + dr <= 7 and 0 <= c + dc <= 7:
                    dest_piece = self.board[r + dr][c + dc]
                    if piece_prefix not in dest_piece:
                        if dest_piece != "rock" and dest_piece != "water":
                            if abs(dr) == 2 or abs(dc) == 2:
                                if (r + dr) // 4 != r // 4:
                                    continue
                            moves.append(Move((r, c), (r + dr, c + dc), self.board))

    def checkEndGame(self, move):
        if "w" in move.pieceMoved and (move.endRow == 0 and move.endCol == 7):
            return True
        elif "b" in move.pieceMoved and (move.endRow == 7 and move.endCol == 0):
            return True
        elif self.existRed == 0 or self.existBlue == 0:
            return True
        else:
            return False


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToCols = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startsq, endsq, board):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToCols[r]
