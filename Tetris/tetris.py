# By: Abdulrahman Abusharbain
# done with class: 3/11/24


from Tetris.tetrisClass import *
from Tetris.tetrisMenu import *
from time import perf_counter, sleep

# start of display
screen = []
win = GraphWin('Tetris', 500, 602, False)
edge = Rectangle(Point(0, 0), Point(500, 600))
edge.setWidth(4)

menu = Rectangle(Point(0, -100), Point(200, 600))
menu.setFill(color_rgb(50, 50, 50))
menu.draw(win)
screen.append(menu)

tetrisText = Text(Point(100, 50), 'TETRIS')
tetrisText.setFill('white')
tetrisText.setStyle('bold')
tetrisText.setStyle('italic')
tetrisText.setFace('courier')
tetrisText.setSize(28)
tetrisText.draw(win)
screen.append(tetrisText)


def drawText(pt, text):
    draftText = Text(pt, text)
    draftText.setFace('courier')
    draftText.setFill('white')
    draftText.setStyle('bold')
    draftText.setSize(11)
    draftText.draw(win)
    screen.append(draftText)
    return draftText


tetrisHighscoreText = drawText(Point(90, 100), 'High Score: ')
tetrisScoreText = drawText(Point(90, 125), 'Score: ')
tetrisClearedText = drawText(Point(90, 150), 'Lines Cleared: ')
tetrisLevelText = drawText(Point(90, 175), 'Level: ')
tetrisDroppedText = drawText(Point(90, 200), 'Blocks Dropped: ')
tetrisNextText = drawText(Point(40, 430), 'Next: ')
for i in range(200, 500, 30):
    for j in range(0, 600, 30):
        backSqrs = Rectangle(Point(i, j), Point(i + 30, j + 30)).draw(win)
        backSqrs.setFill(color_rgb(20, 20, 20))
        backSqrs.setOutline(color_rgb(40, 40, 40))
        backSqrs.setWidth(2)
        screen.append(backSqrs)

comboText = Text(Point(100, 350), '')
comboTextDisplayTime = 2
comboText.setFill('red')
comboText.setStyle('bold')
comboText.setFace('courier')
comboText.setSize(20)
comboText.draw(win)
edge.draw(win)
screen.append(edge)
screen.append(comboText)
# end of display
# press here
beforeCombo = perf_counter()
def play():
    worldList = [menu, Rectangle(Point(500, -100), Point(530, 600)), Rectangle(Point(0, 600), Point(500, 730))]
    win.config(cursor='none')
    piece = pieceList[0]
    piece.draw(win)
    shuffle(pieceList)
    nextPiece = pieceList[0]
    nextPiece.display(win)
    timeBefore = perf_counter()
    buttonTimBefore = perf_counter()
    beforeCombo = perf_counter()
    clone = None
    r, g, b = (100, 0, 0)
    comboText.setText('3')
    update(100)
    sleep(1)
    comboText.setText('2')
    update(100)
    sleep(1)
    comboText.setText('1')
    update(100)
    sleep(1)
    comboText.setText('')
    while not win.closed:
        buttonTimeDif = perf_counter() - buttonTimBefore
        timeNow = perf_counter()
        keys = win.checkKeys()
        r, g, b = incrementRGB(r, g, b)
        tetrisText.setFill(color_rgb(r, g, b))
        edge.setOutline(color_rgb(r, g, b))

        if len(keys) >= 1 and (buttonTimeDif >= 0.15 or keys != clone):
            clone = keys.copy()
            keyType = piece.recieveButton(keys, worldList)
            if keyType == 'paused':
                comboText.setText('Paused')
                update(100)
                sleep(1)
                while win.checkKey() != 'p':
                    update(100)
                comboText.setText('3')
                update(100)
                sleep(1)
                comboText.setText('2')
                update(100)
                sleep(1)
                comboText.setText('1')
                update(100)
                sleep(1)
                comboText.setText('')
            elif keyType == 'restart':
                Tetris.storeHighscore()
                while piece.selected:
                    piece.doYMovement()
                    piece.y = 30
                    piece.checkMovementCollision(worldList)
                Tetris.resetTetris()
                play()


            buttonTimBefore = perf_counter()

        worldList = piece.checkMovementCollision(worldList)
        piece.doXMovement()
        piece.doYMovement()
        piece.rotate(worldList, win)
        if not piece.selected:
            nextPiece.undisplay()
            piece = nextPiece
            piece.selected = True
            piece.draw(win)
            shuffle(pieceList)
            nextPiece = pieceList[0]
            nextPiece.display(win)

        if timeNow - timeBefore > Tetris.dropSpeed:
            piece.y = 30
            timeBefore = perf_counter()

        if Tetris.gameEnded():
            break
        else:
            Tetris.checkLevel()
        combo = Tetris.doTheBreak(worldList)
        if combo == 0 and perf_counter() - beforeCombo > comboTextDisplayTime:
            comboText.setText('')
        elif combo == 1:
            comboText.setText(f'Single!\n+ {100 * Tetris.level}')
            beforeCombo = perf_counter()
        elif combo == 2:
            comboText.setText(f'Double!\n+ {150 * Tetris.level}')
            beforeCombo = perf_counter()
        elif combo == 3:
            comboText.setText(f'Triple!\n+ {200 * Tetris.level}')
            beforeCombo = perf_counter()
        elif combo == 4:
            comboText.setText(f'Tetris!\n+ {300 * Tetris.level}')
            beforeCombo = perf_counter()

        tetrisHighscoreText.setText(f'High Score: {Tetris.getHighscore()}')
        tetrisScoreText.setText(f'Score: {Tetris.score}')
        tetrisClearedText.setText(f'Lines Cleared: {Tetris.clearedLines}')
        tetrisDroppedText.setText(f'Blocks Dropped: {Tetris.numBlocks}')
        tetrisLevelText.setText(f'Level: {Tetris.level}')
        update(100)


if __name__ == '__main__':
    sqrList = []
    while not win.closed:
        redrawMenu(win)
        if sqrList != []:
            untransitionScreen(sqrList, win)
        runMenu(win)
        playText.setText('Restart')
        play()
        Tetris.storeHighscore()
        Tetris.resetTetris()
        sqrList = transitionScreen(win)

win.mainloop()
