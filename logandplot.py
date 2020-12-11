
# Code based on: https://stackoverflow.com/a/38486971
# modified for RMP-specific data collection and to flush the buffer to a file every time it fills up so that data can be analyzed later
from collections import deque
import numpy as np
import pylab as plt
import csv, time, math
from random import *

estimated_rpm= 800
seconds_of_data = 5
fraction_of_minute = seconds_of_data/60
buffer_size = math.ceil(estimated_rpm * fraction_of_minute) # how many data points you want to plot at any given time
#data_buffer = np.zeros( buffer_size) # this is where you will keep the latest data points
data_buffer = deque()

datapoints_added_since_flush = 0
output_filename = "randomdatatest.csv"

#initialize buffer to 0
for i in range( buffer_size):
    data_buffer.append([0,0])

# random = np.random.random( ) # some random temperature data, i dunno

# setup the figure
fig = plt.figure(1)
plt.suptitle('Previous %d datapoints'%buffer_size, fontsize=12)
ax = plt.gca()

# 	try:
	# ser_bytes = ser.readline()
	# decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
	# if (float(decoded_bytes) >0.0 ):
	# 	print(decoded_bytes)

def new_datapoint(datapoint):
	global datapoints_added_since_flush
	if datapoints_added_since_flush == buffer_size:
		# flush to disk
		print("Flushing to disk")
		with open(output_filename,"a") as f:
			writer = csv.writer(f,delimiter=",")
			for sample in data_buffer:
				writer.writerow(sample)
		datapoints_added_since_flush = 0
		print("Done.")
	# either way, write new datapoint
	data_buffer.popleft()
	data_buffer.append(datapoint)
	datapoints_added_since_flush += 1	



while True:
    #data_buffer = np.roll( data_buffer, shift=-1)
    #data_buffer[ -1] = Temp
    new_datapoint([time.time(),random()])
    ax.plot( [item[1] for item in data_buffer], 'rs', ms=6) # whatever style you want...
    plt.draw()
    plt.pause(0.01)
    plt.cla() # clears the axis 
    



# import serial
# import time
# import csv

# ser = serial.Serial('/dev/ttyACM0', 9600)
# ser.flushInput()

# while True:
# 	# try:
# 	ser_bytes = ser.readline()
# 	decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
# 	if (float(decoded_bytes) >0.0 ):
# 		print(decoded_bytes)
# 	with open("test_jack_data2.csv","a") as f:
# 		writer = csv.writer(f,delimiter=",")
# 		writer.writerow([time.time(),decoded_bytes])
# 	# except Exception as e:
# 	# 	print(e)
# 	# 	print("Keyboard Interrupt")
	# 	break


 
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib import dates as mpldates
# from matplotlib import style
# import time
# from datetime import datetime
# style.use('fivethirtyeight')

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

# axes = plt.gca()
# axes.set_ylim([0,1023])

# def animate(i):
#     graph_data = open('test_jack_data2.csv','r').read()
#     lines = graph_data.split('\n')
#     xs = []
#     ys = []
#     for line in lines:
#         if len(line) > 1:
#             x, y = line.split(',')
#             xs.append(float(x))#datetime.fromtimestamp(
#             ys.append(float(y))
#     # dates = mpldates.date2num(xs)
#     ax1.clear()
#     ax1.plot(xs, ys)

# #swap the comments on the following 2 lines to get an static plot instead of a live plot
# ani = animation.FuncAnimation(fig, animate, interval=500)
# # animate(1)
# plt.show()