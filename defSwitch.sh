#!/bin/bash
function listInts { # Returns list of available interfaces
	echo "$(ip link | awk '{print $2}' | grep -oE "tun[0-9]+")"
}

function getActive { # Returns active interface
	if (ip route | grep -qE "tun[0-9]+"); then
		echo "$(ip route | grep "128.0.0.0/1" | awk '{print $5}')"
	else
		echo "None"	
	fi

}

if [[ -z "$1" ]]; then # If no arguments are supplied
	echo "Must provide interface"
	echo "Available interfaces: $(listInts)"
	exit 1

elif [ "$1" == "active" ]; then
	echo "Active interface is: $(getActive)"
	exit 0

elif [ "$1" == "list" ]; then
	echo "Available interfaces: $(listInts)"
	exit 0

elif [[ $EUID -ne 0 ]]; then
	echo "Changing interface requires sudo"
	exit 1

elif !(echo "$(listInts)" | grep -q "$1"); then # If input not in available interfaces
	echo "Interface \"$1\" is not valid"
	echo "Available interfaces: $(listInts)"
	exit 1

else
	echo $1
	ipv4="$(ip address show dev "$1" | grep "inet " | awk '{print $2}' | cut -d"/" -f1 | awk -F'.' '{print $1"."$2"."$3".1"}')"

	if (ip route replace 0.0.0.0/1 via "$ipv4" dev "$1" &> /dev/null) && (ip route replace 128.0.0.0/1 via "$ipv4" dev "$1" &> /dev/null); then
		echo "Successfully set interface to $1"
	else
		echo "Failed to set interface to $1"
	fi	
fi


