from BaseSensor import BaseSensor
import time
import traceback
from math import sin, cos, radians, degrees, atan2
from numpy import average
from datetime import datetime
import State

class DopplerASCII(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(DopplerASCII, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
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
		self.sample['timestamp'] = {'value':'{:%Y-%m-%d %H:%M:%S}'.format(start)}
		self.sample['duration'] = {'value':self._settings["sample_duration"]}
		self.sample['warm_time'] = {'value':self._settings["warm_time"]}
		self._reader.read(self._reader.inWaiting())
		self._sendBreak()
		(mode_id, mode_name) = self.getMode()
		if mode_id == 2:
                        self._reader.write('AS')
                        time.sleep(1)
                        
                        try:
                                sampleTime = 15 #need to change to grap from conf. 
                                #print sampleTime
			
                                if sampleTime != 0:
                                        time.sleep(2)
                                        start = datetime.now()
                                        data = ""
                                        while (datetime.now()-start).total_seconds()<sampleTime:
                                                time.sleep(1)
                                                #print "sleeping 1 second: %s"%i
                                                data = data + self._reader.read(1024)

                                       
                                lines = data.split('\r\n')
                                statusdata = lines.pop(0).split(' ')
        
                                #sample = {}
                                self.sample["sensor_status_code"]= {"value":float(statusdata[8])}
                                self.sample["sensor_status_code"]['maxlimit'] = -100 #RK need to set
                                self.sample["sensor_status_code"]['minlimit'] = 100 #RK need to set
                                self.sample["sensor_status_code"]['units'] = ''  #RK need to check
                                self.sample["sensor_status_code"]['offset'] = 0
                                self.sample["sensor_status_code"]['multiplier'] = 1
        
                                self.sample["battery_voltage"]= {"value":float(statusdata[9])}
                                self.sample["battery_voltage"]['maxlimit'] = 0 #RK need to set
                                self.sample["battery_voltage"]['minlimit'] = 20 #RK need to set
                                self.sample["battery_voltage"]['units'] = 'v'  #RK need to check
                                self.sample["battery_voltage"]['offset'] = 0
                                self.sample["battery_voltage"]['multiplier'] = 1
        
                                self.sample["sound_speed"]= {"value":float(statusdata[10])}
                                self.sample["sound_speed"]['maxlimit'] = 0 #RK need to set
                                self.sample["sound_speed"]['minlimit'] = 15000 #RK need to set
                                self.sample["sound_speed"]['units'] = 'm/s'  #RK need to check
                                self.sample["sound_speed"]['offset'] = 0
                                self.sample["sound_speed"]['multiplier'] = 1
        
                                self.sample["heading_deg"]= {"value":float(statusdata[11])}
                                self.sample["heading_deg"]['maxlimit'] = 0 #RK need to set
                                self.sample["heading_deg"]['minlimit'] = 360 #RK need to set
                                self.sample["heading_deg"]['units'] = 'degrees'  #RK need to check
                                self.sample["heading_deg"]['offset'] = 0
                                self.sample["heading_deg"]['multiplier'] = 1
                                
                                self.sample["pitch_deg"]= {"value":float(statusdata[12])}
                                self.sample["pitch_deg"]['maxlimit'] = 0 #RK need to set
                                self.sample["pitch_deg"]['minlimit'] = 360 #RK need to set
                                self.sample["pitch_deg"]['units'] = 'degrees'  #RK need to check
                                self.sample["pitch_deg"]['offset'] = 0
                                self.sample["pitch_deg"]['multiplier'] = 1

                                self.sample["roll_deg"]= {"value":float(statusdata[13])}
                                self.sample["roll_deg"]['maxlimit'] = 0 #RK need to set
                                self.sample["roll_deg"]['minlimit'] = 360 #RK need to set
                                self.sample["roll_deg"]['units'] = 'degrees'  #RK need to check
                                self.sample["roll_deg"]['offset'] = 0
                                self.sample["roll_deg"]['multiplier'] = 1
                                
                                self.sample["pressure_dbar"]= {"value":float(statusdata[14])}
                                self.sample["pressure_dbar"]['maxlimit'] = 0 #RK need to set
                                self.sample["pressure_dbar"]['minlimit'] = 15000 #RK need to set
                                self.sample["pressure_dbar"]['units'] = 'dbar'  #RK need to check
                                self.sample["pressure_dbar"]['offset'] = 0
                                self.sample["pressure_dbar"]['multiplier'] = 1
                                
                                self.sample["temperature_deg_c"]= {"value":float(statusdata[15])}
                                self.sample["temperature_deg_c"]['maxlimit'] = -30 #RK need to set
                                self.sample["temperature_deg_c"]['minlimit'] = 50 #RK need to set
                                self.sample["temperature_deg_c"]['units'] = 'degc'  #RK need to check
                                self.sample["temperature_deg_c"]['offset'] = 0
                                self.sample["temperature_deg_c"]['multiplier'] = 1
                                
                                self.sample["analog_input_1_counts"]= {"value":float(statusdata[16])}
                                self.sample["analog_input_1_counts"]['maxlimit'] = 0 #RK need to set
                                self.sample["analog_input_1_counts"]['minlimit'] = 15000 #RK need to set
                                self.sample["analog_input_1_counts"]['units'] = ''  #RK need to check
                                self.sample["analog_input_1_counts"]['offset'] = 0
                                self.sample["analog_input_1_counts"]['multiplier'] = 1
                                
                                self.sample["analog_input_2_counts"]= {"value":float(statusdata[17])}
                                self.sample["analog_input_2_counts"]['maxlimit'] = 0 #RK need to set
                                self.sample["analog_input_2_counts"]['minlimit'] = 15000 #RK need to set
                                self.sample["analog_input_2_counts"]['units'] = ''  #RK need to check
                                self.sample["analog_input_2_counts"]['offset'] = 0
                                self.sample["analog_input_2_counts"]['multiplier'] = 1
                                
                                for line in lines:
                                    line = line.split(' ')
                                    bindata = filter(lambda value: value != '', line)
                                    if len(bindata) == 3:
                                        cell = "%02d" % (int(bindata[0]),)
                                        self.sample["cell" + cell + "_speed"] = {"value":float(bindata[1])}
                                        self.sample["cell" + cell + "_speed"]['maxlimit'] = 0 #RK need to set
                                        self.sample["cell" + cell + "_speed"]['minlimit'] = 100 #RK need to set
                                        self.sample["cell" + cell + "_speed"]['units'] = 'mm/s'  #RK need to check
                                        self.sample["cell" + cell + "_speed"]['offset'] = 0
                                        self.sample["cell" + cell + "_speed"]['multiplier'] = 1
                                
                                        self.sample["cell" + cell + "_direction_deg"] = {"value" :float(bindata[2])/10.0}
                                        self.sample["cell" + cell + "_direction_deg"]['maxlimit'] = 0 #RK need to set
                                        self.sample["cell" + cell + "_direction_deg"]['minlimit'] = 360 #RK need to set
                                        self.sample["cell" + cell + "_direction_deg"]['units'] = 'Degrees'  #RK need to check
                                        self.sample["cell" + cell + "_direction_deg"]['offset'] = 0
                                        self.sample["cell" + cell + "_direction_deg"]['multiplier'] = 1
				State.setADCP(self.sample)
                        except:
                            traceback.print_exc()
			    self.NMEA = ""
			    #RK: commenting out for now as we are just sending back nmea data. We will add this back in later as it will be usful for mapping field types

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
			  
				

				
	
