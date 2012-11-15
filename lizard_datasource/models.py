# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import logging

from django.db import models

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


class DatasourceCache(models.Model):
    datasource_layer = models.ForeignKey(DatasourceLayer)
    locationid = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    value = models.FloatField()


class AugmentedDataSource(models.Model):
    """Model holding the configuration of an AugmentedDataSource; see
    augmented_datasource.py."""
    augmented_source = models.ForeignKey(DatasourceModel)

    def __unicode__(self):
#        return "Augmented version of {0}.".format(self.augmented_source)
        return "Augmented version of something.".format(self.augmented_source)
