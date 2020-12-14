 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import dates as mpldates
from matplotlib import style
import time
from helpers.common import LastNlines

from datetime import datetime
style.use('fivethirtyeight')

buffer_size = 7
output_filename = "randomdatatest.csv"


fig, axs = plt.subplots(2, 2)
fig.suptitle('Grid of subplots')
axs[0,0].set_title('Pace')
axs[0,1].set_title('Force')
axs[1,0].set_title('SPM')
axs[1,1].set_title('Distance')


# setup the figure


def process_data_for_plots(i):

	lines = LastNlines(output_filename, buffer_size)
	data = []
	plt.cla() # clears the axis 


	# reader = csv.reader(csvfile, skipinitialspace=True)
	# data.append(tuple(next(reader))) # Header
	# "time": monitor['time'],
	# 		"dist": monitor['distance'],
	# 		"spm": monitor['spm'],
	# 		"pace": monitor['pace'],
	# 		"force": force
	# print(len(lines))
	for line in lines:
		# print(line.split(","))
		time, dist, spm, pace, force = line.split(",")
		try:
			data.append((float(time), float(dist), int(spm), float(pace), [int(f) for f in force.split(";")]))
		except Exception:
			data.append(tuple(line))

	

		axs[0,0].plot( [item[3] for item in data],  label="pace") # 'rs', ms=6
		axs[0,1].plot( forces, label="force")
		axs[1,0].plot( [item[2] for item in data], label="spm")
		axs[1,1].plot( [item[1] for item in data], label="distance")
	

	plt.draw()
	plt.pause(0.01)
	

ani = animation.FuncAnimation(fig, process_data_for_plots, interval=1000)
plt.show()
# data_source.run()