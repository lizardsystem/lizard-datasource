# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import datetime
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
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

    # There is a 'cache latest values' script that runs now and then
    script_times_to_run_per_day = models.IntegerField(default=24)
    script_last_run_started = models.DateTimeField(null=True)
    script_run_next_opportunity = models.BooleanField(default=False)

    def __unicode__(self):
        return "'{0}' from app '{1}'".format(
            self.identifier,
            self.originating_app)

    def activation_for_cache_script(self):
        """Return True if the cache script should active. If it shouldn't,
        if will do nothing this time.

        If True is returned, it is assumed that the script will run now,
        and that is recorded."""

        if self.cache_script_is_due():
            self.script_last_run_started = datetime.datetime.now()
            self.script_run_next_opportunity = False
            self.save()
            return True
        else:
            return False

    def cache_script_is_due(self):
        if self.script_run_next_opportunity:
            return True

        if self.script_last_run_started is None:
            return True

        if not (0 < self.script_times_to_run_per_day <= (24 * 60)):
            return False

        minutes_between_scripts = (
            (60 * 24) // self.script_times_to_run_per_day)

        current_time = datetime.datetime.now()

        minutes_since_midnight = (
            60 * current_time.hour + current_time.minute)

        script_should_run_at_minutes = (
            minutes_since_midnight -
            (minutes_since_midnight % minutes_between_scripts))

        script_should_run_at = current_time.replace(
            hour=script_should_run_at_minutes // 60,
            minute=script_should_run_at_minutes % 60)

        return script_should_run_at > self.script_last_run_started

    class Meta:
        ordering = ('originating_app', 'identifier')


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
    defaultdescription = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def color_for(self, value):
        for colormapline in self.colormapline_set.all():
            color = colormapline.color_for(value)
            if color:
                return color
        return self.defaultcolor

    def legend(self):
        l = [
            (line.color, line.line_description)
            for line in self.colormapline_set.all()]
        if self.defaultcolor:
            description = self.defaultdescription or _("Default")
            l.append((self.defaultcolor, description))
        return l


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
    description = models.CharField(max_length=50, null=True, blank=True)

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

    def line_description(self):
        """Return a description for this line, to be used in legends."""
        if self.description:
            return self.description

        # Otherwise construct one that looks like "0 <= x < 6"
        description = "x"

        if self.minvalue is not None:
            if self.mininclusive:
                description = "{0} <= {1}".format(self.minvalue, description)
            else:
                description = "{0} < {1}".format(self.minvalue, description)

        if self.maxvalue is not None:
            if self.maxinclusive:
                description = "{0} <= {1}".format(description, self.maxvalue)
            else:
                description = "{0} < {1}".format(description, self.maxvalue)

        return description
