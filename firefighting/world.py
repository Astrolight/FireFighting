import numpy as np

from .simulation import temprature, biomass

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
        self.simTime = 0 # Hours
        self.deltaTime = 0.1 # Hours
        
        # Sets the world size
        self.worldSize = (size, size)

        # The inital world temprature in centegrade
        self.worldTemp = temprature.getWorldTemprature(self.simTime)

        # Calculates the area in square meters for each cell 
        self.cellArea = cellLength**2

        # Creates a 2d list/array of TreeCell objects
        self.world = {'WaterLevel': np.zeros(self.worldSize),
                      'BiomassAmount': np.zeros(self.worldSize),
                      'DiffTemprature': np.zeros(self.worldSize),
                      'treeAge': np.zeros(self.worldSize)}

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

        # Updates tree age
        self.world['treeAge'][self.world['treeAge'] != 0] += self.deltaTime

        # If the forrest is not currently on fire
        if not self.isOnFire:
            biomass.growUp(self.world['BiomassAmount'], self.world['treeAge'], self.deltaTime)

        # Temprature only changes when on fire
        if self.isOnFire:
            newTempratures = temprature.getWorldTemprature(self.simTime)
            self.setWorldTempratureArray(newTempratures)