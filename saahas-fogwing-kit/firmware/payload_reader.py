"""  * Copyright (C) 2023 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""

from os.path import expanduser
import os
import json
import time

# Importing custom modules
from pub_iothub_api import APIPub
from status_led import LED


class PayloadReader:
    """
    Class to read payloads and send it to fogwing API.
    """
    def __init__(self):
        """
        Constructor method to initialize the required path to read the payloads.
        """
        self.cred_path = expanduser('~' + '/saahas-fogwing-kit/credentials/sfwkit_cred.json')
        with open(self.cred_path, "r") as open_file:
            self.read_path = json.load(open_file).get('PAYLOADS_PATH')

    def reader(self):
        """
        Method to read the payloads and send it to fogwing API.
        :return: None
        """
        try:
            payloads = sorted(os.listdir(self.read_path))
            for file in payloads:
                try:
                    if led.internet_status():
                        payload_file_path = os.path.join(self.read_path, file)
                        with open(payload_file_path, 'r') as payload_file:
                            payload = payload_file.read()
                        status_code = api_pub.sendtofwg(payload)
                        if status_code == 201:
                            led.data_led()
                            os.remove(payload_file_path)
                        else:
                            break
                    else:
                        break
                except Exception:
                    pass
        except Exception:
            pass


if __name__ == '__main__':
    led = LED()
    api_pub = APIPub()
    pub = PayloadReader()
    try:
        while 1:
            pub.reader()
            time.sleep(0.1)
    except Exception as e:
        pass
