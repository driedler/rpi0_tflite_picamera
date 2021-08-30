#!/usr/bin/bash


set -e

# This library is needed to install some shared libs required by numpy
# sudo apt-get instal -y libwebp-dev libtiff5 libopenjp2-7 openexr
sudo apt-get install -y libatlas-base-dev libjasper-dev libqtgui4 python3-pyqt5 libqt4-test  libopencv-dev libgstreamer1.0-0  python3-pip

# Install debugpy
# https://github.com/microsoft/debugpy/
# Which is used to single-setup debug Python apps remotely
pip3 install debugpy~=1.3.0

# Install picamera
# which is used to access the Raspberry PI Camera module
pip3 install picamera

# Install OpenCV for Python
# which is used to convert JPEG to numpy
# NOTE: We need opencv 3.4.2.17 as that uses numpy-1.19 which is what 
# tflite_micro_runtime uses
pip3 install numpy>=1.19,<1.20
pip3 install opencv-python==3.4.2.17


# Install tflite_micro_runtime
# https://github.com/driedler/tflite_micro_runtime
# Which is used to classify images
pip3 install https://github.com/driedler/tflite_micro_runtime/releases/download/1.0.0/tflite_micro_runtime-1.0.0-cp37-cp37m-linux_armv6l.whl


# Create the project directory
# with permissions to be written by anyone 
# (so that the dirsync tool can sync the dir before debugging)
echo "Creating workspace directory at /home/pi/rpi0_tflite_picamera"
mkdir -p /home/pi/rpi0_tflite_picamera
chmod 0777 /home/pi/rpi0_tflite_picamera
sudo chmod -R 0777 /home/pi/.local/lib/python3.7/site-packages
sudo chmod -R 0777 /usr/lib/python3/dist-packages

