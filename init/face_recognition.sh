#!usr/bin/bash

#sudo apt-get install libboost-all-dev
#sudo apt-get install libgtk-3-dev
#sudo apt-get install build-essential cmake
#sudo apt-get update 
#sudo apt-get install cmake
#sudo apt-get install scikit-image 
#pip3 install scikit-learn 

#pip3 install numpy scikit-learn cmake
#pip3 install dlib
#pip3 install face_recognition

wget http://dlib.net/files/dlib-19.23.tar.bz2
tar jxvf dlib-19.23.tar.bz2
cd dlib-19.23/
mkdir build
cd build/
cmake ..
cmake --build .
cd ../
sudo python3 setup.py install
sudo pip3 install pillow # lack a litle bit
sudo pip3 install face_recognition
