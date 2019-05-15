from ConfigParser import ConfigParser
#from threading import Thread, Event
from time import sleep
from datetime import datetime
import numpy
#import MySQLdb
import traceback
import errno
import os
from time import sleep
from threading import Thread, Event
from math import atan2, degrees
import logging
import json
import zlib
import base64

class BaseSensor(Thread, object):
	def __init__(self, settings, ts, dataset_id = None):
		super(BaseSensor, self).__init__() #Thread.__init__
		self._settings = settings
		logging.info('%s has initialized ', settings['name']); 
		self._reader = self.connect()
		self.dataset_id = dataset_id
		self.NMEA = ""
		self._sampling = True
		self.ts = ts
		if (settings['ctype'] == "sensor"):
			self.sensor = {"Type": settings['type'],
				"Manufacturer": settings['manufacturer'],
				"Model Number": settings['model number'],
				"Serial Number": settings['serial number'],
				"Logger ID": ts.get_short_mac_address(),
				"Start Time": settings['start time']
				}

	def run(self):
		self._turnOn()
		sleep(float(self._settings['warm_time']))
		self._getSample()
		self._turnOff()
	
	def getNMEA(self):
		return self.NMEA

	def getJSON(self):
		json_str = json.dumps({"sensor":self.sensor,"sample":self.sample})
		json_str = zlib.compress(json_str,9)
		json_str = base64.b64encode(json_str)
		str = "PCTEC,JSON," + json_str
		return "$" + str+"*%s\r\n"%self._createNmeaChk(str)

	def _createNmeaChk(self, line):
		line = line.strip('\r\n$')
		#line = line.replace(' ', '')
		calc_cksum = 0
		for s in line:
			calc_cksum ^= ord(s)
		return '%02X' % calc_cksum

	def createNmea(self, line):
		return "$" + line + "*%s\r\n"%self._createNmeaChk(line)	

	def checkNmeaLine(self, line):
		
		# Check NMEA sentences
		line = line.strip('\r\n$')
		line = line.replace(' ', '')
		try :
			nmeadata, cksum = line.split('*', 1)
			calc_cksum = 0
			for s in nmeadata:
				calc_cksum ^= ord(s)
			result = (int(cksum, 16) == calc_cksum)
			if not result:
				line = False
		except ValueError:
			return False
		return line
		

	def connect(self):
		if self._settings['type'] == 'serial':
			import serial
			port = self._settings['port'].strip()
			baud = int(self._settings['baud'].strip())
			parity = self._settings['parity'].strip()
			bytesize = int(self._settings['bytesize'].strip())
			stopbits = float(self._settings['stopbits'].strip())
			timeout = float(self._settings['timeout'].strip())
			ser = serial.Serial(port, baud, bytesize, parity, stopbits, timeout)
			ser.close()
			ser.open()
			reader = ser
		elif self._settings['type'] == "tcp_client":
			import socket
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
			address = self._settings['address'].strip()
			port = int(self._settings['port'].strip())
			timeout = float(self._settings['timeout'].strip())
			s.settimeout(timeout)
			try:
				s.connect((address, port))
				reader = s.makefile("rw")
			except:
				reader = 0;
		elif self._settings['type'] == "tcp_server":
			import socket
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
			#address = self._settings['address'].strip()
			port = int(self._settings['port'].strip())
			timeout = float(self._settings['timeout'].strip())
			#s.settimeout(timeout)
			s.bind(('localhost', port))
			reader = None

			#s.connect((address, port))
			#reader = s.makefile("rw")
			reader = 0;
		elif self._settings['type'] == "file":
			filename = self._settings['filename'].strip()
			try:
				reader = open(filename,'a')
			except:
				reader = 0;
		elif self._settings['type'] == "analog":
			reader = None
		return reader

	def readline(self):
		return self._reader.readline()
	
	def _readBuffer(self):
		return self._reader.read(self._reader.inWaiting())
	
	def _getDataset(self):
		raise NotImplementedError()
	
	def _turnOn(self):
		self.ts.set_ps_enable()
		self.ts.set_relay(self._settings['relay'])

	def _turnOff(self):
		self.ts.set_ps_enable()
		self.ts.clear_relay(self._settings['relay'])
	
	def _createSampleDict(self, dataset):
		sample = {}
		for field in dataset:
			sample[field] = []
			sample[field].append(dataset[field])
		return sample
	
	def _getSample(self):

		start = datetime.now()
		sample = {}
		while self._sampling:
			duration = (datetime.now()-start).total_seconds()
			if duration > float(self._settings['sample_duration'].strip()):
				self._sampling = False
				break
			else:
				
				dataset, staticInfo = self._getDataset()
				if dataset != None:
					if sample == {}:
						sample = self._createSampleDict(dataset)
					else:
						for field in dataset:
							sample[field].append(dataset[field])

		#stats = {}
		self.sample["warm_time"] = {}
		self.sample["duration"] = {}
		self.sample["timestamp"] = {}
		self.sample["warm_time"]["value"] = self._settings['warm_time']
		self.sample["duration"]["value"] = self._settings['sample_duration']
		self.sample["timestamp"]["value"] = '{:%Y-%m-%d %H:%M:%S}'.format(start)
		for field in sample:
			if field in self._ignoreFields:
				pass
			else:
				self.sample[field+"_avg"]["value"] = numpy.average(sample[field])
				"""{#'max':numpy.max(sample[field]),
								#'min':numpy.min(sample[field]),
								'avg':numpy.average(sample[field]),
								#'std':numpy.std(sample[field]),
								#'size':len(sample[field])
								}
				"""

		
		self._addSpecialStats() #addSpecialStats function to be written for cases where just simple average would not work or other stats required such as direction or gust 
		#self._setNMEA()
		return self.sample
		
	def _addSpecialStats(self):
		pass
	
	def _parser(self):
		raise NotImplementedError()
	
	def writeSensor(self, data):
		try:
			self._reader.write(data)
			self._reader.flush()
			os.fsync(self._reader.fileno())	
		except:
			pass

	def close(self):
		try:
			self._reader.close()
		except:
			pass
