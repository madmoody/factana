""" * Copyright (C) 2021 Factana Computing Pvt Ltd.
    * All Rights Reserved.
    * This file is subject to the terms and conditions defined in
    * file 'LICENSE.txt', which is part of this source code package. """


from os.path import expanduser
import json


home = expanduser('~' + '/saahas-fogwing-kit/credentials/sfwkit_cred.json')
with open(home, 'r') as cred:
    api_cred = json.load(cred)


SECRET_KEY = api_cred.get('SECRET_KEY')
APP_SECRET_KEY = api_cred.get('APP_SECRET_KEY')
