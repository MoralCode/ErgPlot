import time
from datasources.concept2 import Concept2

data_source = Concept2()


data_source.setup()

def test_data_rate(function):
	last_val = function()
	update_time_millis = 0

	while True:
		val = function()
		if val != last_val:
			current_millis = int(round(time.time() * 1000))
			delta = current_millis - update_time_millis
			update_time_millis = current_millis
			last_val = val
			print("Updated Value after " + str(delta) + " milliseconds: " + str(val))
		time.sleep(0.01)


test_data_rate(data_source.get_stroke_stats)


