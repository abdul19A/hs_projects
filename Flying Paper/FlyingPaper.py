


#NOTE: this will create a file if it doesn't exist called code6HS.txt
# this will save your highScore
# to download:
# graphics (library), helpMenu.png, bg.png, paper.png, gold.png, cloud1.png,
# paperMenu.png, retryMenu.png


from graphics import *
from time import *
from random import *

#make game
winX = 500
winY = 500
win = GraphWin('Paper Airlines!', winX, winY, False)
oneT = True
def checkButton(button, x1,x2,y1,y2):
    return button.getX() > x1 and button.getX() < x2 and button.getY() > y1 and button.getY() < y2
def helpMenu():
    helpScreen = Image(Point(250, 250), 'helpMenu.png')
    helpScreen.draw(win)
    while True:
        if checkButton(win.getMouse(), 328, 386, 386, 411):
            helpScreen.undraw()
            update(500)
            break

def game():
    # create the background
    win.setBackground(color_rgb(50, 0, 0))
    bg = Image(Point(250,850), 'bg.png')
    bg.draw(win)
    bg1 = Image(Point(1850,350), 'bg.png')
    bg1.draw(win)
    # set countdown
    def countDown():    
        update(10)
        countdown = Text(Point(winX//2,winY//2), '')
        countdown.setSize(30)
        countdown.setFill('white')
        countdown.draw(win)
        for i in range(3, 0, -1):
            sleep(1)
            countdown.setText(str(i))
            update(10)
        countdown.undraw()
        sleep(1)
    countDown()
    # rgb background 
    def rgb(r, g, b): 
      if r < 255 and g == 0 and b == 0:
         r += 1
      elif r == 255 and g < 255 and b == 0:
         g += 1
      elif r > 0 and g == 255 and b == 0:
         r -= 1
      elif r == 0 and g == 255 and b < 255:
         b += 1
      elif r == 0 and g > 0 and b == 255 :
         g -= 1
      elif r < 255 and g ==0 and b == 255:
         r += 1
      elif r == 255 and g == 0 and b > 0:
         b -= 1
      return [r, g, b]
    #boxCreated = False
    try:
        highscore = open("code6HS.txt", 'r')
    except FileNotFoundError:
        highscore = open("code6HS.txt", 'x')
        highscore = open("code6HS.txt", 'w')
        highscore.write("0")
        highscore = open("code6HS.txt", 'r')
    highS = highscore.read()
    #print(highS)
    coinY = randrange(50, winY - 50)
        
    #create paper and interactables
    paper = Image(Point(winX//2 - 7.5, winY//2), "paper.png")
    paper.draw(win)

    coin = Image(Point(winX + 50, coinY), "gold.png")
    coin.draw(win)
    point= 0
    i = 0
    
    cloud1 = Image(Point(winX + 50 ,randrange(50, winY-50)), 'cloud1.png')
    cloud1.draw(win)

    # message setter

    message = Text(Point(winX//2,30), f"Score = {point}\nHighest Score: {highS}")
    message.setFill('white')
    message.draw(win)

    
    # name variables
    pc = paper.getAnchor()
    fast = 0
    updater = -1
    r = 50
    g = 0
    b = 0
    while True:
        if bg.getAnchor().getY() < 350:
            bg.move(0, 10)
        # set Values
        coinX = randrange(50, winY-50)
        paperPoint = paper.getAnchor()
        deathZone= paper.getAnchor().getY()
        newC = deathZone
        # updaters
        update(60)
        updater +=1
        # Background Color
        if updater % 10 == 0:
            rgbLis = rgb(r, g, b)
            r = rgbLis[0]
            g = rgbLis[1]
            b = rgbLis[2]
            win.setBackground(color_rgb(r,g,b))
        # Random Movement
        mvUpd = updater % 1001
        if mvUpd > 500:
            paper.move(0.3, 0)
        elif mvUpd < 500:
            paper.move(-0.3, 0)
    
        # controls
        try:
            key = win.checkKey()
        except GraphicsError:
            break
        
            
        # move stuff

        bg.move(-0.1, 0)
        bg1.move(-0.1, 0)
        cloud1.move(-4 - (fast/2), 0)
        
        if Image.testCollision_ImageVsPoint(cloud1, paperPoint):
            update(10)
            break
        elif cloud1.getAnchor().getX() < -100:
            cloud1.undraw()
            cloud1 = Image(Point(winX + 50 ,randrange(50, winY-50)), 'cloud1.png')
            cloud1.draw(win)
            
        paper.move(0, 2.5)
        coin.move(-2 - (fast/2) , 0)
        # control
        if key == 'space':
            if fast < 0.5:
                paper.move(0, -6)
            else:
                paper.move(0, -7.5)
        elif key == 'x':
            win.close()
            quit()
        elif key == 'p':
            paused = Text(Point(winX//2, winY//2), 'PAUSED')
            paused.setSize(30)
            paused.setFill('white')
            paused.draw(win)
            sleep(0.5)
            while True:
                key = win.checkKey()
                if key == 'p':
                    paused.undraw()
                    sleep(0.5)
                    countDown()
                    break
                elif key == 'x':
                    win.close()
                else:
                    sleep(0.1)
        else:
            key = None
                
        # test collisions
        if Image.testCollision_ImageVsImage(coin, paper):
            coin.undraw()
            point += 1
            #print(point)
            coin = Image(Point(winX + 50, coinX), "gold.png")
            coin.draw(win)
            fast += 0.5 # increase dif
            message.setText(f"Score = {point}\nHighest Score: {highS}")
        elif coin.getAnchor().getX() < -100:
            coin.undraw()
            coin = Image(Point(winX + 50, coinX), "gold.png")
            coin.draw(win)
        # trails
        paperXloco = paper.getAnchor().getX()
        if updater % 60 == 0:
            
            trail = Circle(Point(paperXloco - 3, newC), 3)
            trail.setFill("white")
            trail.setWidth(0)
            trail.draw(win)
        trail.move(-5.1 - (fast/4), 0)
        if updater % 60 == 20:
            
            trail1 = Circle(Point(paperXloco-5, newC), 3)
            trail1.setFill("white")
            trail1.setWidth(0)
            trail1.draw(win)
        try:
            trail1.move(-5.1 - (fast/4), 0)
        except UnboundLocalError:
            pass
        if updater % 60 == 40:
            
            trail2 = Circle(Point(paperXloco-9, newC), 3)
            trail2.setFill("white")
            trail2.setWidth(0)
            trail2.draw(win)
        try:
            trail2.move(-5.1 * (1 + fast/4), 0)
        except UnboundLocalError:
            pass
        # death conditions
        if deathZone > winY or deathZone < 0:
            break

        if point > int(highS):
            highscore = open("code6HS.txt", 'w')
            highscore.write(str(point))
        #end of While Statement
        
    

    # death stuff
    highscore.close()
    cloud1.undraw()
    coin.undraw()
    paper.undraw()
    message.undraw()
    try:
        bg.undraw()
    except NameError:
        pass
    try:
        bg1.undraw()
    except NameError:
        pass
    try:
        trail.undraw()
        trail1.undraw()
        trail2.undraw()
    except UnboundLocalError:
        pass

    return [point, int(highS)]

test = 0
while oneT == True:
    menuScr = Image(Point(250, 250), 'paperMenu.png')
    menuScr.draw(win)
    r = 250
    g = 200
    b = 200
    win.setBackground(color_rgb(r,g,b))
    while True:
        click = win.getMouse()
        if checkButton(click, 113, 174, 306, 336):
            # menu animations
            while menuScr.getAnchor().getY() > -200:
                update(500)
                menuScr.move(0,-1)
            # screen fade
            while r > 50:
                update(5000)
                r -= 1
                g -= 1
                b -= 1
                win.setBackground(color_rgb(r,g,b))
                
            
            update(100)
            
            doRetry = True
            while doRetry == True:
                #print(' doing ')
                doRetry = False
                scoreList = game()
                highScore = scoreList[1]
                finalScore = scoreList[0]
                while r < 250:
                        update(5000)
                        r += 1
                        g += 1
                        b += 1
                        win.setBackground(color_rgb(r,g,b))
                
                retryScr = Image(Point(250, -200), 'retryMenu.png')
                retryScr.draw(win)
                while retryScr.getAnchor().getY() < 250:
                    update(500)
                    retryScr.move(0, 1)
                    
                HStext = Text(Point(256.0, 327.0), str(highScore))
                FStext = Text(Point(200.0, 352.0), str(finalScore))
                HStext.setSize(15)
                FStext.setSize(15)
                HStext.setFill(color_rgb(200,100,100))
                FStext.setFill(color_rgb(200,100,100))
                HStext.setFace('times roman')
                FStext.setFace('times roman')
                HStext.draw(win)
                FStext.draw(win)
                while True:
                    click = win.getMouse()
                    #print(click)
                    if checkButton(click, 311, 379, 201, 334):
                        #retrying
                        while r > 50 and g > 0 and b > 0:
                            if r > 50:
                                r-=1
                            if g > 0:
                                g-=1
                            if b > 0:
                                b-=1
                            win.setBackground(color_rgb(r, g, b))
                            update(200)
                        while bg.getAnchor().getY() < 350:
                            bg.move(0, 1)
                            update(100)
                

                            
                        HStext.undraw()
                        FStext.undraw()
                        while retryScr.getAnchor().getY() > -200:
                            update(500)
                            retryScr.move(0, -1)
                        doRetry = True
                        break
                    elif checkButton(click, 301, 364, 343, 369):
                        helpMenu()
                    elif checkButton(click, 288, 350, 380, 410):
                        win.close()
                        quit()
                    
            # reverse screen fade
        elif checkButton(click, 120, 179, 345, 373):
            helpMenu()
            #show menu
        elif checkButton(click, 130, 189, 386, 412):
            win.close()
            quit()

    





    
