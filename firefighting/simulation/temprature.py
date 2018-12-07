from scipy.signal import convolve2d
import numpy as np

from scipy.constants import pi as PI


def calculateTempratureChanges(init_temprature_Array):
    '''
    Calculates the change in temprature for each cell using a 2d convolution
    '''

    tempratureWeights = np.array([[0.05, 0.05, 0.05],
                                  [0.05, 0.6, 0.05],
                                  [0.05, 0.05, 0.05]])

    newTempratures = convolve2d(
        in1=init_temprature_Array, in2=tempratureWeights, mode='same')

    return newTempratures


def getWorldTemprature(current_time):
    '''
    Calculates the world base temprature for a perticular day/time
    '''

    # Simplistic modeling of temprature
    JanHigh = 2
    JanLow = -6
    JanAvg = np.mean((JanHigh, JanLow))

    JulHigh = 30
    JulLow = 18
    JulAvg = np.mean((JulHigh, JulLow))

    YearAvg = np.mean((JanAvg, JulAvg))

    dayNumberinYear = current_time/24

    dayResolutionTemp = (JulAvg - JanAvg)/2 * \
        np.sin(2*PI * dayNumberinYear/365 - PI/2) + YearAvg

    minuteResolutionTemp = (JanHigh - JanLow) * \
        np.sin(current_time % (24) - PI/2) + dayResolutionTemp

    return minuteResolutionTemp
