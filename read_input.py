import csv
from point import Point as Point
def readInput(filename=None):
    #filename = 'input/dact_easy.csv'
    #filename = 'input/dact_strict.csv'
    #filename = 'input/geolife/010/Trajectory/20081219114010.csv'
    if filename is None: 
        filename = "input/geolife/002/Trajectory/20081023124523.csv"
    
    with open(filename) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = -1
        data = []
        keys = []
        data_list = []
        for row in csv_reader: 
            if line_count == -1: 
                # the keys
                keys = row
                keys.append(4)
                keys.append(5)
            # elif line_count == 0: 
            #     print("Column names" + str(row))
            elif line_count != 0:  
                data_row = []
                point = Point(row[int(keys[0])], row[int(keys[1])], row[int(keys[2])], row[int(keys[3])], row[int(keys[4])],row[int(keys[5])])
                # for key in keys: 
                #     data_row.append(float(row[int(key)]))
                data.append(point)
                
                data_list.append([float(row[int(keys[0])]), float(row[int(keys[1])])])
            line_count += 1
    return data, data_list
