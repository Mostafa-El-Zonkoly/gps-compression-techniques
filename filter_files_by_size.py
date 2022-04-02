from read_input import * 
def calculateResults(size):
    with open('files_stats.txt') as f:
        lines = f.readlines()
    data =[]
    f = open('files.txt', "w+")
    isFirst  = True
    for l in lines[0: len(lines)]: 
        filename, s = l.split(',')
        if int(s) >= size: 
            if not isFirst: 
                f.write("\n")
            f.write(filename)
            isFirst = False
            
    f.flush
        
        


def prepareData():

    with open('files_all.txt') as f:
        lines = f.readlines()
    data = []
    f = open('files_stats.txt', "w+")
    isFirst = True
    for l in lines[len(data):len(lines)]: 
        line = l.strip() 
        filename = line + ".csv"
        d,e = readInput(filename)
        if not isFirst: 
                f.write("\n")
        isFirst = False
        f.write(line + "," + str(len(d)) + "\n")
    f.flush
    
#prepareData()

calculateResults(size = 5e3)
