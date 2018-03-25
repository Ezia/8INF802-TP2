#!/usr/bin/python3
import tkinter as tk
from enum import Enum
from RandomNumberGenerator import BorlandGenerator, NumericalRecipesGenerator
import math
import time
import csv

class WalkType(Enum):
    RANDOM = 'RANDOM'
    NONREVERSING = 'NONREVERSING'
    SELF_AVOIDING = 'SELF_AVOIDING'

class RngType(Enum):
    BORLAND = 'BORLAND'
    NUMERICAL_RECIPES = 'NUMERICAL_RECIPES'

class Application(tk.Frame):
    def __init__(self, master=None, width=60, height=60, gridIntervalWidth=10):
        tk.Frame.__init__(self, master)

        self.numberSteps = tk.StringVar()
        self.numberSteps.set('10')

        self.width=width
        self.height=height
        self.gridIntervalWidth = gridIntervalWidth

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
        self.numberStepsLabel.grid(column=1, row=0)
        self.numberStepsSpinbox = tk.Spinbox(self, from_=1, to=999, increment=1, textvariable=self.numberSteps)
        self.numberStepsSpinbox.grid(column=2, row=0)

        # initialize radio buttons
        self.randomWalkTypeLabel = tk.Label(self, text='Type of random walk:')
        self.randomWalkTypeLabel.grid(column=1, row=1, rowspan=3)
        self.randomWalkRadioButton = tk.Radiobutton(self, text='Random walk', variable=self.walkType, value=WalkType.RANDOM)
        self.randomWalkRadioButton.grid(column=2, row=1)
        self.nonreversingWalkRadioButton = tk.Radiobutton(self, text='Nonreversing walk', variable=self.walkType, value=WalkType.NONREVERSING)
        self.nonreversingWalkRadioButton.grid(column=2, row=2)
        self.selfAvoidingWalkRadioButton = tk.Radiobutton(self, text='Self-avoiding walk', variable=self.walkType, value=WalkType.SELF_AVOIDING)
        self.selfAvoidingWalkRadioButton.grid(column=2, row=3)

        # initialize RNG radio buttons and spinbox
        self.rngTypeLabel = tk.Label(self, text='Random number generator:')
        self.rngTypeLabel.grid(column=1, row=4, rowspan=2)
        self.borlandRngTypeRadioButton = tk.Radiobutton(self, text='Borland generator', variable=self.rngType, value=RngType.BORLAND)
        self.borlandRngTypeRadioButton.grid(column=2, row=4)
        self.numericalRecipesRngTypeRadioButton = tk.Radiobutton(self, text='Numerical recipes generator', variable=self.rngType, value=RngType.NUMERICAL_RECIPES)
        self.numericalRecipesRngTypeRadioButton.grid(column=2, row=5)
        self.seedLabel = tk.Label(self, text='Seed:')
        self.seedLabel.grid(column=1, row=6)
        self.seedSpinbox = tk.Spinbox(self, from_=1, to=99999999, increment=1, textvariable=self.seed)
        self.seedSpinbox.grid(column=2, row=6)

        # initialize buttons
        self.runButton = tk.Button(self, text='Run', command=self.runSimulation)
        self.runButton.grid(column=1, row=7, pady=16)
        self.runButton = tk.Button(self, text='Run for seeds 1 to 100', command=self.runSimulationMultipleSeeds)
        self.runButton.grid(column=2, row=7, pady=16)

    def initCanvas(self):
        canvasWidth = self.width * self.gridIntervalWidth
        canvasHeight = self.height * self.gridIntervalWidth

        self.canvas = tk.Canvas(self, width=canvasWidth, height=canvasHeight)
        self.canvas.grid(column=0, row=0, rowspan=8, padx=16, pady=16)

        for i in range(0, canvasHeight + 1, self.gridIntervalWidth):
            self.canvas.create_line(0, i, canvasWidth, i, fill='#bbb')
        for i in range(0, canvasWidth + 1, self.gridIntervalWidth):
            self.canvas.create_line(i, 0, i, canvasHeight, fill='#bbb')

    def runSimulation(self, log = False):

        if (log == False):
            self.writer = None

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
            iterationNumber = 0
            maxIterationNumber = 10000
            solutionFound = False
            while (iterationNumber < maxIterationNumber and solutionFound == False):
                solutionFound = self.runSelfAvoidingWalk()
                iterationNumber += 1
            if (solutionFound == False):
                print('No solution found in ' + str(maxIterationNumber) + ' iterations...')
        else:
            raise ValueError('Unknown walk type selected')

    def runSimulationMultipleSeeds(self):

        print("\n\n\n#########################\n# STARTING COMPUTATIONS #\n#########################\n")

        for rng in [RngType.NUMERICAL_RECIPES]: # [RngType.BORLAND, RngType.NUMERICAL_RECIPES]:
            self.rngType.set(str(rng))
            for walkType in [WalkType.SELF_AVOIDING]: # [WalkType.RANDOM, WalkType.NONREVERSING, WalkType.SELF_AVOIDING]:

                self.walkType.set(str(walkType))
                with open(str(rng.value).lower() + '_' + str(walkType.value).lower() + '_simulation_data.csv', 'w') as csv_file:
                    self.writer = csv.writer(csv_file, delimiter=',')
                    self.writer.writerow(['Walk type', 'Number of steps', 'Squared euclidian distance'])
                    
                    for j in range(1, 51):
                        self.numberSteps.set(j)
                        self.subTotalDistance = 0.0
                        for i in range(1, 101):
                            self.seed.set(i)
                            self.runSimulation(True)
                        self.writer.writerow([self.walkType.get(), self.numberSteps.get(), str(self.subTotalDistance / 100.0)])

        print("\n\n\n#######################\n# END OF COMPUTATIONS #\n#######################\n")
                        

    def cleanCanvas(self):
        self.canvas.delete('walkRectangle')
    
    def drawMovementLine(self, x0, y0, x1, y1):
        self.canvas.create_line(
            x0 * self.gridIntervalWidth + self.gridIntervalWidth/2,
            y0 * self.gridIntervalWidth + self.gridIntervalWidth/2,
            x1 * self.gridIntervalWidth + self.gridIntervalWidth/2,
            y1 * self.gridIntervalWidth + self.gridIntervalWidth/2,
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

        x = float(currentPosition[0] - self.startingPosition[0])**2.
        y = float(currentPosition[1] - self.startingPosition[1])**2.
        self.printEuclidianDistance(x, y)
        if (self.writer != None):
            self.subTotalDistance += x + y

    def runNonreversingWalk(self):
        currentPosition = self.startingPosition
        previousMovement = (0, 0)
        for i in range(0, int(self.numberSteps.get())):
            oldPosition = currentPosition
            newPosition = (0, 0)
            while True:
                movement = self.getMovementFromIndex(math.floor(self.rng.next(0, 4)))
                newPosition = (currentPosition[0] + movement[0], currentPosition[1] + movement[1])
                if (newPosition[0] >= 0 
                    and newPosition[0] < self.width
                    and newPosition[1] >= 0
                    and newPosition[1] < self.height
                    and (previousMovement[0] + movement[0] != 0
                        or previousMovement[1] + movement[1] != 0)):
                    currentPosition = newPosition
                    previousMovement = movement
                    break
            self.drawMovementLine(oldPosition[0], oldPosition[1], newPosition[0], newPosition[1])

        x = float(currentPosition[0] - self.startingPosition[0])**2.
        y = float(currentPosition[1] - self.startingPosition[1])**2.
        self.printEuclidianDistance(x, y)
        if (self.writer != None):
            self.subTotalDistance += x + y

    def runSelfAvoidingWalk(self):

        currentPosition = self.startingPosition
        previousMovementIndex = None
        pathArray = [[0 for i in range(0, self.height)] for j in range(0, self.width)]
        pathArray[self.startingPosition[0]][self.startingPosition[1]] = 1
        for i in range(0, int(self.numberSteps.get())):
            oldPosition = currentPosition

            if (i != 0):
                movementIndex = (previousMovementIndex + math.floor(self.rng.next(-1, 2))) % 4
            else:
                movementIndex = math.floor(self.rng.next(0, 4))

            movement = self.getMovementFromIndex(movementIndex)

            newPosition = (currentPosition[0] + movement[0], currentPosition[1] + movement[1])
            if (pathArray[newPosition[0]][newPosition[1]] == 0):
                currentPosition = newPosition
                previousMovementIndex = movementIndex
                pathArray[newPosition[0]][newPosition[1]] = 1
            else:
                self.cleanCanvas()
                return False
            self.drawMovementLine(oldPosition[0], oldPosition[1], newPosition[0], newPosition[1])

        x = float(currentPosition[0] - self.startingPosition[0])**2.
        y = float(currentPosition[1] - self.startingPosition[1])**2.
        self.printEuclidianDistance(x, y)
        if (self.writer != None):
            self.subTotalDistance += x + y
        return True
    
    def printEuclidianDistance(self, x, y):
        print("\nRNG: " + self.rngType.get() + "\nWalk type: " + self.walkType.get() + "\nSeed: " + self.seed.get() + "\nNumber of steps: " + self.numberSteps.get() + "\nSquared euclidian distance: " + str(x + y))

if __name__ == "__main__":
    #app = Application()
    app = Application(None, 130, 130, 5)
    app.master.title('Random walk simulator')
    app.master.resizable(False, False)
    app.mainloop()
