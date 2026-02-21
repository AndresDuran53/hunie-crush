from enum import Enum
from PIL import Image,ImageTk
import copy
import random

class MatrixBoard:
    cells = []
    girl = None

    def __init__(self,columnSize,rowSize):
        self.columnSize = columnSize
        self.rowSize = rowSize
        self.cells = MatrixBoard.createNewMatrixCells(columnSize,rowSize)

    @staticmethod
    def fromMatrix(self,cells):
        self.columnSize = columnSize
        self.rowSize = rowSize
        self.cells = MatrixBoard.createNewMatrixCells(columnSize,rowSize)

    @staticmethod
    def createNewMatrixCells(columnSize,rowSize):
        newCells=[]
        for column in range(columnSize):
            newCells.append([])
            for row in range(rowSize):
                newSymbol = MatrixBoard.createRandomSymbol()
                newCells[column].append(newSymbol)
        repetitiveFounded = MatrixBoard.checkMatrix(newCells)
        while(len(list(repetitiveFounded.keys()))!=0):
            listKeys = list(repetitiveFounded.keys())
            for key in listKeys:
                for coordAux in repetitiveFounded[key]:
                    change = random.randint(0,2)
                    if(change==0): newCells[coordAux[0]][coordAux[1]] = MatrixBoard.createRandomSymbol()
            repetitiveFounded = MatrixBoard.checkMatrix(newCells)
        return newCells

    def changeCell(self,column,row,newType):
        newSymbol = Symbol(newType)
        #Validate Diferrent Symbol
        if(newSymbol.type != self.cells[column][row].type):
            self.cells[column][row] = newSymbol
            print("Movement")
        else:
            print("Same Type")

    def getCell(self,column,row):
        return self.cells[column][row]

    def moveColors(self,coord1,coord2):
        cellTypeStart = self.getCell(coord1[0],coord1[1])
        cellTypeEnd = self.getCell(coord2[0],coord2[1])

        #Check If is Same Type
        if(cellTypeStart.type == cellTypeEnd.type):
            print("Cannot be the same type of block")
            return False
        #Check if is a Straight Line
        if(not self.isStraightLine(coord1,coord2)):
            print("Must be a movement on a straight line")
            return False
        #Check If is One Block Away
        if(not self.isOneBlockAway(coord1,coord2)):
            print("Needs to be one block away")
            return False
        
        #is Vertical Movement
        if(coord1[0]==coord2[0]):
            matrixToModify = self.cells
            cellAux = coord1[0]
            startCell = coord1[1]
            endCell = coord2[1]
            transposeCells = False
        #is Horizontal Movement
        else:
            matrixToModify = MatrixBoard.transposeMatrix(self.cells)
            cellAux = coord1[1]
            startCell = coord1[0]
            endCell = coord2[0]
            transposeCells = True

        self.executeMoveCells(matrixToModify,cellAux,startCell,endCell,transposeCells)
        print("Movement Success")
        return True
    
    def isStraightLine(self,coord1,coord2):
        if(coord1[0]==coord2[0] or coord1[1]==coord2[1]):
            return True
        return False
    
    def isOneBlockAway(self,coord1,coord2):
        if(abs(coord1[0]-coord2[0])==1 or abs(coord1[1]-coord2[1])==1):
            return True
        return False
    
    def executeMoveCells(self,cellsMatrix,columnIndex,startRow,endRow,transpose = False):
        valeAux = cellsMatrix[columnIndex].pop(startRow)
        cellsMatrix[columnIndex].insert(endRow,valeAux)
        if(transpose): self.cells = MatrixBoard.transposeMatrix(cellsMatrix)
        else: self.cells = cellsMatrix
    
    @staticmethod
    def createRandomSymbol():
        randValue = random.randint(1,8)
        newSymbol = Symbol(randValue)
        return newSymbol

    @staticmethod
    def transposeMatrix(matrix):
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

    @staticmethod
    def transposeCell(cell):
        return (cell[1],cell[0])

    @staticmethod
    def newMatrixFillBlankCoords(matrix):
        transposeCells = copy.deepcopy(matrix)
        for columnI in range(len(transposeCells)):
            for rowI in range(len(transposeCells[columnI])):
                if(transposeCells[columnI][rowI].typesSymbol==TypesSymbols.Blank):
                    transposeCells[columnI].pop(rowI)
                    transposeCells[columnI].insert(0,MatrixBoard.createRandomSymbol())
        return transposeCells

    @staticmethod
    def newMatrixBlankRepetitive(matrix,repetitiveFounded):
        blankRepetitiveMatrix = copy.deepcopy(matrix)
        listKeys = list(repetitiveFounded.keys())
        for key in listKeys:
            for coordAux in repetitiveFounded[key]:
                blankRepetitiveMatrix[coordAux[0]][coordAux[1]] = Symbol(0)
        return blankRepetitiveMatrix

    @staticmethod
    def checkMatrix(matrix):
        repetitiveCells = {}
        #Check Rows
        for column in range(len(matrix)):
            repetitiveFounded = MatrixBoard.checkRows(column,matrix)
            if(len(list(repetitiveFounded.keys()))>0):
                for key in list(repetitiveFounded.keys()):
                    repetitiveCells[key]=repetitiveFounded[key]
        #Check Columns Using chekcRows transosing matrix
        for row in range(len(matrix[0])):
            transposeCells = MatrixBoard.transposeMatrix(matrix)
            repetitiveFounded = MatrixBoard.checkRows(row,transposeCells)
            if(len(list(repetitiveFounded.keys()))>0):
                for key in list(repetitiveFounded.keys()):
                    repetitiveFoundedFixed = []
                    for cell in repetitiveFounded[key]:
                        cellAux = MatrixBoard.transposeCell(cell)
                        repetitiveFoundedFixed.append(cellAux)
                    repetitiveCells[key]=repetitiveFoundedFixed
        return repetitiveCells

    @staticmethod
    def checkRows(column,pMatrix):
        matrix = copy.deepcopy(pMatrix)
        repetitiveFounded = {}
        for row in range(len(matrix[0])):
            testingType = matrix[column][row].type
            if(repetitiveFounded.get(testingType)!=None and repetitiveFounded.get(testingType).count((column,row))>0):
                continue
            repetitiveFoundedPivote = [(column,row)]
            for rowPivote in range(row+1,len(matrix[0])):
                newType = matrix[column][rowPivote].type
                if(testingType == newType):
                    repetitiveFoundedPivote.append((column,rowPivote))
                    row = rowPivote
                else:
                    break
            if(len(repetitiveFoundedPivote)>2):
                if(repetitiveFounded.get(testingType)==None):
                    repetitiveFounded[testingType]=repetitiveFoundedPivote
                else:
                    repetitiveFounded[testingType]+=repetitiveFoundedPivote
        return repetitiveFounded


class Symbol:
    type = 0
    typesSymbol = None
    color = "#000000"

    def __init__(self,type):
        self.type = type
        self.typesSymbol = TypesSymbols(type)
        self.color = self.typesSymbol.getColor()

class TypesSymbols(Enum):
    Blank = 0
    Red = 1
    Green = 2
    Blue = 3
    Purple = 4
    Yellow = 5
    Orange = 6
    LightBlue = 7
    Pink = 8

    def getColor(self):
        if(self == TypesSymbols.Red):
            return "#b72a2a"
        elif(self == TypesSymbols.Green):
            return "#50dc50"
        elif(self == TypesSymbols.Blue):
            return "#3268cd"
        elif(self == TypesSymbols.Purple):
            return "#7832cd"
        elif(self == TypesSymbols.Yellow):
            return "#cbc743"
        elif(self == TypesSymbols.Orange):
            return "#ce8240"
        elif(self == TypesSymbols.LightBlue):
            return "#40b2ce"
        elif(self == TypesSymbols.Pink):
            return "#d3557f"
        elif(self == TypesSymbols.Blank):
            return "#DDDDDD"
        else:
            return "#333333"

    def getImageName(self):
        if(self == TypesSymbols.Red):
            return "fire"
        elif(self == TypesSymbols.Green):
            return "star"
        elif(self == TypesSymbols.Blue):
            return "note"
        elif(self == TypesSymbols.Purple):
            return "broken-heart"
        elif(self == TypesSymbols.Yellow):
            return "bell"
        elif(self == TypesSymbols.Orange):
            return "moon"
        elif(self == TypesSymbols.LightBlue):
            return "drop"
        elif(self == TypesSymbols.Pink):
            return "heart"
        else:
            return ""

    def getIcon(self):
        name = self.getImageName()
        iconV = Icon("PNG",name,TypesSymbols.loadIcon(name))
        return iconV

    @staticmethod
    def loadIcon(iconName):
        if(iconName==""): return ""
        img = (Image.open(f"src/{iconName}.png"))
        resizedImage = img.resize((50,50), Image.LANCZOS)
        imgResult = ImageTk.PhotoImage(resizedImage)
        return imgResult



class Girl:
    name = ""
    symbolValues = {}

    def __init__(self,name,symbolValues):
        self.name = name
        self.symbolValues = symbolValues


class ScoreCalculator():

    @staticmethod
    def getPointsEachFromGirl(type,girl):
        basePointsEach = 20
        weight = girl.symbolValues[type]
        points = basePointsEach*weight
        return points


class AnimationObject():
    func = None
    args = []
    steps = 0
    maxSteps = 1

    def __init__(self,func,args,endFunc,endArgs,secondsDelay):
        self.func = func
        self.args = args
        self.endFunc = endFunc
        self.endArgs = endArgs
        self.maxSteps = secondsDelay/0.01

    def execute(self):
        if(self.steps<=self.maxSteps):
            self.func(self.args)
            self.steps+=1
            return True
        return False

    def endAnimation(self):
        self.endFunc(self.endArgs)

class Icon():
    type = "PNG"
    name = ""
    image = None

    def __init__(self,type,name,image):
        self.type = type
        self.name = name
        self.image = image
