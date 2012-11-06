"""Datasource API"""

# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import logging
import pkg_resources

from django.utils import simplejson

logger = logging.getLogger(__name__)

FIXED_FLEXIBILITY = object()
AVAILABLE_FLEXIBILITY = object()
CHOSEN_FLEXIBILITY = object()
COLLAPSED_FLEXIBILITY = object()

# List of internal criteria, not to be used by implementing datasources for
# other purposes:
# appname: each datasource must have this set. This is used to find
#          the correct implementing datasources. If get_datasource()
#          is called without this, the global "all data sources
#          combined" data source is returned.


class ChoicesMade(object):
    """Represents a set of choices made. Dict-like.

    Can be initialized in three ways:
    - ChoicesMade(dict={}): initialize from a dict
    - ChoicesMade(json="{}"): initialize from JSON representing a dict
    - ChoicesMade(
         appname="lizard_fewsjdbc",
         slug="brabant"): initialize with keyword parameters.
    """

    def __init__(self, json=None, dict=None, **kwargs):
        if json is not None and dict is None and kwargs == {}:
            self._choices = simplejson.loads(json)
        elif json is None and dict is not None and kwargs == {}:
            self._choices = dict.copy()
        else:
            self._choices = kwargs.copy()
            if json is not None:
                self._choices['json'] = json
            if dict is not None:
                self._choices['dict'] = dict

        logger.debug(
            "End of choices constructor. Dict is {0}.".format(self._choices))

    def __contains__(self, key):
        return key in self._choices

    def __getitem__(self, key):
        return self._choices[key]

    def add(self, key, value):
        choices = self._choices.copy()
        choices[key] = value
        return ChoicesMade(dict=choices)

    def forget(self, key):
        choices = self._choices.copy()
        if key in choices:
            del choices[key]
        return ChoicesMade(dict=choices)

    def json(self):
        return simplejson.dumps(self._choices)

    def __unicode__(self):
        return "ChoicesMade(json={0})".format(
            repr(self.json()))

    def __repr__(self):
        return self.__unicode__()

    def __iter__(self):
        return iter(self._choices)

    def items(self):
        return self._choices.items()


class DataSource(object):
    """Base class for all the DataSource classes. Defines the interface of
    a Lizard data source. Other data sources should subclass this one.

    Datasources have _criteria_. A datasource for which no criteria
    are given represents the entirety of all data reachable through
    the DataSource API.  _Choosing_ extra criteria narrows the dataset
    down and results in a new Datasource representing that data.

    Criteria exist in four _flexibilities_:

    * _Fixed_ criteria were initially given to the call to
      DataSource() constructor by the app. They represent choices that
      are made by the app and that will not by changed, and will stay
      invisible to the user. For instance, the app may choose to see
      only timeseries-backed data.

    * _Chosen_ criteria were added later, presumably by the
      user. These can be _forgotten_, resulting in a new DataSource.

    * _Available_ criteria can be shown to the user to further refine
      the dataset.  They can be _chosen_ resulting in a new
      DataSource.

    * _Collapsed_ criteria are criteria that have only one choice, but
      weren't actively chosen by the user. These shouldn't be shown.

    It is possible that after making a choice, the returned datasource
    has criteria that didn't appear in the old one. E.g. a FEWS data
    source may decide to only offer Parameter criteria once a Filter
    criterium is chosen.

    Criteria may have several _types_ in the future, but initially
    they will just be iterables of possibilities.
    """

    def set_choices_made(self, choices_made):
        self._choices_made = choices_made

    def criteria(self):
        return ()

    def options_for_criterion(self, criterion):
        return ()

    def choose(self, item, value):
        """Return a new datasource with the item selected."""
        pass

    def forget(self, item):
        """Return a new datasource, with criteria equal to the old ones minus
        the forgotten item."""
        pass

    def is_applicable(self, choices_made):
        """Should this data source still be shown, given the choices made?"""
        return False

    def is_drawable(self, choices_made):
        """Can a datasource with these choices made be drawn on the map?"""
        return False


def datasource_entrypoints():
    """Use pkg_resources to find all the data sources."""

    return tuple(pkg_resources.iter_entry_points(group="lizard_datasource"))


def datasources_from_entrypoints():
    datasourcefactories = datasource_entrypoints()
    datasources = []
    for entrypoint in datasourcefactories:
        try:
            factory = entrypoint.load()
            datasources += factory()
        except ImportError, e:
            logger.debug(e)

    return datasources


def get_datasources(choices_made=ChoicesMade()):
    datasources = []
    for datasource in datasources_from_entrypoints():
        if datasource.is_applicable(choices_made):
            datasource.set_choices_made(choices_made)
            datasources.append(datasource)

    return datasources


class CombinedDataSource(DataSource):
    def __init__(self, choices_made=ChoicesMade()):
        try:
            self._datasources = get_datasources(choices_made)
            logger.debug("Datasources: {0}".format(self._datasources))
            self._choices_made = choices_made
        except Exception, e:
            logger.debug(e)

    def criteria(self):
        try:
            criteria = set()
            for ds in self._datasources:
                criteria = criteria.union(set(ds.criteria()))
                logger.debug("Criteria: {0}".format(criteria))
        except Exception, e:
            logger.debug(e)
        return list(criteria)

    def options_for_criterion(self, criterion):
        options = set()
        for ds in self._datasources:
            options = options.union(set(ds.options_for_criterion(criterion)))
        return list(options)

    def chooseable_criteria(self):
        all_criteria = self.criteria()
        chosen_identifiers = set()
        for criterion in all_criteria:
            if (criterion.identifier in self._choices_made or
                len(self.options_for_criterion(criterion)) == 1):
                chosen_identifiers.add(criterion.identifier)

        criteria = []
        for criterion in all_criteria:
            if criterion.identifier in self._choices_made:
                # Already chosen
                continue
            if not all(identifier in chosen_identifiers
                       for identifier in criterion.prerequisites):
                # Not all prerequisites chosen
                continue

            options = self.options_for_criterion(criterion)
            if len(options) > 1:
                values = []
                for option_id, option_desc in options:
                    values.append({
                            'identifier': option_id,
                            'description': option_desc,
                            })
                criteria.append({
                        'criterion': criterion,
                        'values': values,
                        })
        return criteria

    def is_drawable(self, choices_made):
        # Return True if one of our constituents can draw itself given these
        # choices
        return any(ds.is_drawable(choices_made)
                   for ds in self._datasources)
