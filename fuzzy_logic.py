from constants import *
from constants import EPSILON
import numpy as np
from full_fuzzy_logic import getFuzzyMembership as fullFuzzyMembership
from full_fuzzy_logic import resetPoints
import random
import math

import skfuzzy as fuzz
from skfuzzy import control as ctrl
from point import Point as Point
SEGMENT_STATE = None

HEADING_BOUNDARIES = [0,6e1 * EPSILON , 10, 181]
ACCELERATION_BOUNDARIES = [0, 6e1 * EPSILON, 1, 1000]
DISTANCE_BOUNDARIES = [0, 6e1 * EPSILON, 1, 1000]
def resetFuzzyMemberships(heading, acceleration,distance): 
    global HEADING_BOUNDARIES, ACCELERATION_BOUNDARIES, SEGMENT_STATE, DISTANCE_BOUNDARIES
    SEGMENT_STATE = None
    HEADING_BOUNDARIES = heading.copy()
    ACCELERATION_BOUNDARIES = acceleration.copy()
    DISTANCE_BOUNDARIES = distance.copy()
    #print("HEADING BOUNDARIES = " + str(HEADING_BOUNDARIES))
    resetPoints(heading=[0, HEADING_BOUNDARIES[1], HEADING_BOUNDARIES[1] * 3, 180], acceleration=[0, ACCELERATION_BOUNDARIES[1], ACCELERATION_BOUNDARIES[1] * 3, 1000], distance=[0, DISTANCE_BOUNDARIES[1], DISTANCE_BOUNDARIES[1] * 3, 1000])
    #print("Reseting boundaries")
    #print(heading)
    #print(getHeadingBoundaries())
    
def getSegmentState():
    global SEGMENT_STATE
    if SEGMENT_STATE is None: 
        heading = ctrl.Antecedent(np.arange(0, 180, 1e-2), 'heading')
        acceleration = ctrl.Antecedent(np.arange(0, 1000, 1e-1), 'acceleration')
        segment = ctrl.Consequent(np.arange(0, 1, 1e-1), 'segment')
        # heading.automf(3)
        c1 = 2
        c2 = 2
        c3 = 3
        head_anchor = getHeadingBoundaries()[1]
        head_same_right = head_anchor * c1
        head_fuzzy_left = head_anchor / c2
        head_fuzzy_right = head_anchor * c3
        heading['same_segment'] = fuzz.trapmf(heading.universe, [0, 0, head_anchor, head_same_right])
        heading['fuzzy'] = fuzz.trapmf(heading.universe, [head_fuzzy_left, head_anchor, head_fuzzy_right, 1])
        heading['new_segment'] = fuzz.trapmf(heading.universe, [head_fuzzy_right, 1, 180, 180])
        acc_anchor = getAccelerationBoundaries()[1]
        acc_same_right = acc_anchor * c1
        acc_fuzzy_left = acc_anchor / c2
        acc_fuzzy_right = acc_anchor * c3
        # acceleration.automf(3)
        acceleration['same_segment'] = fuzz.trapmf(acceleration.universe, [0, 0, acc_anchor, acc_same_right])
        acceleration['fuzzy'] = fuzz.trapmf(acceleration.universe, [acc_fuzzy_left, acc_anchor, acc_fuzzy_right, 5])
        acceleration['new_segment'] = fuzz.trapmf(acceleration.universe, [acc_fuzzy_right, 5, 1000, 1000])
        #acceleration.automf(3)
        # segment['low'] = fuzz.trimf(segment.universe, [0, 1e-3, 2e-3])
        # segment['medium'] = fuzz.trimf(segment.universe, [1e-3, 3e-3, 5e-3])
        # segment['high'] = fuzz.trimf(segment.universe, [4e-3, 0.75, 1])

        segment['low'] = fuzz.trapmf(segment.universe, [0, 0, 2e-3, 6e-3])
        segment['medium'] = fuzz.trapmf(segment.universe, [2e-3, 4e-3, 1e-2, 5e-2])
        segment['high'] = fuzz.trapmf(segment.universe, [3e-2, 5e-2, 1, 1])

        # segment['medium'] = fuzz.trimf(segment.universe, [1e-3, 3e-3, 5e-3])
        # segment['high'] = fuzz.trimf(segment.universe, [4e-3, 0.75, 1])

        rule1 = ctrl.Rule(heading['new_segment'] & acceleration['new_segment'], segment['high'])
        rule2 = ctrl.Rule(heading['fuzzy'] | acceleration['fuzzy'], segment['medium'])
        rule3 = ctrl.Rule(heading['new_segment'] & acceleration['fuzzy'], segment['medium'])
        rule4 = ctrl.Rule(heading['fuzzy'] | acceleration['new_segment'], segment['medium'])
        rule5 = ctrl.Rule(heading['same_segment'] | acceleration['same_segment'], segment['low'])
        segment_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        SEGMENT_STATE = ctrl.ControlSystemSimulation(segment_ctrl)
        
    return SEGMENT_STATE


def getFuzzyState(current: Point, previous: Point,pre_previous: Point, current_point,fuzzy=False, full_fuzzy=False):
    if not fuzzy: 
       return SAME_SEGMENT_STATUS
    if not full_fuzzy: 
        state =  getFuzzyMembership(current, previous,pre_previous, current_point)    
    else: 
        state = getFuzzyMembershipFullFuzzy(current,previous,current_point)

    return state
    
def getFuzzyMembershipValue(boundaries, old_value, new_value): 
    differnce = abs(new_value - old_value)
    if differnce < boundaries[1]: 
        return SAME_SEGMENT_STATUS
    elif differnce < boundaries[2]: 
        return FUZZY_RECORD_STATUS
    else: 
        return NEW_SEGMENT_STATUS
def getHeadingBoundaries(): 
    global HEADING_BOUNDARIES
    ##print("Heading = " + str(HEADING_BOUNDARIES))
    return HEADING_BOUNDARIES
def setHeadingBoundaries(left): 
    global HEADING_BOUNDARIES, ACCELERATION_BOUNDARIES, DISTANCE_BOUNDARIES
    delta = 5e-3
    if left: 
        HEADING_BOUNDARIES[1] = HEADING_BOUNDARIES[1] * (1-delta)
        ACCELERATION_BOUNDARIES[1] = ACCELERATION_BOUNDARIES[1] * (1-delta)
        DISTANCE_BOUNDARIES[1] = DISTANCE_BOUNDARIES[1] * (1-delta)
    else: 
        HEADING_BOUNDARIES[1] = HEADING_BOUNDARIES[1] * (1 + delta)
        ACCELERATION_BOUNDARIES[1] = ACCELERATION_BOUNDARIES[1] * (1+delta)
        DISTANCE_BOUNDARIES[1] = DISTANCE_BOUNDARIES[1] * (1+delta)
    HEADING_BOUNDARIES[2] = HEADING_BOUNDARIES[1] * 3
    ACCELERATION_BOUNDARIES[2] = ACCELERATION_BOUNDARIES[1] * 3
    DISTANCE_BOUNDARIES[2] = DISTANCE_BOUNDARIES[1] * 3
    resetPoints(heading=[0, HEADING_BOUNDARIES[1], HEADING_BOUNDARIES[1] * 3, 180], acceleration=[0, ACCELERATION_BOUNDARIES[1], ACCELERATION_BOUNDARIES[1] * 3, 1000], distance=[0, DISTANCE_BOUNDARIES[1], DISTANCE_BOUNDARIES[1] * 3, 1000])

        
def getAccelerationBoundaries(): 
    global ACCELERATION_BOUNDARIES
    ##print("Acceleration = " + str(ACCELERATION_BOUNDARIES))
    return ACCELERATION_BOUNDARIES

def convertGPSToXY(point): 
    return [point.latitude, point.longitude]
def estimateNewPosition(point, time): 
    x,y = convertGPSToXY(point)
    delta_time = time - point.timestamp
    distance = delta_time * point.speed
    angle = point.heading # from North 
    delta_x = math.cos(angle) * distance
    delta_y = math.sin(angle) * distance
    return [x+delta_x, y+delta_y]
def estimateDistanceFor(point,new_point): 
    x1,y1 = estimateNewPosition(point, new_point.timestamp)
    x2,y2 = convertGPSToXY(new_point)
    return (math.sqrt(math.pow(x2 - x1, 2) +  math.pow(y2 - y1,2))) # distance between new point and estimated point
def getFuzzyMemberShipPerPoint(current: Point, previous: Point): 
    delta_heading = abs(current.heading - previous.heading)
    delta_acceleration = abs(current.acceleration - previous.acceleration)
    
    #resetPoints(heading_boundaries, acceleration_boundaries)
    #print(delta_heading)
    #print(delta_acceleration)
    fuzzy_state = fullFuzzyMembership(estimateDistanceFor(previous, current), heading=delta_heading, acceleration=delta_acceleration)
    return(fuzzy_state)
def getFuzzyMembership(current: Point, previous: Point,pre_previous: Point, current_point): 
    global EPSILON
    #print("Deltas")
    #heading_boundaries = getHeadingBoundaries()
    #acceleration_boundaries = getAccelerationBoundaries()
    pre_previous_state = getFuzzyMemberShipPerPoint(current, previous)
    previous_state = getFuzzyMemberShipPerPoint(current, pre_previous)
    #print(previous_state + " - " + pre_previous_state)
    if pre_previous_state == NEW_SEGMENT_STATUS or pre_previous_state == FUZZY_RECORD_STATUS: 
        return NEW_SEGMENT_STATUS_AND_PREV
    elif  previous_state == NEW_SEGMENT_STATUS: 
        return NEW_SEGMENT_STATUS
    elif previous_state == FUZZY_RECORD_STATUS or pre_previous_state == FUZZY_RECORD_STATUS: 
        return FUZZY_RECORD_STATUS
    else: 
        return SAME_SEGMENT_STATUS
    # heading_state = getFuzzyMembershipValue(heading_boundaries, previous.heading, current.heading)
    # acceleration_state = getFuzzyMembershipValue(acceleration_boundaries, previous.acceleration, current.acceleration)
    # # acceleration_state = SAME_SEGMENT_STATUS
    # # heading_state = SAME_SEGMENT_STATUS
    # if heading_state == FUZZY_RECORD_STATUS or acceleration_state == FUZZY_RECORD_STATUS:
    #     fuzzy_state = FUZZY_RECORD_STATUS
    # elif heading_state == NEW_SEGMENT_STATUS or acceleration_state == NEW_SEGMENT_STATUS: 
    #     fuzzy_state = NEW_SEGMENT_STATUS
    # else: 
    #     fuzzy_state = SAME_SEGMENT_STATUS
    return fuzzy_state

def getFuzzyMembershipFullFuzzy(current: Point, previous: Point, current_point): 
    global EPSILON
    segment_state = getSegmentState()
    segment_state.input['heading'] = abs(current.heading - previous.heading)
    segment_state.input['acceleration'] = abs(current.acceleration - previous.acceleration)
    segment_state.compute()
    state = segment_state.output['segment']
    if state <= 1e-2:
        return SAME_SEGMENT_STATUS
    if state <= 5e-2: 
        return FUZZY_RECORD_STATUS
    return NEW_SEGMENT_STATUS 
