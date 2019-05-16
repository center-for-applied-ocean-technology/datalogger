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

for (( val=1; val <= 16; val++))
do
	tshwctl --clrdio=$select1
	tshwctl --clrdio=$select2
	tshwctl --clrdio=$select3
	tshwctl --clrdio=$select4


	if [ "$val" -eq 1 ];then
		echo "Relay 1 $type"
	elif [ "$val" -eq 2 ];then
		echo "Relay 2 $type"
		tshwctl --setdio=$select1
	elif [ "$val" -eq 3 ];then
		echo "Relay 3 $type"
		tshwctl --setdio=$select2
	elif [ "$val" -eq 4 ];then
		echo "Relay 4 $type"
		tshwctl --setdio=$select1
		tshwctl --setdio=$select2
	elif [ "$val" -eq 5 ];then
		echo "Relay 5 $type"
		tshwctl --setdio=$select3
	elif [ "$val" -eq 6 ];then
		echo "Relay 6 $type"
		tshwctl --setdio=$select1
		tshwctl --setdio=$select3
	elif [ "$val" -eq 7 ];then
		echo "Relay 7 $type"
		tshwctl --setdio=$select2
		tshwctl --setdio=$select3
	elif [ "$val" -eq 8 ];then
		echo "Relay 8 $type"
		tshwctl --setdio=$select1
		tshwctl --setdio=$select2
		tshwctl --setdio=$select3
	elif [ "$val" -eq 9 ];then
		echo "Relay 9 $type"
		tshwctl --setdio=$select4
	elif [ "$val" -eq 10 ];then
		echo "Relay 10 $type"
		tshwctl --setdio=$select1
		tshwctl --setdio=$select4
	elif [ "$val" -eq 11 ];then
		echo "Relay 11 $type"
		tshwctl --setdio=$select2
		tshwctl --setdio=$select4
	elif [ "$val" -eq 12 ];then
		echo "Relay 12 $type"
		tshwctl --setdio=$select1
		tshwctl --setdio=$select2
		tshwctl --setdio=$select4
	elif [ "$val" -eq 13 ];then
		echo "Relay 13 $type"
		tshwctl --setdio=$select3
		tshwctl --setdio=$select4
	elif [ "$val" -eq 14 ];then
		echo "Relay 14 $type"
		tshwctl --setdio=$select1
		tshwctl --setdio=$select3
		tshwctl --setdio=$select4
	elif [ "$val" -eq 15 ];then
		echo "Relay 15 $type"
		tshwctl --setdio=$select2
		tshwctl --setdio=$select3
		tshwctl --setdio=$select4
	elif [ "$val" -eq 16 ];then
		echo "Relay 16 $type"
		tshwctl --setdio=$select1
		tshwctl --setdio=$select2
		tshwctl --setdio=$select3
		tshwctl --setdio=$select4
	fi

	tshwctl --setdio=$Z

	#sleep 1s for testing
	sleep .25
	if [ "$val" -lt 17 ];then
		if [ $type = "reset" ];then
			tshwctl --setdio=$enable
		elif [ $type = "set" ];then
			tshwctl --clrdio=$enable
		else
			echo "Usage: ./test.sh <output> <set/reset>"
			echo "Example: ./test.sh 1 set"
		fi
	else	
		if [ $type = "reset" ];then
			tshwctl --clrdio=$enable
		elif [ $type = "set" ];then
			tshwctl --setdio=$enable
		else
			echo "Usage: ./test.sh <output> <set/reset>"
			echo "Example: ./test.sh 1 set"
		fi
	fi

	sleep .25

	tshwctl --clrdio=$Z
done 

echo "Disable Power Regulator"
tshwctl --clrdio=$ps_enable

