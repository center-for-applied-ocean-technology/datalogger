from BaseSensor import BaseSensor 
import time 
import traceback 
from math import sin, cos, radians, degrees, atan2 
from numpy import average 
from datetime import datetime 

class WX200(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(WX200, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self._ignoreFields = ["wind_from_direction", "timestamp"] #fields that will not have simple averaging
		self.version = 1.0
		self.sample=	{"wind_from_direction_avg":{},
						"eastward_wind_avg":{}, #may be temp
						"northward_wind_avg":{}, #may be temp
						"wind_speed_avg":{},
						"air_pressure_avg":{},
						"air_temperature_avg":{},
						"hour":{},
						"minute":{},
						"second":{},
						"latitude":{},
						"longitude":{},
						"timestamp":{}
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

		self.sample['air_pressure_avg']['maxlimit'] = 1.085
		self.sample['air_pressure_avg']['minlimit'] = .86
		self.sample['air_pressure_avg']['units'] = 'bars'
		self.sample['air_pressure_avg']['offset'] = 0
		self.sample['air_pressure_avg']['multiplier'] = 10000
		
		self.sample['air_temperature_avg']['maxlimit'] = 60
		self.sample['air_temperature_avg']['minlimit'] = -90
		self.sample['air_temperature_avg']['units'] = 'deg c'
		self.sample['air_temperature_avg']['offset'] = 0
		self.sample['air_temperature_avg']['multiplier'] = 10

		self.sample['latitude']['maxlimit'] = 90
		self.sample['latitude']['minlimit'] = -90
		self.sample['latitude']['units'] = 'deg'
		self.sample['latitude']['offset'] = 0
		self.sample['latitude']['multiplier'] = 10

		self.sample['longitude']['maxlimit'] = 180
		self.sample['longitude']['minlimit'] = -180
		self.sample['longitude']['units'] = 'deg'
		self.sample['longitude']['offset'] = 0
		self.sample['longitude']['multiplier'] = 10

		self.sample['hour']['maxlimit'] = 24
		self.sample['hour']['minlimit'] = 0
		self.sample['hour']['units'] = 'Hours'
		self.sample['hour']['offset'] = 0
		self.sample['hour']['multiplier'] = 1

		self.sample['minute']['maxlimit'] = 60
		self.sample['minute']['minlimit'] = 0
		self.sample['minute']['units'] = 'Minutes'
		self.sample['minute']['offset'] = 0
		self.sample['minute']['multiplier'] = 1

		self.sample['second']['maxlimit'] = 60
		self.sample['second']['minlimit'] = 0
		self.sample['second']['units'] = 'second'
		self.sample['second']['offset'] = 0
		self.sample['second']['multiplier'] = 100

	#def _turnOff(self):
	#	pass

	def _getDataset(self):
		try:
			start = datetime.now()
			while True:
				if (datetime.now()-start).total_seconds() > 5:
					dataSet = None
					break
				line = self.readline()
				line = self.checkNmeaLine(line)
				if line:
					data = line.split(',')
					sentFormat = data[0][2:]
					if sentFormat == 'MDA':
						try:
							float(data[13])
						except:
							data[13] = 0; 
						try:
							float(data[19])
						except:
							data[19] = 0; 
						try:
							float(data[15])
						except:
							data[15] = 0; 
						dataSet = {	"air_pressure": float(data[3])*100000, #bar to pa
									"air_temperature": float(data[5]), # c
									"wind_from_direction": float(data[15]),#magnetic
									"wind_speed": float(data[19]),
									"eastward_wind": cos(radians((float(data[15]))))*float(data[19]),  
									"northward_wind":sin(radians((float(data[15]))))*float(data[19]),
									#"eastward_wind": cos(-1*radians((float(data[15]))))*float(data[19]),  
									#"northward_wind":sin(-1*radians((float(data[15]))))*float(data[19]),
									"timestamp":start
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
		try:
			gga = self.getGGA()
			data = gga.split(",")
			self.sample["hour"]["value"] = int(data[1][:2])
			self.sample["minute"]["value"] = int(data[1][2:4])
			self.sample["second"]["value"] = float(data[1][4:])
			self.sample["latitude"]["value"] = float(data[2][:2]) + float(data[2][2:])/60.0
			self.sample["longitude"]["value"] = float(data[4][:3]) + float(data[4][3:])/60.0
			if data[3] == "N": 
				pass #need to handle north/south
			else:
				self.sample["latitude"]["value"] = self.sample["latitude"]["value"] * -1.0
			if data[5] == "E":
				pass
			else:
				self.sample['longitude']["value"] = self.sample['longitude']["value"]*-1.0
		except:
			#pass#for now
			print traceback.print_exc()
