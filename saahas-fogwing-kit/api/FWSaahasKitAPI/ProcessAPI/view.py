"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from flask import request
from flask import Blueprint
from FWSaahasKitAPI.authentication import required_auth
from FWSaahasKitAPI.ProcessAPI.control import get_processC, post_processC, delete_processC


# Blueprint creation.
sfw_processB = Blueprint("sfw_process", __name__, url_prefix='/sfwProcess')


# This route will return all the process data
@sfw_processB.route("/getProcess", methods=['GET'])
@required_auth
def get_process():
     return get_processC()


# This route will add the new process.
@sfw_processB.route("/addProcess", methods=['POST'])
@required_auth
def post_process():
     if request.method == "POST":
          add_data = request.get_json()
          if add_data:
               return post_processC(add_data)
          else:
               return dict(Unsuccessful="Enter proper process data !")


# This route will delete process data.
@sfw_processB.route("/deleteProcess", methods=['DELETE'])
@required_auth
def delete_process():
     process_ids = request.args.get("sfw_process_id")
     return delete_processC(process_ids)