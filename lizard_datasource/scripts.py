import datetime
import logging
import time

from lizard_datasource import datasource
from lizard_datasource import dates
from lizard_datasource import models
from lizard_datasource import properties

logger = logging.getLogger(__name__)


def _yield_drawable_datasources(ds):
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
            # logger.debug("choices_made: %s", choices_made)
            if criteria:
                criterion = criteria[0]['criterion']
                # logger.debug("criterion: %s", criterion)
                options = criteria[0]['options']
                for option in options.iter_options():
                    # logger.debug("choice: %s", option)
                    choices_mades.append(choices_made.add(
                            criterion.identifier, option.identifier))


def cache_latest_values(ds, allow_cache=True):
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

    # Only actually do something if the script is due.
    if allow_cache and not ds.activation_for_cache_script():
        logger.info("Datasource %s isn't due for action yet, skipping it.",
                    ds)
        return
    logger.info("Caching latest values for datasource %s", ds)

    for drawable in _yield_drawable_datasources(ds):
        # This creates the datasource layer in the database, if it
        # didn't exist yet
        datasource_layer = drawable.datasource_layer

        # Cache the datasource layer's unit, if it wasn't filled in yet
        drawable.cached_unit()

        # If we don't actually use the latest values of this layer, we
        # should skip it.
        if not datasource_layer.latest_values_used:
            continue

        locations = drawable.locations()
        for location in locations:
            try:
                ds_cache = models.DatasourceCache.objects.get(
                    datasource_layer=datasource_layer,
                    locationid=location.identifier)
            except models.DatasourceCache.DoesNotExist:
                ds_cache = models.DatasourceCache(
                    datasource_layer=datasource_layer,
                    locationid=location.identifier)

            if ds_cache.timestamp and allow_cache:
                start_datetime = ds_cache.timestamp
            else:
                start_datetime = dates.utc_now() - datetime.timedelta(days=4)

            timeseries = drawable.timeseries(
                location.identifier,
                start_datetime=start_datetime,
                end_datetime=dates.utc_now())
            if timeseries is None or len(timeseries) == 0:
                logger.info("Didn't find new latest value for ds layer %s "
                            "and location %s since %s",
                            datasource_layer, location, start_datetime)
                continue

            latest = timeseries.latest()
            ds_cache.timestamp = latest.keys()[0]
            ds_cache.value = latest[0]
            logger.info("Found new latest value for ds layer %s "
                        "and location %s: %s",
                            datasource_layer, location, latest[0])
            ds_cache.save()
            time.sleep(1)
