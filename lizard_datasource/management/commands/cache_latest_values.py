# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

from django.core.management.base import BaseCommand

from lizard_datasource import datasource
from lizard_datasource import scripts


class Command(BaseCommand):
    args = ''
    help = """Iterate over all data sources. If possible, retrieve the
    latest values of all timeseries in them, and cache them. This is
    helpful for things like colouring map layers, thresholding, and
    similar functionality."""

    def handle(self, *args, **options):
        for ds in datasource.get_datasources():
            print(ds)
            scripts.cache_latest_values(ds)
