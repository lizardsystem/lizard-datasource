"""Implements a data source that "augments" an existing datasource.
This will by default act as an exact copy of the augmented
datasource, but it should be possible to add various things to it:

- New layers, made by combining other layers in various ways
- Giving color classes to locations, based on latest values of
  timeseries in layers of this datasource
- Adding extra data to timeseries (e.g. percentile bands, metadata,
  multiple graphs?)

Each AugmentedDataSource has a corresponding AugmentedDataSource model
instance that holds its configuration.
"""

# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import logging

from lizard_datasource import datasource
from lizard_datasource import models

logger = logging.getLogger(__name__)


class AugmentedDataSource(datasource.DataSource):
    """By default this just forwards most important methods to the
    datasource that's being augmented. Before returning some results
    may or may not be, well, augmented."""
    def __init__(self, augmented_model_instance):
        self.augmented_model_instance = augmented_model_instance

    @property
    def augmented_source(self):
        if not hasattr(self, '_augmented_source'):
            logger.debug("PING")
            try:
                self._augmented_source = datasource.get_datasource_by_model(
                    self.augmented_model_instance.augmented_source,
                    exclude=self)
            except Exception, e:
                logger.debug("But no PONG: {0}.".format(e))
            logger.debug("The chosen augmented source is: {0}."
                         .format(self._augmented_source))
        return self._augmented_source

    @property
    def PROPERTIES(self):
        logger.debug("I'm in PROPERTIES and my id is {0}.".format(id(self)))
        return self.augmented_source.PROPERTIES

    @property
    def identifier(self):
        return "augmented_{0}".format(
            self.augmented_model_instance.id)

    @property
    def originating_app(self):
        return 'lizard_datasource'

    def set_choices_made(self, choices_made):
        self._choices_made = choices_made
        self.augmented_source.set_choices_made(choices_made)

    def criteria(self):
        return self.augmented_source.criteria()

    def options_for_criterion(self, criterion):
        return self.augmented_source.options_for_criterion(criterion)

    def chooseable_criteria(self):
        return self.augmented_source.chooseable_criteria()

    def is_applicable(self, choices_made):
        return self.augmented_source.is_applicable(choices_made)

    def is_drawable(self, choices_made):
        return self.augmented_source.is_drawable(choices_made)

    def locations(self):
        locations = list(self.augmented_source.locations())

        datasource_layer = self.augmented_source.datasource_layer
        if datasource_layer:
            caches = dict()
            for cache in models.DatasourceCache.objects.filter(
                datasource_layer=datasource_layer):
                caches[cache.locationid] = cache.value
            for location in locations:
                color = "888888"  # Default is gray
                if location['identifier'] in caches:
                    if caches[location['identifier']] < 1050:
                        color = "00ff00"  # Green
                    else:
                        color = "ff0000"  # Red
                location['color'] = color
        return locations

    def timeseries(self, location_id, start_datetime=None, end_datetime=None):
        return self.augmented_source.timeseries(
            location_id, start_datetime, end_datetime)


def factory():
    """Returns an AugmentedDataSource object for each
    AugmentedDataSource model instance."""

    try:
        return [AugmentedDataSource(source)
                for source in models.AugmentedDataSource.objects.all()]
    except Exception, e:
        logger.debug(
            "Exception in augmented datasource factory: {0}".format(e))
        return []
