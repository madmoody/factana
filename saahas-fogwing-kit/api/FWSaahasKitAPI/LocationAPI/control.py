"""  * Copyright (C) 2019 Factana Computing Pvt Ltd.
     * All Rights Reserved.
     * This file is subject to the terms and conditions defined in
     * file 'LICENSE.txt', which is part of this source code package."""


from FWSaahasKitAPI.LocationAPI.model import get_locationsM, post_locationM, delete_locationsM


# This function will return the list of locations based on the location type.
def get_locationsC(location_type):
     return get_locationsM(location_type)


# This function will add the new location.
def post_locationC(add_location):
     if add_location.get("sfw_location_name"):
          return post_locationM(add_location)
     else:
          return dict(Unsuccessful="Enter proper location name !")
          

# This function will delete the location data.
def delete_locationsC(locations):
     location_ids = eval(locations)
     if location_ids:
          return delete_locationsM(location_ids)
     else:
          return dict(Unsuccessful="Select the location to delete !")