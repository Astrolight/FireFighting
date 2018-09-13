import numba
import numpy as np

class TreeCell(object):
    '''
    Class to store the data and functions to act on the data of a single cell
    '''

    AVERAGETREEAGE = 150 # Years

    def __init__(self):
        pass

    def step(self):
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
        self.simTime = 0
        self.deltaTime = 0.1 # Seconds

        if ~isinstance(size, tuple):
            # Sets up for size to be the dims of a 2D matrix
            size = (size,size)

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

    pass