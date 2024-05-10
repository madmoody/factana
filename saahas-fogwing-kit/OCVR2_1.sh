#!/bin/bash

#install ubuntu frame for Kiosk
sudo snap install ubuntu-frame
#set the frame in auto running
sudo snap set ubuntu-frame daemon=true
sudo snap install wpe-webkit-mir-kiosk
sudo snap connect wpe-webkit-mir-kiosk:wayland
sudo snap set wpe-webkit-mir-kiosk daemon=true
sudo snap set wpe-webkit-mir-kiosk url=https://www.google.com

#step towards the Kisok mode configuration

sudo snap start wpe-webkit-mir-kiosk
sudo apt-get install i2c-tools -y
sudo i2cdetect -y 1
sleep 5

sudo cp /boot/firmware/config.txt /boot/firmware/config.txt_backup
echo "dtoverlay=i2c-rtc,ds3231" | sudo tee -a /boot/firmware/config.txt
echo "added ==  [ ok ]"
sudo reboot