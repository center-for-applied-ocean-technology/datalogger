from BaseSensor import BaseSensor
import traceback
import time
import sys

class BT(BaseSensor):
	def __init__(self, settings, ts, dataset_id):
		super(BT, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor

	def run(self):
		self._turnOn()
		time.sleep(float(self._settings['warm_time']))
	
	def close(self):
                self._reader.close()
		self._turnOff()
