"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from FWSaahasKitAPI.ShiftAPI.model import get_shiftsM, put_shiftM


# This function will return the list of shifts.
def get_shiftsC():
     return get_shiftsM()


# This function will update the shifts.
def put_shiftC(update_data):
     shift_data = update_data.get("shift_data")
     if shift_data:
          return put_shiftM(shift_data)
     else:
          return dict(Unsuccessful="Enter proper shift data !")
