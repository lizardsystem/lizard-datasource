"""Tests for lizard_datasource.timeseries"""

import StringIO

import pandas
import pytz

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
        ts = timeseries.Timeseries({
                self.some_date: self.some_value})
        self.assertDataPresent(ts)

    def test_list_of_dicts_constructor(self):
        ts = timeseries.Timeseries([{
                    self.some_date: self.some_value
                    }])
        self.assertDataPresent(ts)

    def test_latest_returns_pandas_timeseries(self):
        ts = timeseries.Timeseries({self.some_date: self.some_value})
        latest = ts.latest()
        self.assertTrue(isinstance(latest, pandas.Series))
        self.assertEquals(len(latest), 1)
        self.assertEquals(latest[self.some_date], self.some_value)

    def test_data_returns_list_of_lists(self):
        ts = timeseries.Timeseries({self.some_date: self.some_value})
        self.assertEquals(ts.data(), [[self.some_date, self.some_value]])

    def test_timeseries_has_a_length(self):
        ts = timeseries.Timeseries({self.some_date: self.some_value})
        self.assertEquals(len(ts), 1)

    def test_two_timeseries_to_csv(self):
        dt1 = dates.utc(2014, 6, 24, 17, 31, 24)
        dt2 = dates.utc(2014, 6, 24, 17, 32, 24)
        dt3 = dates.utc(2014, 6, 24, 17, 33, 24)

        ts = timeseries.Timeseries([
            {dt1: 1.0, dt2: 2.0},
            {dt1: 3.0, dt3: 4.0}
            ])

        outfile = StringIO.StringIO()

        ts.to_csv(outfile, timezone=pytz.timezone('Europe/Amsterdam'))

        # Summer, so two hours difference with UTC
        self.assertEquals(outfile.getvalue(),
                          """Datum + tijd,data_0,data_1
2014-06-24 19:31,1.0,3.0
2014-06-24 19:32,2.0,
2014-06-24 19:33,,4.0
""")
