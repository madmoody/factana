"""  * Copyright (C) 2023 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""

import re
import time
import subprocess
from collections import OrderedDict
import yaml
import RPi.GPIO as GPIO

from .status_led import LED


class WiFiSettings:
    """
    Class for system related configurations
    """
    def __init__(self):
        """
        Constructor to initialize GPIO and path for network configuration
        """
        self.config_path = "/etc/netplan/50-cloud-init.yaml"
        self.PWR_BUTTON = 19
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PWR_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @staticmethod
    def scan_wifi_nw():
        """
        This function is to scan Wi-Fi networks available
        :return: List of the Wi-Fi networks avilable
        """
        try:
            ssid = ""
            cmd_output = subprocess.check_output("sudo iwlist wlan0 scan | grep ESSID", shell=True)
            cmd_res = cmd_output.decode("utf-8")
            time.sleep(0.5)

            while len(cmd_res) != 0:
                match = re.search('ESSID:\"(.+?)\"\n', cmd_res)

                ssid += match.group(1) + ','
                cmd_res = '\n'.join(cmd_res.split('\n')[1:])

            return list(OrderedDict.fromkeys(ssid[:len(ssid) - 1].split(',')))
        except Exception:
            pass

    def wifi_config(self, ssid, pwd):
        """
        This function writes the SSID and password of the Wi-Fi network
        :param ssid: SSID of Wi-Fi
        :param pwd: Password of Wi-Fi
        :return: True if Wi-Fi is connected else false
        """
        config = {
            "network": {
                "version": 2,
                "ethernets": {
                    "eth0": {
                        "dhcp4": True,
                        "optional": True
                    }
                },
                "wifis": {
                    "wlan0": {
                        "dhcp4": True,
                        "optional": True,
                        "access-points": {
                            str(ssid): {
                                "password": str(pwd)
                            }
                        }
                    }
                }
            }
        }
        try:
            with open(self.config_path, "w") as file:
                file.write(yaml.dump(config))

            subprocess.Popen(["sudo", "netplan", "apply"])
            time.sleep(3)
            led_status = LED()
            trials = 0
            conn_status = False
            while trials < 20:
                conn_status = led_status.internet_status()
                if conn_status:
                    conn_status = True
                    break
                else:
                    conn_status = False
                trials += 1
                time.sleep(1)
            return conn_status
        except Exception:
            pass

    def button(self):
        """
        This function is to detect if power button is pressed
        :return: True if button is pressed for more than 2 seconds else false
        """
        try:
            start_time = time.time()
            while GPIO.input(self.PWR_BUTTON) == GPIO.LOW:
                if time.time() - start_time >= 2:
                    return True
            return False
        except Exception:
            pass

    @staticmethod
    def sys_shutdown():
        """
        This function is to shut down the device
        :return: None
        """
        try:
            subprocess.Popen(["sudo", "poweroff"])
        except Exception:
            pass

    @staticmethod
    def sys_reboot():
        """
        This function is to restart the device
        :return: None
        """
        try:
            subprocess.Popen(["sudo", "reboot"])
        except Exception:
            pass
