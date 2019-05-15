from BaseSensor import BaseSensor
import traceback
import time
import sys

class FloodSensor(BaseSensor):
	voltage=sys.float_info.min;

	def __init__(self, settings, ts, dataset_id):
		super(FloodSensor, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor

	def _getSample(self):
		self.voltage = self.ts.read_adc(int(self._settings['adc_channel']));
		stats = {"voltage":self.voltage};
		self._setNMEA();
		return stats
	
	def _getDataset(self):
		dataSet = {"flood_status":self.voltage};
		return dataSet
	
	def _setNMEA(self):
                self.NMEA = "$PCTEC,FLOOD," + "{:.2f}".format(self.voltage)
                self.NMEA = self.NMEA+"*%s\r\n"%self._createNmeaChk(self.NMEA)
