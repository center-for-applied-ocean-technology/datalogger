from BaseSensor import BaseSensor
import traceback
import time
import sys

class Voltage(BaseSensor):
	voltage=sys.float_info.min;

	def __init__(self, settings, ts, dataset_id):
		super(Voltage, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor
		self.sample = {"voltage_avg":{},
				"timestamp":{},
				"warm_time":{},
				"duration":{}}

		self.sample['voltage_avg']['maxlimit'] = 20
		self.sample['voltage_avg']['minlimit'] = 0
		self.sample['voltage_avg']['units'] = 'Volts'
		self.sample['voltage_avg']['multiplier'] = 100
		self.sample['voltage_avg']['offset'] = 0
		self._ignoreFields = ["warm_time", "duration", "timestamp"] #fields that will not have simple averaging

	def _getDataset(self):
		dataSet = {"voltage":self.ts.read_adc(int(self._settings['adc_channel']))*6.1066/1000.0};
		dataSet = {"voltage":self.ts.read_adc(int(self._settings['adc_channel']))*6.1430/1000.0};
		time.sleep(1)
		return dataSet, None
	
	def _setNMEA(self):
                self.NMEA = "$PCTEC,FLOOD," + "{:.2f}".format(self.voltage)
                self.NMEA = self.NMEA+"*%s\r\n"%self._createNmeaChk(self.NMEA)
