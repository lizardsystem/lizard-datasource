"""Tests for lizard_datasource.scripts."""

import mock

from django.test import TestCase

from lizard_datasource import datasource
from lizard_datasource import scripts


class TestYieldLayers(TestCase):
    def test_drawable_datasource_returned(self):
        ds = mock.MagicMock()
        ds.is_drawable.return_value = True
        layers = list(scripts._yield_drawable_datasources(ds))
        self.assertEquals(len(layers), 1)
        self.assertTrue(layers[0] is ds)
