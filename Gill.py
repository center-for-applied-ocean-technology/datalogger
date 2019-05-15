from BaseSensor import BaseSensor 
import time 
import traceback 
from math import sin, cos, radians, degrees, atan2 
from numpy import average 
from datetime import datetime 
import State
class Gill(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(Gill, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self._ignoreFields = ["wind_from_direction"] #fields that will not have simple averaging
		self.version = 1.0
		self.sample=	{"wind_from_direction_avg":{},
						"eastward_wind_avg":{}, #may be temp
						"northward_wind_avg":{}, #may be temp
						"wind_speed_avg":{}
						}
		
		
		self.sample['wind_from_direction_avg']['maxlimit'] = 360
		self.sample['wind_from_direction_avg']['minlimit'] = 0
		self.sample['wind_from_direction_avg']['units'] = 'deg true'
		self.sample['wind_from_direction_avg']['offset'] = 0
		self.sample['wind_from_direction_avg']['multiplier'] = 10

		self.sample['wind_speed_avg']['maxlimit'] = 120
		self.sample['wind_speed_avg']['minlimit'] = 0
		self.sample['wind_speed_avg']['units'] = 'm/s'
		self.sample['wind_speed_avg']['offset'] = 0
		self.sample['wind_speed_avg']['multiplier'] = 10



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
				if line:
					data = line.split(',')
					if len(data) == 6:
						#assuming m/s for now. Need to change.
						#need to code event when there is no data, for example if there is no wind there is no reading on the device.
						if data[1] == "":
						#no wind -- ignore sample
							pass
						else:
							heading = State.getHeading()
							State.setWindspeed(datetime.now(), data[2], data[1])
							if heading != None:
								
								if (datetime.now() - heading[0]).total_seconds() < 5: #right now if compass data is not avaible we will not get any data from gill
									direction = float(data[1])+ heading[1]
									if direction < 0:
										direction += 360
									
									dataSet = {	"wind_from_direction": float(data[1]),#true
										"wind_speed": float(data[2]),
										"eastward_wind": cos(radians(direction))*float(data[2]),  
										"northward_wind":sin(radians(direction))*float(data[2])
									}
								
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



	def getGGA(self):
		return self.getNMEA('GGA')
	
	def getZDA(self):
		return self.getNMEA('ZDA')
	
	def _setNMEA(self):
		#broken code from trying to fix structure. 
		
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

		try:
			direction = degrees(atan2(self.sample["eastward_wind_avg"]["value"], self.sample["northward_wind_avg"]["value"])) 
			if direction < 0:
				direction = direction + 360
			self.sample["wind_from_direction_avg"]["value"] = direction
			self.sample.pop("eastward_wind_avg",None)
			self.sample.pop("northward_wind_avg",None)
			
		except:
			self.sample["wind_from_direction_avg"] = ''
			print traceback.print_exc()

