#!/usr/bin/python3


##### RNG #####


class RandomNumberGenerator:
    """A linear congruential generator with bit selection"""

    def __init__(self, name, modulus, multiplier, increment, seed, firstBit, lastBit):
        self.name = name
        self.modulus = modulus
        self.multiplier = multiplier
        self.increment = increment
        self.seed = seed

        self.firstBit = firstBit
        self.lastBit = lastBit

        # Compute the bit mask according to the first and last bits
        self.mask = (1 << (lastBit + 1)) - 1 - ((1 << firstBit) - 1) 

        # Compute the upper bound of the masked numbers (exclusive)
        self.upperBound = (min(self.mask, modulus - 1) >> self.firstBit) + 1

    def next(self, a, b):
        """Get the next random number within range [a, b[ (a included, b excluded)"""

        # Compute next number in the series
        self.seed = (self.multiplier * self.seed + self.increment) % self.modulus
        
        # Compute the projection of the number in the interval [a, b[
        # Select bits between firstBit and lastBit (inclusive), then scale and add offset
        return ((self.seed & self.mask) >> self.firstBit) * (b - a) / self.upperBound + a

class BorlandGenerator(RandomNumberGenerator):
    def __init__(self, seed):
        RandomNumberGenerator.__init__(self, "Borland C/C++", 2**32, 22695477, 1, seed, 16, 30)

class NumericalRecipesGenerator(RandomNumberGenerator):
    def __init__(self, seed):
        RandomNumberGenerator.__init__(self, "Numerical Recipies", 2**32, 1664525, 1013904223, seed, 0, 31)


##### TESTS #####


def simpleRngTest(a, b, iterationNbr, generator):
    """Test min, max and average values of a generator"""

    # Execute test

    minValue = b
    maxValue = a
    sumValues = 0
    for i in range(iterationNbr):
        randomNumber = generator.next(a, b)
        minValue = min(minValue, randomNumber)
        maxValue = max(maxValue, randomNumber)
        sumValues = sumValues + randomNumber

    # Print

    print("-----------------------------SIMPLE TEST-----------------------------")
    print("RNG parameters : min (inclusive) = " + str(a) + " ; max (exclusive) = " + str(b) 
            + " ; iteration number = " + str(iterationNbr))
    print("results : minValue = " + str(minValue) + " ; maxValue = " + str(maxValue) 
            + " ; average = " + str(sumValues/iterationNbr))

def diceTest(iterationNbr, generator):
    """Throw 2 dice and add their values"""

    print("-----------------------------DICE TEST-----------------------------")
    print("generator and seed : " + generator.name + " ; " + str(generator.seed))

    # expected sum probability from 2 to 12
    expectedProba = [1/36, 1/18, 1/12, 1/9, 5/36, 1/6, 5/36, 1/9, 1/12, 1/18, 1/36]

    # empirical sum statistics from 2 to 12
    empiricalStat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Execute test
    
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

    # Print
    
    if (T1 >= 18.31):
        print("!!!!!!!!!!!!!!!!!! KHI 2 NOT PASSED !!!!!!!!!!!!!!!!!!")
        print("expected probabilities : " + str(["%.4f" % e for e in expectedProba]))
        print("empirical statistics :   " + str(["%.4f" % e for e in empiricalStat]))
        print("khi 2 statistic : " + str(T1) + " ##### khi 2 law of degree 10 with 5% risk = " + str(18.31))
        print("khi 2 statistic (gathered extremities) : " + str(T2) + " ##### khi 2 law of degree 8 with 5% risk = " + str(15.51))
    else:
        print("khi 2 OK")


##### EXECUTION #####

if __name__ == "__main__":
    for i in range(1, 101):
        diceTest(1000,NumericalRecipesGenerator(i))