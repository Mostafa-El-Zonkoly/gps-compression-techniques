from error_calculation import *
from douglas_peucker import compressTrajectory
import constants
from constants import EPSILON, init, setEPSILON, getEPSILON
from datetime import datetime
from read_input import readInput
from vehicle import simulateVehicle
from server_logic import getOverallData, getTransferedData, setupServer
from statistics import * 
from plot_graphs import plotGraphs
from fuzzy_logic import getAccelerationBoundaries, resetFuzzyMemberships, getHeadingBoundaries
import time
import sys,os
import xlwt
from xlwt import Workbook

WB = Workbook()
SHEETS = []
INDEX = 1
MATCHING_COUNT = 0
FILENAME = ""
DATA_SUM = 0
FILTER_SIZE = False
FILTER_SIZE_VALUE = 20e3
TYPE_OPTIONS = {
    # fixed_window, fuzzy, full_fuzzy, adaptive_fuzzy, realtime
    "original": [False, False, False,False,False],
    "fixed_window_fuzzy": [True, True, False, False, False],
    "fixed_window_fully_fuzzy": [True, True, True, False,False],
    "fixed_window": [True, False, False, False,False],
    "variable_window_fuzzy": [False, True, False,False,False],
    "variable_window_fully_fuzzy": [False, True, True,False,False],
    "variable_window": [False, False, False,False,False],
    "adaptive_fixed_window_fuzzy": [True, True, False, True,False],
    "adaptive_variable_window_fuzzy": [False, True, False, True,False],
    "adaptive_realtime_fuzzy": [True, True, False, True, True],
    "realtime_fuzzy": [True, True, False, False, True]
}

SHEET_INDEX = {
    "Dataset": 0, 
    "Size": 1,
    "Output Size": 2,
    "Time": 3, 
    "Error": 4,
    "Compression Ratio": 5,
    "Epsilon": 6,
    "Image Path": 7,
    "Notes": 8,
    "Fuzzy Membership": 9
}
#TYPES = list(set(["original","fixed_window_fuz
# zy", "fixed_window_fully_fuzzy", "fixed_window", "variable_window_fuzzy", "variable_window_fully_fuzzy", "variable_window"]))
# TYPES = ["original", 'fixed_window_fuzzy','adaptive_fixed_window_fuzzy', 'variable_window_fuzzy', 'adaptive_variable_window_fuzzy', 'fixed_window', 'variable_window']
#TYPES = ["original", "fixed_window_fuzzy", "realtime_fuzzy", "adaptive_fixed_window_fuzzy", "adaptive_realtime_fuzzy"]
#TYPES = ["original","fixed_window_fuzzy", "variable_window_"]
#TYPES=['original', 'fixed_window_fuzzy', 'fixed_window', 'variable_window_fuzzy', 'variable_window', 'adaptive_fixed_window_fuzzy', 'adaptive_variable_window_fuzzy', 'adaptive_realtime_fuzzy', 'realtime_fuzzy']
TYPES = ['realtime_fuzzy']

# import other files
def originalResults(data, data_list, output_file): 
    global WB
    global INDEX
    global FILENAME
    sheet = getSheet(original=True, type='original') 
    sheet.write(INDEX ,SHEET_INDEX['Dataset'] , FILENAME)
    sheet.write(INDEX ,SHEET_INDEX['Size'] , str(len(data)))
    start_time_optimal = int(round(time.time() * 1000))
    optimal_result = compressTrajectory(data, getEPSILON())
    end_time_optimal = int(round(time.time() * 1000))
    sheet.write(INDEX ,SHEET_INDEX['Output Size'] ,str(len(optimal_result)))
    sheet.write(INDEX ,SHEET_INDEX['Time'] ,str(end_time_optimal - start_time_optimal) )
    f = open(output_file + 'summary.txt', "a+")
    f.write("*******************************\n")
    f.write("Data Size = " + str(len(data)) + "\n")
    f.write("Optimal is " + str(len(optimal_result)) + "\n")    
    graphs = [[data, 'r','Original','Original'],[optimal_result, 'g', 'Optimal', 'Optimal']]
    f.write(str(data[0].longitude) + "," + str(data[0].latitude) + "\n")
    f.write(str(data[1].longitude) + "," + str(data[1].latitude) + "\n")
    f.write("Original time " + str(end_time_optimal - start_time_optimal) + "\n")
    image_path = plotGraphs(graphs,(output_file + "original" + ".png"), 'Original DP')
    f.flush()
    error = str(calculateError(optimal_result, data))
    ratio = str(compressionRatio(optimal_result, data))
    sheet.write(INDEX ,SHEET_INDEX['Error'] ,error)
    sheet.write(INDEX ,SHEET_INDEX['Compression Ratio'], ratio)
    sheet.write(INDEX ,SHEET_INDEX['Image Path'] ,image_path)
    sheet.write(INDEX ,SHEET_INDEX['Epsilon'], str(getEPSILON()))
    f.write("Error area = " + error + "\n")
    f.write("Compression ratio = " + str(ratio) + "\n")
    f.close()


        

def calculateResults(data, data_list,output_file,type,fuzzy_membership): 
    global FILENAME, MATCHING_COUNT, INDEX
    fixed_window, fuzzy, full_fuzzy, adaptive_fuzzy, realtime = TYPE_OPTIONS[type]
    #print("Calculate Results with membership = " + str(fuzzy_membership))
    init()
    setupServer()
    resetFuzzyMemberships(fuzzy_membership[0], fuzzy_membership[1], fuzzy_membership[2])
    sheet = getSheet(fuzzy,full_fuzzy,fixed_window, False, type)
    #print("STARTING with values --- ")
    #print(getHeadingBoundaries())
    #print(getAccelerationBoundaries())
     
    if len(data) >= FILTER_SIZE_VALUE or not FILTER_SIZE: 
        MATCHING_COUNT += 1
        print("Size matches = " + str(len(data)))
        # return
        sheet.write(INDEX ,SHEET_INDEX['Dataset'] ,FILENAME)
        start_time = int(round(time.time() * 1000))
        result = simulateVehicle(data,fuzzy,full_fuzzy,adaptive_fuzzy,realtime)
        end_time = int(round(time.time() * 1000))
        sheet.write(INDEX ,SHEET_INDEX['Size'] ,str(len(data)))
        sheet.write(INDEX ,SHEET_INDEX['Output Size'] ,str(len(result["output"])))
        sheet.write(INDEX ,SHEET_INDEX['Time'] ,str(end_time - start_time))
        
        f = open(output_file + '/summary.txt', "a+")
        f.write("*******************************\n")
        f.write("Epsilon " + str(getEPSILON()) + "\n")
        f.write("Fuzzy Membership" + str(fuzzy_membership[0][1])+ " / " + str(fuzzy_membership[1][1]) + "\n")
        f.write(getDisplayName(fuzzy, full_fuzzy, fixed_window, adaptive_fuzzy,realtime) +  "\n")
        f.write("Input size = " + str(len(data)) + ", output size = "+ str(len(result['output'])) + " with " + str(result["segments_count"]) + " segment"+ "\n")
        
        f.write("Processed Data = " + str(result['overall'])+ "\n")
        f.write("Transfered Data = " + str(len(getOverallData())) + " and feedback data " + str(len(getTransferedData()))+ "\n")
        f.write("Running time = " + str(end_time - start_time)+ "\n")
        error = str(calculateError(getOverallData(), data))
        ratio = str(compressionRatio(getOverallData(), data))
        f.write("Error area = " + error+ "\n")
        f.write("Compression Ration = " + str(ratio) + "\n")
        graphs = [[getOverallData(), 'r', 'Compressed', 'Compressed'],[data, 'b','Optimal','Optimal']]
        image_path = plotGraphs(graphs,(output_file  + getDisplayName(fuzzy,full_fuzzy, fixed_window,adaptive_fuzzy,realtime) + "_" + str(fuzzy_membership[0][1]) + "_" + str(fuzzy_membership[1][1]) +".png"),getDisplayName(fuzzy, full_fuzzy, fixed_window,adaptive_fuzzy,realtime))
        f.flush()
        
        sheet.write(INDEX ,SHEET_INDEX['Error'] ,error)
        sheet.write(INDEX ,SHEET_INDEX['Compression Ratio'], ratio)
        sheet.write(INDEX ,SHEET_INDEX['Image Path'] ,image_path)
        sheet.write(INDEX ,SHEET_INDEX['Epsilon'], str(getEPSILON()))
        sheet.write(INDEX ,SHEET_INDEX['Notes'] , getDisplayName(fuzzy, full_fuzzy, fixed_window))
        sheet.write(INDEX, SHEET_INDEX['Fuzzy Membership'], str(fuzzy_membership[0][1])+ " / " + str(fuzzy_membership[1][1]))
        f.close()
    else: 
        INDEX -=1
        

def getDisplayName(fuzzy=False, full_fuzzy = False, fixed_window = False, adaptive_fuzzy= False,realtime=False): 
    substring = ""
    if fixed_window: 
        substring = "fixed_window"
    else:
        substring = "variable_window"
    if fuzzy: 
        if full_fuzzy:
            substring = "defuzz_" + substring
        else: 
            substring = "rules_" + substring
        if adaptive_fuzzy:
            substring = "adaptive_" + substring
        if realtime: 
            substring = "realtime_" + substring 

    
        
        
    return substring
def getSheet(fuzzy=False, fullFuzzy=False, fixedWindow=False, original=False, type='original'): 
    global SHEETS
    return SHEETS[TYPES.index(type)]


def setupSheets(): 
    global SHEETS
    SHEETS = []
    for type in TYPES: 
        SHEETS.append(WB.add_sheet(type))
    for sheet in SHEETS:
        setupSheet(sheet)
def setupSheet(sheet): 
    for key in list(SHEET_INDEX.keys()): 
        sheet.write(0, SHEET_INDEX[key], key)
def setupResults(): 
    global WB
    global INDEX
    global FILENAME
    run_number = str(int(round(time.time() * 1000)))
    WB = Workbook()
    setupSheets()
    return run_number

def simulateForFileWithEpsilon(filenames, epsilons,fuzzy_memberships, run_number):
    global WB
    global INDEX
    global FILENAME, DATA_SUM
    INDEX = 1
    for epsilon in epsilons: 
        # Here create all sheets
        for filename in filenames: 
            FILENAME = filename
            simulate(filename, epsilon,fuzzy_memberships, run_number)
            INDEX += 1
            path = "results/" + run_number
            wb_path = path + "/summary.xls"
            WB.save(wb_path)
    # Generate only 1 output file
    
    generateResults(wb_path, path)
    print("---------------" + str(DATA_SUM) + "---------")
    
    
def simulate(filename, epsilon, fuzzy_memberships, run_number='_'): 
    global EPSILON
    global INDEX
    global OVERALL_DATA
    global TRANSFERED_DATA
    global DATA_SUM
    setEPSILON(epsilon)
    data, data_list = readInput(filename + ".csv")#[0:100]
    DATA_SUM += len(data)
    # data = data[0:50]
    # data_list = data_list[0:50]
    #print("Lengths = " + str(len(data)) + " , " + str(len(data_list)))
    new_filename = filename
    new_filename = 'results/' + run_number + "/" + str(epsilon) + "/" + new_filename.replace('/','_') + "/"
    os.makedirs(new_filename)
    for type in TYPES: 
        if type == "original":
            originalResults(data,data_list,new_filename)
        else: 
            if type == 'realtime_fuzzy' or type == 'adaptive_realtime_fuzzy':
                for fuzzy_membership in fuzzy_memberships: 
                    calculateResults(data,data_list,new_filename,type,fuzzy_membership)                    
                    INDEX +=1 
                INDEX -=1 
            else: 
                calculateResults(data,data_list,new_filename,type,fuzzy_memberships[0])                
    
    
def readFiles():
    f = open('report_files.txt','r')
    return f.read().split("\n")

def readEpsilons():
    f = open('epsilons.txt','r')
    return list(map(float, f.read().split("\n")))
#simulate()
files = readFiles()
epsilons = readEpsilons()
#epsilons = list(np.arange(1e-5, 1e-3, 5e-5))

epsilons = [1e-3]
#values = [3e-2,3e-3,3e-4,3e-5]
values = [
    1e-5,
    5e-4,
    1e-4,
    5e-3,
    1e-3,
    5e-2,
    1e-2,
    5e-1,
    1e-1
]
headings = list(np.arange(1e-4,1e-1, 5e-3))
headings.sort()
accelerations = [
    40,
    20,
    10,
    1,
    1e-1,
    1e-2,
     1e-3,
    1e-4,
    1e-5
]
accelerations = list(np.arange(1e-2,1e-1, 1e-2))
accelerations.sort()
# accelerations = [40]
fuzzy_memberships = []
x = 10e-2
accelerations = [x * 50e2]
headings = [x * 11e-1]
distances = [x * 4e5]
for heading in headings: 
    for acceleration in accelerations: 
        for distance in distances: 
            fuzzy_memberships.append([[0, heading, heading * 10, 181], [0, acceleration , acceleration * 10, 1000], [0, distance, distance * 10 , 1000 ]])
run_number = setupResults()
size = 1e5
n = 0
offset = n * size
simulateForFileWithEpsilon(files, epsilons, fuzzy_memberships, run_number)

