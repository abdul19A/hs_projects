from graphics import *
from random import randrange, choice
from Tetris.tetrisClass import incrementRGB

startMenu = Rectangle(Point(0, 0), Point(500, 600))
startMenu.setWidth(5)
startMenu.setFill('black')
startMenu.setOutline('grey')

drawList = []

drawList.append(startMenu)

for i in range(1000):
    pt = Point(randrange(0, 500), randrange(0, 600))
    pt.setFill(color_rgb(randrange(0, 255), randrange(0, 255), randrange(0, 255)))
    drawList.append(pt)

tetrisList = []
tetrisList2 = []
for i, j in enumerate('TETRIS'):
    startMenuText = Text(Point(170 + i * 32, 150), j)
    startMenuText.setFill(color_rgb(100, 0, 0))
    startMenuText.setSize(36)

    startMenuText2 = Text(Point(175 + i * 30, 153), j)
    startMenuText2.setFill('black')
    startMenuText2.setStyle('bold')
    startMenuText2.setSize(36)
    drawList.append(startMenuText2)
    drawList.append(startMenuText)
    tetrisList.append(startMenuText)
    tetrisList2.append(startMenuText2)

startPlayMenu = Rectangle(Point(200, 250), Point(300, 290))
startPlayMenu.setWidth(2)
startPlayMenu.setOutline(color_rgb(50, 150, 50))
startPlayMenu.setFill(color_rgb(0, 255, 0))

startQuitMenu = Rectangle(Point(200, 310), Point(300, 350))
startQuitMenu.setWidth(2)
startQuitMenu.setOutline(color_rgb(150, 50, 50))
startQuitMenu.setFill(color_rgb(255, 0, 0))


def buttonText(point, text):
    startPlayText = Text(point, text)
    startPlayText.setSize(14)
    startPlayText.setFill(color_rgb(250,250,250))
    drawList.append(startPlayText)
    return startPlayText



drawList.append(startPlayMenu)
drawList.append(startQuitMenu)
edge = Rectangle(Point(0,0), Point(500, 600))
edge.setWidth(10)
drawList.append(edge)
playText = buttonText(Point(250,270), 'Play')
buttonText(Point(250, 330), 'Quit')
infoObj = Rectangle(Point(40, 435), Point(460, 585))
infoObj.setFill('black')
drawList.append(infoObj)

infoText = buttonText(Point(250,500), """

Controls:

  ←: left  |  →: right  |  ↑: rotate  |  ↓: down  

   SPACE: drop  |  'ESC': quit  |  'P': Pause  | 'R': Restart

""")
infoText.setFill('lightGrey')

def transitionScreen(win):
    colors = ['red', 'green', 'blue', 'cyan', 'purple', 'orange', 'yellow']
    rectList = []
    for i in range(30):
        x = i%5
        y = i//5
        rect = Rectangle(Point(x * 100, y * 100 - 600), Point(x * 100 + 100, y * 100 - 500))
        rect.setWidth(5)
        rect.setOutline('grey')
        rect.setFill(choice(colors))
        rect.draw(win)
        rectList.append(rect)
    for i in range(30, -1, -5):
        for j in range(6):
            for obj in rectList[i - 5: i]:
                obj.move(0,100)
            update(120)
    return rectList


def untransitionScreen(rectList, win):
    for obj in rectList:
        obj.undraw()
        obj.draw(win)
    for i in range(30, -1, -5):
        for j in range(12):
            for obj in rectList[i - 5: i]:
                obj.move(0,50)
            update(240)
    return rectList
def redrawMenu(win):
    for obj in drawList:
        obj.draw(win)
    return True

def runMenu(win):
    r, g, b = (100, 0, 0)
    win.config(cursor='dotbox')
    update(100)
    while not win.closed:
        update(100)
        click = win.checkMouse()
        r, g, b = incrementRGB(r, g, b)
        r2 = r - 100
        if r2 < 0:
            r2 = 0
        g2 = g - 100
        if g2 < 0:
            g2 = 0
        b2 = b - 100
        if b2 < 0:
            b2 = 0
        for letter in tetrisList:
            letter.setFill(color_rgb(r, g, b))
        for letter in tetrisList2:
            letter.setFill(color_rgb(r2, g2, b2))
        edge.setOutline(color_rgb(r, g, b))
        if click != None:
            if Rectangle.testCollision_RectVsPoint(startPlayMenu, click):
                rectList = transitionScreen(win)
                for obj in drawList:
                    obj.undraw()
                untransitionScreen(rectList, win)
                break
            elif Rectangle.testCollision_RectVsPoint(startQuitMenu, click):
                win.close()
                quit()

# testing
if __name__ == '__main__':
    print('please run tetris.py to play!')

