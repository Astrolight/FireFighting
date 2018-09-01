import numba
import numpy as np

class World(object):

    def __init__(self, Size):
        self.simTime = 0
        self.deltaTime = 0.1 # Seconds

        if ~isinstance(Size, tuple):
            # Sets up for Size to be the dims of a 2D matrix
            Size = (Size,Size)

        # Matrixes contaning world data
        self.tempratureMatrix = np.ones(Size)

# For debuging purposes
if __name__=='__main__':
    test=World(6)

    pass