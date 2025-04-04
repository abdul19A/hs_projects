# Abdulrahman Abusharbain
# Period 4
# 5/6/24

# DO NOT RUN THIS FILE, THIS FILE IS ONLY FOR EDITING THE GAME!


from graphics import *
from BecomeCubeTerrainCreator import *
from time import sleep


class Player:
    def __init__(self, window, spawn):

        pointX, pointY = spawn.getX(), spawn.getY()
        # player shape
        self.shape = Rectangle(Point(pointX - 4, pointY - 4), Point(pointX + 4, pointY + 4))
        self.shape.setWidth(0)
        self.shape.setFill('red')
        self.shape.draw(window)
        self.win = window
        #stats
        self.deaths = 0
        # movement
        self.dx = 0
        self.dy = 0

        # These atr change
        self.inAir = True
        self.respawnPoint = spawn
        self.dirGrav = 1

        # trail added due to graphics glitch (object disappears if moving too quick)
        self.trail = self.shape.clone()
        self.trail.setFill('yellow')
        self.trail.draw(window)

    # checks if it hits hittable blocks
    # as soon as it does, it returns True which reduces time complexity
    # This process makes the player stuck sometimes as it cannot check two collisions at a time
    def checkCollision(self, playerRect):
        for rect in Terrain.hitBox:
            if Rectangle.testCollision_RectVsRect(playerRect, rect):
                return True
        return False

    # checks if it hits stuff that make the player bounce
    def checkBounce(self, playerRect):
        for rect in Terrain.bounceBox:
            if Rectangle.testCollision_RectVsRect(playerRect, rect):
                return True
        return False

    # checks if it hits stuff that makes the player slide
    def checkSlip(self, playerRect):
        for rect in Terrain.slipBox:
            if Rectangle.testCollision_RectVsRect(playerRect, rect):
                return True
        return False

    # undraws -> copy -> draw -> update
    def dotrail(self):
        self.trail.undraw()
        self.trail = self.shape.clone()
        self.trail.draw(self.win)

    # The most complicated thing here

    def allowMovement(self, keys):
        self.dotrail()
        self.checkChangeGrav()
        if 'r' in keys:
            self.die()
        checkBothXY = False
        premoveX = self.shape.clone()
        premoveY = self.shape.clone()
        if 'd' in keys and self.dx < 3:
            self.dx += 0.04
        elif 'a' in keys and self.dx > -3:
            self.dx -= 0.04
        self.dy += 0.1 * self.dirGrav

        premoveX.move(self.dx, 0)
        premoveY.move(0, self.dy)

        if self.checkBounce(premoveY):
            if 'space' in keys:
                self.dy *= -1.1
            else:
                self.dy *= -0.98
        if self.checkBounce(premoveX):
            self.dx *= -0.9

        for i in range(2):
            if self.checkCollision(premoveY):
                checkBothXY = True
                self.dy *= -0.00001
                if not self.checkSlip(premoveY):
                    self.dx *= 0.99
                if ('space' in keys or 'w' in keys) and self.dy > -3:
                    self.dy -= 3 * self.dirGrav
                    premoveY.move(0, self.dy)
                    if self.checkCollision(premoveY):
                        self.dy = 0
        if self.checkCollision(premoveX):
            self.dx *= -0.1

            if checkBothXY:
                if self.checkCollision(premoveX) and self.checkCollision(premoveY):
                    # print('Test')
                    self.dx *= 2
                    self.dy *= 3

        self.shape.move(self.dx, self.dy)

    def checkWinLevel(self, lvl):
        xLoco = self.shape.getCenter().getX()
        if xLoco > 600:
            self.shape.move(-600, 0)
            return 1
        elif xLoco < 0:
            self.shape.move(600, 0)
            return -1
        else:
            return None

    def undraw(self):
        self.shape.undraw()
        self.trail.undraw()
    # death animation
    def die(self):
        self.deaths += 1
        self.trail.undraw()
        self.shape.setFill('blue')
        self.dirGrav = 1
        update()
        sleep(1)
        self.shape.setFill('red')
        self.dx = 0
        self.dy = 0
        center = self.shape.getCenter()
        self.shape.move(self.respawnPoint.getX() - center.getX(), self.respawnPoint.getY() - center.getY())

    # next level
    def nextLevel(self, newlvl):
        self.respawnPoint = newlvl.spawn
        self.shape.redraw()
    # checks if it hits deadly blocks
    def checkHitDanger(self):
        yLoco = self.shape.getCenter().getY()
        if yLoco > 500 or yLoco < 0:
            self.die()
            return
        for item in Terrain.deathBox:
            if Rectangle.testCollision_RectVsRect(self.shape, item):
                self.die()
                return

    # checks if it hits antigrav Blocks
    def checkChangeGrav(self):
        for item in Terrain.upGravBox:
            if Rectangle.testCollision_RectVsRect(self.shape, item):
                self.dirGrav = -1
                self.dy *= 0.98
        for item in Terrain.downGravBox:
            if Rectangle.testCollision_RectVsRect(self.shape, item):
                self.dirGrav = 1
                self.dy *= 0.98

    # developer option
    def doTeleport(self, mouse):
        center = self.shape.getCenter()
        xf, yf = mouse.getX(), mouse.getY()
        xs, ys = center.getX(), center.getY()
        self.dy = 0
        self.dx = 0
        self.shape.move(xf - xs, yf - ys)
