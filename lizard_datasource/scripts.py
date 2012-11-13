from lizard_datasource import properties
from lizard_datasource import datasource


def _yield_layers(ds):
    # This implements a breadth-first search that tries to visit all
    # drawable layers and yields their choices made objects. The case
    # where ChoicesMade is empty functions as the root of the tree.
    choices_mades = [datasource.ChoicesMade()]

    while choices_mades:
        choices_made = choices_mades.pop(0)
        ds.set_choices_made(choices_made)

        if ds.is_drawable(choices_made):
            yield choices_made
        else:
            criteria = ds.chooseable_criteria()
            if criteria:
                criterion = criteria[0]
                options = ds.options_for_criteria(criterion)
                for option_id, option_desc in options:
                    choices_mades.append(choices_made.add(
                            criterion.identifier, option_id))


def cache_latest_values(ds):
    """IF the datasource has both LAYER_POINTS and
    DATA_CAN_HAVE_VALUE_LAYER_SCRIPT source, then we can make an
    instance of DatasourceLayer for each of its layers, get a
    timeseries for each location in each layer and cache its latest
    value. Then this information can be used for colouring,
    thresholding, et cetera."""

    if (not ds.has_property(properties.LAYER_POINTS) or
        not ds.has_property(
            properties.DATA_CAN_HAVE_VALUE_LAYER_SCRIPT)):
        return  # For now, we don't know what to do in this case

    for layer in _yield_layers(ds):
        pass
