import matplotlib.pyplot as plt
import numpy as np


def generateHeatmap(dataArray, minValue=0, maxValue=1, colorMap='inferno'):
    '''
    Takes in a numpy array and generates a heatmap

    Parameters
    ----------
    dataArray: numpy array

    minValue: float

    maxValue: float

    Returns
    -------
    figure object
    '''

    fig, ax = plt.subplots()
    im = ax.imshow(dataArray, vmin=minValue, vmax=maxValue, cmap=colorMap)

    return fig
