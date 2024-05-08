"""  * Copyright (C) 2023 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""

import serial
from time import sleep


class RS232Serial:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):
        """
        Constructor method to initialize the serial communication and configure the properties
        """
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

    def read_rs232_serial(self):
        """
        This function is to read weight from weighing scale
        :returns: Number if greater than 0, -1 otherwise.
        :rtype: int, float, or -1 if an error occurs.
        """
        try:
            self.ser.reset_input_buffer()
            data = self.ser.readline().decode('unicode_escape').strip()
            if not data:
                return -1
            return self.process_weight_data(data)
        except Exception:
            return -1

    @staticmethod
    def process_weight_data(data):
        """
        This function is to process and convert the serial data to the appropriate type
        :param data: weight data
        :returns: Parsed data
        :rtype: int, float
        """
        try:
            result = eval(data)
            return -1 if result < 0 else result
        except Exception:
            return -1 if data < 0 else data