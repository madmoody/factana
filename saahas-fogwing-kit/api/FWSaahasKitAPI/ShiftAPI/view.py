"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from flask import request
from flask import Blueprint
from FWSaahasKitAPI.authentication import required_auth
from FWSaahasKitAPI.ShiftAPI.control import get_shiftsC, put_shiftC


# Blueprint creation.
sfw_shiftB = Blueprint("sfw_shift", __name__, url_prefix='/sfwShift')


# This route will return all the shift data.
@sfw_shiftB.route("/getshifts", methods=['GET'])
@required_auth
def get_shifts():
     return get_shiftsC()


# This route will update the shifts data.
@sfw_shiftB.route("/updateShift", methods=['PUT'])
@required_auth
def put_shifts():
     if request.method == "PUT":
          update_data = request.get_json()
          if update_data:
               return put_shiftC(update_data)
          else:
               return dict(Unsuccessful="Enter proper shift data !")