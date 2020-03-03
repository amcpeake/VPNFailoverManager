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

elif [ "$1" == "clear" ]; then
	if (ip route delete 0.0.0.0/1 &> /dev/null) && (ip route delete 128.0.0.0/1 &>/dev/null); then
		echo "Successfully cleared tunnel configuration"
		exit 0
	else
		echo "Failed to clear tunnel configuration"
		exit 1
	fi

elif !(echo "$(listInts)" | grep -q "$1"); then # If input not in available interfaces
	echo "Interface \"$1\" is not valid"
	echo "Available interfaces: $(listInts)"
	exit 1

else
	ipv4="$(ip address show dev "$1" | grep "inet ")"
	if (echo "$ipv4" | grep -q "peer"); then
		ipv4="$(echo "$ipv4" | awk '{print $4}' | cut -d"/" -f1)"
	else
		ipv4="$(echo "$ipv4" | awk '{print $2}' | cut -d"/" -f1 | awk -F'.' '{print $1"."$2"."$3".1"}')"
	fi
	
	if (ip route replace 0.0.0.0/1 via "$ipv4" dev "$1" &> /dev/null) && (ip route replace 128.0.0.0/1 via "$ipv4" dev "$1" &> /dev/null); then
		echo "Successfully set interface to $1"
		exit 0
	else
		echo "Failed to set interface to $1"
		exit 1
	fi	
fi


