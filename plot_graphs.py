import matplotlib.pyplot as plt
import numpy as np
import time
from point import Point as Point
def getList(point: Point):
    return [point.longitude, point.latitude]
def plotGraphs(graphs,outputfile, title='', yrange= None): 
    plt.cla
    # plt.xticks(list(np.arange(60,100,5)))
    # if yrange is not None: 
    #     plt.yticks(yrange)
    fig = plt.figure()#(figsize=(50,50))
    ax = fig.gca()

    for graph in graphs: 
        if len(graph) < 3:
            graph.append("")
        trajecotry = []
        for point in graph[0]: 
            if point.__class__ == Point: 
                trajecotry.append(getList(point))
            else: 
                trajecotry.append(point)
        # trajectory = list(map(lambda x: [x.longitude, x.latitude], graph[0]))
        points = np.array(trajecotry)
        if len(points) > 0: 
            ax.plot(points[:,0],points[:,1], color=graph[1], label=graph[2])

    ax.legend()
    if title == '': 
        title = outputfile
    plt.title(title)
    filename =  outputfile
    plt.savefig(filename)
    plt.close()
    return filename
    

# graph = [[[1,1], [2,2], [3,3],[4,4]], 'r']
# graph2 = [[[1,2], [2,3], [3,4], [4,5]], 'b']
# plotGraphs([graph, graph2])