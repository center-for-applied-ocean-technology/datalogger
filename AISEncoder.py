class AISEncoder():
    def getDegrees(self, binVal):
        return(self.sint(binVal)/600000.0)

    def sint(self, binStr):        
        if binStr[0] =='1':           
            newString = ""
            for i in range(1, len(binStr)):
                if binStr[i] == '1':
                    newString = newString + '0'
                else:
                    newString = newString + '1'
            intval = (int(newString,2) + 1)*-1
        else:
            intval = int(binStr,2)
        return intval

    def itobs (self, val, length):
        val = int(val)
        if val > 0:
            return ("{0:0%sb}"%length).format(val)
        else:
            val = val*-1
            binstring = ("{0:0%sb}"%length).format(val)
            inverse = ""
            for bit in binstring:
                if bit == '1':
                    inverse = inverse + '0'
                else:
                    inverse = inverse + '1'
        return ("{0:0%sb}"%length).format(int(inverse,2) + 1)
    
    def itobu(self, val, length):
        val = int(val)
        return ("{0:0%sb}"%length).format(val)

    def btos(self, binaryString):
        table44 = ["@", "A", "B", "C", "D", "E", "F", "G", \
		"H", "I", "J", "K", "L", "M", "N", "O", "P", \
		"Q", "R", "S", "T", "U", "V", "W", "X", "Y", \
		"Z", "[", "\\", "]", "^", "_", " ","!", '"', \
		"#", "$", "%", "&", "`", "(", ")", "*", "+", \
		",", "-", ".", "/", "0", "1", "2", "3", "4", \
		"5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?"]
        i = 0
        result = "" 
        while i < len(binaryString):
            result = result + table44[int(binaryString[i:i+6],2)]
            i = i + 6
            
        return result

    def weatherObservation(self, lon = 181*60000, lat = 91*60000, \
		day=0, hour=24, minute=60, weather = 8, visibility = 127, \
		humidity = 101, wind_spd_avg = 127, wind_dir_avg = 360, \
		air_pressure_avg = 403 + 799, air_pressure_tend= 15, \
		air_temp_avg = -102.4, water_temp_avg = 501, \
		wave_period = 63, wave_ht_sig = 25.5, wave_dir_avg = 360, \
		swell_ht_avg = 255, swell_dir_avg = 360, swell_period_avg = 63, \
		spare = 0):

        binstring = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s"

        values = (self.itobu(1,10),  #DAC 001
		self.itobu(11,6),  #FI 21
		self.itobu(0,1),   #Type of Weather Report. Always 0
		self.itobu(0, 120),#Geographic Location. Left blank for now as weather reports are automated.
		self.itobs(lon*60000, 25),
		self.itobs(lat*60000, 24),
		self.itobu(day,5),
		self.itobu(hour,5),
		self.itobu(minute,6),
		self.itobu(weather,4),
		self.itobu(visibility,8),
		self.itobu(humidity,7),
		self.itobu(wind_spd_avg,7),
		self.itobu(wind_dir_avg,9),
		self.itobu(air_pressure_avg-799,9),          
		self.itobu(air_pressure_tend, 4),            #has to be fixed.
		self.itobs(air_temp_avg*10,11),
		self.itobs(water_temp_avg, 10),              #has to be fixed
		self.itobu(wave_period,6),
		self.itobu(wave_ht_sig*10,8),
		self.itobu(wave_dir_avg,9),
		self.itobu(swell_ht_avg,8),
		self.itobu(swell_dir_avg,9),
		self.itobu(swell_period_avg,6),
		self.itobu(0,3))                            #spare, not used. Set to zero.

        payload = self.b2a(binstring%values)
        message = "WIBBM,1,1,1,3,08,%s,0"%payload
        message = "!"+message + "*%s\r\n"%self.createChecksum(message)
        
        return message

    def createChecksum(self,sentence):
        calc_cksum = 0
        for s in sentence:
            calc_cksum ^= ord(s)
        return "%02X"%calc_cksum

    def b2a(self, binaryString):
        result = ""
        i = 0
        result = ""
        payload = ["0","1","2","3","4","5","6","7","8","9",":",\
		";","<","=",">","?","@","A","B","C","D","E","F",\
		"G","H","I","J","K","L","M","N","O","P","Q","R",\
		"S","T","U","V","W","`","a","b","c","d","e","f",\
		"g","h","i","j","k","l","m","n","o","p","q","r",\
		"s","t","u","v","w"]

        while i < len(binaryString):
            dec = int(binaryString[i:i+6],2)
            result = result + payload[dec]

            i = i + 6
           
        return result

