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
