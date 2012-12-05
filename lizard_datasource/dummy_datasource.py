# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import logging

from lizard_datasource import criteria
from lizard_datasource import datasource
from lizard_datasource import location
from lizard_datasource import properties
from lizard_datasource import timeseries
from lizard_datasource.dates import utc

logger = logging.getLogger(__name__)

# Found with Google, http://www.google.com/ig/cities?country=NL
CITIES = {
    "ae":
        [
        {"id": "almere", "name": "Almere",
         "lat": 52299999, "lon": 4769999},
        {"id": "amersfoorst", "name": "Amersfoort",
         "lat": 52130001, "lon": 5269999},
        {"id": "amstelveen", "name": "Amstelveen",
         "lat": 52299999, "lon": 4769999},
        {"id": "amsterdam", "name": "Amsterdam",
         "lat": 52299999, "lon": 4769999},
        {"id": "apeldoorn", "name": "Apeldoorn",
         "lat": 52069999, "lon": 5880000},
        {"id": "breda", "name": "Breda",
         "lat": 51569999, "lon": 4929999},
        {"id": "delft", "name": "Delft",
         "lat": 51950000, "lon": 4449999},
        {"id": "denhaag", "name": "Den Haag",
         "lat": 52270000, "lon": 4300000},
        {"id": "deventer", "name": "Deventer",
         "lat": 52069999, "lon": 5880000},
        {"id": "dordrecht", "name": "Dordrecht",
         "lat": 51950000, "lon": 4449999},
        {"id": "eindhoven", "name": "Eindhoven",
         "lat": 51450000, "lon": 5420000},
        {"id": "enschede", "name": "Enschede",
         "lat": 52069999, "lon": 6650000},
        ],
    "gz": [
        {"id": "groningen", "name": "Groningen",
         "lat": 53130001, "lon": 6579999},
        {"id": "haarlem", "name": "Haarlem",
         "lat": 52419998, "lon": 4550000},
        {"id": "haarlemmermeer", "name": "Haarlemmermeer",
         "lat": 52299999, "lon": 4769999},
        {"id": "heerlen", "name": "Heerlen",
         "lat": 50919998, "lon": 5780000},
        {"id": "helmond", "name": "Helmond",
         "lat": 51450000, "lon": 5420000},
        {"id": "hilversum", "name": "Hilversum",
         "lat": 52099998, "lon": 5179999},
        {"id": "leeuwarden", "name": "Leeuwarden",
         "lat": 53220001, "lon": 5750000},
        {"id": "maastricht", "name": "Maastricht",
         "lat": 50919998, "lon": 5780000},
        {"id": "rotterdam", "name": "Rotterdam",
         "lat": 51950000, "lon": 4449999},
        {"id": "sittard", "name": "Sittard-Geleen",
         "lat": 50919998, "lon": 5780000},
        {"id": "tilburg", "name": "Tilburg",
         "lat": 51569999, "lon": 4929999},
        {"id": "utrecht", "name": "Utrecht",
         "lat": 52099998, "lon": 5179999},
        {"id": "zaandstad", "name": "Zaanstad",
         "lat": 52470001, "lon": 4579999}
        ]
    }


class DummyDataSource(datasource.DataSource):
    PROPERTIES = (
        properties.LAYER_POINTS,
        properties.DATA_CAN_HAVE_VALUE_LAYER_SCRIPT
        )

    @property
    def identifier(self):
        return "dummy_data_source"

    @property
    def description(self):
        return "Dummy data source"

    def criteria(self):
        return (
            criteria.AppNameCriterion(),
            criteria.Criterion(
                identifier='first_letter',
                description='Eerste letter plaatsnaam',
                datatype=criteria.Criterion.TYPE_SELECT,
                prerequisites=("appname",)),
            )

    def options_for_criterion(self, criterion):
        logger.debug(
            "Dummy options for criterion, criterion: {0}".format(criterion))
        if criterion.identifier == 'appname':
            return criteria.OptionList(
                (criteria.Option('lizard_datasource', 'Lizard-DataSource'),))
        if criterion.identifier == 'first_letter':
            return criteria.OptionList((
                    criteria.Option('ae', 'A-E'),
                    criteria.Option('gz', 'G-Z')))
        logger.debug("Fallback")
        return criteria.EmptyOptions()

    def is_applicable(self, choices_made):
        if not super(DummyDataSource, self).is_applicable(choices_made):
            return False

        if ('appname' in choices_made and
            choices_made['appname'] != 'lizard_datasource'):
            return False

        return True

    def is_drawable(self, choices_made=None):
        if choices_made is None:
            choices_made = self._choices_made

        return 'first_letter' in choices_made

    def locations(self):
        if not self.is_drawable():
            raise ValueError(
                "Datasource locations() called when it wasn't drawable")
        cities = CITIES[self._choices_made['first_letter']]

        return [
            location.Location(
                identifier=city['id'],
                latitude=city['lat'] / 1000000.0,
                longitude=city['lon'] / 1000000.0)

            for city in cities
            ]

    def timeseries(self, location_id, start_datetime=None, end_datetime=None):
        return timeseries.Timeseries({
            utc(2012, 11, 13, 11, 0): 10.0,
            utc(2012, 11, 13, 12, 0): 15.0,
            utc(2012, 11, 13, 13, 0): 20.0,
            utc(2012, 11, 13, 14, 0): 14.0
            })


def factory():
    return [DummyDataSource()]
