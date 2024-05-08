"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from flask import request
from flask import Blueprint
from FWSaahasKitAPI.authentication import required_auth
from FWSaahasKitAPI.MaterialAPI.control import get_materialsC, post_materialC, delete_materialsC


# Blueprint creation.
sfw_materialsB = Blueprint("sfw_materials", __name__, url_prefix='/sfwMaterials')


# This route will return all the materials data
@sfw_materialsB.route("/getMaterials", methods=['GET'])
@required_auth
def get_materials():
     return get_materialsC()


# This route will add the new material.
@sfw_materialsB.route("/addMaterials", methods=['POST'])
@required_auth
def post_materials():
     if request.method == "POST":
          add_data = request.get_json()
          if add_data:
               return post_materialC(add_data)
          else:
               return dict(Unsuccessful="Enter proper material data !")


# This route will delete materials data.
@sfw_materialsB.route("/deleteMaterials", methods=['DELETE'])
@required_auth
def delete_materials():
     material_ids = request.args.get("sfw_material_id")
     return delete_materialsC(material_ids)