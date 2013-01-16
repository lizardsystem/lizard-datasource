import datetime
import logging
import time

from lizard_datasource import datasource
from lizard_datasource import dates
from lizard_datasource import models
from lizard_datasource import properties

logger = logging.getLogger(__name__)


def _yield_layers(ds):
    # This implements a breadth-first search that tries to visit all
    # drawable layers and yields their choices made objects. The case
    # where ChoicesMade is empty functions as the root of the tree.
    choices_mades = [datasource.ChoicesMade()]

    while choices_mades:
        choices_made = choices_mades.pop(0)
        ds.set_choices_made(choices_made)

        if ds.is_drawable(choices_made):
            yield ds
        else:
            criteria = ds.chooseable_criteria()

            if criteria:
                criterion = criteria[0]['criterion']
                options = criteria[0]['options']
                for option in options.iter_options():
                    choices_mades.append(choices_made.add(
                            criterion.identifier, option.identifier))


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
        # This creates the datasource layer in the database, if it
        # didn't exist yet
        datasource_layer = layer.datasource_layer

        # If we don't actually use the latest values of this layer, we
        # should skip it.
        if not datasource_layer.latest_values_used:
            continue

        locations = layer.locations()
        for location in locations:
            print(
                "Getting timeseries for location {0}."
                .format(location.identifier))
            timeseries = layer.timeseries(
                location.identifier,
                start_datetime=dates.utc_now() - datetime.timedelta(days=60),
                end_datetime=dates.utc_now())
            if timeseries is None or len(timeseries) == 0:
                continue

            latest = timeseries.latest()
            try:
                cache = models.DatasourceCache.objects.get(
                    datasource_layer=datasource_layer,
                    locationid=location.identifier)
            except models.DatasourceCache.DoesNotExist:
                cache = models.DatasourceCache(
                    datasource_layer=datasource_layer,
                    locationid=location.identifier)
            cache.timestamp = latest.keys()[0]
            cache.value = latest[0]
            print("Saving value {0} for timestamp {1}.".format(
                    latest[0], latest.keys()[0]))
            cache.save()
            time.sleep(1)
