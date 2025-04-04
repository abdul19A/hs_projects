# Abdulrahman Abusharbain
# Period 4
# 5/6/24

# This game is a platformer with many mechanics you can find!
# Run this file!
# Please make sure you have the original Graphics file!


from BecomeCubeCharacters import *
from BecomeCubeTerrainCreator import *

def main():
    win = GraphWin('Become Cube - Version 1.0', 600, 500, autoflush=False)
    win.setBackground('white')
    Terrain.doMenu(win)
    curlvl = Terrain(level=0, window=win)
    player = Player(win, spawn=curlvl.spawn)
    developerMode = False
    while not win.closed:
        # inputs
        if developerMode:
            mouse = win.checkMouse()
            if mouse:
                player.doTeleport(mouse)
                print(mouse)

        # player and level update
        player.allowMovement(win.checkKeys())
        nextLvl = player.checkWinLevel(curlvl.lvl)
        curlvl.doMovinglvlEvent(perf_counter())
        if nextLvl:
            curlvl = curlvl.nextLevel(nextLvl)
            if curlvl is None:
                break
            player.nextLevel(curlvl)
            curlvl.doStaticlvlEvent()
        player.checkHitDanger()
        update(100)
    player.undraw()
    Terrain.endGame(win)
    update()
    input()

# checks if this is the main file
if __name__ == '__main__':
    main()
