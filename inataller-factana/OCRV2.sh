#!/bin/bash

#- **Static hostname:** saahas-ocr
#- **Icon name:** computer
#- **Machine ID:** e06080246717469c9853d27f965c6f3e
#- **Boot ID:** 87f2bd88886a40d1a1d5c46938dd45c1
#- **Operating System:** Ubuntu 20.04.5 LTS
#- **Kernel:** Linux 5.4.0-1080-raspi
#- **Architecture:** arm64

 sudo apt-get update && sudo apt-get upgrade -y 
 echo "updated and upgraded == [ ok ]"
 sleep 10

#disable the password prompts for user

sudo cp /etc/sudoers /etc/sudoers_backup
echo "saahas ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers
sudo visudo -c   

#Install Linux Wireless Extensions for Wi-Fi scanning using the following command

sudo apt install wireless-tools -y
echo "wireless-tools installed [ ok ]"

sleep 5

sudo chmod 777 /etc/netplan/50-cloud-init.yaml
#Install the mesa-utils package ubuntu package
sudo apt install mesa-utils -y

sudo cp /boot/firmware/config.txt /boot/firmware/config.txt_backup

echo "dtoverlay=vc4-kms-v3d-pi4" | sudo tee -a /boot/firmware/config.txt

echo "added ==  [ ok ]"






