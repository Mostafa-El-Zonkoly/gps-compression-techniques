import pandas as pd
import numpy as np
from point import Point
from plot_graphs import plotGraphs
import math
from xlwt import Workbook
ERROR_LOG_BASE = 10
TIME_LOG_BASE = 10
ORIGINAL_COLORS = {
    'original': 'r',
    'variable_window': 'b',
    'fixed_window': 'c',
    'variable_window_fuzzy': 'm',
    'fixed_window_fuzzy': 'y',
    'fixed_window_fully_fuzzy': 'g',
    'variable_window_fully_fuzzy': 'k',
    'adaptive_fixed_window_fuzzy': 'tab:brown',
    'adaptive_variable_window_fuzzy': 'tab:olive',
    'adaptive_realtime_fuzzy':'tab:gray',
    'realtime_fuzzy':'tab:purple'
    }
from sklearn.linear_model import LinearRegression
def simulate():
    path = "/Users/mostafa/python/filter_trajectory/results/old/vip"
    wb_path = path + "/summary_all.xls"
    generateResults(wb_path, path)
    
def removeNan(array): 
    return array[~np.isnan(array)]
def applyRegression(trajectory): 
    x = np.array(list(map(lambda p: p.longitude, trajectory))).reshape((-1,1))
    y = np.array(list(map(lambda p: p.latitude, trajectory))).reshape((-1,1))
    
    model = LinearRegression().fit(x, y)
    y_pred = model.predict(x)
    for i in range(0, len(trajectory)): 
        trajectory[i].latitude = y_pred[i]
    return trajectory
def generateResults(filename, path): 
    xls = pd.ExcelFile(filename)
    results = []
    names = []
    colors = []
    for sheet_name in xls.sheet_names: 
        sheet = pd.read_excel(xls, sheet_name)
        colors.append(ORIGINAL_COLORS[sheet_name])
        data = pd.DataFrame(sheet, columns=['Error', 'Time', 'Compression Ratio', 'Size'])
        results.append(generateStatisticsFor(data, sheet_name, path))
        names.append(sheet_name)
    
    
    colorIndex = 0
    graphs = []
    comparison_types = ['error', 'time']
    index = 0
    for i in range(0,2): 
        graphs = []
        index = 0
        for result in results: 
            if len(result[i]) > 0: 
                trajectory = applyRegression(result[i])
                graphs.append([trajectory, colors[colorIndex], xls.sheet_names[index], xls.sheet_names[index]])
            colorIndex += 1
            colorIndex %= len(colors)
            index += 1
        if comparison_types[i] == 'error': 
            yrange = list(np.arange(0,0.05,2e-3))
        else: 
            yrange = list(np.arange(1000,80000,5000))
        plotGraphs(graphs, path + "/" + 'overall' + "_ratio_" + comparison_types[i] + ".png", comparison_types[i], yrange)    
    generateSummary(filename)
    return names

def generateSummary(filename): 
    xls = pd.ExcelFile(filename)
    WB = Workbook()
    output_sheet = WB.add_sheet('statistics')
    # Add Headers
    for name,index in [['Name', 0], ['Time per 1k point (ms)', 1], ['Average Error', 2],['Average Ratio',3]]: 
        output_sheet.write(0, index, name)
    index = 1
    for sheet_name in xls.sheet_names: 
        sheet = pd.read_excel(xls, sheet_name)
        data = pd.DataFrame(sheet, columns=['Size','Error', 'Time', 'Compression Ratio'])
        result = [sheet_name] + generateSummaryForApproach(data)    
        for item_index,item in enumerate(result): 
            output_sheet.write(index,item_index ,item)
        index +=1 
    
    WB.save(filename.replace('summary', 'statitics'))
    return
def generateSummaryForApproach(data): 
    total_size = sum(data['Size']) 
    count = len(data['Error'])
    average_error = sum(data['Error']) / count
    average_ratio = sum(data['Compression Ratio']) / count
    average_time_per_k = 1000 * sum(data['Time']) / total_size
    return [average_time_per_k, average_error, average_ratio]
    
    
def convertToPoints(key, data,comp = True): 
    points = []
    for i in range(0,len(data)): 
        # if data['Compression Ratio'][i] < 70: 
        if comp: 
            p1 = data["Compression Ratio"][i]
        else: 
            p1 = data["Size"][i]
        p2 = data[key][i]
        if not (p1 is np.nan or p2 is np.nan):
            points.append(Point(p1,p2))
    return points
def generateStatisticsFor(data, type,path): 
    # Sort Data by compression Ratio
    data = data.sort_values(by=['Compression Ratio'])
    result = []
    for key in ['Error', 'Time']: 
        comp = key == 'Error'
        points = convertToPoints(key, data,comp)
        #print("Size of points for key  " + key + " = " + str(len(points)))
        c = 1e3
        trajectory = list(map(lambda p: Point(math.log(p.longitude * c, TIME_LOG_BASE),math.log(p.latitude * c, TIME_LOG_BASE)), points))
        result.append(trajectory)
        plotGraphs([[points, 'b',type]], path + "/" + type + "_ratio_" + key + ".png", title=key)
    return result

def unique(list1):
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list
 


#begin from statistics import *
# filename = "summary.xls"
# grs = generateResults(filename,'results2')
#edn