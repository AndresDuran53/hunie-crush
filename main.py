import tkinter as tk
import time
from PIL import Image,ImageTk
import copy
import Objects
import threading
import ThreadsFunc

matrisSize = 8
cellLenght = 60
margin = 3
marginBelow = 50
marginRight = 200

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #Create Canvas
        self.canvas = tk.Canvas(self, width=matrisSize*cellLenght, height=matrisSize*cellLenght, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both")

        self.createLabels()

        self.isMousePressed = False
        self.rows = self.columns = matrisSize
        self.cellwidth = self.cellheight = cellLenght
        self.margin = margin
        #Cells
        self.excludedCells = {}
        self.highlightedCells = []
        self.pressedCell = None
        #Counter
        self.scoreCounter = 0
        self.timerCounter = 0
        self.moveCounter = 0
        #Animations
        self.animationActive = False
        self.animationStep = 0
        self.animationsObjects = []

        self.shouldCheckMatrixBoard = False
        self.executeInterchangeColors = False
        self.step = 1
        self.iconsType = [Objects.TypesSymbols(i).getIcon() for i in range(9)]
        self.icons = [["" for j in range(matrisSize)] for i in range(matrisSize)]

        self.matrixBoard = Objects.MatrixBoard(matrisSize,matrisSize)
        self.matrixBoardNew = copy.deepcopy(self.matrixBoard)
        self.girl = Objects.Girl("Miku",{1:0.5,2:1,3:1,4:1,5:1,6:1,7:2,8:3})

        self.createTimers()

        #mouse motion
        self.canvas.bind('<Motion>', self.mousePosition)
        #mouseclick event
        self.canvas.bind("<Button 1>",self.mousePressed)
        #mouseRelease event
        self.canvas.bind('<ButtonRelease-1>', self.mouseRelease)

        self.rect = {}
        self.drawGirlInfo()
        self.redraw(10)

    def createLabels(self):
        #Create Label Score
        self.scoreLabel = tk.Label(self, text='Score: ', font=('MS Sans Serif',15), fg='white', borderwidth=0)
        self.scoreLabel.place(x=15, y=matrisSize*cellLenght+10)

        #Create Move Score
        self.moveLabel = tk.Label(self, text='Moves: ', font=('MS Sans Serif',15), fg='white', borderwidth=0)
        self.moveLabel.place(x=200, y=matrisSize*cellLenght+10)


        #Create Label Time
        self.timeLabel = tk.Label(self, text='Time: 00:00', font=('MS Sans Serif',15), fg='white', borderwidth=0)
        self.timeLabel.place(x=380, y=matrisSize*cellLenght+10)

        #Create Label Name Girl
        self.girlNameLabel = tk.Label(self, text='Girl', font=('MS Sans Serif',20), fg='white', borderwidth=0)
        self.girlNameLabel.place(x=matrisSize*cellLenght+10, y=20)

        #Create Label Favorite Color
        self.girlLikeLabel = tk.Label(self, text='Like: ', font=('MS Sans Serif',12), fg='white', borderwidth=0)
        self.girlLikeLabel.place(x=matrisSize*cellLenght+10, y=60)

        #Create Label Hated Color
        self.girlDislikeLabel = tk.Label(self, text='Dislike', font=('MS Sans Serif',12), fg='white', borderwidth=0)
        self.girlDislikeLabel.place(x=matrisSize*cellLenght+10, y=80)

    def drawMatrix(self,matrixBoard):
        for column in range(matrisSize):
            for row in range(matrisSize):
                colorOfCell = matrixBoard.getCell(column,row).color
                iconNameOfCell = matrixBoard.getCell(column,row).typesSymbol.getImageName()
                #print("iconOfCell:",iconOfCell)
                outlineColor = ''
                outlineWidth = 0
                value = (column,row)
                if(len(list(self.excludedCells.keys()))>0 and self.excludedCells.get(value)!=None):
                    lista = self.excludedCells.get(value)
                    colorOfCell,outlineColor,outlineWidth = lista[0]
                elif(self.isCoordPressed(column,row)):
                    outlineColor = 'white'
                    outlineWidth = self.margin*1.5
                elif(self.isHighLighted(column,row)):
                    outlineColor = '#aaaaaa'
                    outlineWidth = self.margin
                self.redrawCell([column,row,colorOfCell,outlineColor,outlineWidth,iconNameOfCell])

    def excludeSpecificCell(self,listArgs):
        coords = listArgs[0]
        listArgs = listArgs[1:]
        self.excludedCells[coords]=listArgs

    def redrawCell(self,listArgs):
        column = listArgs[0]
        row = listArgs[1]
        colorOfCell = listArgs[2]
        outlineColor = listArgs[3]
        outlineWidth = listArgs[4]
        x1 = (column*self.cellwidth) + self.margin
        y1 = (row * self.cellheight) + self.margin
        x2 = (x1 + self.cellwidth) - self.margin
        y2 = (y1 + self.cellheight) - self.margin
        self.rect[column,row] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#333", tags="rect",outline=outlineColor,width=outlineWidth)

        if(len(listArgs)>5):
            iconNameOfCell = listArgs[5]
            for iconType in self.iconsType:
                if(iconType.name == iconNameOfCell):
                    self.icons[column][row] = iconType.image
                    self.canvas.create_image(x1+(self.cellwidth/2), y1+(self.cellwidth/2), image=self.icons[column][row], anchor="center")

    def drawGirlInfo(self):
        self.girlNameLabel['text'] = self.girl.name
        self.girlLikeLabel['text'] = "Like: "+Objects.TypesSymbols(8).name
        self.girlDislikeLabel['text'] = "Dislike: "+Objects.TypesSymbols(1).name

    def drawLabels(self):
        self.scoreLabel['text'] = f"Score: {str(self.scoreCounter)}"
        self.moveLabel['text'] = f"Moves: {str(self.moveCounter)}"

    def redraw(self, delay):
        self.canvas.delete("all")
        self.drawMatrix(self.matrixBoard)
        self.drawLabels()
        self.after(delay, lambda: self.redraw(delay))

    def showAnimation(self):
        if(len(self.animationsObjects)>0):
            self.shouldCheckMatrixBoard = False
            for animation in self.animationsObjects:
                animationIndex = self.animationsObjects.index(animation)
                again = animation.execute()
                if not(again):
                    animation.endAnimation()
                    self.animationsObjects.pop(animationIndex)
            self.animationStep+=1
        else:
            self.matrixBoard = copy.deepcopy(self.matrixBoardNew)
            self.shouldCheckMatrixBoard = True

    def updateTimeLabel(self):
        self.timeLabel['text'] = f"Time: {str(format(self.timerCounter//60, '02d'))}:{str(format(self.timerCounter%60, '02d'))}"
        self.timerCounter+=1

    def isCoordPressed(self,x,y):
        return self.pressedCell == (x,y)


    def isHighLighted(self,column,row):
        return self.highlightedCells.count((column,row))>0


    def highlightStraightLines(self,coordsBase):
        for column in range(matrisSize):
            for row in range(matrisSize):
                if(column == coordsBase[0] or row ==coordsBase[1]):
                    self.highlightedCells.append((column,row))

    def mousePosition(self,event):
        x, y = event.x, event.y
        if(not self.isMousePressed):
            self.highlightedCells = []
            self.highlightedCells.append(self.getCellFromCoord(x,y))
        return (x,y)

    def mousePressed(self, eventorigin):
        coord1 = self.getorigin(eventorigin)
        self.pressedCell = self.getCellFromCoord(coord1[0],coord1[1])
        self.isMousePressed = True
        self.highlightStraightLines(self.pressedCell)

    def mouseRelease(self, eventorigin):
        coord2 = self.getorigin(eventorigin)
        self.releasedCell = self.getCellFromCoord(coord2[0],coord2[1])
        self.isMousePressed = False
        self.interchangeColors(self.pressedCell,self.releasedCell)

    def getorigin(self, eventorigin):
        x = eventorigin.x
        y = eventorigin.y
        return (x,y)

    def getCellFromCoord(self,x,y):
        nColumn = x//cellLenght
        nRow = y//cellLenght
        return (nColumn,nRow)


    def interchangeColors(self,coord1,coord2):
        colorMoved = self.matrixBoard.moveColors(coord1,coord2)
        if(colorMoved):
            self.matrixBoardNew = copy.deepcopy(self.matrixBoard)
            self.moveCounter = self.moveCounter +1
        else:
            pass
        self.highlightedCells = []
        self.pressedCell = None

    def createRemoveAnimation(self,repetitiveFounded):
        listKeys = list(repetitiveFounded.keys())
        for key in listKeys:
            for coord in repetitiveFounded[key]:
                cellSymbol = self.matrixBoard.getCell(coord[0],coord[1])
                newAnimationObject = Objects.AnimationObject(self.excludeSpecificCell,
                                    [coord,[cellSymbol.color,"#DDDDDD",self.margin*1.5]],
                                    self.excludedCells.pop,coord,
                                    0.5)
                self.animationsObjects.append(newAnimationObject)
                self.animationActive = True

    def getScoreByType(self,type,list,girl):
        pointsEach = Objects.ScoreCalculator.getPointsEachFromGirl(type,girl)
        total = pointsEach * len(list)
        return total

    def getTotalScore(self,repetitiveFounded):
        totalScore = 0
        listKeys = list(repetitiveFounded.keys())
        for key in listKeys:
            parcialScore = self.getScoreByType(key,repetitiveFounded[key],self.girl)
            totalScore += parcialScore
        return totalScore

    def checkMatrixBoardRepetitive(self):
        if(self.shouldCheckMatrixBoard):
            repetitiveFounded = Objects.MatrixBoard.checkMatrix(self.matrixBoard.cells)
            if(len(list(repetitiveFounded.keys()))>0):
                self.scoreCounter += self.getTotalScore(repetitiveFounded)
                #Create animation
                self.createRemoveAnimation(repetitiveFounded)
                blankFieldsMatrix = Objects.MatrixBoard.newMatrixBlankRepetitive(self.matrixBoard.cells,repetitiveFounded)
                #AuxMatrix = copy(self.matrixBoard)
                #AuxMatrix.cells = blankFieldsMatrix
                self.matrixBoardNew.cells = copy.deepcopy(Objects.MatrixBoard.newMatrixFillBlankCoords(blankFieldsMatrix))
                #self.matrixBoard.cells = Objects.MatrixBoard.newMatrixFillBlankCoords(blankFieldsMatrix)

    def createTimers(self):
        #Timer Thread
        self.threadTimerEventStopper = threading.Event()
        self.threadTimer = ThreadsFunc.CustomThreads(1,self.updateTimeLabel,self.threadTimerEventStopper)
        self.threadTimer.start()

        #Animation Thread
        self.threadAnimationEventStopper = threading.Event()
        self.threadAnimation = ThreadsFunc.CustomThreads(0.01,self.showAnimation,self.threadAnimationEventStopper)
        self.threadAnimation.start()
        #self.threadAnimation.set()
        #self.threadAnimation.clear()

        #Check Matrix Thread
        self.threadCheckMatrixEventStopper = threading.Event()
        self.threadCheckMatrix = ThreadsFunc.CustomThreads(0.1,self.checkMatrixBoardRepetitive,self.threadCheckMatrixEventStopper)
        self.threadCheckMatrix.start()


if __name__ == "__main__":
    app = App()
    app.geometry(f"{matrisSize*cellLenght+marginRight}x{matrisSize*cellLenght+marginBelow}+{'150'}+{'150'}")
    app.mainloop()
