# This file contains the interface thatdatasources should implement in order to be able to be swapped out
# See https://realpython.com/python-interface/ for info
from helpers.status import Status

class DataSourceInterface:

	def setup(self):
		raise NotImplementedError()
	
	def get_status(self) -> Status:
		raise NotImplementedError() 

	def has_unread_data(self) -> bool:
		raise NotImplementedError()

	# def flush_buffer(self) -> bool:
	#     raise NotImplementedError() 

	def get_data_point(self):
		pass

	def run(self):
		raise NotImplementedError() 

	def get_status(self):
		return self.status

	def get_buffer_size(self):
		return len(self.buffer)