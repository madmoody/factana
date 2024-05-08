"""  * Copyright (C) 2023 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""

import json
from os.path import expanduser
import requests

class APIPub:
    """
    This class is used to send payload data to a Fogwing API.
    """
    def __init__(self):
        """
        Initializes the class instance by setting class-level attributes:
        - cred_path: absolute path to the credentials file
        - api_url: API URL to post payload using API Key
        - account_id: Fogwing account ID
        - api_key: API key for the Fogwing API
        - edge_eui: Edge EUI for the device connected to the Fogwing API
        """
        self.cred_path = expanduser('~' + '/saahas-fogwing-kit/credentials/sfwkit_cred.json')
        with open(self.cred_path, "r") as open_file:
            cred = json.loads(open_file.read()).get('API_CRED')
        self.api_url = cred.get("API_ENDPOINT")
        self.account_id = cred.get("ACCOUNT_ID")
        self.api_key = cred.get("API_KEY")
        self.edge_eui = cred.get("EDGE_EUI")

    def sendtofwg(self, payload):
        """
        Sends payload data to Fogwing API.
        :param payload: Payload data to be sent to Fogwing.
        :return: HTTP status code of the API response.
        :rtype: int
        """
        try:
            header = {"accountID": self.account_id, "apiKey": self.api_key, "edgeEUI": self.edge_eui}
            payload_resp = requests.post(self.api_url, data=payload, headers=header, timeout=3)
            return payload_resp.status_code
        except Exception:
            return None
