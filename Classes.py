from cmu_graphics import *

class Cube:
    def __init__(self, app, state=None, faces=None):
        self.faceNames = ['U', 'L', 'F', 'R', 'B', 'D']
        self.cornerNames = ['ULF', 'URF', 'ULB', 'URB',
                            'DLF', 'DRF','DLB', 'DRB']
        self.edgeNames = ['UF', 'UR', 'UB', 'UL', 'FL', 'RF', 'BR', 'LB',
                          'DF', 'DR', 'DB', 'DL']
        self.corners = dict()
        self.edges = dict()

        if faces is not None:
            self.faces = {face: [row[:] for row in faces[face]] for face in self.faceNames}
        else:
            self.faces = {'U': [['W'] * 3 for _ in range(3)],
                          'D': [['Y'] * 3 for _ in range(3)],
                          'F': [['G'] * 3 for _ in range(3)],
                          'B': [['B'] * 3 for _ in range(3)],
                          'L': [['O'] * 3 for _ in range(3)],
                          'R': [['R'] * 3 for _ in range(3)]}
            if state:
                self.stateToCube(state)

        self.updatePieces(app)

    def __repr__(self):
        msg = ''
        for face in self.faceNames:
            for r in self.faces[face]:
                for color in r:
                    msg += color
        return msg    
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __lt__(self, other):
        return str(self) < str(other)

    def clone(self, app):
        return Cube(app, faces=self.faces)
    
    def stateToCube(self, state):

        for i, face in enumerate(self.faceNames):
            start = i * 9
            end = start + 9
            flatFace = state[start:end]
            
            # Convert the flat string into a 3x3 grid for the face
            self.faces[face] = []
            for row in range(3):
                rowData = []
                for col in range(3):
                    rowData.append(flatFace[row * 3 + col])
                self.faces[face].append(rowData)
            
        
    def updatePieces(self, app):
        self.updateCorners(app)
        self.updateEdges(app)
        
        
    def updateCorners(self, app):
        self.corners['ULF'] = [self.faces['U'][2][0],self.faces['L'][0][2],
                               self.faces['F'][0][0]]
        self.corners['URF'] = [self.faces['U'][2][2],self.faces['R'][0][0],
                               self.faces['F'][0][2]]
        self.corners['ULB'] = [self.faces['U'][0][0],self.faces['L'][0][0],
                               self.faces['B'][0][2]]
        self.corners['URB'] = [self.faces['U'][0][2],self.faces['R'][0][2],
                               self.faces['B'][0][0]]
        self.corners['DLF'] = [self.faces['D'][0][0],self.faces['L'][2][2],
                               self.faces['F'][2][0]]
        self.corners['DRF'] = [self.faces['D'][0][2],self.faces['R'][2][0],
                               self.faces['F'][2][2]]
        self.corners['DLB'] = [self.faces['D'][2][0],self.faces['L'][2][0],
                               self.faces['B'][2][2]]
        self.corners['DRB'] = [self.faces['D'][2][2],self.faces['R'][2][2],
                               self.faces['B'][2][0]]

        
    def updateEdges(self, app):
        self.edges['UF'] = [self.faces['U'][2][1], self.faces['F'][0][1]]
        self.edges['UR'] = [self.faces['U'][1][2], self.faces['R'][0][1]]
        self.edges['UB'] = [self.faces['U'][0][1], self.faces['B'][0][1]]
        self.edges['UL'] = [self.faces['U'][1][0], self.faces['L'][0][1]]
        self.edges['FL'] = [self.faces['F'][1][0], self.faces['L'][1][2]]
        self.edges['RF'] = [self.faces['R'][1][0], self.faces['F'][1][2]]
        self.edges['BR'] = [self.faces['B'][1][0], self.faces['R'][1][2]]
        self.edges['LB'] = [self.faces['L'][1][0], self.faces['B'][1][2]]
        self.edges['DF'] = [self.faces['D'][0][1], self.faces['F'][2][1]]
        self.edges['DR'] = [self.faces['D'][1][2], self.faces['R'][2][1]]
        self.edges['DB'] = [self.faces['D'][2][1], self.faces['B'][2][1]]
        self.edges['DL'] = [self.faces['D'][1][0], self.faces['L'][2][1]]
        
    #check if the color is in the corner
    #return (True or Flase, string of a facing of the color in that cornor)
    def isColorInCorner(self, app, color, corner):
        self.updatePieces(app)
        for i in range(3):
            if color == self.corners[corner][i]:
                return (True, self.corners[corner][i])
        return False
    
    
    #check if the color is in the edge
    #return (True or Flase, string of a facing of the color in that edge)
    def isColorInEdge(self, app, color, edge):
        self.updatePieces(app)
        for i in range(2):
            if color == self.edges[edge][i]:
                return (True, self.edges[edge][i])
        return False
    
    #check if the corner is in the right place (all faces are correct)
    #return boolean
    def isCornerCorrect(self, app, corner):
        self.updatePieces(app)
        for i in range(3):
            if self.corners[corner][i] != app.solvedCube.corners[corner][i]:
                return False
        return True
    
    #check if the edge is in the right place (all faces are correct)
    #return boolean
    def isEdgeCorrect(self, app, edge):
        self.updatePieces(app)
        for i in range(2):
            if self.edges[edge][i] != app.solvedCube.edges[edge][i]:
                return False
        return True
    
    #return string of cross
    def statusCross(self, app):
        edges = ['DF', 'DR', 'DB', 'DL']
        msg = ''
        for edge in edges:
            msg += ''.join(self.edges[edge])
        return msg
    
    #return string of F2L
    def statusF2L1(self, app):
        self.updateEdges(app)
        msg = ''
        msg += self.statusCross(app)
        edges = ['FL', 'RF', 'BR', 'LB']
        for edge in edges:
            msg += ''.join(self.edges[edge])
        corners = ['DLF', 'DLB', 'DRF', 'DRB']
        for corner in corners:
            msg += ''.join(self.corners[corner])                
        return msg
        
    
    #check if cross is done
    def isCrossSolved(self, app):
        self.updateEdges(app)
        edges = ['DF', 'DR', 'DB', 'DL']
        for edge in edges:
            if not self.isEdgeCorrect(app, edge):
                return False
        return True
    
    #check FR pair
    def isPair1Solved(self, app):
        return self.isEdgeCorrect(app, 'RF') and self.isCornerCorrect(app, 'DRF')
    
    #check FL pair
    def isPair2Solved(self, app):
        return self.isEdgeCorrect(app, 'FL') and self.isCornerCorrect(app, 'DLF')
    
    #check BR pair
    def isPair3Solved(self, app):
        return self.isEdgeCorrect(app, 'BR') and self.isCornerCorrect(app, 'DRB')
    
    #check LB pair
    def isPair4Solved(self, app):
        return self.isEdgeCorrect(app, 'LB') and self.isCornerCorrect(app, 'DLB')

    
    #check if F2L is done
    def isF2LSolved(self, app):
        if not self.isCrossSolved(app):
            return False
        a = self.isPair1Solved(app)
        b = self.isPair2Solved(app)
        c = self.isPair3Solved(app)
        d = self.isPair4Solved(app)
        return a and b and c and d
    
    #check if oll cross is done
    def isOLLCrossSolved(self, app):
        self.updateEdges(app)
        colorU = self.faces['U'][1][1]
#         edges = [self.edges['UF'][0], self.edges['UR'][0],  
#                  self.edges['UB'][0], self.edges['UL'][0]]
        edges = [self.faces['U'][0][1], self.faces['U'][1][0],
                 self.faces['U'][1][2], self.faces['U'][2][1]]
        for color in edges:
            if color != colorU:
                return False
        return True
    
    #check if OLL is done
    def isOLLSolved(self, app):
        self.updateEdges(app)
        colorU = self.faces['U'][1][1]
        for row in self.faces['U']:
            for color in row:
                if color != colorU:
                    return False
        return True
                    
    #check if the cube is solved        
    def isCubeSolved(self, app):
        self.updatePieces(app)
        return self == app.solvedCube
    
    def isCubeOriented(self, app, faces):
        self.updatePieces(app)
        colorU = self.faces['U'][1][1]
        colorF = self.faces['F'][1][1]
        if colorU == faces['U'][1][1] and colorF == faces['F'][1][1]:
            return True
        return False
        
    

class Botton:
    def __init__(self, move, x, y, size, height=0):
        self.x = x
        self.y = y
        self.move = move
        self.width = size
        if height != 0:
            self.height = height
        else:
            self.height = size
        self.color = 'white'
        
    def inSquare(self, mouseX, mouseY):
        inX = self.x < mouseX < self.x + self.width
        inY = self.y < mouseY < self.y + self.height
        if inX and inY:
            return True
        else:
            return False
    
    def draw(self, border=None):
        drawRect(self.x, self.y, self.width, self.height,
                 fill=self.color, border=border)
        midX = self.x + self.width/2
        midY = self.y + self.height/2
        drawLabel(self.move, midX, midY)
        
    def __repr__(self):
        msg1 = f"(txt={self.move}, x={self.x}, y={self.y}"
        msg2 = f", w={self.width}, h={self.height})"
        return msg1 + msg2
         
class RotateBotton(Botton):
    def __init__(self, move, x, y, size, rotation):
        super().__init__(move, x, y, size, size)
        self.rotation = rotation
            
    def rotate(self):
        self.rotation(app)
        
class TopButton(Botton):
    def __init__(self, msg, x, y, width, height, func):
        super().__init__(msg, x, y, width, height)
        self.func = func
            
    def function(self):
        self.func(app)
        
