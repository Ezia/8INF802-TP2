#!/usr/bin/python3
import math
from decimal import *

getcontext().prec = 2

class RandomNumberGenerator:
    """A linear congruential generator"""

    def __init__(self, modulus, multiplier, increment, seed, firstBit, lastBit):
        self.modulus = modulus
        self.multiplier = multiplier
        self.increment = increment
        self.seed = seed

        self.firstBit = firstBit
        self.lastBit = lastBit

        # Compute the bit mask according to the first and last bits
        self.mask = (1 << (lastBit + 1)) - 1 - ((1 << firstBit) - 1) 
    
    def next(self, a, b):
        """Get the next random number whithin range [a, b[ (a included, b excluded)"""

        # Compute next number in the series
        self.seed = (self.multiplier * self.seed + self.increment) % self.modulus
        
        # return the projection of the number in the interval ]a, b[
        return (((self.seed & self.mask) >> self.firstBit) * (b - a) / ((self.modulus-1 & self.mask) >> self.firstBit)) + a

class BordlandGenerator(RandomNumberGenerator):
    def __init__(self, seed):
        RandomNumberGenerator.__init__(self, 2**32, 22695477, 1, seed, 16, 30)

class NumericalRecipesGenerator(RandomNumberGenerator):
    def __init__(self, seed):
        RandomNumberGenerator.__init__(self, 2**32, 1664525, 1013904223, seed, 0, 31)

def simpleRngTest(a, b, iterationNbr, generator):
    """Test min, max and average value of a generator"""

    minValue = b
    maxValue = a
    sumValues = 0

    for i in range(iterationNbr):
        randomNumber = generator.next(a, b)
        minValue = min(minValue, randomNumber)
        maxValue = max(maxValue, randomNumber)
        sumValues = sumValues + randomNumber

    print("param : minValue = " + str(a) + " ; maxValue = " + str(b) 
            + " ; iteration number = " + str(iterationNbr))
    print("results : minValue = " + str(minValue) + " ; maxValue = " + str(maxValue) 
            + " ; average = " + str(sumValues/iterationNbr))

def diceTest(iterationNbr):
    generator = BordlandGenerator(6)

    # expected sum probability from 2 to 12
    expectedProba = [1/36, 1/18, 1/12, 1/9, 5/36, 1/6, 5/36, 1/9, 1/12, 1/18, 1/36]

    # empirical sum statistics from 2 to 12
    empiricalStat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Run dice throw
    for i in range(iterationNbr):
        index = int((generator.next(1, 7)) + int(generator.next(1, 7)))-2
        empiricalStat[index] = empiricalStat[index] + 1
    
    # Compute statistics

    # Khi 2 statistic with 11 categories
    T1 = 0
    for i in range(11):
        # empirical statistics
        empiricalStat[i] = empiricalStat[i] / iterationNbr
        # Compute khi 2 statistic
        T1 = T1 + (iterationNbr * empiricalStat[i] - iterationNbr * expectedProba[i])**2/(iterationNbr * expectedProba[i]) 

    # Khi 2 statistic with {2, 3} and {11, 12} values gathered (9 categories)
    T2 = 0
    T2 = T2 + (iterationNbr * (empiricalStat[0]+empiricalStat[1]) - iterationNbr * (expectedProba[0]+expectedProba[1]))**2/(iterationNbr * (expectedProba[0]+expectedProba[1])) 
    T2 = T2 + (iterationNbr * (empiricalStat[9]+empiricalStat[10]) - iterationNbr * (expectedProba[9]+expectedProba[10]))**2/(iterationNbr * (expectedProba[9]+expectedProba[10])) 
    for i in range(2, 9):
        T2 = T2 + (iterationNbr * empiricalStat[i] - iterationNbr * expectedProba[i])**2/(iterationNbr * expectedProba[i]) 

    print("expected probabilities : " + str(["%.4f" % e for e in expectedProba]))
    print("empirical statistics :   " + str(["%.4f" % e for e in empiricalStat]))
    print("khi 2 statistic : " + str(T1) + " ||| khi 2 law with 5% risk of degree 10 = " + str(18.31))
    print("khi 2 statistic (gathered extremities) : " + str(T2) + " ||| khi 2 law with 5% risk of degree 8 = " + str(15.51))


#simpleRngTest(-2, 2, 10000, NumericalRecipesGenerator(1))
diceTest(1000)