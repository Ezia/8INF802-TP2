#!/usr/bin/python3
import math

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

def simpleRngTest(a, b, interationNbr, generator):
    """Test min, max and average value of a generator"""

    minValue = b
    maxValue = a
    sumValues = 0

    for i in range(interationNbr):
        randomNumber = generator.next(a, b)
        minValue = min(minValue, randomNumber)
        maxValue = max(maxValue, randomNumber)
        sumValues = sumValues + randomNumber

    print("minValue = " + str(minValue) + " ; maxValue = " + str(maxValue) 
            + " ; average = " + str(sumValues/interationNbr))

simpleRngTest(-2, 2, 10000, NumericalRecipesGenerator(1))