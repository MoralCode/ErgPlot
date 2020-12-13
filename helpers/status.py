from enum import Enum
class State(Enum):
	ERROR = 0
	WAITING = 1
	READY = 2
	RECORDING = 3

class Status():
	state = State.WAITING
	message = ""

	def __init__(self, state, message):
		self.state = state
		self.message = message
	
	def get_state(self):
		return self.state

	def get_message(self):
		return self.message
