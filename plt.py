import matplotlib.pyplot as plt
import numpy as np
def plotWithTitle(x, title): 
    plt.cla
    fig = plt.figure()
    ax=fig.gca()
    ax.plot([0,x,10 * x], [1,1,0],color='r',label="Same Segment")
    ax.plot([x, 10 * x,1.4 * 10 * x], [0,1,1],color='b', label="New Segment")
    ax.legend()
    plt.savefig(title + '.png')
    plt.close()

plotWithTitle(5e-3, 'heading_mf')
plotWithTitle(5e-3 * 10e3, 'distance_mf')

