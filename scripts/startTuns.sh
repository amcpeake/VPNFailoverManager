#!/bin/bash

if [[ -z "$1" ]]; then
  echo "Please provide a list of tunnels"
fi

if [[ $EUID -ne 0 ]]; then
	echo "Starting tunnels requires sudo"
	exit 1
fi

for f in "$@"; do
  openvpn --config "$f" --daemon
done