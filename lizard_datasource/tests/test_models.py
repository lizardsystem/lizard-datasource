import datetime
import factory
import mock

from django.test import TestCase
from lizard_datasource import models


## Factories, keep them in the same order as in models.py


class DatasourceModelF(factory.Factory):
    FACTORY_FOR = models.DatasourceModel

    identifier = "some_identifier"
    originating_app = "lizard_datasource_tests"
    visible = True

    script_times_to_run_per_day = 24
    script_last_run_started = None
    script_run_next_opportunity = False


class DatasourceLayerF(factory.Factory):
    FACTORY_FOR = models.DatasourceLayer

    datasource_model = factory.SubFactory(DatasourceModelF)


class AugmentedDataSourceF(factory.Factory):
    FACTORY_FOR = models.AugmentedDataSource

    augmented_source = factory.SubFactory(DatasourceModelF)
    name = "test-augmented-source"


class ColorMapF(factory.Factory):
    FACTORY_FOR = models.ColorMap

    name = "kleurprojectie"


class ColorFromLatestValueF(factory.Factory):
    FACTORY_FOR = models.ColorFromLatestValue

    augmented_source = factory.SubFactory(AugmentedDataSourceF)


class ColorMapLineF(factory.Factory):
    FACTORY_FOR = models.ColorMapLine

    colormap = factory.SubFactory(ColorMapF)
    minvalue = 0.0
    maxvalue = 10.0
    mininclusive = False
    maxinclusive = True
    color = "00ff00"


# Test classes


class TestDatasourceModel(TestCase):
    def test_has_unicode(self):
        self.assertTrue(unicode(DatasourceModelF.build()))

    def test_cache_script_is_due_if_not_run_yet(self):
        # Say it's 0:30 AM now and it hasn't run yet, it should
        dt = datetime.datetime.now().replace(hour=0, minute=30)

        self.assertTrue(DatasourceModelF.build(
                script_times_to_run_per_day=24,
                script_last_run_started=None,
                script_run_next_opportunity=False).cache_script_is_due(dt))

    def test_cache_script_is_due_if_last_run_was_earlier(self):
        """We have to run each hour, it's 1:05 am and the last run was at
        0:05 am."""
        dtnow = datetime.datetime.now().replace(hour=1, minute=5)
        dtlast = datetime.datetime.now().replace(hour=0, minute=5)

        self.assertTrue(DatasourceModelF.build(
                script_times_to_run_per_day=24,
                script_last_run_started=dtlast,
                script_run_next_opportunity=False).cache_script_is_due(dtnow))

    def test_cache_script_is_not_due_if_last_run_was_later(self):
        """It's 1:10am, the last run was at 1:05am."""
        dtnow = datetime.datetime.now().replace(hour=1, minute=10)
        dtlast = datetime.datetime.now().replace(hour=1, minute=5)

        self.assertFalse(DatasourceModelF.build(
                script_times_to_run_per_day=24,
                script_last_run_started=dtlast,
                script_run_next_opportunity=False).cache_script_is_due(dtnow))

    def test_cache_script_is_due_if_requested(self):
        dtnow = datetime.datetime.now().replace(hour=1, minute=10)
        dtlast = datetime.datetime.now().replace(hour=1, minute=5)

        self.assertTrue(DatasourceModelF.build(
                script_times_to_run_per_day=24,
                script_last_run_started=dtlast,
                script_run_next_opportunity=True).cache_script_is_due(dtnow))

    def test_cache_script_doesnt_run_if_0_times_per_day(self):
        dtnow = datetime.datetime.now().replace(hour=1, minute=10)
        dtlast = datetime.datetime.now().replace(hour=0, minute=5)

        self.assertFalse(DatasourceModelF.build(
                script_times_to_run_per_day=0,
                script_last_run_started=dtlast,
                script_run_next_opportunity=False).cache_script_is_due(dtnow))


class TestDatasourceLayer(TestCase):
    def test_has_unicode(self):
        self.assertTrue(unicode(DatasourceLayerF.build()))


class TestAugmentedDataSource(TestCase):
    def test_has_unicode(self):
        self.assertTrue(unicode(AugmentedDataSourceF.build()))


class TestColorMapLine(TestCase):
    def test_line_applies_if_value_between_min_and_max(self):
        cml = ColorMapLineF.build()
        color = cml.color_for(5.0)
        self.assertEquals(color, cml.color)

    def test_value_equal_to_min_doesnt_work_if_not_inclusive(self):
        cml = ColorMapLineF.build()
        color = cml.color_for(0.0)
        self.assertEquals(color, None)

    def test_value_equal_does_work_if_inclusive(self):
        cml = ColorMapLineF.build(mininclusive=True)
        color = cml.color_for(5.0)
        self.assertEquals(color, cml.color)

    def test_returns_none_if_max_below_min(self):
        cml = ColorMapLineF.build(maxvalue=0, minvalue=10)
        color = cml.color_for(5.0)
        self.assertEquals(color, None)

    def test_no_minvalue_works_like_infinity(self):
        cml = ColorMapLineF.build(minvalue=None, maxvalue=10)
        color = cml.color_for(5.0)
        self.assertEquals(color, cml.color)

    def test_no_maxvalue_works_like_infinity(self):
        cml = ColorMapLineF.build(minvalue=0, maxvalue=None)
        color = cml.color_for(5.0)
        self.assertEquals(color, cml.color)

    def test_neither_filled_always_true(self):
        cml = ColorMapLineF.build(minvalue=None, maxvalue=None)
        color = cml.color_for(5.0)
        self.assertEquals(color, cml.color)


class TestColorMap(TestCase):
    def test_has_unicode(self):
        self.assertTrue(unicode(ColorMapF.build()))

    def test_finds_correct_colormap_line(self):
        cm = ColorMapF.create()

        ColorMapLineF.create(
            minvalue=0, maxvalue=10, color="ff0000", colormap=cm)
        ColorMapLineF.create(
            minvalue=10, maxvalue=20, color="0000ff", colormap=cm)

        color = cm.color_for(15)
        self.assertEquals(color, "0000ff")

    def test_returns_default_if_not_found(self):
        cm = ColorMapF.create(defaultcolor="00ff00")

        ColorMapLineF.create(
            minvalue=0, maxvalue=10, color="ff0000", colormap=cm)
        ColorMapLineF.create(
            minvalue=10, maxvalue=20, color="0000ff", colormap=cm)

        color = cm.color_for(25)
        self.assertEquals(color, "00ff00")
