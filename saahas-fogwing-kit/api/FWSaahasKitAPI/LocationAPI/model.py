"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from FWSaahasKitAPI import db, ma
from datetime import datetime


class SFWLocations(db.Model):
     sfw_location_id = db.Column(db.Integer, primary_key=True)
     sfw_location_name = db.Column(db.String(256), nullable=False)
     sfw_location_type = db.Column(db.String(256), nullable=False)
     sfw_created_by = db.Column(db.String(256))
     sfw_updated_by = db.Column(db.String(256), default=None)
     sfw_created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
     sfw_updated_at = db.Column(db.DateTime, default=None)


class SFWLocationsSchema(ma.SQLAlchemyAutoSchema):
     class Meta:
          model = SFWLocations 
     
location_schema = SFWLocationsSchema()


# This function will fetch all the locations based on the location_type
def get_locationsM(location_type):
     try:
          locations = SFWLocations.query.with_entities(SFWLocations.sfw_location_name,
                                                       SFWLocations.sfw_location_id, 
                                                       SFWLocations.sfw_location_type) \
                                  .filter_by(sfw_location_type=location_type).all()
          location_schema_data = location_schema.dump(locations, many=True)
          return dict(locations=location_schema_data)
     except Exception:
          return dict(Unsuccessful="Something went wrong !")


# This function will add the new location
def post_locationM(add_data):
     try:
          add_location = SFWLocations(**add_data)
          db.session.add(add_location)
          db.session.commit()
          if add_location.sfw_location_id:
               return dict(Successful="Successfully added {} !".format(add_location.sfw_location_name))
          else:
               return dict(Unsuccessful="Please enter all the required fields !")
     except Exception:
          return dict(Unsuccessful="Something went wrong !")
     finally:
          db.session.close()


# This functions will delete the particular location by sfw_location_id
def delete_locationsM(locations):
     try:
          if locations:
               for location_id in locations:
                    SFWLocations.query.filter(SFWLocations.sfw_location_id==location_id).delete()
                    db.session.commit()
               return dict(Successful="Successfully deleted locations.")
          else:
               return dict(Unsuccessful="Select the location to delete !")
     except Exception:
          return dict(Unsuccessful="Something went wrong !")