# A list of properties a data source may have.

# All properties are unique strings using only characters [a-z0-9_],
# so that they can easily be used anywhere, from URLs to JSON to
# whatever.

# This datasource has layers made out of discrete points
LAYER_POINTS = "layer_points"

# The data in this datasource are integers between 0 and 255
DATA_UINT8 = "data_uint8"

# The data in this datasource are timeseries of doubles
DATA_TIMESERIES_DOUBLE = "data_timeseries_double"

# The datasource can return values for each point on the map (in case of
# timeseries, this would be the last value in the timeseries)
DATA_CAN_HAVE_VALUE_LAYER = "data_can_have_value_layer"

# If lizard-datasource were to run a script trying to received the last
# value of every possible timeseries and storing it in its own tables,
# then that would work to make a layer of the last values.
# If the datasource has DATA_CAN_HAVE_VALUE_LAYER, this won't be used.
DATA_CAN_HAVE_VALUE_LAYER_SCRIPT = "data_can_have_value_layer_script"

# Datasource can return values for all locations in it for arbitrary
# moments in time, not just the most recent.
# If the datasource has this, it is assumed it also has
# DATA_CAN_HAVE_VALUE_LAYER.
DATA_CAN_HAVE_VALUE_LAYER_ARBITRARY_MOMENT = (
    "data_can_have_value_layer_arbitrary_moment")

