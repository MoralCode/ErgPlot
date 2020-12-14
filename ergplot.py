
# Code based on: https://stackoverflow.com/a/38486971
# modified for RMP-specific data collection and to flush the buffer to a file every time it fills up so that data can be analyzed later
from collections import deque
import numpy as np
import pylab as plt
import csv, time, math
from random import *
from datasources.concept2 import Concept2

estimated_rpm= 800
seconds_of_data = 5
fraction_of_minute = seconds_of_data/60
buffer_size = math.ceil(estimated_rpm * fraction_of_minute) # how many data points you want to plot at any given time
#data_buffer = np.zeros( buffer_size) # this is where you will keep the latest data points
data_buffer = deque()

datapoints_added_since_flush = 0
output_filename = "10k.csv"

data_source = Concept2()

#initialize buffer to 0
for i in range( buffer_size):
	data_buffer.append({
			"time": 0,
			"dist":0,
			"spm": 0,
			"pace": 0,
			"force": []
		})

# random = np.random.random( ) # some random temperature data, i dunno




def buffer_new_datapoint(datasource, datapoint):
	global datapoints_added_since_flush, buffer_size
	if datapoints_added_since_flush == buffer_size:
		# flush to disk
		print("Flushing to disk")
		with open(output_filename,"a") as f:
			writer = csv.writer(f,delimiter=",")
			for sample in data_buffer:
				writer.writerow(datasource.data_point_to_csv(sample))
		datapoints_added_since_flush = 0
		print("Done.")
	# either way, write new datapoint
	data_buffer.popleft()
	data_buffer.append(datapoint)
	datapoints_added_since_flush += 1	

def write_new_datapoint(datasource, datapoint):

	with open(output_filename,"a") as f:
		writer = csv.writer(f,delimiter=",")
		writer.writerow(datasource.data_point_to_csv(datapoint).values())


def handle_new_datapoint():
	raw_data = data_source.get_data_point()
	write_new_datapoint(data_source, raw_data)
	

data_source.setup()

data_source.on_new_data_point = handle_new_datapoint
data_source.run()


