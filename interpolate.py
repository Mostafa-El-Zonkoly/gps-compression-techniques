import numpy as np
from point import Point 
    
    
def interpolateCurve(trajectory, originalTrajectory): 
    # trajectory of Point type
    # contains the 
    requiredTimes = list(map(lambda point: point.timestamp, originalTrajectory))
    lats = list(map(lambda point: point.latitude, trajectory))
    longs = list(map(lambda point: point.longitude, trajectory))
    trajectoryTimes = list(map(lambda point: point.timestamp, trajectory))
    interpolatedLats = np.interp(requiredTimes, trajectoryTimes, lats)
    interpolatedLongs = np.interp(requiredTimes, trajectoryTimes, longs)
    size = len(interpolatedLongs)
    interpolatedTrajectory = []
    for i in range(0,size): 
        point = Point(interpolatedLongs[i], interpolatedLats[i], 0, 0, requiredTimes[i])
        interpolatedTrajectory.append(point)
    return(interpolatedTrajectory)
