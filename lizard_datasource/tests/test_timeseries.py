"""Tests for lizard_datasource.timeseries"""

import pandas

from django.test import TestCase

from lizard_datasource import dates
from lizard_datasource import timeseries


class TestTimeseries(TestCase):
    def setUp(self):
        self.some_date = dates.utc(2012, 12, 6, 17, 31, 24)
        self.some_value = 24.0

    # Helper methods, check whether the some_date / some_value was
    # correctly set in the timeseries
    def assertDataPresent(self, ts):
        self.assertEquals(ts.dates()[0], self.some_date)
        self.assertEquals(ts.values()[0], self.some_value)

    def test_dict_constructor(self):
        ts = timeseries.Timeseries(timeseries_dict={
                self.some_date: self.some_value})
        self.assertDataPresent(ts)

    def test_times_values_constructor(self):
        ts = timeseries.Timeseries(
            timeseries_times=(self.some_date,),
            timeseries_values=(self.some_value,))
        self.assertDataPresent(ts)

    def test_pandas_constructor(self):
        ts = timeseries.Timeseries(
            timeseries_pandas=pandas.Series({
                self.some_date: self.some_value}))
        self.assertDataPresent(ts)

    def test_otherwise_valueerror(self):
        self.assertRaises(ValueError, lambda: timeseries.Timeseries())

    def test_latest_returns_pandas_timeseries(self):
        ts = timeseries.Timeseries(
            timeseries_times=(self.some_date,),
            timeseries_values=(self.some_value,))
        latest = ts.latest()
        self.assertTrue(isinstance(latest, pandas.Series))
        self.assertEquals(len(latest), 1)
        self.assertEquals(latest[self.some_date], self.some_value)

    def test_data_returns_list_of_lists(self):
        ts = timeseries.Timeseries(
            timeseries_times=(self.some_date,),
            timeseries_values=(self.some_value,))
        self.assertEquals(ts.data(), [[self.some_date, self.some_value]])

    def test_timeseries_has_a_length(self):
        ts = timeseries.Timeseries(
            timeseries_times=(self.some_date,),
            timeseries_values=(self.some_value,))
        self.assertEquals(len(ts), 1)
