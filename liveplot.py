 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import dates as mpldates
from matplotlib import style
import time
from datetime import datetime
style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

axes = plt.gca()
axes.set_ylim([0,1023])

def animate(i):
    graph_data = open('test_jack_data2.csv','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))#datetime.fromtimestamp(
            ys.append(float(y))
    # dates = mpldates.date2num(xs)
    ax1.clear()
    ax1.plot(xs, ys)

#swap the comments on the following 2 lines to get an static plot instead of a live plot
ani = animation.FuncAnimation(fig, animate, interval=500)
# animate(1)
plt.show()