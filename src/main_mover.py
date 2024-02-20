import pygame as p
from map_drawer import *
from ai import *
import pygame.mixer

Width = Height = 800
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = Height
dim = 8
sq_size = Height // dim
max_fps = 15
IMAGES = {}


def loadImages():
    IMAGES['bb'] = p.transform.scale(p.image.load('images/bb.png'),(sq_size*0.5,sq_size*0.85))
    IMAGES['ww'] = p.transform.scale(p.image.load('images/ww.png'),(sq_size*0.5,sq_size*0.85))
    IMAGES['w2'] = p.transform.scale(p.image.load('images/w2.png'), (sq_size*0.9, sq_size))
    IMAGES['b2'] = p.transform.scale(p.image.load('images/b2.png'), (sq_size*0.9, sq_size))


def main():
    p.init()
    screen = p.display.set_mode((Width, Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()  # initial gamestate
    validMoves = gs.getValidMoves()

    moveLogFont = p.font.SysFont("Arial", 12, False, False)
    gameOver = False
    loadImages()
    moveMade = False
    playerClicks = []
    sqSelected = ()
    running = True
    playerOne = True  # human playing blue
    playerTwo = False  # ai playing red

    while running:
        humanTurn = (gs.BlueToMove and playerOne)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // sq_size
                    row = location[1] // sq_size

                    if sqSelected == (row, col) or col >= 8:
                        sqSelected = ()
                        playerClicks = []

                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)


                    if len(playerClicks) == 2:

                        pygame.mixer.init()
                        move_sound = pygame.mixer.Sound("sound/chess-pieces-hitting-wooden-board-99336.mp3")
                        move_sound.play()

                        move = Move(playerClicks[0], playerClicks[1], gs.board)

                        for i in range(len(validMoves)):  # make the move and check the black piece number
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                if move.pieceCaptured == 'bb':
                                    gs.existRed = gs.existRed - 1

                                moveMade = True
                                sqSelected = ()  # reset
                                playerClicks = []  # reset

                        if not moveMade:
                            playerClicks = [sqSelected]
                        if gs.checkEndGame(move):  # if end game set gameOver to True

                            gameOver = True

            # AI move
            if not gameOver and not humanTurn and not gs.BlueToMove:

                AIMove = findBestMove(gs, validMoves)  # call the apha beta function

                if AIMove is None:  # if no move can make, make random move
                    validMoves2 = gs.getValidMoves2()
                    AIMove = findRandomMove(validMoves2)
                    print('Random Move')

                gs.makeMove(AIMove)
                if move.pieceCaptured == 'ww':  # check the white piece number
                    gs.existBlue = gs.existBlue - 1
                if gs.checkEndGame(AIMove):
                    gameOver = True

                moveMade = True
                AIThinking = False

            if moveMade:
                validMoves = gs.getValidMoves()
                moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)  # draw the gamestate

        if e.type == p.KEYDOWN:
            if e.key == p.K_z:  # undo move when  z is pressed
                gs.undoMove()
                moveMade = True
            if e.key == p.K_r:  # reset the game if r is pressed
                gs = GameState()
                validMoves = gs.getValidMoves()
                sqSelected = ()
                playerClicks = []
                moveMade = False
        if gameOver:
            if gs.BlueToMove:
                text = 'Red Wins'
                drawEndGameText(screen, text)
                if e.type == p.KEYDOWN:
                    if e.key == p.K_r:
                        gs = GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        gameOver = False

            else:
                text = 'Blue Wins'
                drawEndGameText(screen, text)
                if e.type == p.KEYDOWN:
                    if e.key == p.K_r:
                        gs = GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        gameOver = False

        clock.tick(max_fps)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):  # function to color the select square and its valid moves
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.BlueToMove else 'b'):
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(100)  # transperancy value
            s.fill(p.Color('gray'))
            screen.blit(s, (c * sq_size, r * sq_size))
            s.fill(p.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (sq_size * move.endCol, sq_size * move.endRow))


def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):

    colors = [p.Color("white"),p.Color("gray")]
    GRASS = p.transform.scale(p.image.load('images/grass_6.jpg'), (sq_size, sq_size))
    bridge=p.transform.scale(p.image.load('images/bridge.png'), (sq_size, sq_size))
    for i in range(dim):
        for j in range(dim):
            if (i==3 and j==4) or (i==4 and j==4):
                screen.blit(bridge, p.Rect(i * sq_size, j * sq_size, sq_size, sq_size))
            else:
                screen.blit(GRASS, p.Rect(i * sq_size, j * sq_size, sq_size, sq_size))


def drawPieces(screen,board):
    ROCK = p.transform.scale(p.image.load('images/rock_2.png'), (sq_size*0.7, sq_size*0.7))
    CASTLE = p.transform.scale(p.image.load('images/Castle.png'), (sq_size, sq_size))
    RIVER=p.transform.scale(p.image.load('images/lake_5.png'), (sq_size, sq_size))
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece == "rock":
                screen.blit(ROCK, p.Rect(c * sq_size+sq_size*0.18, r * sq_size+sq_size*0.18, sq_size, sq_size))
            elif piece == 'bk' or piece == 'wk':
                screen.blit(CASTLE, p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))
            elif piece == "water":
                screen.blit(RIVER, p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))
            elif piece =="ww" or piece=="bb":
                screen.blit(IMAGES[piece],p.Rect(c*sq_size+sq_size*0.18,r*sq_size,sq_size,sq_size))
            elif piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)  # Setting font
    text_object = font.render(text, 0, p.Color('Black'))

    window_width = Width / 3
    window_height = Height / 6

    text_window = p.Surface((window_width, window_height), p.SRCALPHA)
    text_window.fill((255, 255, 255, 164))

    text_location = p.Rect(0, 0, window_width, window_height).move(
        (window_width - text_object.get_width()) // 2,
        (window_height - text_object.get_height()) // 2
    )
    text_window.blit(text_object, text_location)

    screen.blit(text_window, ((screen.get_width() - window_width) // 2, (screen.get_height() - window_height) // 2))


if __name__ == "__main__":
    main()
