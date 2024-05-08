"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


import time
from flask import request, Response, stream_with_context
from flask import Blueprint
from FWSaahasKitAPI.authentication import required_auth
from FWSaahasKitAPI.HomeAPI.control import create_dataC, get_shift_dataC, \
    get_ssidsC, pswd_validationC, system_reboot_C, system_shutdown_C
from firmware.rs232_serial import RS232Serial
from firmware.system_config import WiFiSettings


# Blueprint creation.
sfw_homeB = Blueprint("sfw_home", __name__, url_prefix='/sfwHome')


payload_data = {
                  "source": None,
                  "destination": None,
                  "process_type": None,
                  "material_type": None,
                  "weight": None
               }


def weight_sent_event():
    while True:
        time.sleep(1)
        yield "id: 1\ndata: {weight}\nevent: online\n\n".format(weight=payload_data.get("weight"))


def weight_stream():
    wscale = RS232Serial()
    while 1:
        weight = wscale.read_rs232_serial()
        yield "id: 1\ndata: {weight}\nevent: online\n\n".format(weight=weight)
        time.sleep(0.2)

# this function will read the button state only
def button_state_listen():
    b_state = WiFiSettings()
    while 1:
        tf_button = b_state.button()
        yield f"id: 1\ndata: {tf_button}\nevent: online\n\n"
        time.sleep(0.5)

# this route will stream the power button state
@sfw_homeB.route("/b_state_listen")
def listen():
    return Response(stream_with_context(button_state_listen()), mimetype="text/event-stream")

# This route will stream the live weight.
@sfw_homeB.route("/weightlisten")
def listen():
     return Response(stream_with_context(weight_stream()), mimetype="text/event-stream")


# This route will stream the live weight.
@sfw_homeB.route("/isWeightSent")
def is_weight_sent():
     return Response(stream_with_context(weight_sent_event()), mimetype="text/event-stream") 


# This route will update the in memory payload data.
@sfw_homeB.route("/updatePayload", methods=['PUT'])
@required_auth
def update_payload():

    """ In the Payload either source or destination will be present both cannot 
        exist at same time. """

    if request.method == "PUT":
        try:
            data = request.get_json()
            if "source" in data:
                data.update({"destination": None})	
                payload_data.update(data)
            elif "destination" in data:
                data.update({"source": None})
                payload_data.update(data)
            else:
                payload_data.update(data)
            return dict(Successful="Successfully updated the data.")
        except Exception:
            return dict(Unsuccessful="Something went wrong !")


# This route will store payload data in JSON file.
@sfw_homeB.route("/getPayloadData")
def create_data():
    return create_dataC(payload_data)


# This route will return current shift data.
@sfw_homeB.route("/getShiftData")
@required_auth
def get_shift_data():
    return get_shift_dataC()


# This route will return available SSID's.
@sfw_homeB.route("/getSSIDs")
@required_auth
def get_ssids():
    return get_ssidsC()


# This route will validate the password for the selected SSID.
@sfw_homeB.route("/pswdValidation", methods=['POST'])
@required_auth
def pswd_validation():
    if request.method == "POST":
        data = request.get_json()
        return pswd_validationC(data)


# This route will reset the weight to zero.
@sfw_homeB.route("/resetWeight")
def reset_weight():
    weight_stream()
    payload_data.update({"weight": 0})
    return dict(Successful="Reset weight.")


# this route will shut down
@sfw_homeB.route("/shutdown")
def system_shutdown():
    system_shutdown_C()
    return dict(Successful="System is Shutting down.")


# this route will reboot the device
@sfw_homeB.route("/reboot")
def system_reboot():
    system_reboot_C()
    return dict(Successful="System is Restarting.")