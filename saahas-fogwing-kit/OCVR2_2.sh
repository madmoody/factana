#!/bin/bash

sudo i2cdetect -y 1
sleep 5

# Backup the original file before making changes
sudo cp /lib/udev/hwclock-set /lib/udev/hwclock-set_backup
# Comment out the specified lines in the hwclock-set file
sudo sed -i -e '/^if \[ -e \/run\/systemd\/system \] ; then/s/^/#/' /lib/udev/hwclock-set 
sudo sed -i '0,/[[:space:]]*exit[[:space:]]*0/s//#&/' /lib/udev/hwclock-set  
sudo sed -i '/^##    \/sbin\/hwclock --rtc=\$dev --systz --badyear/s/^/#/' /lib/udev/hwclock-set
sudo sed -i '/^    \/sbin\/hwclock --rtc=\$dev --systz/s/^/#/' /lib/udev/hwclock-set       
echo "Successfully commented out the lines in hwclock-set"
sleep 5
sudo hwclock -V -r
date
sudo hwclock -w
sudo hwclock -r

#upgrade rpi library
sudo apt-get -y install python3-rpi.gpio rpi.gpio-common python3-pigpio python3-gpiozero
sudo groupadd gpio
sudo usermod -a -G gpio saahas
sudo grep gpio /etc/group
sudo chown root.gpio /dev/gpiomem
sudo chmod g+rw /dev/gpiomem
sudo apt-get install python3-pip
sudo apt install virtualenv
sleep 5
wget https://github.com/madmoody/factana/tree/main/saahas-fogwing-kit
virtualenv szwenv
source szwenv/bin/activate
pip3 install -r requirements.txt
sudo apt update
sudo apt install nginx -y
sudo nginx -v

# Create a systemd service file
sudo touch /etc/systemd/system/api-run.service

# Create a backup of the original service file
sudo cp /etc/systemd/system/api-run.service /etc/systemd/system/api-run.service_backup

# Define the content to be inserted
content="[Unit]\n\
Description=Gunicorn instance to serve Saahas ZWP device API (v1.0)\n\
After=network.target hostapd.service dhcpcd.service\n\
\n\
[Service]\n\
User={username}\n\
Group=www-data\n\
WorkingDirectory=/home/saahas/saahas-fogwing-kit/api\n\
Environment=\"PATH=/home/saahas/saahas-fogwing-kit/szwenv/bin:/usr/bin\"\n\
ExecStart=/home/saahas/saahas-fogwing-kit/bin/python run.py\n\
Restart=on-failure\n\
\n\
[Install]\n\
WantedBy=multi-user.target"

# Insert the content into the service file
echo -e "$content" | sudo tee /etc/systemd/system/api-run.service > /dev/null

#add server
sudo rm /etc/nginx/sites-available/default
sudo rm /etc/nginx/sites-enabled/default

sudo nano /etc/nginx/sites-available/angular-app

sudo cp /etc/nginx/sites-available/angular-app /etc/nginx/sites-available/angular-app_backup
sudo sed -i "s|server {
    listen 80;
    server_name _;
    root /home/saahas/saahas-fogwing-kit/angular-app;
    index index.html index.htm;
    location / {
        try_files $uri $uri/ /index.html;
    }|g" /etc/nginx/sites-available/angular-app

sudo ln -s /etc/nginx/sites-available/angular-app /etc/nginx/sites-enabled/angular-app
sudo systemctl restart nginx
sudo systemctl status nginx
sleep 5
#ubuntu frame
sudo snap set wpe-webkit-mir-kiosk url='https://127.0.0.1'
sudo snap restart wpe-webkit-mir-kiosk

cd /etc/systemd/system || exit
sudo systemctl enable api-run.service
sudo systemctl start api-run.service
sudo systemctl status api-run.service
sleep 5

cd ..

sudo reboot
