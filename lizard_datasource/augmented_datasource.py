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

    def __init__(self, config_object):
        """Initialize the object.

        The config_object is an instance of the AugmentedDataSource
        model. It is used to store configuration for this augmented
        datasource in."""

        self.config_object = config_object

    @property
    def original_datasource(self):
        """Return the datasource object that is augmented by this
        AugmentedDataSource object."""

        if not hasattr(self, '_original_datasource'):
            self._original_datasource = datasource.get_datasource_by_model(
                self.config_object.augmented_source,
                exclude=self)

        return self._original_datasource

    @property
    def PROPERTIES(self):
        return self.original_datasource.PROPERTIES

    @property
    def identifier(self):
        return "augmented_{0}_{1}".format(
            self.config_object.id, self.config_object.name)

    @property
    def originating_app(self):
        return 'lizard_datasource'

    def set_choices_made(self, choices_made):
        self._choices_made = choices_made
        self.original_datasource.set_choices_made(choices_made)

    def criteria(self):
        return self.original_datasource.criteria()

    def options_for_criterion(self, criterion):
        return self.original_datasource.options_for_criterion(criterion)

    def chooseable_criteria(self):
        """Just return the chooseable criteria of the original
        datasource."""
        return self.original_datasource.chooseable_criteria()

    def visible_criteria(self):
        """These are the chooseable criteria from the original source,
        minus the layers that are hidden because they are used for
        stuff like colors and percentiles."""

        criteria = self.chooseable_criteria()

        colorfroms = models.ColorFromLatestValue.objects.filter(
            augmented_source=self.config_object,
            hide_from_layer=True)
        percentiles = models.PercentileLayer.objects.filter(
            augmented_source=self.config_object,
            hide_from_layer=True)

        forbidden_choices_json = [
            colorfrom.layer_to_get_color_from.choices_made
            for colorfrom in colorfroms] + [
            percentile.layer_to_get_percentile_from.choices_made
            for percentile in percentiles]

        clean_criteria = []

        my_choices = self._choices_made

        while criteria:
            retry_criteria = []
            for chooseable in criteria:
                criterion = chooseable['criterion']
                options = chooseable['options']

                for option in options.iter_options():
                    new_choices = my_choices.add_criterion_option(
                        criterion, option)
                    if new_choices.json() in forbidden_choices_json:
                        # Alas, we can't use these options as is,
                        # there is a forbidden option in them.
                        if len(options) > 1:
                            # There is more than one option. Retry this
                            # criterion with one option removed.
                            retry_criteria.append({
                                    'criterion': criterion,
                                    'options': options.minus(option)
                                    })
                        break
                else:
                    # Not forbidden, we can use these options!
                    clean_criteria.append(chooseable)

            # Restart the loop with the retry criteria, if any
            criteria = retry_criteria

        return clean_criteria

    def is_applicable(self, choices_made):
        return self.original_datasource.is_applicable(choices_made)

    def is_drawable(self, choices_made):
        return self.original_datasource.is_drawable(choices_made)

    def unit(self, choices_made):
        return self.original_datasource.unit(choices_made)

    def _colorfrom(self):
        """Returns the used colorfromlatestvalue object, if any."""
        try:
            return models.ColorFromLatestValue.objects.get(
                layer_to_add_color_to=self.datasource_layer)
        except models.ColorFromLatestValue.DoesNotExist:
            return None

    def locations(self, bare=False):
        locations = list(self.original_datasource.locations(bare=bare))

        if bare:
            for location in locations:
                yield location
            return

        cached_values = dict()

        colorfrom = self._colorfrom()
        if colorfrom:
            # If there is a colorfrom, use it
            colormap = colorfrom.colormap
            if colorfrom.layer_to_get_color_from:
                for cached_value in models.DatasourceCache.objects.filter(
                    datasource_layer=colorfrom.layer_to_get_color_from):
                    cached_values[cached_value.locationid] = (
                        cached_value.value)

        for location in locations:
            color = "888888"  # Default is gray
            if location.identifier in cached_values:
                value = cached_values[location.identifier]
                color = colormap.color_for(value)
                if color.startswith("#"):
                    color = color[1:]

            location.color = color
            yield location

    def location_annotations(self):
        """If we have colors, we should have a legend for them."""
        logger.debug("IN ANNOTATIONS")
        colorfrom = self._colorfrom()
        if not colorfrom:
            return None
        logger.debug("HAVE COLORFROM")
        annotations = {
            'color': colorfrom.colormap.legend()
            }
        logger.debug("ANNOTATIONS: {0}".format(annotations))
        return annotations

    def timeseries(self, location_id, start_datetime=None, end_datetime=None):
        return self.original_datasource.timeseries(
            location_id, start_datetime, end_datetime)

    def has_percentiles(self):
        return models.PercentileLayer.objects.filter(
            layer_to_add_percentile_to=self.datasource_layer
            ).exists()

    def percentiles(self, location_id, start_datetime=None, end_datetime=None):
        percentiles = {}
        for percentile_layer in models.PercentileLayer.objects.filter(
            layer_to_add_percentile_to=self.datasource_layer):
            source = datasource.get_datasource_by_layer(
                percentile_layer.layer_to_get_percentile_from)

            percentiles[percentile_layer.percentile] = source.timeseries(
                location_id, start_datetime, end_datetime).data()

        return percentiles


def factory():
    """Return an AugmentedDataSource object for each
    AugmentedDataSource model instance."""

    return [AugmentedDataSource(config_object)
            for config_object in models.AugmentedDataSource.objects.all()]

