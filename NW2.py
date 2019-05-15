from BaseSensor import BaseSensor
import time
import traceback
from math import sin, cos, radians, degrees, atan2
from numpy import average
from time import sleep
from datetime import datetime
import State

class NW2(BaseSensor):
	def __init__(self, settings, ts, dataset_id = None):
		super(NW2, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self._ignoreFields = ["timestamp","duration","warm_time"] #fields that will not have simple averaging

		self.sample = {
			"sea_surace_wave_number_of_zero_crossings_avg": {},
			"sea_surface_wave_mean_height_avg": {},
			"sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment_avg": {},
			"sea_surface_wave_max_height_avg": {},
			"sea_surface_wave_significant_height_avg": {},
			"sea_surface_wave_sig_period_avg": {},
			"sea_surface_wave_mean_height_of_tenth_of_wave_avg": {},
			"sea_surface_wave_mean_period_of_h10_waves_avg": {},
			"sea_surface_wave_mean_wave_period_avg": {},
			"sea_surface_wave_peak_period_avg": {},
			"sea_surface_wave_mean_height_of_fifth_of_wave_avg": {},
			"sea_surface_wave_HMO_avg": {},
			"sea_surface_wave_mean_direction_avg": {},
			"sea_surface_wave_mean_spread_avg": {}
		}

		self.sample['sea_surace_wave_number_of_zero_crossings_avg']['maxlimit'] = 999999 
		self.sample['sea_surace_wave_number_of_zero_crossings_avg']['minlimit'] = 0
		self.sample['sea_surace_wave_number_of_zero_crossings_avg']['units'] = 'tbd'
		self.sample['sea_surace_wave_number_of_zero_crossings_avg']['offset'] = 0
		self.sample['sea_surace_wave_number_of_zero_crossings_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_mean_height_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_mean_height_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_mean_height_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_mean_height_avg']['offset'] = 0
		self.sample['sea_surface_wave_mean_height_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment_avg']['offset'] = 0
		self.sample['sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment_avg']['multiplier'] = 1
		
		self.sample['sea_surface_wave_max_height_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_max_height_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_max_height_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_max_height_avg']['offset'] = 0
		self.sample['sea_surface_wave_max_height_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_significant_height_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_significant_height_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_significant_height_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_significant_height_avg']['offset'] = 0
		self.sample['sea_surface_wave_significant_height_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_sig_period_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_sig_period_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_sig_period_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_sig_period_avg']['offset'] = 0
		self.sample['sea_surface_wave_sig_period_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_mean_height_of_tenth_of_wave_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_mean_height_of_tenth_of_wave_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_mean_height_of_tenth_of_wave_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_mean_height_of_tenth_of_wave_avg']['offset'] = 0
		self.sample['sea_surface_wave_mean_height_of_tenth_of_wave_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_mean_period_of_h10_waves_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_mean_period_of_h10_waves_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_mean_period_of_h10_waves_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_mean_period_of_h10_waves_avg']['offset'] = 0
		self.sample['sea_surface_wave_mean_period_of_h10_waves_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_mean_wave_period_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_mean_wave_period_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_mean_wave_period_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_mean_wave_period_avg']['offset'] = 0
		self.sample['sea_surface_wave_mean_wave_period_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_peak_period_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_peak_period_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_peak_period_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_peak_period_avg']['offset'] = 0
		self.sample['sea_surface_wave_peak_period_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_mean_height_of_fifth_of_wave_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_mean_height_of_fifth_of_wave_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_mean_height_of_fifth_of_wave_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_mean_height_of_fifth_of_wave_avg']['offset'] = 0
		self.sample['sea_surface_wave_mean_height_of_fifth_of_wave_avg']['multiplier'] = 1
		
		self.sample['sea_surface_wave_HMO_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_HMO_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_HMO_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_HMO_avg']['offset'] = 0
		self.sample['sea_surface_wave_HMO_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_mean_direction_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_mean_direction_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_mean_direction_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_mean_direction_avg']['offset'] = 0
		self.sample['sea_surface_wave_mean_direction_avg']['multiplier'] = 1

		self.sample['sea_surface_wave_mean_spread_avg']['maxlimit'] = 999999 
		self.sample['sea_surface_wave_mean_spread_avg']['minlimit'] = 0
		self.sample['sea_surface_wave_mean_spread_avg']['units'] = 'tbd'
		self.sample['sea_surface_wave_mean_spread_avg']['offset'] = 0
		self.sample['sea_surface_wave_mean_spread_avg']['multiplier'] = 1
		
	def _getDataset(self): #had to override getSample because the sensor itself outputs a stats on a sample rather than individual readings
		try:
			dataSet = {}
			self._reader.write("!F3,3,3,3,3,3\n\r")
			self._reader.write("!FT0\n\r")
			#duration should in minutes
			self._reader.write("!R%s\n\r"%(float(self._settings["sample_duration"])/60))
			start = datetime.now()
			
			while True: #wait for data with timeout of 2 minutes past sample duration
				sleep(.5)
				ch = self._reader.read(1)
				if ch == '*':
					data_ready = True
					break
				if ((datetime.now() - start).total_seconds()) > float(self._settings["sample_duration"]) + 120:
					data_ready = False
					break
			
			raw = ""
			start = datetime.now()
			if data_ready:
				start = datetime.now()
				self._reader.write("?MFB\r\n")
				while True: #read data until ** is found or timeout of 1 minute
					buffer = self._reader.read(1024)
					raw = raw + buffer
					
					if "**" in buffer:
							break
							
					if (datetime.now() - start).total_seconds() > 60:
						break
						
				for line in raw.split('\r\n'): #check and package nmea messages and data sample. 
					line = self.checkNmeaLine(line)

					if line != False:
						self.NMEA = self.NMEA + "$"+line+"\r\n"
						data = line.split(',')
						if data[0] == "TSPWA":
							dataSet = {	"sea_surace_wave_number_of_zero_crossings": float(data[7]), #no cf name present
										"sea_surface_wave_mean_height": float(data[8]), #no cf name present
										"sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment": float(data[9]),
										"sea_surface_wave_max_height": float(data[10]), #no cf name present
										"sea_surface_wave_significant_height": float(data[11]),
										"sea_surface_wave_sig_period": float(data[12]), #no cf name present
										"sea_surface_wave_mean_height_of_tenth_of_wave": float(data[13]), #no cf name present
										"sea_surface_wave_mean_period_of_h10_waves": float(data[14]), #no cf name present
										"sea_surface_wave_mean_wave_period":float(data[15]),#no cf name present
										"sea_surface_wave_peak_period":float(data[16]),
										"sea_surface_wave_mean_height_of_fifth_of_wave":float(data[17]),
										"sea_surface_wave_HMO":float(data[18]),
										"sea_surface_wave_mean_direction":float(data[19]),
										"sea_surface_wave_mean_spread":float(data[20].split("*")[0])
								}
							State.setWave(dataSet)

						
			static = None
		#	self.sample = dataSet
			
		except:
			dataSet = None
			staticInfo = None
			print traceback.print_exc()
			
		return dataSet, None
	
	def _addSpecialStats(self):
		pass

			  
				

	
