from skfuzzy import fuzzymath
import constants
from constants import *
from server_logic import getCurrentPoint, getOverallData, getTransferedData, sendData, setAdaptiveFuzzy
from douglas_peucker import compressTrajectory
from fuzzy_logic import getFuzzyState
from point import Point as Point
from full_fuzzy_logic import * 
TARGET_COMPRESSION = 0.95
#
# Sends Data to Server, with feedback about statitics of 
#   - number of dropped points,
#   - number of fuzzy points & 
#   - number of new segment points
# #
def processData(points,dropped_count, fuzzy_count): 
    # global SEGMENTS
    constants.OVERALL_DATA.append(points)
    constants.TRANSFERED_DATA.append(points)
    size = len(points) 
    dropped = dropped_count + fuzzy_count / 2
    # Compression Ratio ? 
    c_ratio = 1 - (size / (size+dropped))
    direction = ((c_ratio - TARGET_COMPRESSION) / c_ratio) + 1
    setBoundariesFeedback(direction)
def simulateVehicle(input_data,fuzzy=True, full_fuzzy=False, adaptive_fuzzy=False, realtime = False): 
    constants.SEGMENTS = []
    setAdaptiveFuzzy(adaptive_fuzzy)
    
    local_history = [input_data[0]] # Contains valid point
    feedback_data = [] # contails feedback points
    feedback_count = 0
    dropped_count = 0
    last_considered_point = input_data[0]
    last_point = input_data[0]
    size = len(input_data)
    for i in range(0, size):
        point = input_data[i]
        fuzzy_state = getFuzzyState(point, previous_point, getCurrentPoint(), fuzzy,full_fuzzy)
        
        if ((fuzzy_state == constants.NEW_SEGMENT_STATUS ) or not sameSegment(point, point, len(local_history))) and (len(local_history) > 20):
            # New Segment or reached window size
            # Send the data
            considered_points += 1
            if previous_similar_point is not None: 
                local_history.append(previous_similar_point)
            local_history.append(point)
            processData(local_history, feedback_data,getEPSILON(),dropped_points, realtime)
            dropped_points = 0
            local_history = []
            feedback_data = []
            segments_count += 1
            previous_point = point
            previous_similar_point = None
        elif fuzzy_state == constants.SAME_SEGMENT_STATUS or i == size - 1: 
            # if same segment do nothing, can neglect these points easily
            previous_similar_point = point
            if not fuzzy: 
                considered_points += 1    
                local_history.append(point)
            else: 
                dropped_points += 1
            #previous_point = point
        else: #if fuzzy_state == constants.FUZZY_RECORD_STATUS  or i >= (size-1) or i == 0: # to handle first and last points
            previous_similar_point = None
            considered_points += 1
            feedback_data.append(point)
            local_history.append(point)
            previous_point = point


        
    if(len(local_history) > 0): 
        # add the remaining items 
        segments_count += 1
        processData(local_history, feedback_data,constants.EPSILON, dropped_points, realtime)
    return {'segments_count': segments_count, 'output': getOverallData(), 'feedback_data': getTransferedData(), 'segments': constants.SEGMENTS, 'overall': considered_points}

