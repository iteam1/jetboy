#!/usr/bin/bash
# refer to https://github.com/dusty-nv/jetson-inference/blob/master/docker/run.sh#L118

banner(){
	echo "_______________________________________________"
	echo "|    _  _____ _____  _____   _____  ___  _    |" 
	echo "|   / |/  __//__ __\/  _  \ /  _  \ \  \//    |"
	echo "|   | ||  \    / \  | | / / | / \ |  \  /     |" 
	echo "|/\_| ||  /_   | |  | |_\ \ | \_/ |  / /      |"  
	echo "|\____/\____\  \_/  \____ / \_____/ /_/ ver0.7|"
	echo "|_____________________________________________|" 
	}

show_help(){
	echo " "
	echo "Usage: Entry point to start Robot-Jetboy"
	echo " "
	echo "Args:"
	echo " "
	echo "  -h|--help: Show this help text and quit"
	echo " "
	echo "  -m|--mission: Do specific mission, example: bash root.sh -m 1"
	echo " "
}

die(){
	printf '%s\n' "$1"
	show_help
	exit 1
}

task1(){
	echo "Task1 Doing..."
}

task2(){
	echo "Task2 Doing..."
}

banner # display banner

while :; # true
do
	# check the first argument after run command
	case $1 in
		-h|-\?|--help) # if the first argument is --help, -h or \?
			show_help # Display a usage synopsis
			exit
			;;
		-m|--mission) # if the first arugment is --mission, -m
			if [ "$2" ]; then # if there is argument after first argument
				task1
				shift
			else
				die 'ERROR: "--mission" requries a non empty option argument'
			fi
			;;
		--mission=) # Handle the case of an empty --mission=
			die 'ERROR: "--mission" requries a non empty option argument'
			;;
		--) # End of all options.
			shift
			break
			;;
		-?*)
			printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
			;;
		*) # Default case: No more options, so break out of the loop
			break
	esac
	shift
done