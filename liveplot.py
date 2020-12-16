 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import dates as mpldates
from matplotlib import style
import time
from helpers.common import LastNlines

from datetime import datetime
style.use('fivethirtyeight')

buffer_size = 15
output_filename = "10k.csv"


fig, axs = plt.subplots(2, 2)
fig.suptitle('Grid of subplots')
axs[0,0].set_title('Pace')
axs[0,1].set_title('Force')
axs[1,0].set_title('SPM')
axs[1,1].set_title('Work')


# setup the figure


def process_data_for_plots(i):

	lines = []
	try:
		lines = LastNlines(output_filename, buffer_size)

		data = []
		forces = []

		# clear all the axes
		for row in range(len(axs)):
			for col in range(len(axs)):
				axs[row,col].clear()

		for line in lines:
			time, dist, spm, pace, work, force = line.split(",")
			try:
				fdata = [int(f) for f in force.split(";")]
				data.append((float(time), float(dist), int(spm), float(pace), int(work), fdata))
				forces.extend(fdata)
			except Exception:
				data.append(tuple(line))
	

		axs[0,0].plot( [item[3] for item in data],  label="pace") # 'rs', ms=6
		axs[0,1].plot( forces, label="force")
		axs[1,0].plot( [item[2] for item in data], label="spm")
		axs[1,1].plot( [item[4] for item in data], label="Work")
	
		# plt.legend(loc='upper right')

		plt.draw()
		plt.pause(0.01)
	except Exception:
		print("Error plotting data")
	

ani = animation.FuncAnimation(fig, process_data_for_plots, interval=1000)
plt.show()