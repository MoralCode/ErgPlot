 
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



# setup the figure
fig = plt.figure(1)
plt.suptitle('Previous %d datapoints'%buffer_size, fontsize=12)
ax = plt.gca()



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

	
	ax.plot( [item[3] for item in data], 'rs', ms=6) # whatever style you want...

	# ax2.plot( [force_sample for stroke in data_buffer for force_sample in stroke["force"]], 'rs', ms=6) # whatever style you want...
	

	plt.draw()
	plt.pause(0.01)
	

ani = animation.FuncAnimation(fig, process_data_for_plots, interval=1000)
plt.show()
# data_source.run()