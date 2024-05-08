"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from FWSaahasKitAPI import db, ma
from datetime import datetime


class SFWProcess(db.Model):
     sfw_process_id = db.Column(db.Integer, primary_key=True)
     sfw_process_type = db.Column(db.String(256), nullable=False)
     sfw_created_by = db.Column(db.String(256))
     sfw_updated_by = db.Column(db.String(256), default=None)
     sfw_created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
     sfw_updated_at = db.Column(db.DateTime, default=None)


class SFWProcessSchema(ma.SQLAlchemyAutoSchema):
     class Meta:
          model = SFWProcess 
     
process_schema = SFWProcessSchema()


# This function will fetch all the process.
def get_processM():
     try:
          process = SFWProcess.query.with_entities(SFWProcess.sfw_process_type,
                                                   SFWProcess.sfw_process_id).all()
          process_schema_data = process_schema.dump(process, many=True)
          return dict(materails=process_schema_data)
     except Exception:
          return dict(Unsuccessful="Something went wrong !")


# This function will add the new process.
def post_processM(add_data):
     try:
          add_process = SFWProcess(**add_data)
          db.session.add(add_process)
          db.session.commit()
          if add_process.sfw_process_id:
               return dict(Successful="Successfully added {}.".format(add_process.sfw_process_type))
          else:
               return dict(Unsuccessful="Please enter all the required fields !")
     except Exception:
          return dict(Unsuccessful="Something went wrong !")
     finally:
          db.session.close()


# This functions will delete the process data.
def delete_processM(process):
     try:
          if process:
               for process_id in process:
                    SFWProcess.query.filter(SFWProcess.sfw_process_id==process_id).delete()
                    db.session.commit()
               return dict(Successful="Successfully deleted process.")
          else:
               return dict(Unsuccessful="Select the process to delete !")
     except Exception:
          return dict(Unsuccessful="Something went wrong !")