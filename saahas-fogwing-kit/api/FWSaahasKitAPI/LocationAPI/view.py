"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from flask import request
from flask import Blueprint
from FWSaahasKitAPI.authentication import required_auth
from FWSaahasKitAPI.LocationAPI.control import get_locationsC, post_locationC, delete_locationsC


# Blueprint creation.
sfw_locationsB = Blueprint("sfw_locations", __name__, url_prefix='/sfwLocations')


# This route will return all the locations data
@sfw_locationsB.route("/byLocationType/<location_type>", methods=['GET'])
@required_auth
def get_locations(location_type):
     return get_locationsC(location_type)


# This route will add the new location.
@sfw_locationsB.route("/addLocation", methods=['POST'])
@required_auth
def post_location():
     if request.method == "POST":
          add_data = request.get_json()
          if add_data:
               return post_locationC(add_data)
          else:
               return dict(Unsuccessful="Enter proper location data !")


# This route will delete locations data.
@sfw_locationsB.route("/deleteLocations", methods=['DELETE'])
@required_auth
def delete_locations():
     location_ids = request.args.get('sfw_location_id')
     return delete_locationsC(location_ids)     

