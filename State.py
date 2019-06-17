import threading
import State
from datetime import datetime
lock = threading.Lock()
_varibles = {};

def update (sensor, dataSet):
	key = "%s_%s_%s"%(sensor["Manufacturer"],sensor["Model Number"], sensor["Serial Number"])
	State.lock.acquire()
	State._varibles[key] = [datetime.now(),dataSet]
	
	State.lock.release()


def getVarible(sensorName, varibleName):
	#should use try: finally: block just in case...
	State.lock.acquire()
	value = None
	if sensorName in State._varibles:
		if varibleName in State._varibles[sensorName][1]:
			#print State._varibles[sensorName]
			value = [State._varibles[sensorName][0], State._varibles[sensorName][1][varibleName]]
	State.lock.release()
	return value

