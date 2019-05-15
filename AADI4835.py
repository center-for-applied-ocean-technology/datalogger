from BaseSensor import BaseSensor 
import time 
import traceback 
from math import sin, cos, radians, degrees, atan2 
from numpy import average 
from datetime import datetime 

class AADI4835(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(AADI4835, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self.version = 1.0
		self._ignoreFields = ["timestamp","duration","warm_time"] #fields that will not have simple averaging
		self.sample=	{
					"oxygen_concentration_avg":{},
					"temperature_avg":{},
					"air_saturation_avg":{},
					"timestamp":{},
					"duration":{},
					"warm_time":{}
				}
		self.sample['oxygen_concentration_avg']['maxlimit'] = 999999 
		self.sample['oxygen_concentration_avg']['minlimit'] = 0
		self.sample['oxygen_concentration_avg']['units'] = 'mg/l'
		self.sample['oxygen_concentration_avg']['offset'] = 0
		self.sample['oxygen_concentration_avg']['multiplier'] = 1
		
		self.sample['temperature_avg']['maxlimit'] = 999999 
		self.sample['temperature_avg']['minlimit'] = -273
		self.sample['temperature_avg']['units'] = 'C'
		self.sample['temperature_avg']['offset'] = 0
		self.sample['temperature_avg']['multiplier'] = 1

		self.sample['air_saturation_avg']['maxlimit'] = 999999 
		self.sample['air_saturation_avg']['minlimit'] = 0
		self.sample['air_saturation_avg']['units'] = 'C'
		self.sample['air_saturation_avg']['offset'] = 0
		self.sample['air_saturation_avg']['multiplier'] = 1

	def _getDataset(self):
		try:
			start = datetime.now()
			while True:
				if (datetime.now()-start).total_seconds() > 5:
					dataSet = None
					break

				self._reader.write("do sample\r\n")
				time.sleep(2)
				line = self._reader.read(self._reader.inWaiting())

				self._reader.write("get temperature\r\n")
				time.sleep(.25)
				line = self._reader.read(self._reader.inWaiting())
				line = line.replace('#', '')
				line = line.strip()
				time.sleep(5)
				temperature = float(line.split('\t')[3])

				self._reader.write("get O2Concentration\r\n")
				time.sleep(.25)
				line = self._reader.read(self._reader.inWaiting())
				line = line.replace('#', '')
				line = line.strip()
				o2 = float(line.split('\t')[3])/31.9988;

				self._reader.write("get AirSaturation\r\n")
				time.sleep(.25)
				line = self._reader.read(self._reader.inWaiting())
				line = line.replace('#', '')
				line = line.strip()
				air_saturation = float(line.split('\t')[3])
				
				dataSet = {	"temperature": temperature,
							"oxygen_concentration": o2, # mg/l
							"air_saturation": air_saturation,
							"timestamp":start,
							"duration":self._settings["sample_duration"],
							"warm_time":self._settings["warm_time"]
						}
				static = None
				break
				
		except:
			dataSet = None
			staticInfo = None
			print traceback.print_exc()
			
		return dataSet, None
	def getNMEA(self, format):
		try:
			start = datetime.now()
			while True:
				if (datetime.now() - start).total_seconds() > 5:
					dataSet = None
					break
				line = self.readline()
				line = self.checkNmeaLine(line)
				if line:
					data = line.split(',')
					sentFormat = data[0][2:]
					
					if sentFormat == format:
						return "$"+line+"\r\n"
						
				
		except:
			return None
			print traceback.print_exc()

	def _setNMEA(self):

		self.NMEA = "$PO2,%.2f,%.2f,%.2f"%(self.sample["temperature"], self.sample["oxygen_concentration"], self.sample["air_saturation"]);
		self.NMEA = self.NMEA+"*%s\r\n"%self._createNmeaChk(self.NMEA)
