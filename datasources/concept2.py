from pyrow import pyrow
from datasources.datasouce import DataSourceInterface, Status
from helpers.status import State
from helpers.common import separate_values
import enum, time


def default_empty_event_handler(obj):
	print('empty handler for id={}'.format(obj.the_id))

class Concept2(DataSourceInterface):

	def __init__(self): 
		self.erglist = list(pyrow.find())
		self.status = Status(State.WAITING, "")
		self.buffer = []
		self.on_new_data_point = default_empty_event_handler
		# self.run = True

	def setup(self):
		assert len(self.erglist) > 0, "Please connect an erg via USB to be able to log data"
		self.erg = pyrow.PyErg(self.erglist[0])
		print("Connected to Erg")

	# This method is heavily based on the code from Py3Row's superceded samples https://github.com/MoralCode/Py3Row/commit/f52501585ec2fa06fb1cb75f8dac60b2829ebb02
	def run(self):
		workout = self.erg.get_workout()

		#Loop until workout has begun
		self.status = Status(State.WAITING, "Waiting for workout to start.")
		print("Waiting for workout to start.")
		while workout['state'] == 0:
			time.sleep(1)
			workout = self.erg.get_workout()

		#Loop until workout ends
		print("Recording Data.")
		while workout['state'] == 1:

			#Record forcecurve data during the drive
			self.collect_data()
			# update workout var so the loop eventually stops
			workout = self.erg.get_workout()
			#Loop during drive

	def collect_data(self):
		monitor = self.erg.get_monitor()
		forceplot = self.erg.get_forceplot()
		strokedata = self.new_data_point(monitor, forceplot['forceplot'], self.get_stroke_stats())
		self.on_new_data_point(strokedata)
		# strokestats = self.get_stroke_stats()
			


	def get_status(self):
		return self.status

	def get_buffer_size(self):
		return len(self.buffer)

	def new_data_point(self, monitor, forcecurve, stats):
		return {
			"time": monitor['time'],
			"dist": monitor['distance'],
			"spm": monitor['spm'],
			"pace": monitor['pace'],
			"strokestats": stats,
			"forcecurve": forcecurve
		}
		
	
	def data_point_to_csv(self, datapoint):
		forcedata = datapoint.pop('forcecurve', [])
		strokestatsdata = datapoint.pop('strokestats', [])
		# manually convert forcecurve data to CSV as it wont get processed properly by the builtin library
		csv_ready = {**datapoint, **strokestatsdata}
		# datapoint["strokestats"] = separate_values(strokestatsdata.values())
		csv_ready["forcecurve"] = separate_values(forcedata, separator=";")
		return csv_ready

	def get_monitor_data(self):
		return self.erg.get_monitor()

	def get_raw_pace(self):
		# CSAFE_SETUSERCFG1_CMD + CSAFE_PM_GET_STROKESTATS
		command_name = 'CSAFE_GETPACE_CMD'
		command = [command_name, ]
		return self.get_raw_csafe(command)[command_name][0]

	def get_stroke_stats(self):
		# CSAFE_SETUSERCFG1_CMD + CSAFE_PM_GET_STROKESTATS
		command = ['CSAFE_PM_GET_STROKESTATS', 0]

		# SEE PAGE 56 of the pdf
		#  A maximum block length of 32 bytes (16 words) can be read. Fewer words can be read by specifying
		# the block length accordingly, but a complete 33 bytes of response data will be returned. Only data
		# samples recorded since the last read will be returned. The first byte of the response will indicate how
		# many valid data bytes are returned.
		result = self.get_raw_csafe(command)
		# print(result)
		# print(result['CSAFE_PM_GET_STROKESTATS'])
		result_dict = {
			"distance": result['CSAFE_PM_GET_STROKESTATS'][0],
			"drivetime": result['CSAFE_PM_GET_STROKESTATS'][1],
			"recoverytime": result['CSAFE_PM_GET_STROKESTATS'][2],
			"strokelength": result['CSAFE_PM_GET_STROKESTATS'][3],
			"strokecount": result['CSAFE_PM_GET_STROKESTATS'][4],
			"peakforce": result['CSAFE_PM_GET_STROKESTATS'][5],
			"impulseforce": result['CSAFE_PM_GET_STROKESTATS'][6],
			"avgforce": result['CSAFE_PM_GET_STROKESTATS'][7],
			"work": result['CSAFE_PM_GET_STROKESTATS'][8]
		}
		return result_dict

	def get_raw_csafe(self, command):
		# 'CSAFE_GETPACE_CMD'
		if type(command) not in (list, tuple):
			command = [command,]
		result = self.erg.send(command)
		return result

	def get_data_point(self):
		assert len(self.buffer) > 0, "No Data in Buffer"
		return self.buffer.pop(0) # treat the buffer like a queue
