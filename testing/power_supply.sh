clear
val=$1

if [ $# -ne 1 ];then
	echo "Usage: ./power_supply.sh <enable/disable>"
	echo "Example: ./power_supply.sh enable"
	exit
fi

enable="1_22"


if [ "$val" = "enable" ];then
	echo "Enable Power Regulator"
	tshwctl --setdio=$enable
elif [ "$val" = "disable" ];then
	echo "Disable Power Regulator"
	tshwctl --clrdio=$enable
fi

