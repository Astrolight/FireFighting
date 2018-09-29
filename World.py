import numpy as np

from scipy.signal import convolve2d
from scipy.constants import convert_temperature, pi

class TreeCell(object):
    '''
    Class to store the data and functions to act on the data of a single cell
    '''

    AVERAGETREEAGE = 150 # Years

    def __init__(self, init_temp, cellArea):
        self.temprature = init_temp
        self.age = 0 # Minutes

        self.cellArea = cellArea

        self.waterLevel = 0 # In mm of water

    def getWaterLevel(self):
        return self.waterLevel

    def setWaterLevel(self, newWaterLevel):
        self.waterLevel = newWaterLevel

    def step(self, dtime):
        '''
        Simulates the growth of trees

        Parameters
        ----------
        dtime: float
            The ammount of time in minutes to step the simulation
        '''
        self.age += dtime

        raise NotImplementedError

class World(object):
    '''
    Class to store the information of and control the simulation of a forest fire.

    Parameters
    ----------
    size: int or sequence of ints
        Defines the size of the simulation in terms of how many subsections there are

    cellLength: float
        Defines the side length of the tree cells in meters
    '''

    def __init__(self, size, cellLength):
        self.simTime = 0 # Minutes
        self.deltaTime = 0.1 # Minutes
        
        # Sets the world size
        self.worldSize = (size, size)

        # The inital world temprature in centegrade
        self.worldTemp = self.getWorldCurrentTemprature()

        # Creates a 2d list/array of TreeCell objects
        self.world = [[TreeCell(self.worldTemp, cellLength**2) for x in range(size)] for y in range(size)]

    def getWorldTempratureArray(self):
        '''
        Returns an array of tempratures for each cell
        '''
        x = self.worldSize[0]
        y = self.worldSize[1]

        TempratureArray = [[self.world[x][y].temprature for x in range(x)] for y in range(y)]

        return TempratureArray
        
    def setWorldTempratureArray(self, newTempratures):
        '''
        Takes a array the same size as the world and sets each cell to the new temprature
        '''
        xSize = self.worldSize[0]
        ySize = self.worldSize[1]

        for x, y in np.ndindex((xSize,ySize)):
            self.world[x][y].temprature = newTempratures[x][y]

    def getWorldCurrentTemprature(self):
        '''
        Calculates the world base temprature for a perticular day/time
        '''
        # Simplistic modeling of temprature
        JanHigh = 2
        JanLow = -6
        JanAvg = np.mean((JanHigh, JanLow))

        JulHigh = 30
        JulLow = 18
        JulAvg = np.mean((JulHigh, JulLow))

        YearAvg = np.mean((JanAvg, JulAvg))

        dayNumberinYear = self.simTime/60/24

        dayResolutionTemp = (JulAvg - JanAvg)/2 * np.sin(2*pi * dayNumberinYear/365 - pi/2) + YearAvg

        minuteResolutionTemp = (JanHigh - JanLow)*np.sin(self.simTime % (60*24) - pi/2) + dayResolutionTemp

        return minuteResolutionTemp

    def chanceOfRain(self):
        '''
        Returns the chance out of 1 for rain to happen on that day
        '''
        # According to NOAA for dayton at least there are 8 days on avg per month with rain

        return  (8*12)/ 365

    def getWorldWaterArray(self):
        x = self.worldSize[0]
        y = self.worldSize[1]

        WaterArray = [[self.world[x][y].getWaterLevel() for x in range(x)] for y in range(y)]

        return WaterArray

    def setWorldWaterArray(self, newWaterLevels):
        xSize = self.worldSize[0]
        ySize = self.worldSize[1]

        for x, y in np.ndindex((xSize,ySize)):
            self.world[x][y].setWaterLevel(newWaterLevels[x][y])

    def calculateTempratureChanges(self):
        '''
        Calculates the change in temprature for each cell using a 2d convolution
        '''
        tempratureArray = self.getWorldTempratureArray()
        currentWorldTemp = self.getWorldCurrentTemprature()

        tempratureWeights = np.array([[  0,0.2,  0],
                                      [0.2,0.2,0.2],
                                      [  0,0.2,  0]])

        # Makes sure we dont create energy
        assert 1 == np.sum(tempratureWeights)

        newTempratures = convolve2d(in1=tempratureArray, in2=tempratureWeights, mode='same', fillvalue=currentWorldTemp)

        return newTempratures

    def step(self):
        '''
        Steps the simulation by deltaT time.
        Simulates tree growth and other requeired processes. 
        '''
        self.simTime += self.deltaTime

        newTempratures = self.calculateTempratureChanges()
        self.setWorldTempratureArray(newTempratures)

        pass


# For debuging purposes
if __name__=='__main__':
    test=World(6, 1)

    test.getWorldTempratureArray()
    test.getWorldCurrentTemprature()
    test.chanceOfRain()

    test.step()