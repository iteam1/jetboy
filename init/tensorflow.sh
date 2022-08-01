#!/bin/bash
# Install TensorFlow
# install tensorflow on jetson nano
sudo apt-get update
# install system packages required by tensorflow
sudo apt-get install libhdf5-serial-dev
sudo apt-get install hdf5-tools
sudo apt-get install libhdf5-serial-dev
sudo apt-get install zlibig-dev 
sudo apt-get install zip   
sudo apt-get install libjpeg8-dev
sudo apt-get install libapack-dev 
sudo apt-get install libblas-dev 
sudo apt-get install gfortran
# install and update pip3
sudo apt-get install python3-pip 
sudo pip3 install -U pip testresources setuptools==49.6.0
# install the python package dependencies
sudo pip3 install -U --no-deps numpy==1.19.4 future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython pkgconfig
sudo env H5PY_SETUP_REQUIRES=0 pip3 install -U h5py==3.1.0
# Install TensorFlow using the pip3 command. This command will install the latest version of TensorFlow compatible with JetPack 4.6.
sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 tensorflow
#Note: TensorFlow version 2 was recently released and is not fully backward compatible with TensorFlow 1.x. If you would prefer to use a TensorFlow 1.x package, it can be installed by specifying the TensorFlow version to be less than 2, as in the following command:
# sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 'tensorflow<2'
# If you want to install the latest version of TensorFlow supported by a particular version of JetPack, issue the following command:
# sudo pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v$JP_VERSION tensorflow

# Upgrading TensorFlow
#Note: Due to the recent package renaming, if the TensorFlow version you currently have installed is older than the 20.02 release, you must uninstall it before upgrading to avoid conflicts. See the section on Uninstalling TensorFlow for more information.To upgrade to a more recent release of TensorFlow, if one is available, run the install command with the ‘upgrade’ flag:
#$ sudo pip3 install --upgrade --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v$461 tensorflow

# Uninstall TensorFlow
# sudo pip3 uninstall -y tensorflow
# if you are a version of tensorflow older than 20.2 package-name is tensorflow-gpu 
#sudo pip3 uninstall -y tensorflow-gpu

# Install tensorflow-hub
pip3 install --upgrade tensorflow-hub

echo "Installation 's done!"