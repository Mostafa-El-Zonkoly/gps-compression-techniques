OVERALL_DATA = []
TRANSFERED_DATA = []
CURRENT_POINTS = [0,0.1,0.2,0.3]
EPSILON = 1e-3
COL_SIZE = 4

NEW_SEGMENT_STATUS = "new_segment"
FUZZY_RECORD_STATUS = "fuzzy_record"
SAME_SEGMENT_STATUS = "same_segment"
NEW_SEGMENT_STATUS_AND_PREV = "new_segment_and_old"
MAX_SEGMENT_LENGTH = MAX_SEGMENT_SIZE = 200
# MAX_SEGMENT_SIZE = 800
MIN_SEGMENT_SIZE = 30

FIXED_SIZE_WINDOW = True
def getFixedSizeWindow(): 
    global FIXED_SIZE_WINDOW
    return FIXED_SIZE_WINDOW
def setFixedSizeWindow(value): 
    global FIXED_SIZE_WINDOW
    FIXED_SIZE_WINDOW = value
def setEPSILON(value): 
    global EPSILON
    EPSILON = value
def getEPSILON():
    global EPSILON
    return EPSILON
def init():
    global OVERALL_DATA
    global TRANSFERED_DATA
    global CURRENT_POINTS
    global EPSILON
    global COL_SIZE
    global NEW_SEGMENT_STATUS
    global FUZZY_RECORD_STATUS
    global SAME_SEGMENT_STATUS
    OVERALL_DATA = []
    TRANSFERED_DATA = []
    CURRENT_POINTS = [0,0.1,0.2,0.3]
    COL_SIZE = 4
