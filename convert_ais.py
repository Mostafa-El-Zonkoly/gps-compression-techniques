import csv
import time
from datetime import datetime

file = '/Users/mostafa/Downloads/ais.csv'
result = {}
keys = []
with open(file, 'rt') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        key = row[1]
        if key in result:
            result[key].append(row)
        else:
            keys.append(key)
            print(key)
            result[key] = [row]
directory = '/Users/mostafa/python/filter_trajectory/ais_data'
for key in keys: 
    if len(result[key]) > 1000: 
        filePath = directory + "/1k/" + key + ".csv"
    else:  
        filePath = directory + '/' + key + ".csv"
    file = open(filePath, 'w')
    file.write("2,3,4,5,0,6\n")
    file.write("t,shipid,lon,lat,heading,course,speed,shiptype,destination")

    for row in result[key]: 
        file.write("\n")
        if key != 'shipid': 
            row[0] = time.mktime(datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%SZ').timetuple())
        file.write(','.join(str(item) for item in row))
    file.close

