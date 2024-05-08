""" * Copyright (C) 2021 Factana Computing Pvt Ltd.
    * All Rights Reserved.
    * This file is subject to the terms and conditions defined in
    * file 'LICENSE.txt', which is part of this source code package. """



import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


# This file is responsible for running the whole application.
from FWSaahasKitAPI import create_app

app = create_app()
app.config['APP_SECRET_KEY'] = app.config["APP_SECRET_KEY"]


if __name__ == "__main__":
    app.run(host="172.16.255.227", port=7077, threaded=True)
