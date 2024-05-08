"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from FWSaahasKitAPI import db, ma
from datetime import datetime


class SFWMaterials(db.Model):
     sfw_material_id = db.Column(db.Integer, primary_key=True)
     sfw_material_type = db.Column(db.String(256), nullable=False)
     sfw_created_by = db.Column(db.String(256))
     sfw_updated_by = db.Column(db.String(256), default=None)
     sfw_created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
     sfw_updated_at = db.Column(db.DateTime, default=None)


class SFWMaterialsSchema(ma.SQLAlchemyAutoSchema):
     class Meta:
          model = SFWMaterials 
     
material_schema = SFWMaterialsSchema()


# This function will fetch all the materials.
def get_materialsM():
     try:
          materails = SFWMaterials.query.with_entities(SFWMaterials.sfw_material_type,
                                                       SFWMaterials.sfw_material_id).all()
          materails_schema_data = material_schema.dump(materails, many=True)
          return dict(materails=materails_schema_data)
     except Exception:
          return dict(Unsuccessful="Something went wrong !")


# This function will add the new material.
def post_materialM(add_data):
     try:
          add_material = SFWMaterials(**add_data)
          db.session.add(add_material)
          db.session.commit()
          if add_material.sfw_material_id:
               return dict(Successful="Successfully added {} !".format(add_material.sfw_material_type))
          else:
               return dict(Unsuccessful="Please enter all the required fields !")
     except Exception:
          return dict(Unsuccessful="Something went wrong !")
     finally:
          db.session.close()


# This functions will delete the particular material.
def delete_materialsM(materials):
     try:
          if materials:
               for material_id in materials:
                    SFWMaterials.query.filter(SFWMaterials.sfw_material_id==material_id).delete()
                    db.session.commit()
               return dict(Successful="Successfully deleted materials.")
          else:
               return dict(Unsuccessful="Select the material to delete !")
     except Exception:
          return dict(Unsuccessful="Something went wrong !")