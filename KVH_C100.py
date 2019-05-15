from BaseSensor import BaseSensor 
import time 
import traceback 
from math import sin, cos, radians, degrees, atan2 
from numpy import average 
from datetime import datetime 
import State

class KVH_C100(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(KVH_C100, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self.version = 1.0
		self._ignoreFields = ["timestamp","duration","warm_time"] #fields that will not have simple averaging
		self.sample=	{
					"heading_avg":{},
					"warm_time":{},
					"duration":{},
					"timestamp":{}
				}
		self.sample['heading_avg']['maxlimit'] = 360 
		self.sample['heading_avg']['minlimit'] = -360
		self.sample['heading_avg']['units'] = 'degees'
		self.sample['heading_avg']['offset'] = 0
		self.sample['heading_avg']['multiplier'] = 1
		

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
				line = self.readline()
				line = self.checkNmeaLine(line)
				data = line.split(',')
				sentFormat = data[0][2:]
				if sentFormat == 'HCHDT':
					try:
						float(data[1]);
					except:
						data[1] = -1;


				dataSet = {	"heading": float(data[1]),
						}
				State.setHeading(datetime.now(),float(data[1]))
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
		self.NMEA = "$PHEADING,%.2f,"%(self.sample["heading"]);
		self.NMEA = self.NMEA+"*%s\r\n"%self._createNmeaChk(self.NMEA)

