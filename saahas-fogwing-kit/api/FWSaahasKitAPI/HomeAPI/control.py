"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from datetime import datetime, timedelta
from firmware.system_config import WiFiSettings
from FWSaahasKitAPI.ShiftAPI.model import get_shiftsM


# This method will genrate the JSON file.
def create_dataC(data):

    """ This function removes None value(source or destination) from the payload and creates
        JSON file that contains payload and shift data. """

    payload_data = data.copy()

    try:
        shift_data = get_shift_dataC()
        if shift_data:
            payload_data["shift_name"] = shift_data.get("shift_name")
            payload_data["shift_range"] = shift_data.get("shift_range")
            payload_data["shift_date"] = shift_data.get("shift_date")
        if payload_data.get("source"):
            del payload_data["destination"]
        elif payload_data.get("destination"):
            del payload_data["source"]
        return payload_data
    except Exception:
        return dict(Unsuccessful="Something went wrong !")


# This method will return the current shift data.
def get_shift_dataC():

    """ This function will check current shift details from all available shifts and
        return the valid shift range and the shift name. """

    try:
        shift_data = {}
        shifts = get_shiftsM().get("shifts")
        for shift in shifts:
            if shift.get("sfw_is_active"):
                shift_start = datetime.strptime(shift.get("sfw_shift_start"), "%H:%M").time()
                shift_end = datetime.strptime(shift.get("sfw_shift_end"), "%H:%M").time()
                current_date = datetime.now()
                current_time = current_date.time()
                previous_date = current_date - timedelta(days=1)
                time_diff = datetime.combine(datetime.today(), shift_end) - datetime.combine(datetime.today(), shift_start)
                
                # Checking time overlap between the shifts and updating the data accordingly.
                if time_diff.days < 0:
                    if (shift_start < current_time > shift_end) or (shift_start > current_time < shift_end):
                        shift_data["shift_range"] = "{} - {}".format(shift.get("sfw_shift_start"), shift.get("sfw_shift_end"))
                        shift_data["shift_name"] = shift.get("sfw_shift_name")
                        if current_time < shift_end:
                            shift_data["shift_date"] = previous_date.strftime("%d %b %Y")
                        else:
                            shift_data["shift_date"] = current_date.strftime("%d %b %Y")
                else:
                    if shift_start < current_time < shift_end:
                        shift_data["shift_range"] = "{} - {}".format(shift.get("sfw_shift_start"), shift.get("sfw_shift_end"))
                        shift_data["shift_name"] = shift.get("sfw_shift_name")
                        shift_data["shift_date"] = current_date.strftime("%d %b %Y")
        if shift_data:
            return shift_data
        else:
            return dict(Unsuccessful="No shift available !")
    except Exception:
        return dict(Unsuccessful="Something went wrong !")


# This function will fetch list of SSID's
def get_ssidsC():
    try:
        wifi_settings = WiFiSettings()
        ssids = wifi_settings.scan_wifi_nw()
        if ssids[0] == "":
            return dict(Unsuccessful="No networks available !")
        elif ssids:
            return dict(ssids=ssids)
        else:
            return dict(ssids=[])
    except Exception as e:
        print(e)
        return dict(Unsuccessful="Backend didn't respond !")


# This function will validate the SSID password.
def pswd_validationC(data):
    try:
        if len(data.get("password")) < 8:
            return dict(Unsuccessful="Password must be between 8 and 63 characters !")
        wifi_settings = WiFiSettings()
        status = wifi_settings.wifi_config(data.get("ssid"), data.get("password"))
        if status:
            return dict(Successful="Successfully connected to {}.".format(data.get("ssid")))
        else:
            return dict(Unsuccessful="Failed to connect !")
    except Exception:
        return dict(Unsuccessful="Backend didn't respond !")


# this route will shutdown the device
def system_shutdown_C():
    action = WiFiSettings()
    action.sys_shutdown()
    
    
# this route will reboot the device
def system_reboot_C():
    action = WiFiSettings()
    action.sys_reboot()
