#!/usr/bin/bash

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
	echo "  --help Show this help text and quit"
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

