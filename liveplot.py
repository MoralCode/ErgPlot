 
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

from datasources.concept2 import Concept2

data_source = Concept2()


data_source.setup()

# setup the figure
fig = plt.figure(1)
plt.suptitle('Previous %d datapoints'%buffer_size, fontsize=12)
axs = plt.gca()


# setup the figure

buffer = []

def process_data_for_plots(i):

	lines = []
	try:
		# lines = LastNlines(output_filename, buffer_size)

		data = []
		forces = []

		# clear all the axes
		plt.cla()
		# for row in range(len(axs)):
		# 	for col in range(len(axs)):
		# 		axs[row,col].clear()
		# 		axs[0,0].set_title('Impulse')
		# 		axs[0,1].set_title('Force')
		# 		axs[1,0].set_title('RPM')
		# 		axs[1,1].set_title('Work')

		# for line in lines:
		# 	time, dist, spm, pace, sdist, drivetime, _, _, _, _, impulse, _, work, force = line.split(",")
		# 	try:
		# 		fdata = [int(f) for f in force.split(";")]
		# 		data.append((float(time), float(dist), int(spm), float(pace), float(sdist), float(drivetime), int(impulse), int(work), fdata))
		# 		forces.extend(fdata)
		# 	except Exception:
		# 		data.append(tuple(line))

		pace_val = get_pace_values()
		# print(pace_val)

		buffer.append(pace_val)
		
		axs.plot( [point["raw"] for point in buffer], label="raw")
		axs.plot( [point["differential"] for point in buffer], label="diff_real")
		axs.plot( [point["differential2"] for point in buffer], label="diff_erg")
		axs.plot( [point["stroke"] for point in buffer], label="stroke")
		# 3 different ways



		# axs[0,0].plot( [item[6] for item in data],  label="impulse") # 'rs', ms=6
		# axs[0,1].plot( forces, label="force")
		# axs[1,0].plot( [convert_to_rpm(item[4], item[5]) for item in data], label="rpm")
		# axs[1,0].plot( [item[4]/item[5] for item in data], label="dist/stroke")

		# plt.legend(loc='upper right')
		# axs[1,1].plot( [item[7] for item in data], label="Work")
	
		plt.legend(loc='upper right')

		plt.draw()
		plt.pause(0.01)
	except Exception as e:
		print("Error plotting data")
		print(e)
	
def convert_to_rpm(pace):
	speed = 1/(pace/500)
	return (speed*60*12.93)/3


last_dist = 0
last_duration = 0
timestamp = int(round(time.time() * 1000))

def get_differential_pace():
	global last_duration, last_dist, timestamp
	mon = data_source.get_monitor_data()

	delta_x = delta_t = delta_t2 = 0

	if mon["distance"] != last_dist or mon["time"] != last_duration:
		current_millis = int(round(time.time() * 1000))
		delta_t = (current_millis - timestamp)/1000
		delta_t2 = (mon["time"] - last_duration)/100
		delta_x = (mon["distance"] - last_dist)/10
		timestamp = current_millis
		last_dist = mon["distance"]
		last_duration = mon["time"]
	# substitute delta_t2 here for the erg-distance-based delta 
		# print(delta_x)
		# print(delta_t)
		# if time == "actual":
		return (delta_x/delta_t, delta_x/delta_t2)
	return 0




def get_stroke_pace():
	sp = data_source.get_stroke_stats()
	totaltime = (sp["drivetime"]+sp["recoverytime"])/100
	return (sp["distance"]/100)/totaltime

def get_pace_values():
	# # all of these should be in meters per second
	# point = {
	# 	"raw": convert_to_rpm(1/(data_source.get_raw_pace()/500)),
	# 	"differential": convert_to_rpm(get_differential_pace()),
	# 	"stroke": convert_to_rpm(get_stroke_pace())
	# }
	diff_real, diff_erg=get_differential_pace()
	point = {
		"raw": 1/(data_source.get_raw_pace()/500),
		"differential": diff_real,
		"differential2": diff_erg,
		"stroke": get_stroke_pace()
	}
	print(point)
	return point



ani = animation.FuncAnimation(fig, process_data_for_plots, interval=40)

plt.show()
print(buffer)
# print(get_pace_values())