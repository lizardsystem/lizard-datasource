"""Tests for augmented_datasource.py."""

import mock

from django.test import TestCase

from lizard_datasource import augmented_datasource
from lizard_datasource.tests import test_models


class TestAugmentedSource(TestCase):
    def test_creation(self):
        model_instance = test_models.AugmentedDataSourceF.build()
        augmented_source = augmented_datasource.AugmentedDataSource(
            model_instance)
        self.assertEquals(
            augmented_source.config_object,
            model_instance)

    def test_can_call_unit_without_extra_arguments(self):
        """Because that didn't work, some day..."""
        with mock.patch(
            'lizard_datasource.augmented_datasource.'
            'AugmentedDataSource.original_datasource'):
            model_instance = test_models.AugmentedDataSourceF.build()
            augmented_source = augmented_datasource.AugmentedDataSource(
                model_instance)

            augmented_source.unit()


class TestAugmentedSourceFactory(TestCase):
    def test_returns_source(self):
        test_models.AugmentedDataSourceF.create()
        sources = augmented_datasource.factory()
        self.assertEquals(len(sources), 1)
