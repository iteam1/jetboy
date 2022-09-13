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
	echo "  -m|--mission: Do specific mission, example: sudo bash root.sh -m 1"
	echo " "
}

die(){
	printf '%s\n' "$1"
	show_help
	exit 1
}

mission_1(){
	python3 ./utils/helloworld.py
}

mission_2(){
	python3 ./utils/helloworlds.py
}

mission_3(){
	python3 gpio.py &
	python3 server.py &
}

# display banner
banner
echo ""

# give super-user permission
#sudo su 

# list all serial port and store in serials array
serials=($(ls /dev/ttyUSB*))
echo "Serial devices connected in port: "
#echo ${serials[1]}
for i in ${serials[@]}
do
	chmod a+rw ${i}
	echo "${i}"
done
echo "---"

# list all camera and store in videos array
videos=($(ls /dev/video*))
echo "Camera devices connected: "
for i in ${videos[@]}
do
	echo "${i}"
done
echo "---"

while :; # true
do
	# check the first argument after run command
	case $1 in
		-h|-\?|--help) # if the first argument is --help, -h or \?
			show_help # Display a usage synopsis
			exit
			;;
		-m|--mission) # if the first arugment is --mission, -m
			# echo "MISSION case"
			if [ "$2" ]; then # if there is argument after first argument
				echo "MISSION ${2} archieved."
				case $2 in
					1)
						echo "MISSION ${2} doing."
						mission_1
					;;
					2)
						echo "MISSION ${2} doing."
						mission_2
					;;
					3)
						echo "MISSION ${2} doing."
						mission_3
					;;
				esac
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