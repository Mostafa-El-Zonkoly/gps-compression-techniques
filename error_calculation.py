import numpy as np
from math import sin, cos, sqrt, atan2, radians
import similaritymeasures
from point import Point as Point
from interpolate import interpolateCurve
from plot_graphs import plotGraphs

def compressionRatio(trajectory, original): 
    return (1 - (len(trajectory) / max(len(original), 1)) )#* 100#len(original) / len(trajectory)
def calculateError(trajectory, original):
    size = len(trajectory)
    pointTrajectory = []
    for i in range(0,size): 
        pointTrajectory.append(Point(trajectory[i][0], trajectory[i][1],0,0,trajectory[i][2]))
    if len(pointTrajectory) == 0:
        return 10000
    interpolatedTrajectory = interpolateCurve(pointTrajectory, original)
    plotGraphs([[interpolatedTrajectory, 'r']], 'interpolated.png')
    return SED(interpolatedTrajectory, original)/len(original)

def SED(trajectory, original):
    size = min(len(trajectory), len(original))
    distance = 0
    for i in range(0, size): 
         distance += calcDistance(trajectory[i], original[i])
    return distance / len(original)
    
def calcDistance(point1, point2): 
    R = 6373.0
    lat1 = radians(point1.latitude)
    lon1 = radians(point1.longitude)
    lat2 = radians(point2.latitude)
    lon2 = radians(point2.longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance * 1000
