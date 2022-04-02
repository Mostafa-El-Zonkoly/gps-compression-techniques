from constants import * 
import numpy as np
# these values gets set by the simulation at the beging 
HEADING_POINTS = np.array([0,3e-3,3e-3,180])
ACCELERATION_POINTS = np.array([0,3e-3,3e-3,1000])
DISTANCE_POINTS = np.array([0,3e-3,3e-3,1000])
# Calculate Fuzzy Input
def interpolate(value,membershipFunction):
    #print ("MembershipFunction = " + str(membershipFunction))
    _,a1,a2,_ = membershipFunction
    if value < a1:
        return  [1,0]
    elif value > a2: 
        return [0,1]
    else:
        
       sameSegmentValue = abs((a2 - value) / (a2 - a1))
       newSegmentValue = abs((value - a1) / (a2 - a1))
       return [sameSegmentValue, newSegmentValue]
# Calculate Fuzzy Output 
def getFuzzyMembership(distance,heading, acceleration):
    #print("Distance = " + str(distance))
    hMembership = interpolate(heading, getHeadingPoints())
    aMembership = interpolate(acceleration, getAccelerationPoints())
    dMembership = interpolate(distance, getDistancePoints())
    allMemberships = [hMembership[1]] + [aMembership[1]] + [dMembership[1]]
    allMemberships = [l for l in allMemberships if l != 1]
    # both are new segments 
    if len(allMemberships) == 0:
        allMemberships = [1]
    
    # dMembership = [1,0]
    new_strength = max([hMembership[1]] + [aMembership[1]] + [dMembership[1]])
    same_strength = max([hMembership[0]] + [aMembership[0]] + [dMembership[0]])
    
    fuzzy_strength = max(allMemberships)
    # print("*****")
    # print("hMembership = " + str(hMembership) + " --- " + str(heading))
    # print("aMembership = " + str(aMembership)+ " --- " + str(acceleration))
    # print("dMembership = " + str(dMembership)+ " --- " + str(distance))
    # # if hMembership[1] > aMembership[1]: 
    # #     new_strength = hMembership[1]
    # # else: 
    # #     new_strength = aMembership[1]
    # # Either A or B is a new Segment 
    # if hMembership[0] < aMembership[1]: 
    #     f1 = hMembership[0]
    # else: 
    #     f1 = aMembership[1]
    # if hMembership[1] < aMembership[0]: 
    #     f2 = hMembership[1]
    # else: 
    #     f2 = aMembership[0]
    # if f1 > f2:
    #     fuzzy_strength  = f1 
    # else: 
    #     fuzzy_strength = f2
    # if hMembership[0] < aMembership[0]: 
    #     same_strength = hMembership[0]
    # else: 
    #     same_strength = aMembership[0]
    #fuzzy_strength = max(min(hMembership[0], aMembership[1]), min(hMembership[1],aMembership[0])) 
    # Both A & B are same Segment
    #same_strength = min(hMembership[0], aMembership[0]) 
    # Rule Evaluation
    if new_strength >= fuzzy_strength and new_strength >= same_strength: 
        return NEW_SEGMENT_STATUS
    elif fuzzy_strength >= new_strength and fuzzy_strength >= same_strength: 
        return FUZZY_RECORD_STATUS
    else:
        return SAME_SEGMENT_STATUS


    
    
# Setting Input Memberships 
def getHeadingPoints(): 
    global HEADING_POINTS
    return HEADING_POINTS
def getAccelerationPoints(): 
    global ACCELERATION_POINTS
    return ACCELERATION_POINTS
def getDistancePoints(): 
    global DISTANCE_POINTS
    return DISTANCE_POINTS
def resetPoints(heading, acceleration, distance):
    global HEADING_POINTS, ACCELERATION_POINTS, DISTANCE_POINTS
    HEADING_POINTS = np.array(heading)
    ACCELERATION_POINTS = np.array(acceleration)
    DISTANCE_POINTS = np.array(distance)
def setBoundariesFeedback(factor): 
    global HEADING_POINTS, ACCELERATION_POINTS, DISTANCE_POINTS
    HEADING_POINTS = HEADING_POINTS * (1 + factor)
    ACCELERATION_POINTS = ACCELERATION_POINTS * (1 + factor)
    DISTANCE_POINTS = DISTANCE_POINTS * (1+factor)