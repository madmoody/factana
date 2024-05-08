"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from FWSaahasKitAPI.ProcessAPI.model import get_processM, post_processM, delete_processM


# This function will return the list of process.
def get_processC():
     return get_processM()


# This function will add the new process.
def post_processC(add_process):
     if add_process.get("sfw_process_type"):
          return post_processM(add_process)
     else:
          return dict(Unsuccessful="Enter proper process name !")


# This function will delete the process.
def delete_processC(process):
     process_ids = eval(process)
     if process_ids:
          return delete_processM(process_ids)
     else:
          return dict(Unsuccessful="Select the process to delete !")