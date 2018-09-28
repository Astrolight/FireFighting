import numpy as np

from scipy.constants import convert_temperature

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
        raise NotImplementedError

    def chanceOfRain(self):
        '''
        Returns the chance out of 1 for rain to happen on that day
        '''
        raise NotImplementedError

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