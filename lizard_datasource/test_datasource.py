from unittest import TestCase

from lizard_datasource import datasource
from lizard_datasource import dummysource


class TestEntrypoints(TestCase):
    def test_no_datasources(self):
        """During testing we should find no real entry points"""
        self.assertEquals(datasource.datasource_entrypoints(), ())


@dummysource.uses_dummy_datasource
def TestDummyEntryPoint(TestCase):
    def test_whee(self):
        datasources = datasource.datasource_entrypoints()
        self.assertEquals(len(datasources), 1)
        self.assertEquals(datasources[0].name, 'dummy data source')
