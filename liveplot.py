 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import dates as mpldates
from matplotlib import style
import time
from helpers.common import LastNlines, calculate_differential, convert_to_rpm

from datetime import datetime
style.use('fivethirtyeight')

buffer_size = 50
output_filename = "10k.csv"




# change the book to true and paste data in here  to display a fixed graph
fixed_graph = False
buffer = []


# setup the figure
fig, axs = plt.subplots(2, 2)
fig.suptitle('Grid of subplots')
axs[0,0].set_title('Impulse')
axs[0,1].set_title('Force')
axs[1,0].set_title('RPM')
axs[1,1].set_title('Work')


# setup the figure


def process_data_for_plots(i):

	lines = []
	# try:
	lines = LastNlines(output_filename, buffer_size)

	data = []
	forces = []

	# clear all the axes
	# plt.cla()
	for row in range(len(axs)):
		for col in range(len(axs)):
			axs[row,col].clear()
			axs[0,0].set_title('Impulse')
			axs[0,1].set_title('Force')
			axs[1,0].set_title('RPM')
			axs[1,1].set_title('Work')
	if not fixed_graph:
		# print(lines)
		for line in lines:
			line = line.strip()
			time, dist, spm, pace, sdist, drivetime, _, _, _, _, impulse, _, work, force = line.split(",")
			
			try:
				fdata = []
				if force != "":
					fdata = [int(f) for f in force.split(";")]

				newpoint = (float(time), float(dist), float(spm), float(pace), float(sdist), float(drivetime), float(impulse), float(work), fdata)
				# print(newpoint)
				data.append(newpoint)
				forces.extend(fdata)
			except Exception as e:
				
				data.append(tuple(line))
				# exit(0)
	axs[0,0].plot( [item[6] for item in data[1:]],  label="impulse") # 'rs', ms=6
	axs[0,1].plot( forces, label="force")
	axs[1,0].plot( differentials_over(data[1:], value_key=1, time_key=0, calculate_rpm=True), label="rpm")
	axs[1,1].plot( [item[7] for item in data[1:]], label="Work")

	plt.legend(loc='upper right')

	plt.draw()
	plt.pause(0.01)
	# except Exception as e:
	# 	print("Error plotting data")
	# 	print(e)


last_dist = 0
last_duration = 0





def differentials_over(data, average_over=0, value_key="value", time_key="timestamp", calculate_rpm=False):
	
	smoothed_data = []
	# for every other data point
	for i in range(len(data)-1):
		if i <= average_over:
			# ignore the first average_over number of datapoints as none of them are able to be smoothed due to not enough preceeding datapoints
			smoothed_data.append(0)#data[i][value_key]
			
		else:
			diff = calculate_differential(
				data[i-1-average_over][value_key],
				data[i-1-average_over][time_key],
				data[i][value_key],
				data[i][time_key]
				)
			if calculate_rpm:
				diff = convert_to_rpm(diff)
			# smooth the data
			smoothed_data.append(diff)
	return smoothed_data





ani = animation.FuncAnimation(fig, process_data_for_plots, interval=500)

plt.show()
print(buffer)
# print(get_pace_values())