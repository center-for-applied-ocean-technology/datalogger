from BaseSensor import BaseSensor 
import time 
import traceback 
from math import sin, cos, radians, degrees, atan2 
import numpy
from datetime import datetime 
import json
import zlib
import base64
import re

class VemcoVR2C(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(VemcoVR2C, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self.version = 1.0
		self._ignoreFields = ["timestamp","duration","warm_time","line_counter","raw_memory", "coding_type", "detection_count", "unit_timestamp", "serial_number", "adc_value", "battery_used", "ping_count" ] #fields that will not have simple averaging
		self.sample=	{
					"line_counter":{},
					"timestamp":{},
					"detection_count":{},
					"ping_count":{},
					"line_voltage_avg":{},
					"battery_voltage_avg":{},
					"battery_used":{},
					"water_temperature_avg":{},
					"detection_memory_avg":{},
					"raw_memory":{},
					"noise_avg":{},
					"narrow_band_noise_avg":{},
					"warm_time":{},
					"duration":{},
					"tiltx_avg":{},
					"tilty_avg":{},
					"tiltz_avg":{},
				}

		self.sample['ping_count']['maxlimit'] = 999999
                self.sample['ping_count']['minlimit'] = 0
                self.sample['ping_count']['units'] = 'tbd'
                self.sample['ping_count']['offset'] = 0
                self.sample['ping_count']['multiplier'] = 1

		self.sample['line_voltage_avg']['maxlimit'] = 999999
                self.sample['line_voltage_avg']['minlimit'] = 0
                self.sample['line_voltage_avg']['units'] = 'tbd'
                self.sample['line_voltage_avg']['offset'] = 0
                self.sample['line_voltage_avg']['multiplier'] = 1

		self.sample['tiltx_avg']['maxlimit'] = 999999
                self.sample['tiltx_avg']['minlimit'] = 0
                self.sample['tiltx_avg']['units'] = 'tbd'
                self.sample['tiltx_avg']['offset'] = 0
                self.sample['tiltx_avg']['multiplier'] = 1

		self.sample['tilty_avg']['maxlimit'] = 999999
                self.sample['tilty_avg']['minlimit'] = 0
                self.sample['tilty_avg']['units'] = 'tbd'
                self.sample['tilty_avg']['offset'] = 0
                self.sample['tilty_avg']['multiplier'] = 1

		self.sample['tiltz_avg']['maxlimit'] = 999999
                self.sample['tiltz_avg']['minlimit'] = 0
                self.sample['tiltz_avg']['units'] = 'tbd'
                self.sample['tiltz_avg']['offset'] = 0
                self.sample['tiltz_avg']['multiplier'] = 1

		self.sample['battery_voltage_avg']['maxlimit'] = 999999
                self.sample['battery_voltage_avg']['minlimit'] = 0
                self.sample['battery_voltage_avg']['units'] = 'tbd'
                self.sample['battery_voltage_avg']['offset'] = 0
                self.sample['battery_voltage_avg']['multiplier'] = 1

		self.sample['water_temperature_avg']['maxlimit'] = 999999
                self.sample['water_temperature_avg']['minlimit'] = 0
                self.sample['water_temperature_avg']['units'] = 'tbd'
                self.sample['water_temperature_avg']['offset'] = 0
                self.sample['water_temperature_avg']['multiplier'] = 1

		self.sample['detection_memory_avg']['maxlimit'] = 999999
                self.sample['detection_memory_avg']['minlimit'] = 0
                self.sample['detection_memory_avg']['units'] = 'tbd'
                self.sample['detection_memory_avg']['offset'] = 0
                self.sample['detection_memory_avg']['multiplier'] = 1

		self.sample['noise_avg']['maxlimit'] = 999999
                self.sample['noise_avg']['minlimit'] = 0
                self.sample['noise_avg']['units'] = 'tbd'
                self.sample['noise_avg']['offset'] = 0
                self.sample['noise_avg']['multiplier'] = 1

		self.sample['narrow_band_noise_avg']['maxlimit'] = 999999
                self.sample['narrow_band_noise_avg']['minlimit'] = 0
                self.sample['narrow_band_noise_avg']['units'] = 'tbd'
                self.sample['narrow_band_noise_avg']['offset'] = 0
                self.sample['narrow_band_noise_avg']['multiplier'] = 1

		self.sample['detection_count']['maxlimit'] = 999999
                self.sample['detection_count']['minlimit'] = 0
                self.sample['detection_count']['units'] = 'tbd'
                self.sample['detection_count']['offset'] = 0
                self.sample['detection_count']['multiplier'] = 1

		self.sample['raw_memory']['maxlimit'] = 999999
                self.sample['raw_memory']['minlimit'] = 0
                self.sample['raw_memory']['units'] = 'tbd'
                self.sample['raw_memory']['offset'] = 0
                self.sample['raw_memory']['multiplier'] = 1

		self.sample['battery_used']['maxlimit'] = 999999
                self.sample['battery_used']['minlimit'] = 0
                self.sample['battery_used']['units'] = 'tbd'
                self.sample['battery_used']['offset'] = 0
                self.sample['battery_used']['multiplier'] = 1

		self.sample['line_counter']['maxlimit'] = 999999
                self.sample['line_counter']['minlimit'] = 0
                self.sample['line_counter']['units'] = 'tbd'
                self.sample['line_counter']['offset'] = 0
                self.sample['line_counter']['multiplier'] = 1

		#self.sample['unit_timestamp']['maxlimit'] = 999999
                #self.sample['unit_timestamp']['minlimit'] = 0
                #self.sample['unit_timestamp']['units'] = 'tbd'
                #self.sample['unit_timestamp']['offset'] = 0
                #self.sample['unit_timestamp']['multiplier'] = 1
	
		self.sensor_sample=	{"sensor_id":[],
				"adc_value":[],
				"detection_level":[],
				"timestamp":[],
				"line_counter":[],
				"coding_type":[],
				"serial_number":[],
				"noise":[]
				}


		
					

	def checkVemcoLine(self, line):
		
		# Check Vemco sentences
		line = line.strip('\r\n$')
		try :
			nmeadata, rem = line.split(',', 1)
			data,cksum = line.split('#',1)
			data=data.strip(',')
			calc_cksum = 0
			for s in data:
				calc_cksum += ord(s)
			result = (int(cksum, 16) == calc_cksum&0xff)
			if not result:
				line = False
		except ValueError:
			return False
		return data 
	
	def _getSample(self):
		start = datetime.now()
		sample = {}
		sensor_sample = {}
		while self._sampling:
			duration = (datetime.now()-start).total_seconds()
			if duration > float(self._settings['sample_duration'].strip()):
				self._sampling = False
				break
			else:
				dataset, staticInfo = self._getDataset()
				if dataset != None:
					if dataset["coding_type"] == "STS":
						if sample == {}:
							sample = self._createSampleDict(dataset)
						else:
							for field in dataset:
								sample[field].append(dataset[field])
					elif dataset["coding_type"] == "A69-9002":
						if sensor_sample == {}:
							sensor_sample = self._createSampleDict(dataset)
						else:
							for field in dataset:
								sensor_sample[field].append(dataset[field])
							

		#stats = {}
		
		self.sample["raw_memory"]["value"] = sample['raw_memory'][0]
		self.sample["warm_time"]["value"] = self._settings['warm_time']
		self.sample["duration"]["value"] = self._settings['sample_duration']
		self.sample["timestamp"]["value"] = '{:%Y-%m-%d %H:%M:%S}'.format(start)
		#self.sample["unit_timestamp"]["value"] = sample['unit_timestamp'][0]
		self.sample["detection_count"]["value"] = sample['detection_count'][0]
		self.sample["battery_used"]["value"] = sample['detection_count'][0]
		self.sample["line_counter"]["value"] = sample['line_counter'][0]
		self.sample["ping_count"]["value"] = sample['ping_count'][0]
		for field in sample:
			if field in self._ignoreFields:
				pass
			else:
				self.sample[field+"_avg"]["value"] = numpy.average(sample[field])
		for ii in range(0, len(sensor_sample["sensor_id"])):
			self.sensor_sample["sensor_id"].append(sensor_sample["sensor_id"][ii])
			self.sensor_sample["adc_value"].append(int(sensor_sample["adc_value"][ii]))
			self.sensor_sample["noise"].append(int(sensor_sample["noise"][ii]))
			self.sensor_sample["detection_level"].append(float(sensor_sample["detection_level"][ii]))
			self.sensor_sample["timestamp"].append((sensor_sample["timestamp"][ii]))
			self.sensor_sample["line_counter"].append((sensor_sample["line_counter"][ii]))
			self.sensor_sample["coding_type"].append((sensor_sample["coding_type"][ii]))
			self.sensor_sample["serial_number"].append((sensor_sample["serial_number"][ii]))
				
		
		self._addSpecialStats() #addSpecialStats function to be written for cases where just simple average would not work or other stats required such as direction or gust 
		#self._setNMEA()
		return self.sample, self.sensor_sample
	
	def getJSON(self):
		try:
			json_str = json.dumps({"sensor":self.sensor,"sample":self.sample,"vsensors":self.sensor_sample})
			json_str = zlib.compress(json_str,9)
			json_str = base64.b64encode(json_str)
			str = "PCTEC,JSON," + json_str
			return "$" + str+"*%s\r\n"%self._createNmeaChk(str)
		except: 
			return " "


	def _getDataset(self):
		try:
			dataSet = None
			start = datetime.now()
			if (datetime.now()-start).total_seconds() > 60:
				dataSet = None
			line = self.readline()
			line = self.checkVemcoLine(line)
			if line:
				data = line.split(',')
				id = data[1].strip()
				sample_time = data[2]
				sentFormat = data[3]
				if sentFormat == 'STS' and len(data) == 15:
					try:
						m = re.search(r'\d+',data[0])
						data[0] = m.group()
					except:
						data[0] = -1;
					
					try:
						data[1] = int(data[1])
					except:
						data[1] = -1;

					#parse detection counter
					try:
						if data[4][0:3] == 'DC=':
							data[4] = int(data[4][4:])
					except:
						data[4] = -1
					
					#parse ping counter				
					try:
						if data[5][0:3] == 'PC=':
							data[5] = int(data[5][4:])
					except:
						data[5] = -1

					#parse line voltage				
					try:
						if data[6][0:3] == 'LV=':
							data[6] = float(data[6][4:])
					except:
						data[6] = -1

					#parse battery voltage				
					try:
						if data[7][0:3] == 'BV=':
							data[7] = float(data[7][4:])
					except:
						data[7] = -1
					
					#parse battery used
					try:
						if data[8][0:3] == 'BU=':
							data[8] = float(data[8][4:])
					except:
						data[8] = -1

					#water temperature
					try:
						if data[9][0:2] == 'T=':
							data[9] = float(data[9][3:])
					except:
						data[9] = -1

					#parse detect memory
					try:
						if data[10][0:3] == 'DU=':
							data[10] = float(data[10][4:])
					except:
						data[10] = -1

					#parse raw memory
					try:
						if data[11][0:3] == 'RU=':
							data[11] = float(data[11][4:])
					except:
						data[11] = -1

					#parse tilt
					tilt = data[12][5:]
					try:
						if data[12][0:4] == 'XYZ=':
							tilt = (data[12][5:]).split(':')
							float(tilt[0])					
							float(tilt[1])					
							float(tilt[2])					
							data[12] = (data[12][5:]).split(':')					
					except:
						data[12] = -1

					#parse noise
					try:
						if data[13][0:2] == 'N=':
							data[13] = float(data[13][3:])
					except:
						data[13] = -1

					#parse narrow band
					try:
						if data[14][0:3] == 'NP=':
							data[14] = float(data[14][4:])
					except:
						data[14] = -1

					dataSet = {"line_counter":data[1],
					"unit_timestamp":data[2],
					"coding_type":data[3],
					"detection_count":data[4],
					"ping_count":data[5],
					"line_voltage":data[6],
					"battery_voltage":data[7],
					"battery_used":data[8],
					"water_temperature":data[9],
					"detection_memory":data[10],
					"raw_memory":data[11],
					"tiltx":float(data[12][0]),
					"tilty":float(data[12][1]),
					"tiltz":float(data[12][2]),
					"noise":data[13],
					"narrow_band_noise":data[14],
					"timestamp":start
					}
				elif sentFormat == 'A69-9002' and len(data) == 8:
					#parse detection level 
					try:
						if data[6][0:2] == 'S=':
							data[6] = float(data[6][3:])
					except:
						data[6] = -1
					try:
						if data[7][0:2] == 'N=':
							data[7] = float(data[7][3:])
					except:
						data[7] = -1
					dataSet ={"timestamp":data[2],
						"line_counter":data[1],
						"serial_number":data[0].strip('\x00'),
						"coding_type":data[3],
						"sensor_id":data[4],
						"adc_value":data[5],
						"detection_level":data[6],
						"noise":data[7]
					}
					#print "Serial Number",data[0]
					#print "Line Counter",data[1]
					#print "Date/Time",data[2]
					#print "SensorID",int(data[4])
					#sensorType = int(data[4])&0x03
					#if sensorType == 0:
					#	print "\tTilt", data[5]
					#elif sensorType == 1:
					#	print "Diagnostic"
					#	print "\tAcoustic Power Level", int(data[5])&0xf
					#	logmem = (int(data[5])&0x30)>>4
					#	if logmem == 0:
					#		print "\tLog Memory Used (0-25%)"
					#	elif logmem == 1:
					#		print "\tLog Memory Used (25-50%)"
					#	elif logmem == 2:
					#		print "\tLog Memory Used (50-75%)"
					#	elif logmem == 3:
					#		print "\tLog Memory Used (75-100%)"
					#	batvolt = (int(data[5])&0xc0)>>6
					#	if batvolt == 0:
					#		print "\tBattery Voltage below 0.85v)"
					#	elif batvolt == 1:
					#		print "\tBattery Voltage (0.85v - 1.04v)"
					#	elif batvolt == 2:
					#		print "\tBattery Voltage (1.05v - 1.24v)"
					#	elif batvolt == 3:
					#		print "\tBattery Voltage above 1.25v"
					#		
					#elif sensorType == 3:
					#	print "Temperature"
					#	print "\tTemperature = ", int(data[5])/10.0
					#	
					#elif sensorType == 2:
					#	print "D0"
					#	print "\t% Saturation = ",(int(data[5])/255.0)*140.0
					#else:
					#	print "Type not recognized"
					#print "Detection Level", data[6]
		
		except:
			dataSet = None
			staticInfo = None
			print traceback.print_exc()
		return dataSet,None
		

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
	#def _addSpecialStats(self):


