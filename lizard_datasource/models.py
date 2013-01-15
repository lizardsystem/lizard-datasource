# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import logging

from django.db import models
import colorful.fields

logger = logging.getLogger(__name__)


class DatasourceModel(models.Model):
    """Each datasource we find should have a corresponding entry in
    this table. It controls whether the datasource should be visible
    to users, and possibly other metadata, like how often to run
    scripts related to the datasource."""

    # We need: Some kind of unique identifier / description thingy to
    # show to a user in the admin. Let's call it "identifier" for
    # conceptual continuity with the rest of this app.
    identifier = models.CharField(max_length=200)

    # The originating app, surely. Although it'll probably be
    # contained in the identifier as well.
    originating_app = models.CharField(max_length=100)

    # A boolean saying whether this is visible, because we promised to
    # have one of those
    visible = models.BooleanField(default=False)

    def __unicode__(self):
        return "'{0}' from app '{1}'".format(
            self.identifier,
            self.originating_app)


class DatasourceLayer(models.Model):
    """Represents a set of choices that could be made in a datasource
    that would result in a drawable layer. This is, for now, only relevant
    for those layers for which lizard_datasource caches the latest values
    of each timeseries."""

    datasource_model = models.ForeignKey(DatasourceModel)

    # To store JSON. Note that the JSON for this field should ALWAYS
    # be constructed with json.dumps(..., sort_keys=True) so that
    # output of identical dictionaries will always result in identical
    # JSON.
    choices_made = models.TextField()

    def __unicode__(self):
        return "{0}: {1}".format(self.datasource_model, self.choices_made)

    @property
    def latest_values_used(self):
        """The only thing that latest values are used for as yet is
        for ColorFromLatestValue."""
        return self.colors_used_by.exists()


class DatasourceCache(models.Model):
    datasource_layer = models.ForeignKey(DatasourceLayer)
    locationid = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    value = models.FloatField()


class AugmentedDataSource(models.Model):
    """Model holding the configuration of an AugmentedDataSource; see
    augmented_datasource.py."""
    augmented_source = models.ForeignKey(DatasourceModel)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class ColorMap(models.Model):
    """Model holding a mapping from a float value to a color. It has a
    name, and several ColorMapLines that have a min, a max,
    "inclusive" checkboxes and a color."""
    name = models.CharField(max_length=100)
    defaultcolor = colorful.fields.RGBColorField(null=True)

    def __unicode__(self):
        return self.name

    def color_for(self, value):
        for colormapline in self.colormapline_set.all():
            color = colormapline.color_for(value)
            if color:
                return color
        return self.defaultcolor


class ColorFromLatestValue(models.Model):
    augmented_source = models.ForeignKey(AugmentedDataSource)
    layer_to_add_color_to = models.ForeignKey(
        DatasourceLayer, related_name="colors_from")
    layer_to_get_color_from = models.ForeignKey(
        DatasourceLayer, null=True, related_name="colors_used_by")
    colormap = models.ForeignKey(ColorMap)
    hide_from_layer = models.BooleanField(default=False)


class PercentileLayer(models.Model):
    augmented_source = models.ForeignKey(AugmentedDataSource)
    layer_to_add_percentile_to = models.ForeignKey(
        DatasourceLayer, related_name="percentiles_from")
    layer_to_get_percentile_from = models.ForeignKey(
        DatasourceLayer, related_name="percentiles_used_by")
    percentile = models.FloatField(default=0.0)
    hide_from_layer = models.BooleanField(default=False)


class ColorMapLine(models.Model):
    class Meta:
        ordering = ['minvalue', 'maxvalue']

    colormap = models.ForeignKey(ColorMap)

    minvalue = models.FloatField(null=True, blank=True)
    maxvalue = models.FloatField(null=True, blank=True)
    mininclusive = models.BooleanField(default=False)
    maxinclusive = models.BooleanField(default=True)

    color = colorful.fields.RGBColorField()

    def color_for(self, value):
        if self.minvalue is None:
            minvalue = value - 1
        else:
            minvalue = self.minvalue

        if self.maxvalue is None:
            maxvalue = value + 1
        else:
            maxvalue = self.maxvalue

        if ((minvalue < value < maxvalue) or
            (self.mininclusive and minvalue == value) or
            (self.maxinclusive and maxvalue == value)):
            return self.color

        return None
