"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from FWSaahasKitAPI.config import Config
from flask_cors import CORS


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/saahas-fogwing-kit/FWSaahas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

def create_app(config_class=Config):
     app.config.from_object(Config)
     db.init_app(app)
     ma.init_app(app)

     from FWSaahasKitAPI.HomeAPI.view import sfw_homeB
     app.register_blueprint(sfw_homeB)
     from FWSaahasKitAPI.PasscodeAPI.view import sfw_passcodeB
     app.register_blueprint(sfw_passcodeB)
     from FWSaahasKitAPI.LocationAPI.view import sfw_locationsB
     app.register_blueprint(sfw_locationsB)
     from FWSaahasKitAPI.MaterialAPI.view import sfw_materialsB
     app.register_blueprint(sfw_materialsB)
     from FWSaahasKitAPI.ProcessAPI.view import sfw_processB
     app.register_blueprint(sfw_processB)
     from FWSaahasKitAPI.ShiftAPI.view import sfw_shiftB
     app.register_blueprint(sfw_shiftB)

     return app

