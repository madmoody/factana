"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from FWSaahasKitAPI import db, ma, app
import jwt


class SFWUsers(db.Model):
     sfw_user_id = db.Column(db.Integer, primary_key=True)
     sfw_user_role = db.Column(db.String, nullable=False)
     sfw_user_passcode = db.Column(db.String, nullable=False)


class SFWUsersSchema(ma.SQLAlchemyAutoSchema):
     class Meta:
          model = SFWUsers 
     
user_schema = SFWUsersSchema()


# This function will authenticate the account level user.
def user_validationM(passcode):
    try:
        user = SFWUsers.query.filter_by(sfw_user_role='worker')
        user_schema_data = user_schema.dump(user, many=True)
        if user_schema_data:
            if passcode["passcode"] == user_schema_data[0]["sfw_user_passcode"]:
                payload = {"Successful": "User authentication was successfull!"}
                token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
                return {"token": token}
            else:
                return dict(Unsuccessful="Please enter the proper passcode !")
        else:
            return dict(Unsuccessful="User not found !")
    except Exception as e:
        print(e)
        return dict(Unsuccessful="Something went wrong !")


# This function will authenticate the admin level user
def admin_validationM(passcode):
     try:
          user = SFWUsers.query.filter_by(sfw_user_role='admin')
          user_schema_data = user_schema.dump(user, many=True)
          if user_schema_data:
               if passcode["passcode"] == user_schema_data[0]["sfw_user_passcode"]:
                    payload = {"Successful": "Admin authentication was successfull!"}
                    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
                    return {"token": token}
               else:
                    return dict(Unsuccessful="Please enter the proper passcode !")
          else:
               return dict(Unsuccessful="User not found !")
     except Exception:
          return dict(Unsuccessful="Something went wrong !")


# This function will update the terminal passcode.
def update_terminal_passcodeM(update_data):
     try:
          user = SFWUsers.query.filter_by(sfw_user_role='worker')
          user_schema_data = user_schema.dump(user, many=True)
          if update_data["old_passcode"] == user_schema_data[0]["sfw_user_passcode"]:
               user.update({"sfw_user_passcode": update_data["new_passcode"]})
               db.session.commit()
               return dict(Successful="Successfully updated terminal passcode.")
          else:
               return dict(Unsuccessful="Please enter valid old passcode !")
     except Exception:
          return dict(Unsuccessful="Something went wrong !")