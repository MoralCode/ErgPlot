from pyrow import pyrow
from datasources.datasouce import DataSourceInterface, Status
from helpers.status import State
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
		while workout['state'] == 1:

			forceplot = self.erg.get_forceplot()
			#Loop while waiting for drive
			self.status = Status(State.READY, "Waiting for drive.")
			print("Waiting for drive.")
			while forceplot['strokestate'] != 2 and workout['state'] == 1:
				#ToDo: sleep?
				forceplot = self.erg.get_forceplot()
				workout = self.erg.get_workout()

			self.status = Status(State.RECORDING, "Recording Data.")
			print("Recording Data.")
			#Record forcecurve data during the drive
			forcecurve = forceplot['forceplot'] #start of pull (when strokestate first changed to 2)
			monitor = self.erg.get_monitor() #get monitor data for start of stroke
			#Loop during drive
			while forceplot['strokestate'] == 2:
				#ToDo: sleep?
				forceplot = self.erg.get_forceplot()
				forcecurve.extend(forceplot['forceplot'])

			forceplot = self.erg.get_forceplot()
			forcecurve.extend(forceplot['forceplot'])

			#save data to buffer
			print("SaveData")
			strokedata = self.new_data_point(monitor, forcecurve)

			
			self.buffer.append(strokedata)
			self.on_new_data_point()


	def get_status(self):
		return self.status

	def get_buffer_size(self):
		return len(self.buffer)

	def new_data_point(self, monitor, forcecurve):
		return {
			"time": monitor['time'],
			"dist": monitor['distance'],
			"spm": monitor['spm'],
			"pace": monitor['pace'],
			"forcecurve": forcecurve
		}
		
	
	def data_point_to_csv(self, datapoint):
		forcedata = datapoint.pop('forcecurve', [])
		data = list(datapoint.values())

		# Convert data to CSV
		forcedata = ";".join([str(f) for f in forcedata])
		strokedata = ",".join([str(p) for p in data])
		datapoint["forcecurve"] = forcedata
		return datapoint

	def get_data_point(self):
		assert len(self.buffer) > 0, "No Data in Buffer"
		return self.buffer.pop(0) # treat the buffer like a queue
