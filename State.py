import threading
import State
import time
import os
lock  = threading.Lock()
heading = None
latitude = None
longitude = None
windspeed = None
enabled = False
met = None
adcp = None
wave = None
pos = None


def getPos():
	return pos
	
def getHeading():
	return heading

def setPos(timestamp, latitude, longitude):
	State.lock.acquire()
	State.pos= [timestamp, latitude, longitude]
	State._writeStateFile()
	State.lock.release()

def setHeading(timestamp, heading):
	State.lock.acquire()
	State.heading = [timestamp, heading]
	State._writeStateFile()
	State.lock.release()

def setWindspeed(timestamp, windspeed, direction):
	State.lock.acquire()
	State.windspeed = [timestamp, windspeed, direction]
	State._writeStateFile()
	State.lock.release()

def setMetData(timestamp, pressure, air_temp, dew_point, relative_humidity):
	State.lock.acquire()
	State.met = [timestamp, pressure, air_temp, dew_point, relative_humidity]
	State._writeStateFile()
	State.lock.release()

def setADCP(sample):
	State.lock.acquire()
	State.adcp = sample
	State._writeStateFile()
	State.lock.release()
	
def setWave(sample):
	State.lock.acquire()
	State.wave= sample
	State._writeStateFile()
	State.lock.release()
	
def _writeStateFile():
	try:
		tmp_filename = "/mnt/ramdisk/.state.txt"
		filename = "/mnt/ramdisk/state.txt"
		file = open(tmp_filename, "w")

		if ~State.enabled:
			file.write("Disabled in ini file\n")
		else:

			file.write("Current Time = %s\n" % time.asctime())

			if heading != None:
				file.write("\nHeading\n")
				file.write("\nHeading = %f\n" % State.heading[1])
				file.write("Timestamp = %s\n" % State.heading[0])

			if pos != None:
				file.write("\nGPS\n")
				file.write("Latitude = %f\n" % State.pos[1])
				file.write("Longitude = %f\n" % State.pos[2])
				file.write("Timestamp = %s\n" % State.pos[0])

			if windspeed != None:
				file.write("\nWind\n")
				file.write("\nWind Speed = %s\n" % State.windspeed[1])
				file.write("Wind Direction = %s\n" % State.windspeed[2])
				file.write("Timestamp = %s\n" % State.windspeed[0])

			if met != None:
				file.write("\nMet Sensor\n")
				file.write("Air Pressure = %s\n" % State.met[1])
				file.write("Air Temperature = %s\n" % State.met[2])
				file.write("Dew Point= %s\n" % State.met[3])
				file.write("Relative Humidity = %s\n" % State.met[4])
				file.write("Timestamp = %s\n" % State.met[0])
				
			if adcp != None:
				file.write("\nADCP\n")
				for key,value in sorted(State.adcp.items()):
					for key1,value1 in sorted(value.items()):
						if key1 == "value":
							file.write("%s %s\n" % (key, value1))
			if wave != None:
				file.write("\nWaves\n")
				for key,value in sorted(State.wave.items()):
					file.write("%s %s\n" % (key, value))
		
		
		file.close()
		os.rename(tmp_filename,filename);
		
	except:
		file.close()
		os.rename(tmp_filename,filename);

