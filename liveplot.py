 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import dates as mpldates
from matplotlib import style
import time
from helpers.common import LastNlines

from datetime import datetime
style.use('fivethirtyeight')

buffer_size = 10
output_filename = "10k.csv"


fig, axs = plt.subplots(2, 2)
fig.suptitle('Grid of subplots')


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
				axs[0,0].set_title('Impulse')
				axs[0,1].set_title('Force')
				axs[1,0].set_title('RPM')
				axs[1,1].set_title('Work')

		for line in lines:
			time, dist, spm, pace, sdist, drivetime, _, _, _, _, impulse, _, work, force = line.split(",")
			try:
				fdata = [int(f) for f in force.split(";")]
				data.append((float(time), float(dist), int(spm), float(pace), float(sdist), float(drivetime), int(impulse), int(work), fdata))
				forces.extend(fdata)
			except Exception:
				data.append(tuple(line))
	
		
		axs[0,0].plot( [item[6] for item in data],  label="impulse") # 'rs', ms=6
		axs[0,1].plot( forces, label="force")
		axs[1,0].plot( [convert_to_rpm(item[4], item[5]) for item in data], label="rpm")
		axs[1,0].plot( [item[4]/item[5] for item in data], label="dist/stroke")

		# plt.legend(loc='upper right')
		axs[1,1].plot( [item[7] for item in data], label="Work")
	
		# plt.legend(loc='upper right')

		plt.draw()
		plt.pause(0.01)
	except Exception as e:
		print("Error plotting data")
		print(e)
	
def convert_to_rpm(pace):
	speed = 1/(pace/500)
	return (speed*60*12.93)/3

ani = animation.FuncAnimation(fig, process_data_for_plots, interval=1000)
plt.show()