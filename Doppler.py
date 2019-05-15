from BaseSensor import BaseSensor
import time
import traceback
from math import sin, cos, radians, degrees, atan2
from numpy import average
from datetime import datetime
class Doppler(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(Doppler, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self.sample = {}
	def toint(self,i):
		try:
			i = int(i)
		except:
			i = None
		return i

	def _sendBreak(self):
		self._reader.read(self._reader.inWaiting()) #clearing read buffer... Flush does not seam to do anything
		self._reader.write("@@@@@@") #break
		time.sleep(1)	   #sleep as per Section 2.2 of manual
		self._reader.write("K1W%!Q") #not sure what this does. As per Section 2.2 of manual
		time.sleep(.1)	   
		self._reader.write("MC")
		time.sleep(.1)		#Don't think we really need this as next line will read until it gets 1024 bits or times out
		return self._reader.read(1024) #returning response from 
		
	def _getSample(self):
		self._sendBreak()
		self._getDataset()

	def getMode(self):
		time.sleep(.1)
		self._reader.read(self._reader.inWaiting())#clear what in buffer

		self._reader.write("II")
		time.sleep(.1)
		response = self._reader.read(1024)
		#print response
		
		#if ackFound(response):
		mode = ["Firmware Upgrade Mode",
				"Measurement Mode",
				"Command Mode",
				"Data Retrieval Mode",
				"Confirmation Mode"]
		return [ord(response[0]),mode[ord(response[0])]]

	def _getDataset(self):
		start = datetime.now()
		self._reader.read(self._reader.inWaiting())
		self._reader.write('NM')
		time.sleep(2)
		i = 0
		try:
			sampleTime = self._reader.read(1024)
			#print sampleTime
			sampleTime = int(sampleTime)
			#print sampleTime
			if sampleTime != 0:
				time.sleep(2)
				start = datetime.now()
				nmea = ""
				while (datetime.now()-start).total_seconds()<sampleTime:
					time.sleep(1)
					#print "sleeping 1 second: %s"%i
					i = i +1
					nmea = nmea + self._reader.read(1024)
			self.NMEA = nmea
			#print self.NMEA
			lines = self.NMEA.split('\r\n')
			self.sample['timestamp'] = {'value':str(start)}
			self.sample['duration'] = {'value':self._settings["sample_duration"]}
			self.sample['warm_time'] = {'value':self._settings["warm_time"]}
			for line in lines:
				#print line
				#line = self.checkNmeaLine(line)
				if line:
					data = line.split('*')[0]
					data = data.split(',')
					sentFormat = data[0][1:]
					#print sentFormat
					if sentFormat == 'PNORI':
						pass
						
						self.sensor["instrument_type"] = self.toint(data[1]) #0=aquadopp, 2=profiler, 3=awac
						self.sensor["head_id"] = data[2]
						self.sensor["number_of_beams"] = self.toint(data[3])
						self.sensor["number_of_cells"] = self.toint(data[4])
						self.sensor["blanking_m"] = float(data[5])
						self.sensor["cell_size_m"] = float(data[6])
						self.sensor["coordinate_system"] = self.toint(data[7]) #0=ENU,1=XYZ,2=Beam  
						
						
					elif sentFormat == 'PNORS':
						
						#self.sample["sensor_date"] = {"value":data[1]}
						#self.sample["sensor_time"] = {"value": data[2]}
						#self.sample["sensor_error_code"] = {"value": data[3]}
						self.sample["sensor_status_code"]= {"value":data[4]}
						self.sample["sensor_status_code"]['maxlimit'] = -100 #RK need to set
						self.sample["sensor_status_code"]['minlimit'] = 100 #RK need to set
						self.sample["sensor_status_code"]['units'] = ''  #RK need to check
						self.sample["sensor_status_code"]['offset'] = 0
						self.sample["sensor_status_code"]['multiplier'] = 1
						
						self.sample["battery_voltage"]= {"value":float(data[5])}
						self.sample["battery_voltage"]['maxlimit'] = 0 #RK need to set
						self.sample["battery_voltage"]['minlimit'] = 20 #RK need to set
						self.sample["battery_voltage"]['units'] = 'v'  #RK need to check
						self.sample["battery_voltage"]['offset'] = 0
						self.sample["battery_voltage"]['multiplier'] = 1
						
						self.sample["sound_speed"]= {"value":float(data[6])}
						self.sample["sound_speed"]['maxlimit'] = 0 #RK need to set
						self.sample["sound_speed"]['minlimit'] = 15000 #RK need to set
						self.sample["sound_speed"]['units'] = 'm/s'  #RK need to check
						self.sample["sound_speed"]['offset'] = 0
						self.sample["sound_speed"]['multiplier'] = 1
						
						self.sample["heading_deg"]= {"value":float(data[7])}
						self.sample["heading_deg"]['maxlimit'] = 0 #RK need to set
						self.sample["heading_deg"]['minlimit'] = 360 #RK need to set
						self.sample["heading_deg"]['units'] = 'degrees'  #RK need to check
						self.sample["heading_deg"]['offset'] = 0
						self.sample["heading_deg"]['multiplier'] = 1
						
						self.sample["pitch_deg"]= {"value":float(data[8])}
						self.sample["pitch_deg"]['maxlimit'] = 0 #RK need to set
						self.sample["pitch_deg"]['minlimit'] = 360 #RK need to set
						self.sample["pitch_deg"]['units'] = 'degrees'  #RK need to check
						self.sample["pitch_deg"]['offset'] = 0
						self.sample["pitch_deg"]['multiplier'] = 1

						self.sample["roll_deg"]= {"value":float(data[9])}
						self.sample["roll_deg"]['maxlimit'] = 0 #RK need to set
						self.sample["roll_deg"]['minlimit'] = 360 #RK need to set
						self.sample["roll_deg"]['units'] = 'degrees'  #RK need to check
						self.sample["roll_deg"]['offset'] = 0
						self.sample["roll_deg"]['multiplier'] = 1
						
						self.sample["pressure_dbar"]= {"value":float(data[10])}
						self.sample["pressure_dbar"]['maxlimit'] = 0 #RK need to set
						self.sample["pressure_dbar"]['minlimit'] = 15000 #RK need to set
						self.sample["pressure_dbar"]['units'] = 'dbar'  #RK need to check
						self.sample["pressure_dbar"]['offset'] = 0
						self.sample["pressure_dbar"]['multiplier'] = 1
						
						self.sample["temperature_deg_c"]= {"value":float(data[11])}
						self.sample["temperature_deg_c"]['maxlimit'] = -30 #RK need to set
						self.sample["temperature_deg_c"]['minlimit'] = 50 #RK need to set
						self.sample["temperature_deg_c"]['units'] = 'degc'  #RK need to check
						self.sample["temperature_deg_c"]['offset'] = 0
						self.sample["temperature_deg_c"]['multiplier'] = 1
						
						self.sample["analog_input_1_counts"]= {"value":float(data[12])}
						self.sample["analog_input_1_counts"]['maxlimit'] = 0 #RK need to set
						self.sample["analog_input_1_counts"]['minlimit'] = 15000 #RK need to set
						self.sample["analog_input_1_counts"]['units'] = ''  #RK need to check
						self.sample["analog_input_1_counts"]['offset'] = 0
						self.sample["analog_input_1_counts"]['multiplier'] = 1
						
						self.sample["analog_input_2_counts"]= {"value":float(data[13])}
						self.sample["analog_input_2_counts"]['maxlimit'] = 0 #RK need to set
						self.sample["analog_input_2_counts"]['minlimit'] = 15000 #RK need to set
						self.sample["analog_input_2_counts"]['units'] = ''  #RK need to check
						self.sample["analog_input_2_counts"]['offset'] = 0
						self.sample["analog_input_2_counts"]['multiplier'] = 1
						
							
					elif sentFormat == 'PNORC':
						cell = str(data[3])
						#self.sample["velocity_date"] = {"value":data[1]}
						#self.sample["velocity_time"] = {"value":data[2]}
						self.sample["cell" + cell + "_velocity1"] = {"value":float(data[4])}
						self.sample["cell" + cell + "_velocity1"]['maxlimit'] = -100 #RK need to set
						self.sample["cell" + cell + "_velocity1"]['minlimit'] = 100 #RK need to set
						self.sample["cell" + cell + "_velocity1"]['units'] = 'm/s'  #RK need to check
						self.sample["cell" + cell + "_velocity1"]['offset'] = 0
						self.sample["cell" + cell + "_velocity1"]['multiplier'] = 1

						self.sample["cell" + cell + "_velocity2"] = {"value":float(data[5])}
						self.sample["cell" + cell + "_velocity2"]['maxlimit'] = -100 #RK need to set
						self.sample["cell" + cell + "_velocity2"]['minlimit'] = 100 #RK need to set
						self.sample["cell" + cell + "_velocity2"]['units'] = 'm/s'  #RK need to check
						self.sample["cell" + cell + "_velocity2"]['offset'] = 0
						self.sample["cell" + cell + "_velocity2"]['multiplier'] = 1
						
						self.sample["cell" + cell + "_velocity3"] = {"value":float(data[6])}
						self.sample["cell" + cell + "_velocity3"]['maxlimit'] = -100 #RK need to set
						self.sample["cell" + cell + "_velocity3"]['minlimit'] = 100 #RK need to set
						self.sample["cell" + cell + "_velocity3"]['units'] = 'm/s'  #RK need to check
						self.sample["cell" + cell + "_velocity3"]['offset'] = 0
						self.sample["cell" + cell + "_velocity3"]['multiplier'] = 1
						
						self.sample["cell" + cell + "_speed"] = {"value":float(data[7])}
						self.sample["cell" + cell + "_speed"]['maxlimit'] = 0 #RK need to set
						self.sample["cell" + cell + "_speed"]['minlimit'] = 100 #RK need to set
						self.sample["cell" + cell + "_speed"]['units'] = 'm/s'  #RK need to check
						self.sample["cell" + cell + "_speed"]['offset'] = 0
						self.sample["cell" + cell + "_speed"]['multiplier'] = 1
						
						
						self.sample["cell" + cell + "_direction_deg"] = {"value" :float(data[8])}
						self.sample["cell" + cell + "_direction_deg"]['maxlimit'] = 0 #RK need to set
						self.sample["cell" + cell + "_direction_deg"]['minlimit'] = 360 #RK need to set
						self.sample["cell" + cell + "_direction_deg"]['units'] = 'Degrees'  #RK need to check
						self.sample["cell" + cell + "_direction_deg"]['offset'] = 0
						self.sample["cell" + cell + "_direction_deg"]['multiplier'] = 1
						
						self.sample["cell" + cell + "_amplitude1"] = {"value":self.toint(data[10])}
						self.sample["cell" + cell + "_amplitude1"]['maxlimit'] = 0 #RK need to set
						self.sample["cell" + cell + "_amplitude1"]['minlimit'] = 360 #RK need to set
						self.sample["cell" + cell + "_amplitude1"]['units'] = 'Degrees'  #RK need to check
						self.sample["cell" + cell + "_amplitude1"]['offset'] = 0
						self.sample["cell" + cell + "_amplitude1"]['multiplier'] = 1
						
						self.sample["cell" + cell + "_amplitude2"]= {"value":self.toint(data[11])}
						self.sample["cell" + cell + "_amplitude2"]['maxlimit'] = 0 #RK need to set
						self.sample["cell" + cell + "_amplitude2"]['minlimit'] = 360 #RK need to set
						self.sample["cell" + cell + "_amplitude2"]['units'] = 'Degrees'  #RK need to check
						self.sample["cell" + cell + "_amplitude2"]['offset'] = 0
						self.sample["cell" + cell + "_amplitude2"]['multiplier'] = 1
						
						self.sample["cell" + cell + "_amplitude3"]= {"value":self.toint(data[12])}
						self.sample["cell" + cell + "_amplitude3"]['maxlimit'] = 0 #RK need to set
						self.sample["cell" + cell + "_amplitude3"]['minlimit'] = 360 #RK need to set
						self.sample["cell" + cell + "_amplitude3"]['units'] = 'Degrees'  #RK need to check
						self.sample["cell" + cell + "_amplitude3"]['offset'] = 0
						self.sample["cell" + cell + "_amplitude3"]['multiplier'] = 1
						
						self.sample["cell" + cell + "_correlation1"]= {"value":self.toint(data[13])}
						self.sample["cell" + cell + "_correlation1"]['maxlimit'] = 0 #RK need to set
						self.sample["cell" + cell + "_correlation1"]['minlimit'] = 360 #RK need to set
						self.sample["cell" + cell + "_correlation1"]['units'] = 'Degrees'  #RK need to check
						self.sample["cell" + cell + "_correlation1"]['offset'] = 0
						self.sample["cell" + cell + "_correlation1"]['multiplier'] = 1
						
						self.sample["cell" + cell + "_correlation2"]= {"value":self.toint(data[14])}
						self.sample["cell" + cell + "_correlation2"]['maxlimit'] = 0 #RK need to set
						self.sample["cell" + cell + "_correlation2"]['minlimit'] = 360 #RK need to set
						self.sample["cell" + cell + "_correlation2"]['units'] = 'Degrees'  #RK need to check
						self.sample["cell" + cell + "_correlation2"]['offset'] = 0
						self.sample["cell" + cell + "_correlation2"]['multiplier'] = 1
						
						self.sample["cell" + cell + "_correlation3"]= {"value":self.toint(data[15])}
						self.sample["cell" + cell + "_correlation3"]['maxlimit'] = 0 #RK need to set
						self.sample["cell" + cell + "_correlation3"]['minlimit'] = 360 #RK need to set
						self.sample["cell" + cell + "_correlation3"]['units'] = 'Degrees'  #RK need to check
						self.sample["cell" + cell + "_correlation3"]['offset'] = 0
						self.sample["cell" + cell + "_correlation3"]['multiplier'] = 1
					
					
			#print self.sample

		except:
			traceback.print_exc()
			self.NMEA = ""
			#RK: commenting out for now as we are just sending back nmea data. We will add this back in later as it will be usful for mapping field types
		"""try:
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
					if sentFormat == 'PNORI':
						dataSet = {	"instrument_type": int(data[1]), #0=aquadopp, 2=profiler, 3=awac
									"head_id": data[2],
									"number_of_beams": int(data[3]),
									"number_of_cells": int(data[4]),
									"blanking_m": float(data[5]),
									"cell_size_m": float(data[6]),
									"coordinate_system": int(data[7]), #0=ENU,1=XYZ,2=Beam  
								}
						static = None
						break
					elif sentFormat == 'PNORS':
						dataSet = {	"sensor_date": data[1],
									"sensor_time": data[2],
									"sensor_error_code": data[3]
									"sensor_status_code": data[4]
									"battery_voltage": float(data[5]),
									"sound_speed": float(data[6]),
									"heading_deg": float(data[7]),
									"pitch_deg": float(data[8]),
									"roll_deg": float(data[9]),
									"pressure_dbar": float(data[10]),
									"temperature_deg_c": float(data[11]),
									"analog_input_1_counts": float(data[12]),
									"analog_input_2_counts": float(data[13]),
								}
					elif sentFormat == 'PNORC':
						cell = str(data[3])
						dataSet = {	"velocity_date": data[1],
									"velocity_time": data[2],
									"cell_" + cell + "velocity_1": float(data[4]),
									"cell_" + cell + "velocity_2": float(data[5]),
									"cell_" + cell + "velocity_3": float(data[6]),
									"cell_" + cell + "speed": float(data[7]),
									"cell_" + cell + "direction_deg": float(data[8]),
									"cell_" + cell + "amplitude_units": data[9],
									"cell_" + cell + "amplitude_1": int(data[10]),
									"cell_" + cell + "amplitude_2": int(data[11]),
									"cell_" + cell + "amplitude_3": int(data[12]),
									"cell_" + cell + "correlation_1": int(data[13]),
									"cell_" + cell + "correlation_2": int(data[14]),
									"cell_" + cell + "correlation_3": int(data[15]),
								}
				
		except:
			dataSet = None
			staticInfo = None
			print traceback.print_exc()
			
		return dataSet, None
		"""
	#Get NMEA Funtion not really needed. May need to get rid of, or perhaps put in basesensor class??
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
			#print traceback.print_exc()
	def _setNMEA(self):
		pass #RK we are just using nmea messages from the nortek for now. May need to change later
		"""
		self.NMEA = "$PWX200,%.2f,%.2f,%.2f,%.2f"%(self.sample["air_pressure_avg"], self.sample["air_temperature_avg"], self.sample["wind_speed_avg"], self.sample["wind_from_direction_avg"]) 
		self.NMEA = self.NMEA+"*%s\r\n"%self._createNmeaChk(self.NMEA)
		self.NMEA = self.NMEA + self.getGGA()
		"""
		"""
	def _addSpecialStats(self):
		
		direction = degrees(atan2(-1*self.sample["eastward_wind_avg"], -1*self.sample["northward_wind_avg"])) 
		if direction < 0:
			direction = direction + 360
		self.sample["wind_from_direction_avg"] = direction
		"""
			  
				

				
	
