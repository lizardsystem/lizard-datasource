"""Datasource API"""

# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import itertools
import logging
import pkg_resources

from django.utils import simplejson

from lizard_datasource import models
from lizard_datasource import criteria
from lizard_datasource.functools import memoize

logger = logging.getLogger(__name__)


class ChoicesMade(object):
    """Represents a set of choices made. Dict-like.

    Can be initialized in three ways:
    - ChoicesMade(dict={}): initialize from a dict
    - ChoicesMade(json="{}"): initialize from JSON representing a dict
    - ChoicesMade(
         appname="lizard_fewsjdbc",
         slug="brabant"): initialize with keyword parameters.

    ChoicesMade objects are immutable value objects. They can be used
    as dictionary keys and can be relied on not to change. Therefore,
    methods like add() that add choices do so by returning a new
    ChoicesMade instance.

    Unfortunately this class only stores the identifiers of choices
    made, and not the extra data of lizard_datasource.criteria.Option
    objects (primarily the description of an option). This is mostly
    to be able to represent a ChoicesMade instance as JSON in a way
    that is fairly small and constant.

    Although dictionaries are not ordered, the JSON serialization of a
    ChoicesMade object is always in alphabetical order. If the JSON
    representation of two objects is different, they are different.
    """

    def __init__(self, json=None, dict=None, **kwargs):
        if (json is not None) and (dict is None) and (kwargs == {}):
            # Initialize using JSON.
            self._choices = simplejson.loads(json)
        elif (json is None) and (dict is not None) and (kwargs == {}):
            # Initialize using dict.
            self._choices = dict.copy()
        else:
            # Initialize using kwargs.
            self._choices = kwargs.copy()
            if json is not None:
                self._choices['json'] = json
            if dict is not None:
                self._choices['dict'] = dict

    def __contains__(self, key):
        """Return true if the criterion identified by key is in the
        choices made."""
        return key in self._choices

    def __getitem__(self, key):
        """Return the identifier of the option chosen for this
        criterion."""
        return self._choices[key]

    def get(self, key, default=None):
        """Return the identifier of the option chosen for this
        criterion, or the default if the criterion isn't found."""
        return self._choices.get(key, default)

    def add(self, criterion_identifier, option_identifier):
        """Return a new instance of ChoicesMade with this choice added."""
        choices = self._choices.copy()
        choices[criterion_identifier] = option_identifier
        return ChoicesMade(dict=choices)

    def add_criterion_option(self, criterion, option):
        """Return a new instance of ChoicesMade with this choice added."""
        return self.add(criterion.identifier, option.identifier)

    def forget(self, criterion_identifier):
        """Return a new instance of ChoicesMade with this choice removed."""
        choices = self._choices.copy()
        if criterion_identifier in choices:
            del choices[criterion_identifier]
        return ChoicesMade(dict=choices)

    def json(self):
        """Return a JSON representation of this ChoicesMade instance.

        The keys are always sorted, and two equal ChoicesMade instances have equal
        JSON representations, and vice versa.

        E.g., for two choicesmades 'a' and 'b',

        (a == b) == (a.json() == b.json())
        """
        return simplejson.dumps(self._choices, sort_keys=True)

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
    """

    @property
    def identifier(self):
        return ''  # Only the base has the empty identifier

    @property
    def description(self):
        return "Base datasource"

    @property
    def originating_app(self):
        return 'lizard_datasource'

    @property
    def datasource_model(self):
        if not hasattr(self, '_dsm') or not self._dsm:
            try:
                self._dsm = models.DatasourceModel.objects.get(
                    identifier=self.identifier,
                    originating_app=self.originating_app)
            except models.DatasourceModel.DoesNotExist:
                self._dsm = models.DatasourceModel(
                    identifier=self.identifier,
                    originating_app=self.originating_app)
                self._dsm.save()
        return self._dsm

    @property
    def visible(self):
        return self.datasource_model.visible

    @property
    def datasource_layer(self):
        """Return the DatasourceLayer model instance that relates to
        this datasource and the curently set ChoicesMade. Create the
        instance if it doesn't exist yet."""

        # Don't cache, because choices_made is mutated regularly.
        json = self._choices_made.json()
        dsm = self.datasource_model

        try:
            return models.DatasourceLayer.objects.get(
                datasource_model=dsm,
                choices_made=json)
        except models.DatasourceLayer.DoesNotExist:
            dsl = models.DatasourceLayer(
                datasource_model=dsm,
                choices_made=json)
            dsl.save()
            return dsl

    def activation_for_cache_script(self):
        """Return True if the cache script should active. If it shouldn't,
        if will do nothing this time.

        If True is returned, it is assumed that the script will run now,
        and that is recorded."""
        return self.datasource_model.activation_for_cache_script()

    def set_choices_made(self, choices_made):
        self._choices_made = choices_made

    def get_choices_made(self):
        return self._choices_made

    def criteria(self):
        return ()

    def options_for_criterion(self, criterion):
        """Return a criteria.Options object that represents the options this
        datasource has for that criterion.

        Datasources can be asked to supply options for criterion that
        they don't even have. In that case, they should return
        criteria.EmptyOptions().  It is important that all datasources
        return the same type of Options object (OptionList,
        OptionTree, ...) for the same criterion, because
        CombinedDataSource will try to add them together."""

        return criteria.EmptyOptions()

    def chooseable_criteria(self):
        all_criteria = self.criteria()
        chosen_identifiers = set()
        for criterion in all_criteria:
            options = self.options_for_criterion(criterion)
            if (criterion.identifier in self._choices_made or
                len(options) == 1):
                chosen_identifiers.add(criterion.identifier)

        criterions = []
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
                criterions.append({
                        'criterion': criterion,
                        'options': options
                        })
            elif len(options) == 1:
                # It is still "chooseable" in a way if the resulting
                # datasource can be drawn
                option = options.only_option()
                resulting_choices = self._choices_made.add(
                    criterion.identifier, option.identifier)

                if self.is_drawable(resulting_choices):
                    criterions.append({
                            'criterion': criterion,
                            'options': options
                            })

        return criterions

    def visible_criteria(self):
        """Return those chooseable criteria that should be visible to
        the user."""
        return self.chooseable_criteria()

    def is_applicable(self, choices_made):
        """Should this data source still be shown, given the choices made?"""
        own_criteria_identifiers = set(
            criterion.identifier for criterion in self.criteria())
        if any(choice_identifier not in own_criteria_identifiers
               for choice_identifier in choices_made):
            return False

        return True

    def is_drawable(self, choices_made=None):
        """Can a datasource with these choices made be drawn on the map?"""
        return False

    def unit(self, choices_made=None):
        """Returns a unicode string describing the unit of the data
        drawable by this datasource.

        Should only be called if the datasource is_drawable with these
        choices, because if there are still choices to be made before
        a layer can be drawn, it is likely that the data has more than
        one unit.

        Optional. This function is allowed to simply return None."""
        return None

    def has_property(self, property):
        """Does the datasource have this property? See properties.py
        for a list."""
        return hasattr(self, 'PROPERTIES') and property in self.PROPERTIES

    def locations(self, bare=True):
        """Should return an Exception if the datasource is not drawable.
        Should return an Exception if the datasource is not LAYER_POINTS.

        Returns an iterable of lizard_datasource.location.Location objects.

        If bare is False, other helpful information like coloring may
        be included in the locations. If bare is True, the fastest way
        to return the right locations should be used.
        """
        return []

    def timeseries(self, location_id, start_datetime=None, end_datetime=None):
        """Return the relevant timeseries at that location id. Start
        and end datetimes are in UTC. Results in a
        lizard_datasource.timeseries.Timeseries object, or None if
        there are no timeseries available."""
        return None

    def location_annotations(self):
        """A datasource may add annotations (extra fields) to the
        Locations it returns.

        If it doesn't, this function returns None, or {}.

        If it does, this function returns a dictionary with the
        field names as keys.  The values are either None (in which
        case this just serves to note that the field exists) or a list
        of tuples of the form (value, description), which can be
        used for things like legends."""
        return None

    def has_percentiles(self):
        return False


class CombinedDataSource(DataSource):
    """If there are several visible datasources in the system, a
    CombinedDataSource is presented to any client code instead.

    Conceptually, the CombinedDataSource represents the combined data
    of all its underlying data sources.

    Most methods will be implemented by calling all data sources in a
    loop and combining the result in some way.

    Most methods added to DataSource will have to be added to
    CombinedDataSource as well.

    The CombinedDataSource should not have any state, other than the list
    of datasources, so it has no config object in the database and does not
    by itself keep track of choices made.
    """
    def __init__(self, datasources):
        self._datasources = datasources
        self._choices_made = None

    @property
    def identifier(self):
        return 'CombinedDataSource'

    @property
    def description(self):
        return 'CombinedDataSource'

    @property
    def originating_app(self):
        return 'lizard_datasource'

    @property
    def datasource_model(self):
        """Should never be called."""
        raise ValueError()

    @property
    def visible(self):
        # True, because we are a combination of visible data sources
        return True

    @property
    def datasource_layer(self):
        """Should never be called."""
        raise ValueError()

    def set_choices_made(self, choices_made):
        for datasource in self._datasources:
            datasource.set_choices_made(choices_made)
        self._choices_made = choices_made

    def get_choices_made(self):
        return self._choices_made

    def criteria(self):
        crits = set()
        for ds in self._datasources:
            crits = crits.union(set(ds.criteria()))

        return list(crits)

    def options_for_criterion(self, criterion):
        options = criteria.EmptyOptions()
        for ds in self._datasources:
            options = options.add(ds.options_for_criterion(criterion))
        return options

    # chooseable_criteria not overridden
    # visible_criteria not overriden

    def is_drawable(self, choices_made=None):
        """Return True if some of our constituents can draw themselves
        given these choices"""

        if choices_made is None:
            choices_made = self._choices_made

        return any(ds.is_drawable(choices_made)
                   for ds in self._datasources)

    def unit(self, choices_made=None):
        """If the constituent data sources all give the same answer,
        return it, otherwise return None."""
        if choices_made is None:
            choices_made = self._choices_made

        units = set(ds.unit(choices_made) for ds in self._datasources)
        if len(units) == 1:
            return units.pop()
        else:
            return None

    def has_property(self, property):
        """CombinedDataSource has a property iff there are underlying
        data source and they all the underlying data sources have the
        property."""
        return self._datasources and all(ds.has_property(property)
                   for ds in self._datasources)

    def locations(self):
        """Return locations from all the underlying datasources."""
        return itertools.chain(*(
            datasource.locations()
            for datasource in self._datasources))

    def timeseries(self):
        pass

    def has_percentiles(self):
        pass


@memoize
def datasource_entrypoints():
    """Use pkg_resources to find all the data source entry points."""

    return tuple(pkg_resources.iter_entry_points(group="lizard_datasource"))


def datasources_from_entrypoints():
    """Return all datasources in the system."""

    datasourcefactories = datasource_entrypoints()
    datasources = []
    for entrypoint in datasourcefactories:
        try:
            datasource_factory = entrypoint.load()
            datasources += datasource_factory()
        except ImportError, e:
            logger.warn(e)

    return datasources


def get_datasources(choices_made=ChoicesMade()):
    """Return all the datasources defined by entrypoints that are
    applicable to the given choices_made."""

    datasources = []
    for datasource in datasources_from_entrypoints():
        if datasource.visible and datasource.is_applicable(choices_made):
            datasource.set_choices_made(choices_made)
            datasources.append(datasource)

    return datasources


def get_datasource_by_model(datasource_model, exclude=None):
    """Find and return a given datasource using its stored model.

    All datasources by implementing apps need to have an 'originating_app'
    property and an 'identifier' property. Datasource_models store these,
    plus some central configuration options for the datasources. If you
    have a datasource_model instance, use this function to get the
    corresponding datasource."""
    for datasource in datasources_from_entrypoints():
        if exclude and datasource is exclude:
            continue

        if (datasource_model.originating_app == datasource.originating_app
            and datasource.identifier == datasource_model.identifier):
            return datasource


def get_datasource_by_layer(datasource_layer):
    """Return the datasource defined by datasource_layer.

    A datasource layer is defined by a datasource model and a set of
    choices made. This function retrieves the datasource using the
    datasource model, and sets the choices made before returning it."""
    datasource = get_datasource_by_model(
        datasource_layer.datasource_model)

    choices_made = ChoicesMade(json=datasource_layer.choices_made)
    datasource.set_choices_made(choices_made)

    return datasource


def datasource(choices_made=ChoicesMade()):
    """Get the global datasource. If there is only one applicable
    datasource, return that, otherwise return a CombinedDatasource
    made up of all of them. We should perhaps have an EmptyDataSource
    for the zero case. For now, return None."""

    datasources = get_datasources(choices_made)

    if len(datasources) == 0:
        return None
    elif len(datasources) == 1:
        return datasources[0]
    else:
        datasource = CombinedDataSource(datasources)
        datasource.set_choices_made(choices_made)
        return datasource
