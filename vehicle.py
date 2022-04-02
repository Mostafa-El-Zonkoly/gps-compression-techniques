


from skfuzzy import fuzzymath
import constants
from constants import *
from server_logic import getCurrentPoint, getOverallData, getTransferedData, sendData, setAdaptiveFuzzy
from douglas_peucker import compressTrajectory
from fuzzy_logic import getFuzzyState
from point import Point as Point

def excludeRemovedData(sent_data, vehicle_data): 
    # for data in sent_data: 
    #     vehicle_data.remove(data)
    return (vehicle_data)
def sameSegment( length): 
    
    if length > constants.MAX_SEGMENT_LENGTH: 
        return False
    return True
def simulateVehicle(input_data,fuzzy=True, full_fuzzy=False, adaptive_fuzzy=False, realtime = False): 
    constants.SEGMENTS = []
    setAdaptiveFuzzy(adaptive_fuzzy)
    local_history = [] # Contains valid point
    feedback_data = [] # contails feedback points
    segments_count = 0
    size = len(input_data)
    last_point = Point(0,0)
    last_considered_point = Point(0,0)
    considered_points = 0
    
    
    dropped_points = 0
    for i in range(0, size):
        point = input_data[i]
        fuzzy_state = getFuzzyState(point, last_considered_point,last_point, getCurrentPoint(), fuzzy,full_fuzzy)
        same_segment = sameSegment(len(local_history)) 
        if fuzzy_state == constants.SAME_SEGMENT_STATUS and same_segment: 
            # if same segment do nothing, can neglect these points easily
            previous_similar_point = point
            if not fuzzy: 
                considered_points += 1    
                local_history.append(point)
            else: 
                dropped_points += 1
            last_point = point 
            #last_considered_point = point
        elif not same_segment or realtime :
            # New Segment or reached window size
            # Send the data
            #if fuzzy_state == NEW_SEGMENT_STATUS_AND_PREV:
            
            if last_point.timestamp != last_considered_point.timestamp and fuzzy: 
                
                local_history.append(last_point)
                    

            considered_points += 1
            local_history.append(point)
            segments_count += 1
            processData(local_history, feedback_data,getEPSILON(),dropped_points, realtime,adaptive_fuzzy)
            dropped_points = 0
            local_history = []
            feedback_data = []
            segments_count += 1
            last_point = point
            last_considered_point = point
            
        else: #if fuzzy_state == constants.FUZZY_RECORD_STATUS  or i >= (size-1) or i == 0: # to handle first and last points
            if last_point.timestamp != last_considered_point.timestamp:
                local_history.append(last_point)

            
            considered_points += 1
            feedback_data.append(point)
            local_history.append(point)
            last_point = point
            last_considered_point = point


        
    if(len(local_history) > 0): 
        # add the remaining items 
        segments_count += 1
        processData(local_history, feedback_data,constants.EPSILON, dropped_points, realtime,adaptive_fuzzy)
    return {'segments_count': segments_count, 'output': getOverallData(), 'feedback_data': getTransferedData(), 'segments': constants.SEGMENTS, 'overall': considered_points}
def processData(fuzzy_trajectory, feedback_data, eps,removed_count,realtime,adapt): 
    # global SEGMENTS
    constants.SEGMENTS.append(len(fuzzy_trajectory))
    result = compressTrajectory(fuzzy_trajectory, eps, realtime)
    if not realtime:
        removed_count = len(fuzzy_trajectory) - len(result)
    
    sendData(result, feedback_data, removed_count, adapt)

            
        