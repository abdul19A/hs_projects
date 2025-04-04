from graphics import *
from time import sleep
from random import shuffle

oPieceRot = [
    [(1, 1), (1, 2), (2, 1), (2, 2)]
]

iPieceRot = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(2, -1), (2, 0), (2, 1), (2, 2)]
]

sPieceRot = [
    [(0, 2), (1, 2), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)]
]

zPieceRot = [
    [(0, 1), (1, 1), (1, 2), (2, 2)],
    [(2, 0), (2, 1), (1, 1), (1, 2)]
]

lPieceRot = [
    [(0, 1), (1, 1), (2, 1), (0, 2)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(0, 1), (1, 1), (2, 1), (2, 0)],
    [(1, 0), (1, 1), (1, 2), (2, 2)]
]
jPieceRot = [
    [(0, 1), (1, 1), (2, 1), (2, 2)],
    [(1, 0), (1, 1), (1, 2), (0, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(1, 0), (2, 0), (1, 1), (1, 2)]
]

tPieceRot = [
    [(0, 1), (1, 1), (2, 1), (1, 2)],
    [(1, 0), (1, 1), (0, 1), (1, 2)],
    [(0, 1), (1, 1), (1, 0), (2, 1)],
    [(1, 0), (1, 1), (2, 1), (1, 2)]
]

rotationDic = {
    'o': oPieceRot,
    'i': iPieceRot,
    's': sPieceRot,
    'z': zPieceRot,
    'l': lPieceRot,
    'j': jPieceRot,
    't': tPieceRot
}


class Tetris:
    columnTestList = [[], [], [], [], [],
                      [], [], [], [], [],
                      [], [], [], [], [],
                      [], [], [], [], []]
    nextIndex = 0
    clearedLines = 0
    level = 1
    score = 0
    dropSpeed = 1
    allBlocks = []
    displayList = []
    numBlocks = 0

    def __init__(self, color, blockName):
        self.rotDic = rotationDic[blockName]
        self.allowRotate = True
        self.rotN = 0
        self.doRotate = False
        self.blockCords = rotationDic[blockName][0]
        self.blockList = []
        self.prevBlockList = []
        self.color = color
        self.blockName = blockName
        self.selected = True
        self.x = 0
        self.y = 0
        self.dxTotal = 0
        self.dyTotal = 0
        self.key = None

    def display(self, win):

        for x, y in self.blockCords:
            block = Rectangle(Point(30 + x * 30, 450 + y * 30), Point(60 + x * 30, 480 + y * 30))
            block.setFill(self.color)
            block.setOutline('grey')
            block.setWidth(1)
            block.draw(win)
            Tetris.displayList.append(block)

    def undisplay(self):
        for block in Tetris.displayList:
            block.undraw()

    def undraw(self):
        for block in self.blockList:
            block.undraw()

    def draw(self, win):
        for x, y in self.blockCords:
            block = Rectangle(Point(290 + x * 30, -90 + y * 30), Point(320 + x * 30, -60 + y * 30))
            block.setFill(self.color)
            block.setOutline('grey')
            block.setWidth(1)
            block.draw(win)
            self.blockList.append(block)

    def recieveButton(self, buttons, worldList):
        if 'Left' in buttons:
            self.x = -30
        elif 'Right' in buttons:
            self.x = 30
        elif 'space' in buttons:
            while self.selected:
                self.doYMovement()
                self.y = 30
                self.checkMovementCollision(worldList)
        elif 'Down' in buttons:
            self.y = 30
        elif 'Up' in buttons:
            self.doRotate = True
        if 'Escape' in buttons:
            quit()
        if 'p' in buttons:
            return 'paused'
        if 'r' in buttons:
            return 'restart'

    def doXMovement(self):
        if self.selected:
            for blocks in self.blockList:
                blocks.move(self.x, 0)
            self.dxTotal += self.x
            self.x = 0

    def doYMovement(self):
        if self.selected:
            for blocks in self.blockList:
                blocks.move(0, self.y)
            self.dyTotal += self.y
            self.y = 0

    def checkMovementCollision(self, world):
        if self.selected:
            for block in self.blockList:

                p1x = block.getP1().getX()
                p1y = block.getP1().getY()
                p2x = block.getP2().getX()
                p2y = block.getP2().getY()
                cloneP1X = p1x + 1
                cloneP2X = p2x - 1
                cloneP1Y = p1y + 1
                cloneP2Y = p2y - 1

                hitBoxX = Rectangle(Point(cloneP1X, cloneP1Y), Point(cloneP2X, cloneP2Y))
                hitBoxY = hitBoxX.clone()

                hitBoxX.move(self.x, 0)
                hitBoxY.move(0, self.y)

                for stuff in world:
                    if Rectangle.testCollision_RectVsRect(hitBoxY, stuff):
                        Tetris.nextIndex += 1
                        self.selected = False
                        self.doFlash()
                        for block2 in self.blockList:
                            world.append(block2)
                            Tetris.allBlocks.append(block2)
                        Tetris.numBlocks += 1
                        self.getColumns()
                        self.reset()
                        return world
                    if Rectangle.testCollision_RectVsRect(hitBoxX, stuff):
                        self.x = 0
        return world

    def rotate(self, world, win):
        if self.doRotate:
            orig = self.rotN
            self.rotN -= 1
            length = len(self.rotDic)
            if self.rotN < 0:
                self.rotN = length - 1
            elif self.rotN >= length:
                self.rotN = 0
            self.blockCords = self.rotDic[self.rotN]
            doRotate2 = True
            for x, y in self.blockCords:
                block = Rectangle(Point(291 + x * 30 + self.dxTotal, -89 + y * 30 + self.dyTotal),
                                  Point(319 + x * 30 + self.dxTotal, -61 + y * 30 + self.dyTotal))
                for stuff in world:
                    if Rectangle.testCollision_RectVsRect(block, stuff):
                        self.blockCords = self.rotDic[self.rotN]
                        doRotate2 = False
                        break
            if doRotate2:
                self.redraw(win)
            self.doRotate = False

    def reset(self):
        self.rotN = 0
        self.blockList = []
        self.y = 0
        self.x = 0
        self.dxTotal = 0
        self.dyTotal = 0

    def redraw(self, win):
        self.undraw()
        self.blockList = []
        for x, y in self.blockCords:
            block = Rectangle(Point(290 + x * 30 + self.dxTotal, -90 + y * 30 + self.dyTotal),
                              Point(320 + x * 30 + self.dxTotal, -60 + y * 30 + self.dyTotal))
            block.setFill(self.color)
            block.setOutline('grey')
            block.setWidth(1)
            block.draw(win)
            self.blockList.append(block)

    def doFlash(self):
        for blocks in self.blockList:
            blocks.setWidth(0)
            blocks.setFill('black')
        update(100)
        sleep(0.1)
        for blocks in self.blockList:
            blocks.setFill(self.color)
        update(100)
        sleep(0.1)
        for blocks in self.blockList:
            blocks.setWidth(0)
            blocks.setFill('black')
        update(100)
        sleep(0.1)
        for blocks in self.blockList:
            blocks.setFill(self.color)
            blocks.setWidth(1)

    def getColumns(self):
        for block in self.blockList:
            Tetris.columnTestList[int(block.getP2().getY() // 30 - 1)].append(block)

    @staticmethod
    def doTheBreak(world):
        greatest = 0
        combo = 0

        for yList in Tetris.columnTestList:
            lenYlist = len(yList)
            if lenYlist > greatest:
                greatest = len(yList)
            if lenYlist >= 10:
                combo += 1
                Tetris.clearedLines += 1
                for blocks in yList:
                    blocks.undraw()
                    world.remove(blocks)
                for i in range(3):
                    for lists in Tetris.columnTestList[:Tetris.columnTestList.index(yList)]:
                        for blocks in lists:
                            blocks.move(0, 10)
                        update(200)
                Tetris.columnTestList.insert(0, [])
                Tetris.columnTestList.remove(yList)
        if combo == 1:
            Tetris.score += 100 * Tetris.level
        elif combo == 2:
            Tetris.score += 150 * Tetris.level
        elif combo == 3:
            Tetris.score += 200 * Tetris.level
        elif combo == 4:
            Tetris.score += 300 * Tetris.level
        return combo

    @staticmethod
    def gameEnded():
        for block in Tetris.allBlocks:
            if block.getP1().getY() <= 0 or block.getP2().getY() <= 0:
                return True
        return False

    @staticmethod
    def checkLevel():
        if Tetris.level != Tetris.clearedLines // 3 + 1:
            Tetris.level += 1
            if Tetris.level <= 7:
                Tetris.dropSpeed -= .12
            elif Tetris.level <= 9:
                Tetris.dropSpeed -= .06
            elif Tetris.level > 10:
                Tetris.dropSpeed = 0.05

    @staticmethod
    def resetTetris():
        for obj in Tetris.allBlocks:
            obj.undraw()
        for obj2 in Tetris.displayList:
            obj2.undraw()
        update(100)
        Tetris.columnTestList = [[], [], [], [], [],
                                 [], [], [], [], [],
                                 [], [], [], [], [],
                                 [], [], [], [], []]
        Tetris.nextIndex = 0
        Tetris.clearedLines = 0
        Tetris.level = 1
        Tetris.score = 0
        Tetris.dropSpeed = 1
        Tetris.allBlocks = []
        Tetris.displayList = []
        Tetris.numBlocks = 0

    @staticmethod
    # chat-gpt Code
    def getHighscore():
        try:
            with open("tetrisHighScore.txt", "r") as file:
                high_score = int(file.read())
        except FileNotFoundError:
            # If the file doesn't exist yet, create it and set high score to 0
            high_score = 0
            with open("tetrisHighScore.txt", "w") as file:
                file.write("0")
        return high_score

    def storeHighscore():
        high_score = Tetris.getHighscore()
        if Tetris.score > high_score:
            with open("tetrisHighScore.txt", "w") as file:
                file.write(str(Tetris.score))



# extra funcs
def incrementRGB(r, g, b):
    if r < 255 and g == 0 and b == 0:
        r += 3
    elif r == 255 and g < 255 and b == 0:
        g += 3
    elif r > 0 and g == 255 and b == 0:
        r -= 3
    elif r == 0 and g == 255 and b < 255:
        b += 3
    elif r == 0 and g > 0 and b == 255:
        g -= 3
    elif r < 255 and g == 0 and b == 255:
        r += 3
    elif r == 255 and g == 0 and b > 0:
        b -= 3
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    return r, g, b


# Tetris info


oPiece = Tetris(color_rgb(255, 255, 0), 'o')
iPiece = Tetris(color_rgb(0, 255, 255), 'i')
sPiece = Tetris(color_rgb(0, 255, 0), 's')
zPiece = Tetris(color_rgb(255, 0, 0), 'z')
lPiece = Tetris(color_rgb(255, 127, 0), 'l')
jPiece = Tetris(color_rgb(0, 0, 255), 'j')
tPiece = Tetris(color_rgb(128, 0, 128), 't')

pieceList = [oPiece, iPiece, sPiece, zPiece, lPiece, jPiece, tPiece]
pieceListLength = len(pieceList)
shuffle(pieceList)

if __name__ == '__main__': 
    print('please run tetris.py to play!')
