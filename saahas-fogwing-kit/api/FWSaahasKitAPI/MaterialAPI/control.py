"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from FWSaahasKitAPI.MaterialAPI.model import get_materialsM, post_materialM, delete_materialsM


# This function will return the list of materials.
def get_materialsC():
     return get_materialsM()


# This function will add the new material.
def post_materialC(add_material):
     if add_material.get("sfw_material_type"):
          return post_materialM(add_material)
     else:
          return dict(Unsuccessful="Enter proper material name !")


def delete_materialsC(materials):
     material_ids = eval(materials)
     if material_ids:
          return delete_materialsM(material_ids)
     else:
          return dict(Unsuccessful="Select the material to delete !")