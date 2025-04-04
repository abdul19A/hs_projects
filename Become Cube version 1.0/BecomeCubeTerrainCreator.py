# Abdulrahman Abusharbain
# Period 4
# 5/6/24

# DO NOT RUN THIS FILE, THIS FILE IS ONLY FOR EDITING THE GAME!

from graphics import *
from time import perf_counter
from math import *

class Terrain:
    # all colors to add
    colorOptions = ['#ADD8E6', '#567D46', '#92725C', '#FFFFFF', '#800080', '#A9A9A9', '#BC9E82', '#00008B', '#000000',
                    '#D4D4D4', '#FF00FF', '#6e7f80', '#FFBF00', '#a35fa5', '#1F3B4D', '#660000', '#32CD32', '#D5FFFF']
    # prevents impossibly hard to find errors in textfile
    for color in colorOptions:
        if color[0] != '#' or '#' in color[1:] or len(color) > 7:
            print('Error')
            raise SyntaxError
    drawingList = []
    hitBox = []
    deathBox = []
    downGravBox = []
    upGravBox = []
    flexibleBox = []
    bounceBox = []
    slipBox = []
    prevTime = None
    x = 0
    y = 0
    filePath = 'BecomeCubeTerrainData.txt'
    levelsData = open(filePath, 'r').read().split('\n')
    lenLevelsData = len(''.join(levelsData))
    # controls to colors
    keysToClicks = {
        'b': 0,
        'g': 1,
        'r': 2,
        'w': 3,
        'i': 4,
        's': 5,
        'l': 6,
        'd': 7,
        'f': 8,
        'q': 9,
        'a': 10,
        'c': 11,
        'o': 12,
        'm': 13,
        'e': 14,
        'z': 15,
        'n': 16,
        'h': 17

    }
    # player spawn points
    # idea: I could put this on the other file
    spawnPoints = {
        0: Point(65, 55),
        1: Point(55, 420),
        2: Point(55, 150),
        3: Point(10, 285),
        4: Point(60, 454),
        5: Point(114, 433),
        6: Point(75, 459),
        7: Point(14.0, 113.0),
        8: Point(19, 25),
        9: Point(22, 50),
        10: Point(49, 228),
        11: Point(126, 26),
        12: Point(20, 463),
        13: Point(86, 112),
        14: Point(11, 227),
        15: Point(9, 78),
        16: Point(19, 471),
        17: Point(131, 390),
        18: Point(10, 225),
        19: Point(13, 153),
        20: Point(12, 470),
        21: Point(12, 470),
        22: Point(12, 470),
        23: Point(12, 470),
        24: Point(12, 470),
        25: Point(12, 470),

    }

    def __init__(self, level, window):
        self.win = window
        self.lvl = level
        self.spawn = Terrain.spawnPoints[level]
        self.lvlCode = Terrain.levelsData[level]
        i = 0
        for y in range(0, 500, 10):
            for x in range(0, 600, 10):
                rect = Rectangle(Point(x, y), Point(x + 10, y + 10))
                idx = int(i * 6)
                color = '#' + self.lvlCode[idx:idx + 6]
                rect.setFill(color)
                rect.setWidth(0)
                rect.draw(window)
                i += 1
                if color in Terrain.colorOptions:
                    colorIdx = Terrain.colorOptions.index(color)
                    if colorIdx in [1, 2, 5]:
                        Terrain.hitBox.append(rect)
                    elif colorIdx in [4, 7, 10]:
                        Terrain.deathBox.append(rect)
                    elif colorIdx == 8:
                        Terrain.upGravBox.append(rect)
                    elif colorIdx == 12:
                        Terrain.downGravBox.append(rect)
                    elif colorIdx in [15, 14, 13]:
                        Terrain.flexibleBox.append([rect, colorIdx])
                    elif colorIdx == 16:
                        Terrain.bounceBox.append(rect)
                    elif colorIdx == 17:
                        Terrain.slipBox.append(rect)
                        Terrain.hitBox.append(rect)

                Terrain.drawingList.append(rect)
        self.doStaticlvlEvent()

    @staticmethod
    def doMenu(win):
        def checkClickPlay():
            for box in Terrain.bounceBox:
                if Rectangle.testCollision_RectVsPoint(box, mouse):
                    return True
            for box in Terrain.upGravBox:
                if Rectangle.testCollision_RectVsPoint(box, mouse):
                    return True
            return False

        Terrain(21, win)
        creatorText = Text(Point(300.0, 30.0), 'Created by \nAbdulrahman Abusharbain')
        creatorText.draw(win)
        creatorText.setFill('grey')
        creatorText.setFace('courier')
        while not win.closed:
            mouse = win.getMouse()
            if checkClickPlay():
                break
        creatorText.undraw()
        for i in Terrain.drawingList:
            i.undraw()
        Terrain.drawingList = []
        Terrain.hitBox = []
        Terrain.deathBox = []
        Terrain.upGravBox = []
        Terrain.downGravBox = []
        Terrain.flexibleBox = []
        Terrain.bounceBox = []
        Terrain.slipBox = []

    def editMode(self):
        clicks = 0
        stop = True
        brushSize = 0
        cordsToSave = []
        cList = []
        while not self.win.closed:

            update(100)
            self.doMovinglvlEvent(perf_counter())
            try:
                key = self.win.checkKey()
                mouse = self.win.getCurrentMouseLocation()
                click = self.win.checkMouse()
            except Exception:
                pass

            if click:
                print(mouse)
                stop = True
            if key in Terrain.keysToClicks.keys():
                clicks = Terrain.keysToClicks[key]
                stop = False
            elif key == 'p':
                stop = True
            elif key in [str(i) for i in range(10)]:
                stop = True
                brushSize = int(key)
            elif key == "Right" or key == 'Left':
                break

            if mouse and not stop:
                mX, mY = mouse.getX(), mouse.getY()
                for i in range(-brushSize, brushSize + 1):
                    newmX = mX + 5 * i
                    for j in range(-brushSize, brushSize + 1):
                        newmY = mY + 5 * j
                        cords = int(newmY / 10) * 60 + int(newmX / 10)
                        if newmX < 600 and newmY < 500:
                            newColor = Terrain.colorOptions[clicks]
                            Terrain.drawingList[cords].setFill(newColor)
                            if [cords, newColor] not in cordsToSave:
                                cordsToSave.append([cords, newColor])
                                cList.append(cords)
                                if cList.count(cords) > 1:
                                    idxCds = cList.index(cords)
                                    cList.remove(cords)
                                    cordsToSave.pop(idxCds)
        lenCTS = len(cordsToSave)
        for i, each in enumerate(cordsToSave[::-1]):
            idx, col = each[0] * 6, each[1][1:]
            if col != self.lvlCode[idx:idx + 6]:
                # this piece of code is very inefficient(possible future change)
                self.lvlCode = self.lvlCode[:idx] + col + self.lvlCode[idx + 6:]
                print(f'{i}/{lenCTS} ({int((i / lenCTS) * 100)}%)')

        Terrain.levelsData[self.lvl] = self.lvlCode
        if Terrain.levelsData == [] or len(Terrain.levelsData) < 10:
            print('save unsuccessful')
            return
        with open(Terrain.filePath, 'w') as file:
            for level in Terrain.levelsData:
                file.write(level + '\n')
            file.close()
            print('Saved Level ', self.lvl)
        if key == "Right":
            if self.lvl < 25:
                return self.nextLevel(1)
        elif key == "Left":
            if self.lvl > 0:
                return self.nextLevel(-1)
        elif not win.closed:
            return self.nextLevel(0)

    # resets Terrain atr
    # (Code could be rewritten here to make these attributes for each specific level)
    def nextLevel(self, newlvl):
        for i in Terrain.drawingList:
            i.undraw()
        Terrain.drawingList = []
        Terrain.hitBox = []
        Terrain.deathBox = []
        Terrain.upGravBox = []
        Terrain.downGravBox = []
        Terrain.flexibleBox = []
        Terrain.bounceBox = []
        Terrain.slipBox = []
        if self.lvl + newlvl > 20:
            return None
        new = Terrain(level=self.lvl + newlvl, window=self.win)
        return new

    # changes color and adds them to list of hitbox
    # could be changed to init
    def doMovinglvlEvent(self, time):
        timely = int(time) % 4 > 1
        if timely != Terrain.prevTime:
            for sqr, colorIdx in Terrain.flexibleBox:
                if colorIdx == 15:
                    if timely and sqr in Terrain.hitBox:
                        sqr.setFill('#C3C3C3')
                        Terrain.hitBox.remove(sqr)

                    elif sqr not in Terrain.hitBox:
                        sqr.setFill('#808080')
                        Terrain.hitBox.append(sqr)
                if colorIdx == 14:
                    if not timely and sqr in Terrain.hitBox:
                        sqr.setFill('#C3C3C3')
                        Terrain.hitBox.remove(sqr)

                    elif sqr not in Terrain.hitBox:
                        sqr.setFill('#808080')
                        Terrain.hitBox.append(sqr)

            Terrain.prevTime = timely

    # does the texts
    def doStaticlvlEvent(self):
        def doText(cords, text):
            textObj = Text(cords, text)
            textObj.setSize(11)
            textObj.setFace('courier')
            textObj.setFill('darkBlue')
            return textObj

        if self.lvl == 0:
            textList = [
                doText(Point(63, 42), 'Use A and D\n to move!'),
                doText(Point(240, 50), 'Use "SPACE" or W to jump!'),
                doText(Point(275, 160), 'Blue and Purple squares\n WILL kill you!'),
                doText(Point(386, 238), 'This game is not perfect...\n press R if you are stuck'),
                doText(Point(200, 300), 'Find new\nTechniques!'),
                doText(Point(430, 430), 'The Void is deadly!'),
            ]
        elif self.lvl == 1:
            textList = [
                doText(Point(260, 400), 'Have fun!')
            ]
        elif self.lvl == 10:
            textList = [
                doText(Point(248.0, 223.0), 'Jump in \nthe black water!'),
                doText(Point(446.0, 17.0), 'Yellow makes you normal!')
            ]
        elif self.lvl == 16:
            textList = [
                doText(Point(211, 421), 'Bounce!'),
                doText(Point(310.0, 84.0), 'Hold Space\nTo Bounce Higher!')
            ]

        else:
            textList = []

        for text in textList:
            text.draw(self.win)

    @staticmethod
    def endGame(win):

        # endGame animation
        win.setBackground('#ADD8E6')
        rect1 = Rectangle(Point(0,0), Point(600, 200))
        rect2 = Rectangle(Point(0, 300), Point(600, 500))
        rect3 = Rectangle(Point(-90, 220), Point(-10, 300))
        for rect in rect1, rect2, rect3:
            rect.setFill('#A9A9A9')
            rect.setWidth(0)
            rect.draw(win)
        rect3.setFill('red')
        while rect3.getP1().getX() < 600:
            rect3.move(6, 0)
            update(100)
        for rect in rect1, rect2, rect3:
            rect.undraw()
        rect4 = Rectangle(Point(0,0), Point(200, 225))
        rect5 = Rectangle(Point(0, 275), Point(200, 500))
        rect6 = Rectangle(Point(-50, 235), Point(-10, 275))
        for rect in rect4, rect5, rect6:
            rect.setFill('#A9A9A9')
            rect.setWidth(0)
            rect.draw(win)
        rect6.setFill('red')
        i = 0.01
        while rect6.getP1().getX() < 600:
            rect6.move(7 + i, 0)
            i += 0.01
            update(100)
        for rect in rect4, rect5, rect6:
            rect.undraw()
        rect7 = Rectangle(Point(-18, 246), Point(-10, 254))
        rect7.setFill('red')
        rect7.setWidth(0)
        rect7.draw(win)
        rect8 = rect7.clone()
        while rect7.getP1().getX() < 296:
            rect8.draw(win)
            rect7.move(2 + i, 0)
            i += 0.01
            update(100)
            rect8.undraw()
            rect8.move(2 + i, 0)
        for i in range(4, 20):
            rect7.undraw()
            rect7 = Rectangle(Point(300 - i, 250 - i), Point(300 + i, 250 + i))
            rect7.setFill('red')
            rect7.setWidth(0)
            rect7.draw(win)
            update(100)
        def getDist(c1, c2):
            return ((c2.getX() - c1.getX())**2 + (c2.getY() - c1.getY())**2)**.5
        def getdxdy(c1, c2):
            angle = atan2(c2.getY() - c1.getY(), c2.getX() - c1.getX())
            return 4*cos(angle), 4*sin(angle)
        center7 = rect7.getCenter()
        colors2 = ['blue', 'yellow', color_rgb(100,255,100), 'orange', 'purple']
        ptsX = [0, 300, 600, 400, 200]
        ptsY = [-40, -40, -40, 540, 540]
        for i in range(5):
            rect = Rectangle(Point(ptsX[i] - 20, ptsY[i]-20), Point(ptsX[i] + 20, ptsY[i] + 20))
            rect.setFill(colors2[i])
            rect.setWidth(0)
            rect.draw(win)
            rect7.redraw()
            centRect = rect.getCenter()
            dx, dy = getdxdy(centRect, center7)
            while getDist(centRect, center7) > 3:

                centRect = rect.getCenter()
                rect.move(dx, dy)
                update(100)
            rect.undraw()
        y = 1
        while rect7.getCenter().getY() < 520:
            rect7.move(0, y)
            y += 0.1
            update(100)
        rect7.undraw()

        rect9 = Rectangle(Point(0, 400), Point(600, 500))
        rect9.setFill('lightGrey')
        rect9.draw(win)

        poly1 = Polygon(Point(280 + 400**.5, 430 - 400**.5), Point(320 + 400**.5, 430 - 400**.5), Point(320, 430), Point(280, 430))
        poly1.setFill('yellow')
        poly1.draw(win)

        poly2 = Polygon(Point(320, 470), Point(320, 430), Point(320 + 400**.5, 430 - 400**.5), Point(320 + 400**.5, 470 - 400**.5))
        poly2.setFill(color_rgb(100,255,100))
        poly2.draw(win)

        rect10 = Rectangle(Point(280, 430), Point(320, 470))
        rect10.setFill('red')
        rect10.draw(win)

        fText = Text(Point(300, 550), 'You have become\nCUBE')
        fText.setFace('courier')
        fText.setSize(34)
        fText.draw(win)

        for shape in rect9, rect10, poly1, poly2:
            shape.move(0, 150)
            update()
        for i in range(150):
            fText.move(0, -3)
            for shape in rect9, rect10, poly1, poly2:
                shape.move(0, -1)
            update(100)

        win.getMouse()
        win.close()
        quit()


editorMode = True
if __name__ == '__main__' and editorMode:
    win = GraphWin('Terrain Editor: close to save!', 600, 500, False)
    level = Terrain(level=21, window=win)
    while not win.closed:
        update(100)
        level = level.editMode()
