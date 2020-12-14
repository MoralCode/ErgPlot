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
	