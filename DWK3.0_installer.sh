
#!/bin/bash
#ADD FROM gitt hub

# Consider this snippet from ./OCRV2.sh

chmod +x OCRV2.sh
chmod +x OCVR2_1.sh
chmod +x OCVR2_2.sh

./OCRV2.sh

echo "@reboot sleep 10 && ./OCVR2_1.sh" >> /etc/crontab
sudo reboot

./OCVR2_1.sh

echo "@reboot sleep 10 && ./OCVR2_2.sh" >> /etc/crontab
sudo reboot

./OCVR2_2.sh

echo "Installation completed"
