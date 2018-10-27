from firefighting.simulation import temprature

import numpy as np

def test_zeroTemprature():
    zeroArray = np.zeros((128, 128))

    newTemp = temprature.calculateTempratureChanges(zeroArray)

    np.testing.assert_equal(zeroArray, newTemp)

def test_lossOfEnergy():
    random_array = np.random.rand(128,128)

    starting_energy = np.sum(random_array)

    newTemp = temprature.calculateTempratureChanges(random_array)

    ending_energy = np.sum(newTemp)

    assert ending_energy <= starting_energy