"""  * Copyright (C) 2023 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""

import socket
from time import sleep
from os.path import expanduser
import json
import RPi.GPIO as GPIO


class LED:
    """
    Class for controlling the LED status of the device
    """
    def __init__(self):
        """
        Constructor to initialize the class variables and set the GPIO pins
        """
        self.ONLINE_LED = 20
        self.DATA_LED = 18

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.ONLINE_LED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.DATA_LED, GPIO.OUT, initial=GPIO.LOW)

        # Load the credentials file
        cred_path = expanduser('~' + '/saahas-fogwing-kit/credentials/sfwkit_cred.json')
        with open(cred_path, "r") as open_file:
            cred = json.loads(open_file.read()).get('MQTT_CRED')
        self.host = cred.get("SERVER_HOST")
        self.port = cred.get("PORT")

    def internet_status(self):
        """
        This function is to check the Internet connection status.
        :return: True if internet connection is available, False otherwise.
        :rtype: bool
        """
        try:
            socket.create_connection((self.host, self.port), timeout=2)
            return True
        except (socket.timeout, socket.error, Exception):
            return False

    def online_led(self):
        """
        This function to is control the state of the online LED based on the 
        internet connection status.
        :return: None
        """
        try:
            if self.internet_status():
                GPIO.output(self.ONLINE_LED, GPIO.HIGH)
            else:
                GPIO.output(self.ONLINE_LED, GPIO.LOW)
        except Exception:
            pass

    def data_led(self):
        """
        This function is to blink the data LED three times
        :return: None
        """
        count = 0
        while count < 3:
            try:
                GPIO.output(self.DATA_LED, GPIO.HIGH)
                sleep(0.2)
                GPIO.output(self.DATA_LED, GPIO.LOW)
                sleep(0.2)
                count += 1
            except Exception:
                pass


if __name__ == '__main__':
    # Main code block to run the LED status check in an infinite loop
    status = LED()
    while True:
        status.online_led()
        sleep(1)
