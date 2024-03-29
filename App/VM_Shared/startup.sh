#!/bin/bash

TIMEOUT=0
TEST_DIR="/media/"
SHARED_DIR="/media/sf_Program_Shared/"

while [ $TIMEOUT -lt 100 ]
do
	if [ -d "$SHARED_DIR" ]; then
		cd "$SHARED_DIR" 2> /tmp/Error
		message=$(cat /tmp/Error)
		messageLength=$(expr length "$message")
		if [ $messageLength -lt 1 ]; then
			notify-send "Starting teaching software..."
			cd $SHARED_DIR"App/"
			python3 runner.py
			exit
		fi
	fi

	sleep 5
	TIMEOUT=$((TIMEOUT+1))
	echo "Attempt to find file $TIMEOUT"
done

notify-send "Could not find shared file."
