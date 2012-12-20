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
            augmented_source.augmented_model_instance,
            model_instance)


class TestAugmentedSourceFactory(TestCase):
    def test_returns_source(self):
        test_models.AugmentedDataSourceF.create()
        sources = augmented_datasource.factory()
        self.assertEquals(len(sources), 1)

    def test_exception_somewhere_returns_empty_list(self):
        test_models.AugmentedDataSourceF.create()
        with mock.patch(
            'lizard_datasource.models.AugmentedDataSource.objects.all',
            side_effect=ValueError('testing')):
            sources = augmented_datasource.factory()
        self.assertEquals(sources, [])
