from time import sleep
import os
import threading
import subprocess
import logging

#Thread safe class for access the TS Hardware Control
#
#Class TsHardware
#
#Public Methods:
#	set_relay(relay)
#	clear_relay(relay)
#	clear_all_relays()
#	set_all_relays()
#	read_adc(channel)
#	diagnostics_connected()


class TsHardware(threading.Thread, object):
	RELAY_MUX_ENABLE = "1_16";
	RELAY_SELECT_1 = "1_17";
	RELAY_SELECT_2 = "1_18";
	RELAY_SELECT_3 = "1_19";
	RELAY_SELECT_4 = "1_20";
	RELAY_ENABLE = "1_21";
	PS_ENABLE = "1_22";
	RELAY_STATUS = "1_14";
	RELAYS = 16;
	DIAGNOSTICS_CONNECTED = "1_8";
	
	adc = {};

	ADC = {"LRADC_ADC1_millivolts":1, "LRADC_ADC2_millivolts":2, "LRADC_ADC3_millivolts":3, "LRADC_ADC4_millivolts":4};

	def __init__(self):
		self.lock = threading.Lock();

	#set relay address (1-16)
	def _set_relay_address(self,relay):
		relay = int(relay);
		relay = relay -1;
		if ((relay & 0x0001)):
			args = "--setdio=" + self.RELAY_SELECT_1
			subprocess.call(["tshwctl", args])
		else:
			args = "--clrdio=" + self.RELAY_SELECT_1
			subprocess.call(["tshwctl", args])
		if ((relay & 0x0002)):
			args = "--setdio=" + self.RELAY_SELECT_2
			subprocess.call(["tshwctl", args])
		else:
			args = "--clrdio=" + self.RELAY_SELECT_2
			subprocess.call(["tshwctl", args])
		if ((relay & 0x0004)):
			args = "--setdio=" + self.RELAY_SELECT_3;
			subprocess.call(["tshwctl", args]);
		else:
			args = "--clrdio=" + self.RELAY_SELECT_3;
			subprocess.call(["tshwctl", args]);
		if ((relay & 0x0008)):
			args = "--setdio=" + self.RELAY_SELECT_4;
			subprocess.call(["tshwctl", args]);
		else:
			args = "--clrdio=" + self.RELAY_SELECT_4;
			subprocess.call(["tshwctl", args]);
	
	def _set_relay_enable(self):
		args = "--clrdio=" + self.RELAY_ENABLE;
		subprocess.call(["tshwctl", args]);
		
	def _clear_relay_enable(self):
		args = "--setdio=" + self.RELAY_ENABLE;
		subprocess.call(["tshwctl", args]);
	
	def set_ps_enable(self):
		args = "--setdio=" + self.PS_ENABLE;
		subprocess.call(["tshwctl", args]);
		
	def clear_ps_enable(self):
		args = "--clrdio=" + self.PS_ENABLE;
		subprocess.call(["tshwctl", args]);
	
	def _set_mux_enable(self):
		args = "--setdio=" + self.RELAY_MUX_ENABLE;
		subprocess.call(["tshwctl", args]);
	
	def _get_relay_status(self):
		args = "--getdio=" + self.RELAY_STATUS;
		p = subprocess.Popen(["tshwctl", args],stdout=subprocess.PIPE, bufsize=1);
                tmp = p.stdout.read()
                tmp = tmp.split("\n")
                val = tmp[0].split("=")
		if (val[1] == "1"):
			return 1
		else:
			return 0
		
	def _clear_mux_enable(self):
		args = "--clrdio=" + self.RELAY_MUX_ENABLE;
		subprocess.call(["tshwctl", args]);

	def feed_watchdog(self, time):
		#feed watchdog with interval if diagnostic cable is not attached
		#if (self.diagnostics_connected()==0):
		while (time > 0):
			if (time > 99.9):
				watchdog = 'f999'
			else:
				watchdog = 'f{:3.0f}'.format(time*10)
			self.lock.acquire();
			wd = os.open("/dev/watchdog", os.O_RDWR|os.O_SYNC)
			os.write(wd,watchdog)
			os.close(wd)
			self.lock.release();
			sleep(1)
			time -= 1

	def disable_watchdog(self):
		#feed watchdog with "3" to disable 
		self.lock.acquire();
		wd = os.open("/dev/watchdog", os.O_RDWR|os.O_SYNC)
		os.write(wd,"3")
		os.close(wd)
		self.lock.release();

	def diagnostics_connected(self):
		#if the appropiate pins are crossed on the diagnostic cable
		#the DIAGNOSTICS pin will be pulled low indicating that the
		#the cable is connected.  This can be used with in the script
		#to prevent the computer from rebooting.
		args = "--getdio=" + self.DIAGNOSTICS_CONNECTED
		self.lock.acquire()
		p = subprocess.Popen(["tshwctl", args],stdout=subprocess.PIPE, bufsize=1)
		self.lock.release();
                tmp = p.stdout.read()
                tmp = tmp.split("\n")
                val = tmp[0].split("=")
		if (val[1] == "1"):
			return 0
		else:
			return 1

	def set_relay(self,relay):
		self.lock.acquire()
		self.set_ps_enable();
		self._set_relay_address(relay);
		self._set_mux_enable();
		self._set_relay_enable();
		self._clear_mux_enable();
		self.clear_ps_enable();
		self.lock.release();
		
	def clear_relay(self,relay):
		self.lock.acquire()
		self.set_ps_enable();
		self._set_relay_address(relay);
		self._set_mux_enable();
		self._clear_relay_enable();
		self._clear_mux_enable();
		#self.clear_ps_enable();
		self.lock.release();
		
	def clear_all_relays(self):
		self.lock.acquire()
		self.set_ps_enable();
		for relay in range(1,self.RELAYS+1):
			self._set_relay_address(relay);
			self._set_mux_enable();
			self._clear_relay_enable();
			self._clear_mux_enable();
		self.clear_ps_enable();
		self.lock.release();
		
	def set_all_relays(self):
		self.lock.acquire()
		self.set_ps_enable();
		for relay in range(1,self.RELAYS+1):
			self._set_relay_address(relay);
			self._set_mux_enable();
			self._set_relay_enable();
			self._clear_mux_enable();
		self.clear_ps_enable();
		self.lock.release();
	
	def get_all_relays_status(self):
		status = []
		for relay in range(1,self.RELAYS+1):
			tmp = self.get_relay_status(relay)

	def get_relay_status(self,relay):
		self.lock.acquire()
		self.set_ps_enable();
		self._set_relay_address(relay);
		#self._set_mux_enable();
		status=self._get_relay_status();
		self.clear_ps_enable();
		self.lock.release();
		return status;
		

	def read_adc(self,channel):
		tmp=[];
		self.lock.acquire();
		p = subprocess.Popen(["tshwctl", "--cpuadc"],stdout=subprocess.PIPE, bufsize=1)
		self.lock.release();
                tmp = p.stdout.read()
                tmp = tmp.split("\n")
                for line in tmp:
                        if len(line) > 0:
                                val=line.split("=")
				if (val[0] in self.ADC):
					self.adc[self.ADC[val[0]]]=int(val[1])
		return self.adc[channel]
	
	def ps_enabled(self):
		tmp=[];
		self.lock.acquire();
		p = subprocess.Popen(["tshwctl", "--getdio="+self.PS_ENABLE],stdout=subprocess.PIPE, bufsize=1)
		self.lock.release();
                tmp = p.stdout.read()
                tmp = tmp.split("\n")
                for line in tmp:
			if len(line) > 0:
				val=line.split("=")
				if (val[0] == "dio"+self.PS_ENABLE):
					return val[1]
				else:
					return -1

	def set_system_time_from_ZDA(self, zda):
		#parse NMEA ZDA string
		tmp=zda.split(",");
		nmea_type=tmp[0]
		if (nmea_type == "$GPZDA"):
			time_str=tmp[1];
			day=tmp[2];
			month=tmp[3];
			year=tmp[4];

		#TOD0: need to set system time
		#subprocess.call(["date", args])

	def get_short_mac_address(self):
		args = "--getmac";
		p = subprocess.Popen(["tshwctl", args],stdout=subprocess.PIPE, bufsize=1);
                tmp = p.stdout.read()
                tmp = tmp.split("\n")
                val = tmp[1].split("=")
		return val[1]
		
#	def close(self):
