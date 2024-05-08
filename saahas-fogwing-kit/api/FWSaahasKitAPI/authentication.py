"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


import jwt
from functools import wraps
from flask import request
from FWSaahasKitAPI import app


# This method will validate the Authentication.
def required_auth(req_data):
    @wraps(req_data)
    def decorated(*args, **kwargs):
        token = None
        if 'APIKEY' in request.headers:
            token = request.headers['APIKEY']
        if not token:
            return {'message': 'Required Authentication !'}
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return {'message': 'Invalid Authentication !'}
        except jwt.ExpiredSignatureError:
            return {'authentication expired': 'Please login again !'}
        return req_data(*args, **kwargs)
    return decorated