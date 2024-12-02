from cmu_graphics import *
from main import *
from Classes import *
import random
import heapq
import math
import time

def cloneFaces(faces):
    return {face: [row[:] for row in faceRows] for face, faceRows in faces.items()}

############################## onAppStart ####################################
def onAppStart(app):    
    app.squareSize, app.margin, app.bottonSize, app.bottonMargin, \
    app.solutionDisplayWidth = gameDimensions()  
    app.background = 'black' #rgb(255,204,153)  
    app.colors = {'W': 'white', 'Y': 'yellow', 'R': 'red',      
        'O': 'orange', 'B': 'blue', 'G': 'green' }   
    getMovesAndMaps(app)
    getCubes(app)
    getFlags(app)
    app.solutionMovesCount = 0
    app.solutionSteps = []
    onAppStartSettings(app)
    app.moveHistory = []    
    app.movesBottons = []
    getMoveBottons(app)        
    app.rotateBottons = []
    getRotateBotton(app)    
    app.scrambles = []
    app.topButtons = getTopButtons(app)
    app.LBButtons = getLeftBottomButtons(app)
    app.startTime = 0
    app.passedTime = formatTime(0)

    
def getCubes(app):
    app.cube = Cube(app)
    app.tmpCube = Cube(app)
    app.solvedCube = Cube(app)
    app.orientation = cloneFaces(app.cube.faces)
    app.timerScrambleButton = getNewScrambleButtonTimer(app)

def getFlags(app):
    app.timerSqSize = app.squareSize / 2
    app.timeout = False
    app.is3D = False
    app.showPic = False
    app.solvingStage = 'Cross'
    app.isSolving = False
    app.callSolve = 0  
    app.timerMode = False
    app.isTimerStart = False
    app.timer = 0
    app.timerToggler = 0
    app.sol1Dcount = 0
    app.applyAllSol = False
    app.solAllTimer = 0
    app.timerColor = 'white'
    app.solutionMoves = []
    app.prevMove = ""
    app.clickViolated = False
    
def getMovesAndMaps(app):   
    app.moves = ["U", "U'", "F", "F'", "R", "R'",
                 "D", "D'", "B", "B'", "L", "L'"]
    app.movesGroups = [["R", "R'", "R2"], ["L", "L'", "L2"], ["F", "F'", "F2"],
                   ["B", "B'", "B2"], ["U", "U'", "U2"], ["D", "D'", "D2"],]
    app.movesGroupsDict = {'U': ["U", "U'", "U2"], "D":["D", "D'", "D2"],
                          "R": ["R", "R'", "R2"], "L":["L", "L'", "L2"],
                          "F": ["F", "F'", "F2"], "B":["B", "B'", "B2"]}
    app.movesAndRotations = {
        "U": rotateU, "U'": rotateCounterU,
        "F": rotateF, "F'": rotateCounterF,
        "R": rotateR, "R'": rotateCounterR,
        "D": rotateD, "D'": rotateCounterD,
        "B": rotateB, "B'": rotateCounterB,
        "L": rotateL, "L'": rotateCounterL,
        "X": rotateCubeX, "Y": rotateCubeY,
        "Y'": rotateCubeYPrime, "X'": rotateCubeXPrime
    }
    app.rotations = ['X', 'Y', "Y'", "X'"]
    app.rotated = False


def getTopButtons(app):
    buttons = ["get new scramble", "apply scramble", "reset cube",
               "get solution", "apply 1 move",'apply whole solution', "change view"]
    funcs = [getScramble, applyMoves, resetCube,
             solveButton, applyOneMoveClicked, applySolution, toggle3DView]
    topButtons = []
    xStart = 0
    yStart = 0
    width = app.width // len(buttons)
    for i in range(len(buttons)):
        xBotton = xStart + (width + app.bottonMargin) * i 
        msg = buttons[i]
        func = funcs[i]
        topButtons.append(TopButton(msg, xBotton, yStart, width,
                                    app.squareSize, func))
    return topButtons

def getMoveBottons(app):
    xStart = app.margin
    yStart = 4*app.margin + 9*app.squareSize
    moveIndex = 0
    for row in range(2):
        for col in range(6):
            xBotton = xStart + (app.squareSize + app.bottonMargin)*col
            yBotton = yStart + (app.squareSize + app.bottonMargin)*row
            app.movesBottons.append(Botton(app.moves[moveIndex], xBotton,
                                           yBotton, app.squareSize))
            moveIndex += 1
    
def getRotateBotton(app):
    xStart = 2*app.margin + (app.squareSize + app.bottonMargin)*6 
    yStart = 4*app.margin + 9*app.squareSize
    index = 0
    for row in range(3):
        for col in range(3):
            if (row, col) in [(0,0), (0,2), (1,1), (2,0), (2,2)]:
                continue
            rotation = app.rotations[index]
            xBotton = xStart + (app.squareSize + app.bottonMargin)*col
            yBotton = yStart + (app.squareSize/2 + app.bottonMargin)*row
            if (row, col) == (2, 1):
                yBotton -=  app.bottonMargin
            app.rotateBottons.append(RotateBotton(rotation, xBotton, yBotton,
                                        app.squareSize,
                                        app.movesAndRotations[rotation]))
            index += 1
            
def getLeftBottomButtons(app):
    buttons = ["Moves Notations", "Timer mode"]
    funcs = [toggleMovesNotations, toggleTimerMode]
    xStart = 2*app.margin + (app.squareSize + app.bottonMargin)*10 
    yStart = 4*app.margin + 9*app.squareSize
    width = (app.width - app.margin - xStart) // len(buttons)
    height = 2*app.squareSize
    LBbuttons = []
    for i in range(len(buttons)):
        xBotton = xStart + (width + app.bottonMargin) * i 
        msg = buttons[i]
        func = funcs[i]
        LBbuttons.append(TopButton(msg, xBotton, yStart, width,
                                    height, func))
    return LBbuttons

def getNewScrambleButtonTimer(app):
    xStart = 0.2*app.margin
    yStart = 0
    width = 3*app.squareSize + app.bottonMargin
    height = 2*app.squareSize
    xBotton = 0
    msg = 'get new scramble'
    button = TopButton(msg, xBotton, yStart, width,
                                height, getScrambleTimer)
    return button
            
def solveButton(app):
    print("Solving the cube...")
    app.timeout = False
    app.isSolving = True
    app.callSolve = 1
    app.orientation = cloneFaces(app.cube.faces)
  
    
        
def toggle3DView(app):
    app.is3D = not app.is3D
    if app.is3D:
        setup3DCube(app)
        
def applySolution(app):
    orientCube(app, app.orientation)
    app.applyAllSol = True
        
        
def toggleMovesNotations(app):
    app.showPic = not app.showPic
    
def toggleTimerMode(app):
    app.timerMode = not app.timerMode
    resetCube(app)
    
def getScrambleTimer(app):
    app.scrambles = []
    groupM = app.movesGroupsDict
    moves = groupM['F'] + groupM['B'] + groupM['R'] +\
            groupM['L'] + groupM['U'] + groupM['D']
    prevMove = ''
    for _ in range(10):
        move = random.choice(moves)
        if prevMove != '':
            while groupM[prevMove[0]] == groupM[move[0]]:
                move = random.choice(moves)
        prevMove = move
        app.scrambles.append(move)



############################## solver functions ##############################
def solveCube(app):
    print('Solving cube:')
    tmpFaces = cloneFaces(app.cube.faces)
    app.solutionSteps = []
    funcs = [solveCross, solveF2L, solveOLLCross, solveOLL, solvePLL]
    for func in funcs:
        moves = func(app)
        if moves == None:
            app.timeout = True
            app.cube.faces = tmpFaces
            updateCubes(app)
            return
        if func == solveF2L:
            app.solutionSteps.extend(moves)
        else:
            app.solutionSteps.append(moves)
    app.solutionMovesCount = getMovesCount(app.solutionSteps)
    app.cube.faces = tmpFaces
    updateCubes(app)
    app.isSolving = False
    

def getMovesCount(L):
    # L is a 2d list
    counter = 0
    for moves in L:
        for move in moves:
            counter += 1
    return counter
           
#dijkstra algorithm
def solver(app, startState, statusFunction, isGoalFunction, moves):
    def applyMoveToNeighbor(state, move):
        neighborCube = Cube(app, faces=state.faces)
        for singleMove in move.split(' '):  # handling composite move
            if len(singleMove) == 2 and singleMove[1] == '2':
                turn = app.movesAndRotations[singleMove[0]]
                for _ in range(2):
                    neighborCube.faces = turn(neighborCube.faces)
            elif singleMove in app.movesAndRotations:
                turn = app.movesAndRotations[singleMove]
                neighborCube.faces = turn(neighborCube.faces)
        neighborCube.updatePieces(app)
        return neighborCube

    def stateToString(state):
        return statusFunction(app, state)
    
    startState = startState.clone(app)

    #Priority queue for Dijkstra's algorithm
    priorityQueue = []
    heapq.heappush(priorityQueue, (0, startState))

    #Cost dictionary to track the minimum cost to reach a state
    #cost is number of moves to the certain state
    startStateStr = stateToString(startState)
    costs = {startStateStr: 0}
    comesFromDict = {}
    
    timeStart = time.time()
    while priorityQueue:
        if time.time() - timeStart > app.timeLimit:
            print("It takes too long!!!!!.")
            app.timeout = True
            app.isSolving = False
            return None
        currentCost, currentState = heapq.heappop(priorityQueue)
        currentStateStr = stateToString(currentState)

        #check if the goal for this step is reached
        if isGoalFunction(app, currentState):
            #Reconstruct the path
            path = []
            while currentStateStr in comesFromDict:
                currentStateStr, move = comesFromDict[currentStateStr]
                path.append(move)
                
            splittedPath = []
            for splitted in reversed(path):
                splittedPath += splitted.split(" ")
            return splittedPath  #return the move sequence

        #check neighbors (all possible moves)
        for move in moves:
            neighborState = applyMoveToNeighbor(currentState, move)
            neighborStateStr = stateToString(neighborState)
            newCost = currentCost + len(move.split(' '))
            #if the neighbor state is not visited or we found a cheaper path
            if neighborStateStr not in costs \
               or newCost < costs[neighborStateStr]:
                costs[neighborStateStr] = newCost
                comesFromDict[neighborStateStr] = (currentStateStr, move)
                heapq.heappush(priorityQueue, (newCost, neighborState))
    return []  
     
def solveCross(app):
    print("solving cross")
    group = app.movesGroupsDict
    edges = ["DB", "DL", "DF", "DR"] 
    compositeMoves = ["R U R'", "R' U' R", "L' U' L", "L U L'"]
    specificMoves = [group['D']+group['F']+group['B']+group['R']+group['L'],
                    group['F'] + group['R'] + group['L'],
                    group['F'], group['R'],
                    group['R']]   
    movesUsed = []    
    for i in range(len(edges)):
        edge = edges[i]
        allowedMoves = specificMoves[i] + group['U'] + compositeMoves
        moves = solver(app, app.cube,
            lambda app, state: str(state),  
            lambda app, state: state.isEdgeCorrect(app, edge),  
            allowedMoves)
        print(edge, 'solved', moves)
        if moves == None:
            return
        applyMovesToCube(app, app.cube, moves)
        movesUsed += moves
    return movesUsed


def getF2LMoves(app):
    app.F2LMoves = dict()
    moves = [["L' U L", "F U F'", "L' U' L", "F U' F'"],
             ["R U' R'", "R U R'", "F' U F", "F' U' F"],
             ["L U L'", "L U' L'", "B' U B", "B' U' B"],
             ["R' U R", "R' U' R", "B U' B'", "B U B'"]]
    app.F2LMoves[("DLF", "FL")] = moves[0] + moves[1] 
    app.F2LMoves[("DRF", "RF")] = moves[1]
    app.F2LMoves[("DLB", "LB")] = moves[0] + moves[1] + moves[2] + moves[3]
    app.F2LMoves[("DRB", "BR")] = moves[0] + moves[1] + moves[3]
    
# solve F2l
def solveF2L(app):
    print('solving f2l')
    f2lPairs = [
        ("DLB", "LB"),  # front left pair ("DLF", "FL")
        ("DRB", "BR"),  # front right pair ("DRF", "RF")
        ("DLF", "FL"),  # back left pair ("DLB", "LB")
        ("DRF", "RF"),  # back right pair ("DRB", "BR")
    ]
    getF2LMoves(app)
    movesUsed = []
    for i, (corner, edge) in enumerate(f2lPairs):
        allowedMoves = ["U", "U'", "U2"] + app.F2LMoves[(corner, edge)] 
        def statusFunction(app, state):
            return str(state)
        def isGoalFunction(app, state):
            return state.isCornerCorrect(app, corner) and \
                   state.isEdgeCorrect(app, edge)

        moves = solver(app, app.cube, statusFunction,
                                   isGoalFunction, allowedMoves)
        if moves == None:
            return
        
        applyMovesToCube(app, app.cube, moves)
        print(f"{corner, edge}: {moves}")            
        movesUsed.append(moves)   

    print(f"F2L solved! in {len(movesUsed)} moves")
    return movesUsed

    
def solveOLLCross(app):
    print('solving OLL Cross')
    allowedMoves = ["F R U R' U' R U R' U' F'",  # Dot algorithm
                    "F R U R' U' F'",            # Line algorithm
                    "F U R U' R' F'",            # L algorithm
                    "U", "U'", "U2"              # U face rotations
    ]
    movesUsed = solver(
        app,
        app.cube,
        lambda app, state: str(state),  
        lambda app, state: state.isOLLCrossSolved(app),
        allowedMoves,
    )    
    if movesUsed != None:
        applyMovesToCube(app, app.cube, movesUsed)
        print(f"OLL Cross Solved with {len(movesUsed)} Moves: {movesUsed}")
        
        return movesUsed

def solveOLL(app):
    updateCubes(app)
    print("Solving OLL...")
    if not app.cube.isOLLCrossSolved(app):
        print("OLL cross is not done !!!!")
        return
    
    algsOLL = [
        "R2 D' R U2 R' D R U2 R",
        "R U R D R' U' R D' R2",
        "R' F R B' R' F' R B",
        "R U2 R' U' R U' R'",
        "R U R' U R U2 R'",
        "R U2 R' U' R U R' U' R U' R'",
        "R U2 R2 U' R2 U' R2 U2 R",
    ]
    
    allowedMoves = algsOLL + ["U", "U'", "U2"]  
    
    
    movesUsed = solver(
        app,
        app.cube,
        lambda app, state: str(state),  
        lambda app, state: state.isOLLSolved(app),  
        allowedMoves
    )
    if movesUsed != None:
        applyMovesToCube(app, app.cube, movesUsed)
        print(f"OLL Solved with {len(movesUsed)} Moves: {movesUsed}")
        
        return movesUsed

def solvePLL(app):
    print("Solving PLL...")
    algsPLL = getPLLAlgs()

    allowedMoves = algsPLL + ["U", "U'", "U2"]  # Include U rotations
   
    movesUsed = solver(
        app,
        app.cube,
        lambda app, state: str(state),  
        lambda app, state: state.isCubeSolved(app),  
        allowedMoves)
    if movesUsed != None:
        applyMovesToCube(app, app.cube, movesUsed)
        print(f"PLL Solved with {len(movesUsed)} Moves: {movesUsed}")
        
        return movesUsed

def getPLLAlgs():
    algsPLL = ["X L2 D2 L' U' L D2 L' U L' X'",
        "X' L2 D2 L U L' D2 L U' L X",
        "R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R",
        "R2 U R' U R' U' R U' R2 U' D R' U R D'",
        "R' U' R U D' R2 U R' U R U' R U' R2 D",
        "R2 U' R U' R U R' U R2 U D' R U' R' D",
        "R U R' U' D R2 U' R U' R' U R' U R2 D'",
        "R' U L' U2 R U' R' U2 R L", "R2 F R U R U' R' F' R U2 R' U2 R",
        "R U R' F' R U R' U' R' F R2 U' R'", "R2 U2 R U2 R2 U2 R2 U2 R U2 R2",
        "R U' R' U' R U R D R' U' R D' R' U2 R'",       
        "R U R' U' R' F R2 U' R' U' R U R' F'",
        "X' L' U L D' L' U' L D L' U' L D' L' U L D X",
        "R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'",
        "R' U R U' R' F' U' F R U R' F R' F' R U' R",
        "R' U R' U' Y R' F' R2 U' R' U R' F R F Y'",
        "F R U' R' U' R U R' F' R U R' U' R' F R F'",
        "R2 U R U R' U' R' U' R' U R'", "R U' R U R U R U' R' U' R2",        
        "R' U' R U' R U R U' R' U R U R2 U' R'"]
    return algsPLL

# use X and Y to get the right cube orientation (when clicked the solve button)
def orientCube(app, orientation):
    allowedMoves = ["X", "X'", "Y", "Y'"]
    movesUsed = solver(
        app, app.cube,
        lambda app, state: str(state),  
        lambda app, state: state.isCubeOriented(app, orientation),  
        allowedMoves)
    if movesUsed != None:
        applyMovesToCube(app, app.cube, movesUsed)
    return movesUsed
    

######################## move and rotate #########################
def updateCubes(app):
    app.tmpCube.faces = cloneFaces(app.cube.faces)
    app.cube.updatePieces(app)
    app.tmpCube.updatePieces(app)
    app.solvedCube.updatePieces(app)
        
def rotateClockwise(face):
    rotated = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            rotated[j][2 - i] = face[i][j]
    return rotated

# Rotate a single face counter-clockwise
def rotateCounterClockwise(face):
    rotated = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            rotated[2 - j][i] = face[i][j]
    return rotated

# cube rotation along the X axis
def rotateCubeX(faces):
    newFaces = cloneFaces(faces)

    newFaces['D'] = rotateClockwise(rotateClockwise(faces['B']))
    newFaces['R'] = rotateClockwise(faces['R'])
    newFaces['L'] = rotateCounterClockwise(faces['L'])
    newFaces['B'] = rotateClockwise(rotateClockwise(faces['U']))
    newFaces['U'], newFaces['F'] = faces['F'], faces['D']

    return newFaces

def rotateCubeXPrime(faces):
    for _ in range(3):
        faces = rotateCubeX(faces)
    return faces

# cube rotation along the Y axis
def rotateCubeY(faces):
    newFaces = cloneFaces(faces)

    newFaces['U'] = rotateClockwise(faces['U'])
    newFaces['D'] = rotateCounterClockwise(faces['D'])
    newFaces['L'], newFaces['F'], newFaces['R'], newFaces['B'] = \
        faces['F'], faces['R'], faces['B'], faces['L']

    return newFaces

def rotateCubeYPrime(faces):
    for _ in range(3):
        faces = rotateCubeY(faces)
    return faces

# U face rotation
def rotateU(faces):
    newFaces = cloneFaces(faces)

    newFaces['U'] = rotateClockwise(faces['U'])
    newFaces['F'][0], newFaces['R'][0], newFaces['B'][0], newFaces['L'][0] = \
        faces['R'][0], faces['B'][0], faces['L'][0], faces['F'][0]

    return newFaces

def rotateCounterU(faces):
    newFaces = cloneFaces(faces)

    newFaces['U'] = rotateCounterClockwise(faces['U'])
    newFaces['F'][0], newFaces['L'][0], newFaces['B'][0], newFaces['R'][0] = \
        faces['L'][0], faces['B'][0], faces['R'][0], faces['F'][0]

    return newFaces

# D face rotation
def rotateD(faces):
    newFaces = cloneFaces(faces)

    newFaces['D'] = rotateClockwise(faces['D'])
    newFaces['F'][2], newFaces['L'][2], newFaces['B'][2], newFaces['R'][2] = \
        faces['L'][2], faces['B'][2], faces['R'][2], faces['F'][2]

    return newFaces

def rotateCounterD(faces):
    newFaces = cloneFaces(faces)

    newFaces['D'] = rotateCounterClockwise(faces['D'])
    newFaces['F'][2], newFaces['R'][2], newFaces['B'][2], newFaces['L'][2] = \
        faces['R'][2], faces['B'][2], faces['L'][2], faces['F'][2]

    return newFaces

# F face rotation
def rotateF(faces):
    newFaces = cloneFaces(faces)

    newFaces['F'] = rotateClockwise(faces['F'])
    for i in range(3):
        newFaces['U'][2][i], newFaces['R'][i][0], newFaces['D'][0][2 - i], \
        newFaces['L'][2 - i][2] = faces['L'][2 - i][2], faces['U'][2][i], \
        faces['R'][i][0], faces['D'][0][2 - i]

    return newFaces

def rotateCounterF(faces):
    newFaces = cloneFaces(faces)

    newFaces['F'] = rotateCounterClockwise(faces['F'])
    for i in range(3):
        newFaces['U'][2][i], newFaces['L'][2 - i][2], newFaces['D'][0][2 - i], \
        newFaces['R'][i][0] = faces['R'][i][0], faces['U'][2][i], \
        faces['L'][2 - i][2], faces['D'][0][2 - i]

    return newFaces

# B face rotation
def rotateB(faces):
    newFaces = cloneFaces(faces)

    newFaces['B'] = rotateClockwise(faces['B'])
    for i in range(3):
        newFaces['U'][0][2 - i], newFaces['L'][i][0], newFaces['D'][2][i], \
        newFaces['R'][2 - i][2] = faces['R'][2 - i][2], faces['U'][0][2 - i], \
        faces['L'][i][0], faces['D'][2][i]

    return newFaces

def rotateCounterB(faces):
    newFaces = cloneFaces(faces)

    newFaces['B'] = rotateCounterClockwise(faces['B'])
    for i in range(3):
        newFaces['U'][0][2 - i], newFaces['R'][2 - i][2], newFaces['D'][2][i], \
        newFaces['L'][i][0] = faces['L'][i][0], faces['U'][0][2 - i], \
        faces['R'][2 - i][2], faces['D'][2][i]

    return newFaces

#L face rotation
def rotateL(faces):
    newFaces = cloneFaces(faces)

    newFaces['L'] = rotateClockwise(faces['L'])
    for i in range(3):
        newFaces['U'][i][0], newFaces['F'][i][0], newFaces['D'][i][0],\
        newFaces['B'][2 - i][2] =  faces['B'][2 - i][2], faces['U'][i][0], \
        faces['F'][i][0], faces['D'][i][0]

    return newFaces

def rotateCounterL(faces):
    newFaces = cloneFaces(faces)

    newFaces['L'] = rotateCounterClockwise(faces['L'])
    for i in range(3):
        newFaces['U'][i][0], newFaces['B'][2 - i][2], newFaces['D'][i][0], \
        newFaces['F'][i][0] =  faces['F'][i][0], faces['U'][i][0],\
        faces['B'][2 - i][2], faces['D'][i][0]

    return newFaces

#R face rotation
def rotateR(faces):
    newFaces = cloneFaces(faces)

    newFaces['R'] = rotateClockwise(faces['R'])
    for i in range(3):
        newFaces['U'][i][2], newFaces['B'][2 - i][0], newFaces['D'][i][2],\
        newFaces['F'][i][2] = faces['F'][i][2], faces['U'][i][2],\
        faces['B'][2 - i][0], faces['D'][i][2]

    return newFaces

def rotateCounterR(faces):
    newFaces = cloneFaces(faces)

    newFaces['R'] = rotateCounterClockwise(faces['R'])
    for i in range(3):
        newFaces['U'][i][2], newFaces['F'][i][2], newFaces['D'][i][2], \
        newFaces['B'][2 - i][0] =  faces['B'][2 - i][0], faces['U'][i][2],\
        faces['F'][i][2], faces['D'][i][2]

    return newFaces
        
# random a scramble
def getScramble(app):
    app.scrambles = []
    groupM = app.movesGroupsDict
    moves = groupM['F'] + groupM['B'] + groupM['R'] + groupM['L'] + groupM['U']
    prevMove = ''
    for _ in range(app.lenScrambles):
        move = random.choice(moves)
        if prevMove != '':
            while groupM[prevMove[0]] == groupM[move[0]]:
                move = random.choice(moves)
        prevMove = move
        app.scrambles.append(move)

        
def applyMovesToCube(app, cube, moves):
    if moves is None:
        return cube
    for move in moves:
        for singleMove in move.split(' '):  
            if len(singleMove) == 2 and singleMove[1] == '2':  
                turn = app.movesAndRotations[singleMove[0]]
                for _ in range(2):
                    cube.faces = turn(cube.faces)
            elif singleMove in app.movesAndRotations:  
                turn = app.movesAndRotations[singleMove]
                cube.faces = turn(cube.faces)
    return cube
                   
def applyMoves(app):
    applyMovesToCube(app, app.cube, app.scrambles)
    updateCubes(app)   
        
def resetCube(app):
    originalFaces = {
        'U': [['W'] * 3 for _ in range(3)],  
        'D': [['Y'] * 3 for _ in range(3)],  
        'F': [['G'] * 3 for _ in range(3)],  
        'B': [['B'] * 3 for _ in range(3)],  
        'L': [['O'] * 3 for _ in range(3)],  
        'R': [['R'] * 3 for _ in range(3)]   
        }
    app.solvedCube.faces = cloneFaces(originalFaces)
    app.cube.faces = cloneFaces(originalFaces)
    updateCubes(app)
    
def moves1DList(L):
    res = []
    for moves in L:
        res += moves
    return res

def popFirstMove(L):
    L = [moves[:] for moves in L]
    if len(L) >= 1:
        while len(L[0]) == 0:
            L.pop(0)
        if len(L[0]) >= 1:
            L[0].pop(0)       
    return L

def applyOneMoveClicked(app):
    if not app.rotated:
        orientMoves = orientCube(app, app.orientation)
        applyMovesToCube(app, app.cube, orientMoves)
        updateCubes(app)
    applyOneMove(app)

def applyOneMove(app):
    moves = moves1DList(app.solutionSteps)
    print(moves)
    if moves != []:
        moves = moves1DList(app.solutionSteps)
        nextMove = moves.pop(0)
        if nextMove in ['X', "X'", "Y", "Y'"]:
            app.rotated = True
        app.solutionSteps = popFirstMove(app.solutionSteps)
        applyMovesToCube(app, app.cube, [nextMove])  # Apply the move
        updateCubes(app)
        print(f"Applied move: {nextMove}")
    else:
        app.rotated = False
        print("No more moves.")
        
def formatTime(time):
    hours = int((time // 60) // 60)
    hoursText = f"{hours}:" if hours != 0 else ""
    minutes = int(time // 60) % (60)
    minutesText = f"{minutes:02}:" if minutes != 0 else ""
    seconds = int(time % 60)
    milliseconds = int((time * 1000) % 100)
    return f"{hoursText}{minutesText}{seconds:02}.{milliseconds:02}"

