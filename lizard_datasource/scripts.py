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
            logger.debug("Chooseable critera: {0}".format(criteria))
            if criteria:
                criterion = criteria[0]['criterion']
                options = criteria[0]['values']
                for option in options:
                    choices_mades.append(choices_made.add(
                            criterion.identifier, option['identifier']))


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
        datasource_layer = layer.datasource_layer
        logger.debug("Before locations")
        locations = layer.locations()
        logger.debug("Got locations")
        for location in locations:
            print(
                "Getting timeseries for location {0}."
                .format(location['identifier']))
            timeseries = layer.timeseries(
                location['identifier'],
                start_datetime=dates.utc(2012, 11, 1),
                end_datetime=dates.utc_now())
            if timeseries is None or len(timeseries) == 0:
                continue
            latest = timeseries.tail(1)
            try:
                cache = models.DatasourceCache.objects.get(
                    datasource_layer=datasource_layer,
                    locationid=location['identifier'])
            except models.DatasourceCache.DoesNotExist:
                cache = models.DatasourceCache(
                    datasource_layer=datasource_layer,
                    locationid=location['identifier'])
            cache.timestamp = latest.keys()[0]
            cache.value = latest[0]
            print("Saving value {0} for timestamp {1}.".format(
                    latest[0], latest.keys()[0]))
            cache.save()
            time.sleep(1)