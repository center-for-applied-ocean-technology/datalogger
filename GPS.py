from BaseSensor import BaseSensor 
import time 
import traceback 
import State
from math import sin, cos, radians, degrees, atan2 
from numpy import average 
from datetime import datetime 

class GPS(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(GPS, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self._ignoreFields = ["timestamp", "latitude", "longitude"] #fields that will not have simple averaging
		self.version = 1.0
		self.sample=	{"hour":{},
						"minute":{},
						"second":{},
						"latitude":{},
						"longitude":{},
						"timestamp":{}
						}
		
		
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
			line = self.getGGA()
			line = self.checkNmeaLine(line)
			data = line.split(',')
			sentFormat = data[0][2:]
			if sentFormat == 'GGA':
				try:
					float(data[2]);
				except:
					data[2] = 0;
				try:
					float(data[4]);
				except:
					data[4] = 0;

				if data[3] == "S": 
					data[2] = -1.0*data[2] #need to handle north/south
				if data[5] == "E":
					data[4] = -1.0*data[4]
				dataSet = 	{	"timestamp": data[1],
								"latitude": float(data[2]),
								"longitude": float(data[4])
							}
				#set position
				State.setPos(datetime.now(),float(data[2]), float(data[4]))
				#State.timestamp = datetime.now()
				static = None
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
		self.NMEA = "" 
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
	def _addSpecialStats(self):
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
