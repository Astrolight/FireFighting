import numba
import numpy as np

class World(object):
    '''
    Class to store the information of and control the simulation of a forest fire.

    Parameters
    ----------
    size: int or sequence of ints
        Defines the size of the simulation in terms of how many subsections there are
    '''

    AVERAGETREEAGE = 150 # Years

    def __init__(self, size):
        self.simTime = 0
        self.deltaTime = 0.1 # Seconds

        if ~isinstance(size, tuple):
            # Sets up for size to be the dims of a 2D matrix
            size = (size,size)

        # Matrixes contaning world data
        self.tempratureMatrix = np.ones(size)
        self.waterLevelMatrix = np.ones(size)
        self.biomassMatrix = np.ones(size)
        self.treeAgeMatrix = np.ones(size)

    def getWorldCurrentTemprature(self):
        '''
        Calculates the world base temprature for a perticular day/time
        '''
        NotImplementedError

    def chanceOfRain(self):
        '''
        Returns the chance out of 1 for rain to happen on that day
        '''
        NotImplementedError


# For debuging purposes
if __name__=='__main__':
    test=World(6)

    pass