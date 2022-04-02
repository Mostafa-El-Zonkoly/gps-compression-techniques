


import constants
import numpy as np
import similaritymeasures
import matplotlib.pyplot as plt
from fuzzy_logic import setHeadingBoundaries
from constants import *
from numpy import trapz
ADAPTIVE_FUZZY = False

def setAdaptiveFuzzy(value): 
    global ADAPTIVE_FUZZY
    ADAPTIVE_FUZZY = value
def getCurrentPoint(): 
    # global CURRENT_POINTS
    return constants.CURRENT_POINTS
def setupServer():
    # TODO
    # global OVERALL_DATA
    # global TRANSFERED_DATA
    # global CURRENT_POINTS
    # constants.OVERALL_DATA = []
    # constants.TRANSFERED_DATA = []
    # constants.CURRENT_POINTS = startingPoint
    constants.OVERALL_DATA = []
    constants.TRANSFERED_DATA = []
    


def sendData(trajectory, feedback_data, removed_count,adapt=False): 
    global ADAPTIVE_FUZZY
    for traj in trajectory:
        constants.OVERALL_DATA.append(traj)
    for feed in feedback_data: 
        constants.TRANSFERED_DATA.append(feed)
    if len(trajectory) > 0 and removed_count > 0:
        compression_ratio = ((len(trajectory)) / (len(trajectory) + removed_count))
        if ADAPTIVE_FUZZY: # means I have too many points that I can neglect 
            # if compression ration > 80% that means that most of the points are helpfull, so I need to include more points
           if compression_ratio * 100 < 5: 
                setHeadingBoundaries(left=True)
           elif compression_ratio * 100 > 70: 
               setHeadingBoundaries(left=False)
        
            
        if  getFixedSizeWindow() and adapt:             
            constants.MAX_SEGMENT_LENGTH = min(max((compression_ratio + 0.25) * constants.MAX_SEGMENT_SIZE, 50), constants.MAX_SEGMENT_SIZE)
        
        
         
        
def getOverallData(): 
    # global OVERALL_DATA
    return constants.OVERALL_DATA
def getTransferedData():
    # global TRANSFERED_DATA
    return constants.TRANSFERED_DATA

