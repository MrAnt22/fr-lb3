#!/bin/bash

echo "Start"

echo -e "Ulimit soft:"
ulimit -aS

echo -e "Ulimit hard:"
ulimit -aH

echo -n "Max open files:"
ulimit -n

echo -n "Max user procces:"
ulimit -u

echo -n "Max stack size:"
ulimit -s

echo -n "Max CPU time:"
ulimit -t

echo -n "Max virtual memory:"
ulimit -v

echo -e "Modifying:"

try_set(){
	local name="$1"
	local opt="$2"
	local val="$3"
	echo -n "Setting $name to $val:"
	if ulimit -$opt $val 2>/dev/null; then
		echo "Success":
	else
		echo "Failed"
	fi
}


try_set "max open files" n 2048
try_set "max stack size" s 1024
try_set "max CPU time" t 10

ulimit -aS

echo "End"




