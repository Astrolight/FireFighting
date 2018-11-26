import numpy as np
from scipy.signal import convolve2d


def growUp(biomass_ammount, age, dage):
    '''
    Simulates the growth of a tree with a biomass and a specific age

    Parameters
    ----------
    biomass_ammount: float
        Defines the ammount of biomass that is being dealt with

    age: integer
        Defines the age of the tree in hours

    dage: float
        Defines the change of age
    '''

    #! All of these values are completly arbratary and need to be adjusted
    #! For now, biomass_ammount is not being used for reasons of simplisity
    # The ideal mass of an adult tree
    OPTIMUM_TREE_MASS = 14385  # Or 14.385 tonns
    TREELIFETIME = 120*365*24  # AKA 120 years

    if age <= TREELIFETIME:
        # Linear line bettwen age=0,biomass=0 to age=TREELIFETIME, biomass=OPTIMUM_TREE_MASS
        newBiomass = 0.0136834094368 * age

    elif TREELIFETIME < age:
        newBiomass = -0.082100456621 * age + 100688  # Rots completely in 20 years

    else:
        raise Exception(
            'Error in growUp, Age: {}, TREELIFETIME: {}'.format(age, TREELIFETIME))

    return newBiomass


def spread(biomass_ammount):
    '''
    Does the spreading of trees to new areas

    Returns a binary array where 1 values are trees spreading
    '''

    # Gets the size of the world
    world_shape = biomass_ammount.shape

    # 1% change every day to spread
    spread_chance = np.array([[0.01,0.01,0.01],
                              [0.01,0.00,0.01],
                              [0.01,0.01,0.01]])

    binary_biomass = biomass_ammount != 0

    conv_array = convolve2d(binary_biomass, spread_chance, mode='same')

    # 1% chance of spreading from single ajacent cell
    spread_rand_binary_matrix = conv_array < np.random.random_sample(world_shape)

    return spread_rand_binary_matrix
