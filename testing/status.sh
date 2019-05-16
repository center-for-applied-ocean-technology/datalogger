clear

if [ $# -ne 0 ];then
	echo "Usage: ./clear_all.sh"
	exit
fi

#clear dio
select1="1_17"
select2="1_18"
select3="1_19"
select4="1_20"
enable="1_21"
ps_enable="1_22"
Z="1_16"
type="reset"
	
#enable relay board power supply
echo "Enable Relay Board Power Regulator"
tshwctl --setdio=$ps_enable
#tshwctl --clrdio=$Z

for (( val=1; val <= 16; val++))
do
	tshwctl --clrdio=$select1,$select2,$select3,$select4


	if [ "$val" -eq 1 ];then
		tshwctl --clrdio=$select1,$select2,$select3,$select4
	elif [ "$val" -eq 2 ];then
		tshwctl --setdio=$select1
	elif [ "$val" -eq 3 ];then
		tshwctl --setdio=$select2
	elif [ "$val" -eq 4 ];then
		tshwctl --setdio=$select1,$select2
	elif [ "$val" -eq 5 ];then
		tshwctl --setdio=$select3
	elif [ "$val" -eq 6 ];then
		tshwctl --setdio=$select1,$select3
	elif [ "$val" -eq 7 ];then
		tshwctl --setdio=$select2,$select3
	elif [ "$val" -eq 8 ];then
		tshwctl --setdio=$select1,$select2,$select3
	elif [ "$val" -eq 9 ];then
		tshwctl --setdio=$select4
	elif [ "$val" -eq 10 ];then
		tshwctl --setdio=$select1,$select4
	elif [ "$val" -eq 11 ];then
		tshwctl --setdio=$select2,$select4
	elif [ "$val" -eq 12 ];then
		tshwctl --setdio=$select1,$select2,$select4
	elif [ "$val" -eq 13 ];then
		tshwctl --setdio=$select3,$select4
	elif [ "$val" -eq 14 ];then
		tshwctl --setdio=$select1,$select3,$select4
	elif [ "$val" -eq 15 ];then
		tshwctl --setdio=$select2,$select3,$select4
	elif [ "$val" -eq 16 ];then
		tshwctl --setdio=$select1,$select2,$select3,$select4
	fi
	#tshwctl --setdio=$Z

	a=`tshwctl --getdio="1_14"`
	b=`expr substr $a 9 10`
	echo "Relay $val = $b"
	#sleep 1s for testing
	sleep .01
	#tshwctl --clrdio=$Z

done 

echo "Disable Power Regulator"
tshwctl --clrdio=$ps_enable

