# Python implementation to 
# read last N lines of a file 
# Using OS module and buffering policy 
		
# importing os module 
# import os 
from collections import deque
from io import StringIO

# Function to read 
# last N lines of the file 
def LastNlines(fname, n): 
	with open(fname, 'r') as f:
		q = deque(f, n)  # replace 2 with n (lines read at the end)
		return list(q)
	
def separate_values(data, separator=","):
	return separator.join([str(value) for value in data])

def calculate_differential(start_val, start_time, end_val, end_time):
	return (end_val-start_val)/((end_time-start_time)/1000)

def convert_to_rpm(speed):
	# speed = 1/(pace/500)
	return (speed*60*12.93)/3