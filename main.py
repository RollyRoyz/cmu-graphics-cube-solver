from cmu_graphics import *
from Classes import *
from functions import *
import random
import heapq
import math
import time


def onAppStartSettings(app):
    # for changing some settings
    app.lenScrambles = 6  # change scrmble moves count here
    app.timeLimit = 120  # time limit for each stage (in seconds)
                              
############################ mouse funtions ################################# 
def onMousePress(app, x, y):
    updateCubes(app)
    grey = rgb(185, 185, 185)
    if not app.timerMode:
        clickMovesButtons(app, x, y, grey)
        clickRotateButtons(app, x, y, grey)
        clickTopButtons(app, x, y, grey)
    else:
        clickScrambleTimerButton(app, x, y, grey)
        
    clickLBButtons(app, x, y, grey)
    
             
def clickMovesButtons(app, x, y, color):
    if app.applyAllSol:
        app.clickViolated = True
        return
    for button in app.movesBottons:
        if button.inSquare(x, y):
            button.color = color
            move = app.movesAndRotations[button.move]
            app.cube.faces = move(app.cube.faces)
            
def clickRotateButtons(app, x, y, color):
    if app.applyAllSol:
        app.clickViolated = True
        return
    for button in app.rotateBottons:
        if button.inSquare(x, y):
            button.color = color
            move = app.movesAndRotations[button.move]
            app.cube.faces = move(app.cube.faces)
            app.solvedCube.faces = move(app.solvedCube.faces)
            
def clickTopButtons(app, x, y, color):
    for button in app.topButtons:
        if button.inSquare(x, y):
            button.color = color
            func = button.func
            func(app)
        
            
def clickLBButtons(app, x, y, color):
    for button in app.LBButtons:
        if button.inSquare(x, y):
            button.color = color
            func = button.func
            if func == toggleTimerMode:
                app.scrambles = []
                app.passedTime = formatTime(0)
                app.isTimerStart = False 
            func(app)
        
def clickScrambleTimerButton(app, x, y, color):
    if app.timerScrambleButton.inSquare(x,y):
        app.timerScrambleButton.color = color
        getScrambleTimer(app)
        resetCube(app)
        applyMovesToCube(app, app.cube, app.scrambles)
        
        
        
def onMouseRelease(app, mouseX, mouseY):
    updateCubes(app)
    #change the color back
    for botton in app.movesBottons:
        botton.color = 'white'
    for botton in app.rotateBottons:
        botton.color = 'white'
    for botton in app.topButtons:
        botton.color = 'white'
    for botton in app.LBButtons:
        botton.color = 'white'
    app.timerScrambleButton.color = 'white'
                            
                            
############################## key press and hold #############################
def onKeyPress(app, key):
    updateCubes(app)
    if not app.timerMode:
        if key == 'u':
            app.cube.faces = rotateU(app.cube.faces)
        elif key == 'i':
            app.cube.faces = rotateCounterU(app.cube.faces)
        elif key == 'd':
            app.cube.faces = rotateD(app.cube.faces)
        elif key == 's':
            app.cube.faces = rotateCounterD(app.cube.faces)
        elif key == 'f':
            app.cube.faces = rotateF(app.cube.faces)
        elif key == 'g':
            app.cube.faces = rotateCounterF(app.cube.faces)
        elif key == 'b':
            app.cube.faces = rotateB(app.cube.faces)
        elif key == 'n':
            app.cube.faces = rotateCounterB(app.cube.faces)
        elif key == 'l':
            app.cube.faces = rotateL(app.cube.faces)
        elif key == 'k':
            app.cube.faces = rotateCounterL(app.cube.faces)
        elif key == 'r':
            app.cube.faces = rotateR(app.cube.faces)
        elif key == 't':
            app.cube.faces = rotateCounterR(app.cube.faces)
        elif key == 'x':
            app.cube.faces = rotateCubeX(app.cube.faces)
        elif key == 'y':
            app.cube.faces = rotateCubeY(app.cube.faces)
        elif key == 'z':
            app.cube.faces = rotateCubeXPrime(app.cube.faces)
        elif key == 'q':
            app.cube.faces = rotateCubeYPrime(app.cube.faces)

        
def onKeyHold(app, keys):
    # for starting the timer
    if 'space' in keys:
        if not app.isTimerStart:          
            app.timerToggler += 1
            #every half second
            if app.timerToggler > (app.stepsPerSecond // 2):
                app.timerColor = 'green'            
            else:
                app.timerColor = 'red'
        else:
            app.isTimerStart = False
            app.timerToggler = 0
            now = time.time()
            app.passedTime = now - app.startTime
            app.passedTime = formatTime(app.passedTime)
            

def onKeyRelease(app, key):
    if app.timerColor == 'green':
        app.startTime = time.time()
        #app.passedTime = 0
        app.isTimerStart = True
    app.timerColor = 'white'
    
############################## draw funtions ##################################
def redrawAll(app):
    if not app.timerMode:
        if app.is3D:
            draw3DCube(app)
        else:
            drawCube(app)
        drawMoveBottons(app)
        drawRotateCubeBottons(app)
        drawScrambles(app)
        drawTopButtons(app)
    
        if not app.isSolving:
            if not app.timeout:
                drawSolution(app)
            else:
                drawTimeout(app)
        else:
            drawIsSolving(app)
    elif app.timerMode:
        drawCubeTimer(app)
        drawtimerScramble(app)
        app.timerScrambleButton.draw(border='black')
        drawTimer(app)
    drawLBButtons(app)
    drawCubeNotations(app)

def drawCube(app):
    facePositions = {'U': (app.margin + 3*app.squareSize, 3*app.margin-2),
        'F': (app.margin + 3*app.squareSize, 3*app.margin + 3*app.squareSize),
        'L': (app.margin-2, 3*app.margin + 3*app.squareSize),
        'R': (app.margin+2+ 6*app.squareSize, 3*app.margin + 3*app.squareSize),
        'B': (app.margin+4+ 9*app.squareSize, 3*app.margin + 3*app.squareSize),
        'D': (app.margin+ 3*app.squareSize, 3*app.margin + 6*app.squareSize+2)}    
    for face, pos in facePositions.items():
        xStart, yStart = pos
        counter = 0
        for row in range(3):
            for col in range(3):                
                if counter % 9 == 0:
                    xStart, yStart = xStart + 1, yStart + 1
                color = app.colors[app.cube.faces[face][row][col]]
                xSquare = xStart + col * app.squareSize
                ySquare = yStart + row * app.squareSize
                drawRect(xSquare, ySquare, app.squareSize, app.squareSize,
                         fill=color, border='black')
                counter += 1
                
def drawCubeTimer(app):
    y, sq = 9.6 * app.margin, app.timerSqSize
    facePositions = {'U': (2*app.margin + 3 * sq, y + sq-1),
        'F': (2*app.margin + 3 * sq, y + 4 * sq),
        'L': (2*app.margin-1, y + 4 * sq),
        'R': (2*app.margin+1 + 6 * sq, y + 4 * sq),
        'B': (2*app.margin+2 + 9 * sq, y + 4 * sq),
        'D': (2*app.margin + 3 * sq, y + 7 * sq+1)}

    # Draw each face of the cube in timer mode
    for face, pos in facePositions.items():
        xStart, yStart = pos
        for row in range(3):
            for col in range(3):
                color = app.colors[app.cube.faces[face][row][col]]
                xSquare = xStart + col * sq
                ySquare = yStart + row * sq
                drawRect(xSquare, ySquare, sq, sq,
                         fill=color, border='black')
    
def drawtimerScramble(app):
    drawRect(0,0,app.width,2*app.squareSize,fill='white',border='black')
    midX = app.width - (9*app.squareSize + app.bottonMargin) 
    midY = app.squareSize
    msg = "  ".join(app.scrambles)
    if app.scrambles != []:
        drawLabel(msg, midX, midY, size=15)

                                
def drawMoveBottons(app):
    for botton in app.movesBottons:
        botton.draw()
        
def drawRotateCubeBottons(app):
    for rotation in app.rotateBottons:
        rotation.draw()
        
def drawTopButtons(app):
    for button in app.topButtons:
        button.draw()
        
def drawLBButtons(app):
    for button in app.LBButtons:
        button.draw()
        
def drawScrambles(app):
    width = app.width//len(app.topButtons)
    #x = 3*(width + app.bottonMargin)/2
    x = 0.025*app.width
    scramblesTxt = ' '.join(app.scrambles)
    drawLabel("Scramble: " + scramblesTxt, x, 3/2*app.margin,
              fill='white', size=20, align='left')
    
def drawSolution(app):
    xStart = 20 + app.margin + 12 * app.squareSize +app.solutionDisplayWidth/2
    yStart = app.margin + 10
    lineHeight = 20
    drawLabel("Solution", xStart, yStart, size=16, fill='white')
    yStart += lineHeight
    drawLabel(f"{app.solutionMovesCount} moves", xStart, yStart, size=16,
              fill='white')
    yStart += lineHeight

    for moves in app.solutionSteps:
        if moves == []:
            continue
        movesText = " ".join(moves)
        yStart += lineHeight      
        drawLabel(movesText, xStart, yStart, size=13, fill='white')
        
def drawTimer(app):
    time = f"{app.timer:.2f}"
    x = app.width//2
    y = app.height//2-30
    drawLabel(app.passedTime, x, y,
              size=45, fill=app.timerColor)
    msg = 'Hold SPACE BAR To Start The Timer'
    drawLabel(msg, x, y+50, size=17, fill='white')
        
def drawTimeout(app):
    if app.timeout:
        xStart = app.margin + 12*app.squareSize + app.solutionDisplayWidth/2
        yStart = app.margin
        msg = "Timeout: Exceeded time limit"
        drawLabel(msg, xStart, yStart+10, size=16, fill="red", bold=True)
        msg2 = 'Try new scramble'
        drawLabel(msg2, xStart, yStart+30, size=16, fill="red", bold=True)
        
def drawIsSolving(app):
    xStart = app.margin + 12*app.squareSize + app.solutionDisplayWidth/2
    yStart = app.margin + 30
    msg = "Finding Solution"
    drawLabel(msg, xStart, yStart, size=16, fill="white", bold=True)
        
# points of 3 corners of 3d cube
def setup3DCube(app):
    app.faces3D = [
        [(61, 116), (206, 190), (202, 359), (57, 285)],  
        [(198, 41), (343, 115), (206, 190), (61, 116)],  
        [(206, 190), (343, 115), (339, 284), (202, 359)]  
    ]

    app.faces3D = moveDots(app.faces3D, 57, 41, 100, 150)
    
    app.grids3D = [create3x3Grid(corners) for corners in app.faces3D]
    app.polygons3D = [draw3x3Squares(grid) for grid in app.grids3D]
    
# moving the dots
def moveDots(L, minX, minY, startX, startY):
    res = []
    for i, face in enumerate(L):
        res.append([])
        for x, y in face:
            newX = startX + x - minX
            newY = startY + y - minY
            res[i].append((newX, newY))
    return res

def linspace(start, end, n):
    step = (end - start) / n
    return [start + i * step for i in range(n + 1)]

# linspace for coordinate (x,y)
def coordsLin(a, b, n):
    x1, y1 = a
    x2, y2 = b
    xs = linspace(x1, x2, n)
    ys = linspace(y1, y2, n)
    return list(zip(xs, ys))

#generate 4x4 grid
def create3x3Grid(corners):
    topLeft, topRight, bottomRight, bottomLeft = corners
    leftEdge = coordsLin(topLeft, bottomLeft, 3)
    rightEdge = coordsLin(topRight, bottomRight, 3)
    return [coordsLin(leftEdge[i], rightEdge[i], 3) for i in range(4)]

def draw3x3Squares(grid):
    return [(grid[row][col], grid[row][col + 1], grid[row + 1][col + 1],
             grid[row + 1][col])for row in range(3) for col in range(3)]

def draw3DCube(app):
    faceColors = {'F': 'green', 'U': 'white', 'R': 'red'}  
    faceMapping = ['F', 'U', 'R']  

    for faceIndex, polygons in enumerate(app.polygons3D):
        face = faceMapping[faceIndex]
        for polygonIndex, polygon in enumerate(polygons):
            xys = [coord for point in polygon for coord in point]
            row = polygonIndex // 3
            col = polygonIndex % 3
            color = app.colors[app.cube.faces[face][row][col]]
            drawPolygon(*xys, fill=color, border="black")
            
def drawCubeNotations(app):
    if app.showPic:
        # from https://www.cubelelo.com/blogs/cubing/cool-3x3-cube-patterns
        url = 'cubeNotations.png'
        drawImage(url, 120, 150)
    
    
################################## on step #################################
def onStep(app):
    if app.isTimerStart and app.timerMode:
        now = time.time()
        app.passedTime = now - app.startTime
        app.passedTime = formatTime(app.passedTime)
        app.timer += 1/app.stepsPerSecond
    app.sol1Dcount = 0
    # flag to apply all solution moves
    if app.applyAllSol and not app.timerMode:
        app.solAllTimer += 1
        if app.solAllTimer % (app.stepsPerSecond//2) == 0:
            #orientCube(app, app.orientation)
            if moves1DList(app.solutionSteps) != []:
                applyOneMove(app)
                updateCubes(app)
            else:
                app.applyAllSol = False
                app.solAllTimer = 0
    # flag to solve the cube
    if app.callSolve == 2 and not app.timerMode:
        app.solutionMoves = solveCube(app)
        app.callSolve = 0
        app.isSolving = False
    if app.callSolve == 1:
        app.callSolve = 2

def cube():
    squareSize, margin, bottonSize, bottonMargin, solutionDisplayWidth = \
                gameDimensions()
    width = 2 * margin + 12 * squareSize + solutionDisplayWidth
    height = 5 * margin + 9 * squareSize + 2 * bottonSize + bottonMargin
    runApp(width=width, height=height)
    
def gameDimensions():
    squareSize = 40
    margin = 50
    bottonSize = 50
    bottonMargin = 2
    solutionDisplayWidth = 250  
    return (squareSize, margin, bottonSize, bottonMargin, solutionDisplayWidth)
        
if __name__ == '__main__':
    cube()
















