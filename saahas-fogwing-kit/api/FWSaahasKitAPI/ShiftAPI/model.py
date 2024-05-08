"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from FWSaahasKitAPI import db, ma
from datetime import datetime


class SFWShifts(db.Model):
     sfw_shift_id = db.Column(db.Integer, primary_key=True)
     sfw_shift_name = db.Column(db.String(256), nullable=False)
     sfw_shift_start = db.Column(db.String(256), nullable=False)
     sfw_shift_end = db.Column(db.String(256), nullable=False)
     sfw_is_active = db.Column(db.Boolean, default=True)
     sfw_created_by = db.Column(db.String(256))
     sfw_updated_by = db.Column(db.String(256), default=None)
     sfw_created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
     sfw_updated_at = db.Column(db.DateTime, default=None)


class SFWShiftsSchema(ma.SQLAlchemyAutoSchema):
     class Meta:
          model = SFWShifts 
     
shifts_schema = SFWShiftsSchema()


# This function will fetch all the shifts.
def get_shiftsM():
     try:
          shifts = SFWShifts.query.with_entities(SFWShifts.sfw_shift_id, SFWShifts.sfw_shift_name,
                                                 SFWShifts.sfw_shift_start, SFWShifts.sfw_shift_end,
                                                 SFWShifts.sfw_is_active).all()
          shifts_schema_data = shifts_schema.dump(shifts, many=True)
          return dict(shifts=shifts_schema_data)
     except Exception:
          return dict(Unsuccessful="Something went wrong !")


# This functions will update the shift.
def put_shiftM(shifts):
     try:
          if shifts:

               shift_not_active = {"sfw_shift_start": "00:00", "sfw_shift_end": "00:00"}

               for shift_data in shifts:
                    shift = SFWShifts.query.filter_by(sfw_shift_id=shift_data.get("sfw_shift_id"))
                    del shift_data["sfw_shift_id"]
                    if shift_data.get("sfw_is_active"):
                         shift.update(shift_data)
                         db.session.commit()
                    else:
                         shift_data.update(shift_not_active)
                         shift.update(shift_data)
                         db.session.commit()
               return dict(Successful="Successfully updated shifts.")
          else:
               return dict(Unsuccessful="Select the shift to update !")
     except Exception:
          return dict(Unsuccessful="Something went wrong !")