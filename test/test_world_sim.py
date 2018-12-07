from firefighting import world

import numpy as np


def test_baren_world():
    '''
    Test if a baren forest will not spontainaly gain trees
    '''
    forest = world.World(10)

    InitBiomass = forest.getInfo()['worldData']['BiomassAmount']

    # Assert that all values are zero
    assert not np.any(InitBiomass)

    # Just do 1000 random runs
    for _ in range(1000):
        forest.step()

    EndingBiomass = forest.getInfo()['worldData']['BiomassAmount']

    # Assert that all ending biomass is zero
    assert not np.any(EndingBiomass)

    # Assert that inital and final biomass is zero
    np.testing.assert_array_equal(InitBiomass, EndingBiomass)
