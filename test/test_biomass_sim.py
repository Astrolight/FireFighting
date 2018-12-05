from firefighting.simulation import biomass

import numpy as np
import random


def test_spontaneousGrowth():
    '''
    Tests to make sure a tree cant just spontainusly grow from nothing
    '''
    
    age = 0
    dt = 1

    assert biomass.growUp(0, age, dt) == 0


def test_adultBiomass():
    '''
    Tests to make sure that the tree has a specific biomass at its adult age
    '''

    adultAge = 120*365*24
    dt = 1

    assert 14380 <= biomass.growUp(1, adultAge, dt) <= 14385


def test_treeDeath():
    '''
    Makes sure tree at end of life is completely gone
    '''

    deathAge = 120*365*24 + 20*365*24
    dt = 1

    np.testing.assert_almost_equal(biomass.growUp(1, deathAge, dt), 0)
