"""  * Copyright (C) 2023 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""

from time import sleep
import requests
import RPi.GPIO as GPIO

# Importing custom modules
from payload_writer import PayloadWriter
from rs232_serial import RS232Serial

# Define the buzzer and push button pins
BUZZER_PIN = 23
PUSH_BUTTON_PIN = 24

# Initializing the GPIOs for the buzzer and push button
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PUSH_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def is_button_pressed():
    """
    This fuction is to check the state of a button.
    :returns: True if button is pressed, False otherwise.
    :rtype: bool 
    """
    try:
        return not GPIO.input(PUSH_BUTTON_PIN)
    except Exception:
        return False


def buzzer():
    """
    This function is used to turn on the buzzer for 1 second.
    :returns: None
    """
    try:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        sleep(1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    except Exception:
        pass


if __name__ == "__main__":
    # The script runs an infinite loop to constantly check if the button is pressed.
    payload = PayloadWriter()
    check_dtype = RS232Serial()
    temp_list = ["null", None]
    while True:
        try:
            if is_button_pressed():
                wscale_data = requests.get(url="http://127.0.0.1:7077/sfwHome/getPayloadData").json()
                endpoint_url = "http://127.0.0.1:7077/sfwHome/resetWeight"
                # Converting weight to either an integer or a float
                weight = check_dtype.process_weight_data(wscale_data.get("weight"))

                process_type = wscale_data.get("process_type")
                material_type = wscale_data.get("material_type")
                wscale_data.update({"weight": weight})

                # Check if the weight, process_type, and material_type are valid
                if weight and process_type not in temp_list and material_type not in temp_list:
                    if process_type == "Inward / Incoming":
                        if wscale_data.get("source") not in temp_list:
                            payload.writer(wscale_data)
                            buzzer()
                            requests.get(url=endpoint_url)
                    elif process_type == "Outward / Outgoing":
                        if wscale_data.get("destination") not in temp_list:
                            payload.writer(wscale_data)
                            buzzer()
                            requests.get(url=endpoint_url)
                    else:
                        payload.writer(wscale_data)
                        buzzer()
                        requests.get(url=endpoint_url)
                sleep(0.5)
            sleep(0.1)
        except Exception:
            pass
