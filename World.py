import numpy as np

from scipy.signal import convolve2d
from scipy.constants import convert_temperature, pi, R as Ideal_Gas_Constant


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

        # Calculates the area in square meters for each cell 
        self.cellArea = cellLength**2

        # Creates a 2d list/array of TreeCell objects
        self.world = {'WaterLevel': np.zeros(self.worldSize),
                      'BiomassAmount': np.zeros(self.worldSize),
                      'DiffTemprature': np.zeros(self.worldSize)}

        self.isOnFire = True #!: Make sure you change this back to default later!

    #* Functions to deal with temprature
    def getWorldTempratureArray(self):
        '''
        Returns an array of tempratures for each cell
        '''
        return self.world['DiffTemprature']
        
    def setWorldTempratureArray(self, newTempratures):
        '''
        Takes a array the same size as the world and sets each cell to the new temprature
        '''
        self.world['DiffTemprature'] = newTempratures

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

    def calculateTempratureChanges(self):
        '''
        Calculates the change in temprature for each cell using a 2d convolution
        '''
        tempratureArray = self.getWorldTempratureArray()

        tempratureWeights = np.array([[0.05,0.05,0.05],
                                      [0.05,0.6 ,0.05],
                                      [0.05,0.05,0.05]])

        # Makes sure we dont create energy
        assert 1 == np.sum(tempratureWeights)

        newTempratures = convolve2d(in1=tempratureArray, in2=tempratureWeights, mode='same')

        return newTempratures

    #* Functions to deal with water
    def chanceOfRain(self):
        '''
        Returns the chance out of 1 for rain to happen on that day
        '''
        # According to NOAA for dayton at least there are 8 days on avg per month with rain

        return  (8*12)/ 365

    def getWorldWaterArray(self):
        return self.world['WaterLevel']

    def setWorldWaterArray(self, newWaterLevels):
        self.world['WaterLevel'] = newWaterLevels

    #* Functions to deal with the simulation itself
    def step(self):
        '''
        Steps the simulation by deltaT time.
        Simulates tree growth and other requeired processes. 
        '''
        self.simTime += self.deltaTime

        # Temprature only changes when on fire
        if self.isOnFire:
            newTempratures = self.calculateTempratureChanges()
            self.setWorldTempratureArray(newTempratures)

        pass


# For debuging purposes
if __name__=='__main__':
    test=World(6, 1)

    test.getWorldTempratureArray()
    a1 = test.getWorldCurrentTemprature()
    test.chanceOfRain()

    test.step()