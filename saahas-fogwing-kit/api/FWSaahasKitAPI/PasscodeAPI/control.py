"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from FWSaahasKitAPI.PasscodeAPI.model import user_validationM, admin_validationM, \
                                          update_terminal_passcodeM


# This function will authenticate the account level user.
def user_validationC(passcode):
     return user_validationM(passcode)


# This function will authenticate the admin level user
def admin_validationC(passcode):
     return admin_validationM(passcode)


# This function will update the terminal passcode.
def update_terminal_passcodeC(update_data):
     if len(update_data["new_passcode"]) < 3:
          return dict(Unsuccessful="Passcode should contain minimum four characters !")
     return update_terminal_passcodeM(update_data)