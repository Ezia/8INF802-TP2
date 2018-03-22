#!/usr/bin/python3
import tkinter as tk
from enum import Enum
from RandomNumberGenerator import BorlandGenerator, NumericalRecipesGenerator
import math

class WalkType(Enum):
    RANDOM = 'RANDOM'
    NONREVERSING = 'NONREVERSING'
    SELF_AVOIDING = 'SELF_AVOIDING'

class RngType(Enum):
    BORLAND = 'BORDLAND'
    NUMERICAL_RECIPES = 'NUMERICAL_RECIPES'

class Application(tk.Frame):
    def __init__(self, master=None, width=80, height=40):
        tk.Frame.__init__(self, master)

        self.numberSteps = tk.StringVar()
        self.numberSteps.set('10')

        self.width=width
        self.height=height

        # self.array = [[0 for i in range(0, width)] for j in range(0, height)]
        self.startingPosition = (math.floor(width/2), math.floor(height/2))

        self.rngType = tk.StringVar()
        self.rngType.set(RngType.BORLAND)

        self.walkType = tk.StringVar()
        self.walkType.set(WalkType.RANDOM)
        self.seed = tk.StringVar()
        self.seed.set('1337')

        self.grid()
        self.initWidgets()

    def initWidgets(self):

        # initialize canvas
        self.initCanvas()

        # initialize number of steps spinbox
        self.numberStepsLabel = tk.Label(self, text='Number of steps:')
        self.numberStepsLabel.grid(column=0, row=1, pady=8)
        self.numberStepsSpinbox = tk.Spinbox(self, from_=1, to=999, increment=1, textvariable=self.numberSteps)
        self.numberStepsSpinbox.grid(column=0, row=2)

        # initialize radio buttons
        self.randomWalkTypeLabel = tk.Label(self, text='Type of random walk:')
        self.randomWalkTypeLabel.grid(column=1, row=1, pady=8)
        self.randomWalkRadioButton = tk.Radiobutton(self, text='Random walk', variable=self.walkType, value=WalkType.RANDOM)
        self.randomWalkRadioButton.grid(column=1, row=2)
        self.nonreversingWalkRadioButton = tk.Radiobutton(self, text='Nonreversing walk', variable=self.walkType, value=WalkType.NONREVERSING)
        self.nonreversingWalkRadioButton.grid(column=1, row=3)
        self.selfAvoidingWalkRadioButton = tk.Radiobutton(self, text='Self-avoiding walk', variable=self.walkType, value=WalkType.SELF_AVOIDING)
        self.selfAvoidingWalkRadioButton.grid(column=1, row=4)

        # initialize RNG radio buttons and spinbox
        self.rngTypeLabel = tk.Label(self, text='Random number generator:')
        self.rngTypeLabel.grid(column=0, row=5, pady=8)
        self.borlandRngTypeRadioButton = tk.Radiobutton(self, text='Borland generator', variable=self.rngType, value=RngType.BORLAND)
        self.borlandRngTypeRadioButton.grid(column=0, row=6)
        self.numericalRecipesRngTypeRadioButton = tk.Radiobutton(self, text='Numerical recipes generator', variable=self.rngType, value=RngType.NUMERICAL_RECIPES)
        self.numericalRecipesRngTypeRadioButton.grid(column=0, row=7)
        self.seedLabel = tk.Label(self, text='Seed:')
        self.seedLabel.grid(column=0, row=8, pady=8)
        self.seedSpinbox = tk.Spinbox(self, from_=1, to=99999999, increment=1, textvariable=self.seed)
        self.seedSpinbox.grid(column=0, row=9)

        # initialize buttons
        self.runButton = tk.Button(self, text='Run', command=self.runSimulation)
        self.runButton.grid(column=1, row=5, rowspan=5, pady=16)

    def initCanvas(self):
        self.gridInterval = 10
        canvasWidth = self.width * self.gridInterval
        canvasHeight = self.height * self.gridInterval

        self.canvas = tk.Canvas(self, width=canvasWidth, height=canvasHeight)
        self.canvas.grid(column=0, row=0, columnspan=2, padx=16, pady=16)

        for i in range(0, canvasHeight + 1, self.gridInterval):
            self.canvas.create_line(0, i, canvasWidth, i, fill='#bbb')
        for i in range(0, canvasWidth + 1, self.gridInterval):
            self.canvas.create_line(i, 0, i, canvasHeight, fill='#bbb')

    def runSimulation(self):
        self.cleanCanvas()

        if (self.rngType.get() == str(RngType.BORLAND)):
            self.rng = BorlandGenerator(int(self.seed.get()))
        elif (self.rngType.get() == str(RngType.NUMERICAL_RECIPES)):
            self.rng = NumericalRecipesGenerator(int(self.seed.get()))
        else:
            raise ValueError('Unknown RNG type selected')

        if (self.walkType.get() == str(WalkType.RANDOM)):
            self.runRandomWalk()
        elif (self.walkType.get() == str(WalkType.NONREVERSING)):
            self.runNonreversingWalk()
        elif (self.walkType.get() == str(WalkType.SELF_AVOIDING)):
            self.runSelfAvoidingWalk()
        else:
            raise ValueError('Unknown walk type selected')

    def cleanCanvas(self):
        self.canvas.delete('walkRectangle')
    
    def drawMovementLine(self, x0, y0, x1, y1):
        self.canvas.create_line(
            x0 * self.gridInterval + self.gridInterval/2,
            y0 * self.gridInterval + self.gridInterval/2,
            x1 * self.gridInterval + self.gridInterval/2,
            y1 * self.gridInterval + self.gridInterval/2,
            fill='black', tags='walkRectangle')

    def getMovementFromIndex(self, i):
        if (i == 0):
            return (0, 1)
        elif (i == 1):
            return (1, 0)
        elif (i == 2):
            return (0, -1)
        elif (i == 3):
            return (-1, 0)
        else:
            raise ValueError('Wrong index!')

    def runRandomWalk(self):
        currentPosition = self.startingPosition
        for i in range(0, int(self.numberSteps.get())):
            oldPosition = currentPosition
            newPosition = (0, 0)
            while True:
                movement = self.getMovementFromIndex(math.floor(self.rng.next(0, 4)))
                newPosition = (currentPosition[0] + movement[0], currentPosition[1] + movement[1])
                if (newPosition[0] >= 0 and newPosition[0] < self.width and newPosition[1] >= 0 and newPosition[1] < self.height):
                    currentPosition = newPosition
                    break
            self.drawMovementLine(oldPosition[0], oldPosition[1], newPosition[0], newPosition[1])

    def runNonreversingWalk(self):
        pass

    def runSelfAvoidingWalk(self):
        pass

if __name__ == "__main__":
    app = Application()
    app.master.title('Random walk simulator')
    app.master.resizable(False, False)
    app.mainloop()
