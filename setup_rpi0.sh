#!/usr/bin/bash


set -e

# This library is needed to install some shared libs required by numpy
sudo apt-get install -y libatlas-base-dev


# Install debugpy
# https://github.com/microsoft/debugpy/
# Which is used to single-setup debug Python apps remotely
pip3 install debugpy==1.3.0

# Install picamera
# which is used to access the Raspberry PI Camera module
pip3 install picamera

# Install OpenCV for Python
# which is used to convert JPEG to numpy
pip3 install opencv-python


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


