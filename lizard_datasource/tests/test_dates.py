from django.test import TestCase

from lizard_datasource import dates

import datetime
import pytz


class TestToUtc(TestCase):
    def test_naive_date_becomes_utc(self):
        d = datetime.datetime(2012, 11, 13, 12, 00)
        u = dates.to_utc(d)

        self.assertRaises(TypeError, lambda: d == u)
        self.assertEquals(u.tzinfo, dates.UTC)

        self.assertEquals(d.utctimetuple(), u.timetuple())

    def test_other_timezone_becomes_utc(self):
        d = datetime.datetime(
            2012, 11, 13, 12, 00,
            tzinfo=pytz.timezone('Europe/Amsterdam'))
        u = dates.to_utc(d)
        self.assertEquals(u.tzinfo, dates.UTC)

    def test_utc_unchanged(self):
        d = datetime.datetime(
            2012, 11, 13, 12, 00,
            tzinfo=dates.UTC)
        u = dates.to_utc(d)
        self.assertEquals(d, u)


class TestUtc(TestCase):
    def test_same_result_as_manual(self):
        d = datetime.datetime(
            2012, 11, 13, 12, 00,
            tzinfo=dates.UTC)
        u = dates.utc(2012, 11, 13, 12, 00)
        self.assertEquals(d, u)
