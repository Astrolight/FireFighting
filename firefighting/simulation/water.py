import numpy as np

def chanceOfRain(self):
    '''
    Returns the chance out of 1 for rain to happen on that day
    '''
    # According to NOAA for dayton at least there are 8 days on avg per month with rain

    return  (8*12)/ 365