import numpy as np

from scipy.constants import convert_temperature, pi

class TreeCell(object):
    '''
    Class to store the data and functions to act on the data of a single cell
    '''

    AVERAGETREEAGE = 150 # Years

    def __init__(self, init_temp):
        self.temprature = init_temp
        self.age = 0 # Minutes

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
    '''

    def __init__(self, size):
        self.simTime = 0 # Minutes
        self.deltaTime = 0.1 # Minutes
        
        # Sets the world size
        self.worldSize = (size, size)

        # The inital world temprature in centegrade
        self.worldTemp = 25

        # Creates a 2d list/array of TreeCell objects
        self.world = [[TreeCell(self.worldTemp) for x in range(size)] for y in range(size)]

    def getWorldTempratureArray(self):
        x = self.worldSize[0]
        y = self.worldSize[1]

        TempratureArray = [[self.world[x][y].temprature for x in range(x)] for y in range(y)]

        return TempratureArray
        
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

    def step(self):
        '''
        Steps the simulation by deltaT time.
        Simulates tree growth and other requeired processes. 
        '''
        raise NotImplementedError


# For debuging purposes
if __name__=='__main__':
    test=World(6)

    test.getWorldTempratureArray()
    test.getWorldCurrentTemprature()
    test.chanceOfRain()