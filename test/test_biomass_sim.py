from firefighting.simulation import biomass

import numpy as np
import random


def test_spontaneousGrowth():
    '''
    Tests to make sure a tree cant just spontainusly grow from nothing
    '''
    currentBiomass = np.zeros((1,1))
    age = np.zeros((1,1))
    dt = 1

    assert biomass.growUp(currentBiomass, age, dt) == 0


def test_adultBiomass():
    '''
    Tests to make sure that the tree has a specific biomass at its adult age
    '''
    currentBiomass = 14385 * np.ones((1,1))
    adultAge = 120*365*24 * np.ones((1,1))
    dt = 1

    assert 14380 <= biomass.growUp(currentBiomass, adultAge, dt) <= 14385


def test_treeDeath():
    '''
    Makes sure tree at end of life is completely gone
    '''
    currentBiomass = np.ones((1,1))
    deathAge = (120*365*24 + 20*365*24) * np.ones((1,1))
    dt = 1

    np.testing.assert_almost_equal(biomass.growUp(currentBiomass, deathAge, dt), 0)
