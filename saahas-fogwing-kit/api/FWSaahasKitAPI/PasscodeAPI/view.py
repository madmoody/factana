"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from flask import request
from flask import Blueprint
from FWSaahasKitAPI.authentication import required_auth
from FWSaahasKitAPI.PasscodeAPI.control import user_validationC, admin_validationC, \
                                            update_terminal_passcodeC


# Blueprint creation.
sfw_passcodeB = Blueprint("sfw_passcode", __name__, url_prefix='/sfwUser')


# This route will validate the account user and returns the token.
@sfw_passcodeB.route("/user/passcode", methods=['POST'])
def user_validation():
     if request.method == "POST":
          passcode = request.get_json()
          if passcode:
               return user_validationC(passcode)
          else:
               return dict(Unsuccessful="Enter the passcode !")


# This route will validate the admin user and returns the token.
@sfw_passcodeB.route("/admin/passcode", methods=['GET', 'POST'])
@required_auth
def admin_validation():
     if request.method == "POST":
          passcode = request.get_json()
          if passcode:
               return admin_validationC(passcode)
          else:
               return dict(Unsuccessful="Enter the passcode !")


# This route will update the terminal passcode.
@sfw_passcodeB.route("/update/terminal/passcode", methods=['PUT'])
@required_auth
def update_terminal_passcode():
     if request.method == "PUT":
          update_data = request.get_json()
          if update_data:
               return update_terminal_passcodeC(update_data)
          else:
               return dict(Unsuccessful="Enter the passcode !")

