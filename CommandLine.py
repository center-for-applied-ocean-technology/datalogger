from BaseSensor import BaseSensor
import traceback
import time
import sys

class CommandLine(BaseSensor):
	def __init__(self, settings, ts, dataset_id):
		super(CommandLine, self).__init__(settings, ts, dataset_id) #__init__ Base Sensor

	def run(self):
		time.sleep(float(self._settings['warm_time']))
	
#	def close(self):
#                self._reader.close()
#
