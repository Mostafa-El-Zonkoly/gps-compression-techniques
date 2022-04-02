import numpy as np
from geographiclib.geodesic import Geodesic
from pathlib import Path

def calculateHeading(p1, p2): 
    values = Geodesic.WGS84.Inverse(p1[0],p1[1], p2[0],p2[1])
    return values['azi1'] * 1e-3
def calculateSpeed(p1, p2): 
    # need to have the time, and position of both 
    values = Geodesic.WGS84.Inverse(p1[0],p1[1], p2[0],p2[1])
    distance = values['s12']
    time = abs(p1[4] - p2[4])
    if time == 0: 
        return 0
    speed = distance / time
    return(speed)
def calculateAccerlation(p1,p2): 
    speed1 = p1[5]
    speed2 = calculateSpeed(p1, p2)
    time = abs(p1[4] - p2[4])
    if time == 0 :
        return 0
    acceleration =  1e-12 * (speed2 - speed1) / time
    return acceleration
def convertData(path,filename): 
    data = []
    lines = np.genfromtxt(path+"/"+filename+".plt", delimiter=',',skip_header=6)
    for line in lines: 
        data.append(line)
    point = list(data[0][0:2]) # contains lat / lng only
    point.append(0) # heading
    point.append(0) #speed
    point.append(0) # acceleration
    point.append(0) # time
    
    result = []
    result.append(point)
    for p in data: 
        new_point = [p[0], p[1], calculateHeading(point, p), calculateAccerlation(point, p), p[4], calculateSpeed(point, p)]
        point = new_point
        result.append(new_point)
    output_file_name = "input/"+path+"/"+filename+".csv"
    Path("input/"+path+"/").mkdir(parents=True, exist_ok=True)
    f = open(output_file_name, "w+")
    f.write("0,1,2,3\n")
    f.write("Longitude, Latitude, Heading, Acceleration, Time, Speed\n")
    for line in result: 
        strr = ""
        for part in line: 
            strr += str(part) + ","
        f.write(strr + "\n")
    
    f.close()
    return(result)

# data = convertData("geolife/010/Trajectory", "20081219114010")
# data = convertData("geolife/000/Trajectory", "20081023025304")
import sys,os
root = 'geolife'
for path, subdirs, files in os.walk(root):
    for name in files:
        if ".plt" in name: 
            convertData(path, name.replace('.plt',''))