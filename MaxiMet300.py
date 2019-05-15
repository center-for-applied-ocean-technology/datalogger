from BaseSensor import BaseSensor 
import time 
import traceback 
from math import sin, cos, radians, degrees, atan2 
from numpy import average 
from datetime import datetime 
import State

class MaxiMet300(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(MaxiMet300, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self._ignoreFields = [] #fields that will not have simple averaging
		self.version = 1.0
		self.sample=	{"pressure_avg":{},
						"relative_humidity_avg":{}, #may be temp
						"air_temp_avg":{}, #may be temp
						"dew_point_avg":{},
						"voltage_avg":{}
						}
						
		self.sample['pressure_avg']['maxlimit'] = 99999
		self.sample['pressure_avg']['minlimit'] = 0
		self.sample['pressure_avg']['units'] = 'hPa'
		self.sample['pressure_avg']['offset'] = 0
		self.sample['pressure_avg']['multiplier'] = 99999

		self.sample['relative_humidity_avg']['maxlimit'] = 120
		self.sample['relative_humidity_avg']['minlimit'] = 0
		self.sample['relative_humidity_avg']['units'] = '%RH'
		self.sample['relative_humidity_avg']['offset'] = 0
		self.sample['relative_humidity_avg']['multiplier'] = 999999
		
		self.sample['air_temp_avg']['maxlimit'] = 50
		self.sample['air_temp_avg']['minlimit'] = -50
		self.sample['air_temp_avg']['units'] = 'deg C'
		self.sample['air_temp_avg']['offset'] = 0
		self.sample['air_temp_avg']['multiplier'] = 999999
		
		self.sample['dew_point_avg']['maxlimit'] = 120
		self.sample['dew_point_avg']['minlimit'] = 0
		self.sample['dew_point_avg']['units'] = 'deg C'
		self.sample['dew_point_avg']['offset'] = 0
		self.sample['dew_point_avg']['multiplier'] = 999999
		
		self.sample['voltage_avg']['maxlimit'] = 120
		self.sample['voltage_avg']['minlimit'] = 0
		self.sample['voltage_avg']['units'] = '%RH'
		self.sample['voltage_avg']['offset'] = 0
		self.sample['voltage_avg']['multiplier'] = 999999


	#def _turnOff(self):
	#	pass

	def _getDataset(self):
		try:
			dataSet = None
			start = datetime.now()
			while True:
				if (datetime.now()-start).total_seconds() > 5:
					dataSet = None
					break
				line = self.readline()
				
				#line = self.checkNmeaLine(line)
				#need to rewrite checkline for gill as it is not a nmea sentFormat
				line = self.checkLine(line)
				if line:
					data = line.split(',')
					State.setMetData(datetime.now(), data[1], data[3], data[4], data[2])
					dataSet = 	{	"pressure": float(data[1]),#true
									"relative_humidity": float(data[2]),
									"air_temp": float(data[3]),  
									"dew_point":float(data[4]),
									"voltage":float(data[6])
								}
								
					break
				
		except:
			dataSet = None
			staticInfo = None
			print traceback.print_exc()
			
		return dataSet, None
		

		
	def checkLine(self,line):
		
		try:
			line = line[1:]
			
			calc_cksum = 0
			for ch in line[0:line.rfind(',')+1]:
				
				calc_cksum ^= ord(ch)
			data = line.split(",")
			
			cksum = data[len(data)-1][1:]
			
			result = (int(cksum,16) == calc_cksum)
			if not result:
				line = False
		except ValueError:
			return False
		except:
			print traceback.print_exc()
		return line
	def _setNMEA(self):
		#broken code from trying to fix structure. 
		pass
		"""
		self.NMEA = "$PWX200,%.2f,%.2f,%.2f,%.2f"%(self.sample["air_pressure_avg"], self.sample["air_temperature_avg"], self.sample["wind_speed_avg"], self.sample["wind_from_direction_avg"]) 
		self.NMEA = self.NMEA+"*%s\r\n"%self._createNmeaChk(self.NMEA)
		gga = self.getGGA()
		self.NMEA = self.NMEA + gga
		data = gga.split(",")
		self.sample["time"] = data[1]

		if data[3] == "N": 
			self.sample["latitude"] = float(data[2]) #need to handle north/south
		else:
			self.sample["latitude"] = float(data[2]) * -1.0
		if data[5] == "E":
			self.sample['Longitude'] = float(data[4])
		else:
			self.sample['Longitude'] = float(data[4])*-1.0
		"""
	def _addSpecialStats(self):
		pass

