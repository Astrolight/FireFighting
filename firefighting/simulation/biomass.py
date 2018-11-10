import numpy as np


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
    # The ideal mass of an adult tree
    #OPTIMUM_TREE_MASS = 14385 # Or 14.385 tonns

    natralArbratray = 7

    # Grows slowly, then quickly, then tapers out
    natral_Growth = biomass_ammount - (biomass_ammount/natralArbratray)**1.1
    
    # Thatway the growth is independent of the times the function is called per unit time
    natral_Growth = natral_Growth * dage

    # Biomass lost at a spicific age 
    arbratray_value = 12.1
    age_growth = (age / arbratray_value)**1.1

    #! Lets see how this goes
    # Final arb value
    finalArbValue = 7/1E8
    return finalArbValue * max(natral_Growth - age_growth, 0)