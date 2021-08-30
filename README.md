# TF-Lite Image Classification for Raspberry PI Zero W

This demonstrates how to run image classification on a Raspberry PI Zero W using:
- [Tensorflow-Lite Micro](https://github.com/tensorflow/tflite-micro)
- [PicCamera](https://picamera.readthedocs.io/en/release-1.13/)

This uses the [tflite_micro_runtime](https://github.com/driedler/tflite_micro_runtime) Python package for image classification
which is similar to the [tflite_runtime]() package but is 8x faster since it's based on Tensorflow-Lite for Microcontrollers. 

This project also demonstrates how to use VSCode to single-step debug Python from your local PC while executing on a remote Raspberry PI Zero.


__NOTE:__ This assumes your using Windows for local debugging but a very similar setup should work for Linux/OSX.


# Hardware 

This assumes you have a Raspberry Pi Zero W (W = built-in wifi/bluetooth support).
There a tons of dev kits available, e.g.:
https://www.canakit.com/raspberry-pi-zero-wireless.html?src=raspberrypi

__NOTE:__ You need a micro SD card, the RPI board-only doesn't have onboard ROM to store the OS.

__NOTE:__ You might also need a micro SD reader if you computer doesn't have one. e.g.:  
https://www.amazon.com/s?k=usb+micro+sd+card+reader

It also assumes for have a Raspberry Pi Camera Module:
https://www.raspberrypi.org/products/camera-module-v2/



# Raspberry Pi Setup

## 1) Program Raspberry Pi OS to SD Card 

Plug the SD card in your computer's SD card reader, then  
use the Raspberry PI Imager to program RPI OS-Lite to your micro SD card:  
https://www.raspberrypi.org/software/

Select the __RPI OS-Lite__ image.

## 2) Configure RaspberryPI Boot Config

After programming RPI OS-Lite from setup 1, unplug the SD card, then plugin it back into your computer.
Go to your file explorer, you should see the SD card be mounted as a new drive (at least on Windows)
with a description as: `boot`.

Open the SD card 'boot' drive and create the following files in the root of the SD card:

__wpa_supplicant.conf:__ 
Create the the file `wpa_supplicant.conf` and copy and paste the following to the file.
Be sure to update `NAME OF YOUR WIFI` and  `WIFI PASSWORD` with your local Wi-Fi network's info.

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
    ssid="NAME OF YOUR WIFI"
    psk="WIFI PASSWORD"
    scan_ssid=1
}
```

__ssh__   
Create empty file named `ssh` in root of the SD card

__config.txt__
Open the file `config.txt` and uncomment the following entries to enable the PiCamera:
```
start_x=1             # essential
gpu_mem=128           # at least, or maybe more if you wish
disable_camera_led=1  # optional, if you don't want the led to glow
```


## 3) Install mDNS onto your computer

If you're using Windows, install:
https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US

If you're using Linux, install:
```
sudo apt-get install avahi-daemon
```

## 4) Start the Raspberry Pi Zero W

Unmount the SD card an plug it into the RPI.
Then plug the USB micro into the RPI's `USB` port (_not_ PWR) and the other side into your computer.


## 5) Open an SSH session to the RPI

On Windows, PuTTY is recommended: http://www.putty.org/

Wait until the green LED on the RPI0 is solid green before continuing.

Connect over SSH (port 22) with connection string: `pi@raspberrypi.local`   
Accept certificate  
Default password is `raspberry`


On Ubuntu, putty can be install with:

```bash
sudo apt-get install putty-tools
```

NOTE: The `plink` command is used by the scripts in this project.


## 6) Update Pi, install samba, config samba

From the RPI SSH session (step 5), issue the commands:

```
sudo apt-get update
sudo apt-get install -y samba samba-common-bin
```

Then issue:

```
sudo nano /etc/samba/smb.conf
```
Add to the end of file:
```
[root]
path=/
browsable=yes
writable=yes
only guest=no
create mask=0777
directory mask=0777
public=yes
```

Then issue:
```
sudo service smbd restart
```

In your local file explorer, you should be able to open (on Windows):
```
\\RASPBERRYPI\root
```

__NOTE:__ While useful for development, this opens a __major security hole__ into your RPI.  
Do NOT do the above if you're on an unsecure network!!


## 7) Resize your Pi partition to use all available space on SD card

From the RPI SSH session (step 5), issue the commands:
```
sudo raspi-config --expand-rootfs
sudo reboot
```

# Prepare VSCode Workspace


## 1) Map Network Drive

If using Windows, map the `\\RASPBERRYPI\root` network drive, more details [here](https://support.microsoft.com/en-us/windows/map-a-network-drive-in-windows-10-29ce55d1-34e3-a7e2-4801-131475f9557d)  
After this is complete, you should have a new drive, e.g. `Z:\` that points to your RPI's `/` directory.

This is required so we can easily sync the local workspace with the RPI's workspace.
It also allows the VSCode Python indexer to search the RPI Python packages.

After completing this step, you should be able to open the directory `Z:\` (or whatever drive letter you gave it) from your file explorer.

## 2) Run the setup script

Next, in a local terminal, run the setup script that comes with this repo:

```bash
python3 ./workspace_setup.py <network drive>
```

Where `<network drive>` is the mounted network drive from step 1.  
This will setup the local Python environment as well as RPI0 environment.
In will also configure the VSCode workspace file.

See the [setup_workspace.py](./setup_workspace.py) for more details.


## 3) Open VSCode Workspace

Assuming you cloned this repo, open the VSCode 'workspace' that is at the root of this repo: `workspace.code-workspace` 
then install the 'Recommended Extensions'.

# Run the debugger

That's it! Running the `Debug Python on RPI0` [debug configuration](https://code.visualstudio.com/docs/python/debugging) should:
1. Synchronize the local workspace with the RPI's workspace (assuming the network drive is properly mapped)
2. Start the `main.py` python script with remote debugging enabled
3. Cause VSCode to connect to the debug server and allow for single-stepping in the Python script as if it were running locally

Additionally, the VSCode Python indexer will search the RPI0 for Python packages. 
So, for instance, the indexer will resolve the `picamera` package which is on the RPI0 as if it were installed locally.

See the [main.py](./main.py) for more details on how the image classification works.
