"""  * Copyright (C) 2023 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""

from os.path import expanduser
from datetime import datetime
import json
import os


class PayloadWriter:
    """
    Class to write payloads into a folder
    """
    def __init__(self):
        """
        Constructor method to initialize the required write path for the JSON payloads.
        """
        self.cred_path = expanduser('~' + '/saahas-fogwing-kit/credentials/sfwkit_cred.json')
        with open(self.cred_path, "r") as open_file:
            cred = json.load(open_file)
        self.write_path = cred.get('PAYLOADS_PATH')

    @staticmethod
    def utcnow():
        """
        Returns the current UTC time and the corresponding local time.
        :return: A tuple of 3 elements, the first element is the current UTC time in epoch format,
                the second is the local date and the third is the local time.
        :rtype: Tuple
        """

        try:
            local_time = datetime.now()
            epoch_time_utc = local_time.timestamp()
            return (
                str(epoch_time_utc).replace(".", "").ljust(16, '0'),
                local_time.strftime("%d %b %Y"),
                local_time.strftime("%I:%M:%S %p")
            )
        except Exception:
            return None

    def writer(self, payload):
        """
        Writes the payload to a file with a timestamp in the filename.
        :param payload: (Dict): The JSON payload to be written to the file.
        :return: True if the payload is written to the file successfully, False otherwise.
        :rtype: bool, str if there is exception
        """
        epoch_stamp, date, time_c = self.utcnow()
        try:
            payload_with_time = {"date": date, "time": time_c, **payload}
            file_name = f"wscale_{epoch_stamp}.json"
            file_path = os.path.join(self.write_path, file_name)
            with open(file_path, "w") as file:
                json.dump(payload_with_time, file, indent=2)
            if os.path.getsize(file_path) == 0:
                return False
            return True
        except (FileNotFoundError, Exception):
            return False
