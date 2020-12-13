# Python implementation to 
# read last N lines of a file 
# Using OS module and buffering policy 
		
# importing os module 
import os 

# Function to read 
# last N lines of the file 
def LastNlines(fname, N): 
	# taking buffer size of 8192 bytes 
	bufsize = 8192
	
	# calculating size of 
	# file in bytes 
	fsize = os.stat(fname).st_size 
	
	iter = 0
	
	# opening file using with() method 
	# so that file get closed 
	# after completing work 
	with open(fname) as f: 
		if bufsize > fsize: 
				
			# adjusting buffer size 
			# according to size 
			# of file 
			bufsize = fsize-1
			
			# list to store  
			# last N lines 
			fetched_lines = [] 
			
			# while loop to 
			# fetch last N lines 
			while True: 
				iter += 1
				
				# moving cursor to 
				# the last Nth line 
				# of file 
				f.seek(fsize-bufsize * iter) 
				
				# storing each line 
				# in list upto 
				# end of file 
				fetched_lines.extend(f.readlines()) 
				
				# halting the program 
				# when size of list 
				# is equal or greater to 
				# the number of lines requested or 
				# when we reach end of file 
				if len(fetched_lines) >= N or f.tell() == 0: 
						# print(''.join(fetched_lines[-N:])) 
						return [line.strip() for line in fetched_lines]
						# break