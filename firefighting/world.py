import numpy as np

from .simulation import temprature, biomass

import h5py
import time
import os.path

class World(object):
    '''
    Class to store the information of and control the simulation of a forest fire.

    Parameters
    ----------
    size: int or sequence of ints
        Defines the size of the simulation in terms of how many subsections there are

    cellLength: float
        Defines the side length of the tree cells in meters

    save_file_name: string
        Defines the hdf5 file name to be used when saving the simulation state
        If 'Default', the current iso time will be used
    '''

    def __init__(self, size, save_file_name='Default'):
        self.simTime = 0  # Hours
        self.deltaTime = 1  # Hours

        # Sets the world size
        self.worldSize = (size, size)

        # The inital world temprature in centegrade
        self.worldTemp = temprature.getWorldTemprature(self.simTime)

        # Creates a 2d list/array of TreeCell objects
        self.world = {'WaterLevel': np.zeros(self.worldSize),
                      'BiomassAmount': np.zeros(self.worldSize),
                      'DiffTemprature': np.zeros(self.worldSize),
                      'treeAge': np.zeros(self.worldSize)}

        self.isOnFire = False

        # Stuff for creating h5 file
        if save_file_name=='Default':
            # Returns the current time in ISO 8601 UTC Format (yyyyMMddTHHmmssZ)
            # yyyy=year, MM=month, dd=day, HH=hour (24H), mm=minute, ss=second, Z means UTC (Zero offset)
            self.save_file_name = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
        else:
            self.save_file_name = save_file_name

        self.fp = None
        self.__create_h5__()

    def initRandomBiomass(self):
        '''
        Generates a random ammount of biomass and age
        '''

        randomAges = 120*365*24*np.random.random_sample(self.worldSize)

        randomBiomass = 14385*np.random.random_sample(self.worldSize)

        self.world['treeAge'] = randomAges

        self.world['BiomassAmount'] = biomass.growUp(
            randomBiomass, randomAges, 24 * self.deltaTime)

    # * Functions to deal with temprature
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

    def getInfo(self):
        '''
        Returns
        -------
        out: dict
            Contains information on the current state of the simulation
        '''

        Info = {
            'simTime': self.simTime,
            'worldSize': self.worldSize,
            'worldTemp': self.worldTemp,
            'worldData': self.world
        }

        return Info

    # * Functions to deal with the simulation itself
    def step(self):
        '''
        Steps the simulation by deltaT time.
        Simulates tree growth and other required processes. 
        '''
        self.simTime += self.deltaTime

        # Updates tree age
        self.world['treeAge'][self.world['treeAge'] != 0] += self.deltaTime

        # If the forrest is not currently on fire and once per day
        if self.simTime % 24 == 0 and not self.isOnFire:
            self.world['BiomassAmount'] = biomass.growUp(
                self.world['BiomassAmount'], self.world['treeAge'], 24 * self.deltaTime)

            biomass_spread = biomass.spread(self.world['BiomassAmount'])
            self.world['treeAge'][biomass_spread] += 1

        # Temprature only changes when on fire
        if self.isOnFire:
            newTempratures = temprature.getWorldTemprature(self.simTime)
            self.setWorldTempratureArray(newTempratures)

    def __create_h5__(self):
        '''
        Creates new h5 file if it does not exist
        '''
        if not os.path.isfile(self.save_file_name):
            self.fp = h5py.File(self.save_file_name, mode='a')
        else:
            raise FileExistsError('File named {} already Exists'.format(self.save_file_name))


        self.fp_world = self.fp.create_group('world_data')
        

    def saveState(self, append=True):
        '''
        Saves the file in a hdf5 file format
        '''
        if append:
            file_mode = 'a'
        else:
            file_mode = 'w'
        
        # Checks if h5 file already exists and if not creates it
        if not os.path.isfile(self.save_file_name):
            self.__create_h5__()

        fp = h5py.File(self.save_file_name, mode=file_mode)

        fp.

        yield NotImplementedError()
