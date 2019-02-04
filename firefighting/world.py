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

    chunkSize = 16

    def __init__(self, size, save_file_name='Default'):
        self.simTime = 0  # Hours
        self.deltaTime = 1  # Hours

        # Sets the world size
        self.worldSize = (size, size)

        # The inital world temprature in centegrade
        self.globalTemp = temprature.getWorldTemprature(self.simTime)

        # Creates a 2d list/array of TreeCell objects
        self.world = {'WaterLevel': np.zeros(self.worldSize),
                      'BiomassAmount': np.zeros(self.worldSize),
                      'DiffTemprature': np.zeros(self.worldSize),
                      'treeAge': np.zeros(self.worldSize),
                      'hasFire': np.zeros(self.worldSize, dtype='bool')}

        self.isOnFire = False

        # Stuff for creating h5 file
        if save_file_name == 'Default':
            # Returns the current time in ISO 8601 UTC Format (yyyyMMddTHHmmssZ)
            # yyyy=year, MM=month, dd=day, HH=hour (24H), mm=minute, ss=second, Z means UTC (Zero offset)
            self.save_file_name = time.strftime(
                '%Y%m%dT%H%M%SZ', time.gmtime())+'.h5'
        else:
            self.save_file_name = save_file_name

        self.fp = None
        self.fp_world_data = {}
        self.__create_h5__()

        self.autoSaveState()

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
            'onFire': self.isOnFire,
            'worldSize': self.worldSize,
            'globalTemp': self.globalTemp,
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

        # Temprature only changes when on fire
        if self.isOnFire:
            # Saves simulation if on fire during specified interval
            if self.fireInterval != 0 and self.simTime % self.fireInterval == 0:
                self.saveState()

            newTempratures = temprature.getWorldTemprature(self.simTime)
            self.setWorldTempratureArray(newTempratures)
        else:
            # If the forrest is not currently on fire and once per day
            if self.simTime % 24 == 0:
                self.world['BiomassAmount'] = biomass.growUp(
                    self.world['BiomassAmount'], self.world['treeAge'], 24 * self.deltaTime)

                biomass_spread = biomass.spread(self.world['BiomassAmount'])
                self.world['treeAge'][biomass_spread] += 1


            # Saves simulation if not on fire during specified interval
            if self.normalInterval != 0 and self.simTime % self.normalInterval == 0:
                self.saveState()

    # * Functions to deal with saving of data

    def __create_h5__(self):
        '''
        Creates new h5 file if it does not exist
        '''
        if not os.path.isfile(self.save_file_name):
            self.fp = h5py.File(self.save_file_name, mode='a')
        else:
            raise FileExistsError(
                'File named {} already Exists'.format(self.save_file_name))

        self.fp_simTime = self.fp.create_dataset('simTime', shape=(self.chunkSize,), maxshape=(None,), chunks=(self.chunkSize,), dtype='int32')
        self.fp_onFire = self.fp.create_dataset('onFire', shape=(self.chunkSize,), maxshape=(None,), chunks=(self.chunkSize,), dtype='bool8')
        self.fp_globalTemp = self.fp.create_dataset('globalTemp', shape=(self.chunkSize,), maxshape=(None,), chunks=(self.chunkSize,), dtype='float16')

        self.fp_world = self.fp.create_group('world_data')

        datasets = ['WaterLevel', 'BiomassAmount', 'DiffTemprature', 'treeAge', 'hasFire']
        for dataset in datasets:
            self.fp_world_data[dataset] = self.fp_world.create_dataset(dataset, dtype='single', shape=(self.worldSize[0], self.worldSize[0], self.chunkSize), maxshape=(
                self.worldSize[0], self.worldSize[0], None), chunks=(self.worldSize[0], self.worldSize[0], self.chunkSize))

        self.currentLayer = 0

    def autoSaveState(self, normalInterval=720, fireInterval=3):
        '''
        Autosaves data to the h5 file every x timesteps.

        Set to 0 to disable auto save

        Default is to save every simulation 30 days and every 3 steps during a fire
        '''
        self.normalInterval = normalInterval
        self.fireInterval = fireInterval

    def saveState(self):
        '''
        Saves the file in a hdf5 file format
        '''

        # Opens file if it was not already open
        if self.fp == None:
            self.fp = h5py.File(self.save_file_name, mode='a')
            self.fp_world = self.fp['world_data']

            self.fp_simTime = self.fp['simTime']
            self.fp_onFire = self.fp['onFire']
            self.fp_globalTemp = self.fp['globalTemp']

            datasets = ['WaterLevel', 'BiomassAmount',
                        'DiffTemprature', 'treeAge', 'hasFire']
            for dataset in datasets:
                self.fp_world_data[dataset] = self.fp_world[dataset]

        world_info = self.getInfo()

        # Saves the 1d arrays
        file_pointers_1D = [self.fp_simTime,
                            self.fp_onFire, self.fp_globalTemp]
        file_pointers_1D_Name = ['simTime', 'onFire', 'globalTemp']
        for i in range(len(file_pointers_1D)):
            curr_fp = file_pointers_1D[i]
            curr_fp_name = file_pointers_1D_Name[i]     
            curr_fp[self.currentLayer] = world_info[curr_fp_name]

            if self.currentLayer % self.chunkSize == 0:
                curr_fp.resize(curr_fp.shape[0]+self.chunkSize, axis=0)

        # Saves the 2d arrays
        file_pointers_2D = self.fp_world_data
        file_pointers_2D_keys = list(file_pointers_2D.keys())
        file_pointers_2D_Name = ['WaterLevel',
                                 'BiomassAmount', 'DiffTemprature', 'treeAge', 'hasFire']
        for i in range(len(file_pointers_2D)):
            curr_fp = file_pointers_2D[file_pointers_2D_keys[i]]
            curr_fp_name = file_pointers_2D_Name[i]        
            curr_fp[:, :, self.currentLayer] = world_info['worldData'][curr_fp_name]

            if self.currentLayer % self.chunkSize == 0:
                curr_fp.resize(curr_fp.shape[2]+self.chunkSize, axis=2)

        self.currentLayer += 1