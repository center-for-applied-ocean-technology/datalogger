from BaseSensor import BaseSensor 
import time 
import traceback 
from math import sin, cos, radians, degrees, atan2 
from numpy import average 
from datetime import datetime 
import seawater
class AADI4319(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(AADI4319, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self.version = 1.0
		self._ignoreFields = ["timestamp","duration","warm_time"] #fields that will not have simple averaging
		self.sample=	{
					"conductivity_avg":{},
					"temperature_avg":{},
					"salinity_avg":{},
					"warm_time":{},
					"duration":{},
					"timestamp":{}
				}
		self.sample['conductivity_avg']['maxlimit'] = 999999 
		self.sample['conductivity_avg']['minlimit'] = 0
		self.sample['conductivity_avg']['units'] = 'tbd'
		self.sample['conductivity_avg']['offset'] = 0
		self.sample['conductivity_avg']['multiplier'] = 1
		
		self.sample['temperature_avg']['maxlimit'] = 999999 
		self.sample['temperature_avg']['minlimit'] = -273
		self.sample['temperature_avg']['units'] = 'C'
		self.sample['temperature_avg']['offset'] = 0
		self.sample['temperature_avg']['multiplier'] = 1

		self.sample['salinity_avg']['maxlimit'] = 999999 
		self.sample['salinity_avg']['minlimit'] = 0
		self.sample['salinity_avg']['units'] = 'PSS-78'
		self.sample['salinity_avg']['offset'] = 0
		self.sample['salinity_avg']['multiplier'] = 1

	def _getDataset(self):
		try:
			start = datetime.now()
			while True:
				if (datetime.now()-start).total_seconds() > 5:
					dataSet = None
					break

				self._reader.write("do_sample\r\n")
				time.sleep(.5)
				line = self._reader.read(self._reader.inWaiting())

				self._reader.write("get temperature\r\n")
				time.sleep(.25)
				line = self._reader.read(self._reader.inWaiting())
				line = line.replace('#', '')
				line = line.strip()
				temperature = float(line.split('\t')[3])

				self._reader.write("get conductivity\r\n")
				time.sleep(.25)
				line = self._reader.read(self._reader.inWaiting())
				line = line.replace('#', '')
				line = line.strip()
				cond = float(line.split('\t')[3]);

				ref= 42.914
                                salinity = seawater.salt(cond/ref,temperature,10)

				dataSet = {	"temperature": temperature,
						"conductivity": cond, # mg/l
						"timestamp": start,
                                                "salinity": salinity
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

		self.NMEA = "$PO2,%.2f,%.2f,%.2f"%(self.sample["temperature"], self.sample["conductivity"]);
		self.NMEA = self.NMEA+"*%s\r\n"%self._createNmeaChk(self.NMEA)
