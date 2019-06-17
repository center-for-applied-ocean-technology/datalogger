#!/usr/bin/python
import math
import time
import threading
from ConfigParser import ConfigParser
import serial
#import State
from subprocess import call,PIPE,Popen
from subprocess import check_output 
from TsHardware import TsHardware
from datetime import datetime
import sys
from imp import reload
import logging

t_start = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())

state = {}
def read_config (ini_file):
	config=ConfigParser()
	config.read(ini_file)
	return config


#connect to TS7400
ts = TsHardware()

#read ini file
threads = []
id = 1

config = read_config("buoy.ini")


interval = config.getint('Main','Interval');
logfile = config.get('Main','LogFile')
loglevel = eval("logging." + config.get('Main','LogLevel'))
watchdog = config.getboolean('Main','watchdog');
#State.enabled = config.getboolean('Main', 'webInterface');

#setup logger
logging.basicConfig(filename=logfile,level=loglevel,
	format='%(asctime)s : %(name)s : %(levelname)s : %(message)s')
logging.debug('Buoy Script Started')


sensors = []
comms = []

#feed watchdog
max_time_s = -1
if watchdog:
	ts.feed_watchdog(99)

for section in config.sections():
	if (config.has_option(section,'module') & config.has_option(section,'name')):
		settings = dict(config.items(section))
		settings['start time'] = t_start
		logging.info(settings)
		module = __import__(settings['module'])
		device = getattr(module, settings['module'])(settings,ts,id)
		logging.debug('Loaded Module %s', settings['module'])
		if (settings['ctype'] == "sensor"):
			sensors.append(device)
			tm = float(settings['warm_time'])+float(settings['sample_duration'])
			if (tm > max_time_s):
				#max time in seconds
				max_time_s = tm;
		else:
			comms.append(device)
			tm = float(settings['warm_time'])
			if (tm > max_time_s):
				#max time in seconds
				max_time_s = tm;
		id += 1

#add check to ensure other relays are off?

#start data acquisition
for sensor in sensors:
	sensor.start()


if watchdog:
	ts.feed_watchdog(max_time_s)

#wait for acquisition to finish
for sensor in sensors:
	logging.debug('Waiting for Sensor to join')
	sensor.join()


#logging.debug('Wait 60s for connection')
#time.sleep(60)

#start up external communications
for comm in comms:
	comm.start();

for comm in comms:
	logging.debug('Waiting for Comm to join')
	comm.join();
	comm.writeSensor(comm.createNmea("PCTEC,STATUS,START," + t_start))

t_end = time.time();
t_wkup = int(t_end) - (int(t_end)%interval) + interval

for sensor in sensors:
	sensor.close()
	for comm in comms:
		logging.debug('write NMEA to comm')
		comm.writeSensor(sensor.getJSON())
		#comm.writeSensor('\r\n')
	

#Some debugging commands
for comm in comms:
	comm.writeSensor(comm.createNmea("PCTEC,STATUS,END," + time.ctime()))
	comm.writeSensor(comm.createNmea("PCTEC,STATUS,Next power on at " + time.ctime(t_wkup)))
	comm.writeSensor(comm.createNmea("PCTEC,STATUS,Sleeping (" + str(t_wkup - time.time()) + "s)......zzzzz"))

logging.debug('Next power on at %s', time.ctime(t_wkup))

p = Popen(["users"],stdout=PIPE, bufsize=1)

#wait specified time before sleeping so user can connect
users = p.stdout.read()
users = users.strip()

#if (len(users) == 0 and ts.diagnostics_connected()==0):
logging.debug('len(users) %s',str(len(users)))

#close all comms
for comm in comms:
	comm.close()

#ts.clear_all_relays()
if (len(users) == 0):
	wakeup = t_wkup - time.time()
	logging.debug('wakeup %s',str(wakeup))
	logging.shutdown()
	if (wakeup > 0):
		t_cmd = "--timewkup=" + str(wakeup)
		call(["tshwctl", t_cmd, "--sleep"])
	Popen(["nohup", "/home/buoy/datalogger/buoy.py"])
else:
	logging.debug('TS 7400 did not sleep')
	if watchdog:
		ts.disable_watchdog()
		logging.debug('Disable Watchdog')
	if (len(users) > 0):
		logging.debug(' %s logged on', users)
#	if (ts.diagnostics_connected()==1):
#		logging.debug('diagnostics cable detected')
	wakeup = t_wkup - time.time()
	logging.debug('wakeup %s',str(wakeup))
	logging.shutdown()
	if (wakeup < 0):
		wakeup=0
	time.sleep(wakeup)
	Popen(["nohup", "/home/buoy/datalogger/buoy.py"])

exit();

