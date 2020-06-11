import serial
import time
import csv

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.flushInput()

while True:
	# try:
	ser_bytes = ser.readline()
	decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
	if (float(decoded_bytes) >0.0 ):
		print(decoded_bytes)
	with open("test_jack_data2.csv","a") as f:
		writer = csv.writer(f,delimiter=",")
		writer.writerow([time.time(),decoded_bytes])
	# except Exception as e:
	# 	print(e)
	# 	print("Keyboard Interrupt")
	# 	break