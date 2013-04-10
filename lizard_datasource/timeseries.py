"""Module for the Timeseries class. It is a wrapper around a pandas
timeseries."""

import logging
import pandas

from itertools import izip

from pandas import DataFrame

logger = logging.getLogger(__name__)


class Timeseries(object):
    def __init__(self, data):

        """
        Can be called with either:

        timeseries_dict, a dict with UTC datetimes as keys and floats
        as values.

        A list of such dicts."""

        if isinstance(data, dict):
            series = pandas.Series(data)
            self._dataframe = DataFrame({'data': series})
        else:
            self._dataframe = DataFrame(dict([
                        ('data_{0}'.format(i), series)
                        for i, series in enumerate(data)]))

    def add(self, timeseries):
        """Return a new Timeseries instance, with the columns from
        this one and the added one."""
        return Timeseries([
                self._dataframe[columnname]
                for columnname in self._dataframe.columns] + [
                timeseries._dataframe[columnname]
                for columnname in timeseries._dataframe.columns])

    @property
    def dataframe(self):
        return self._dataframe

    @property
    def timeseries(self):
        """Return the first of the series in dataframe"""
        return self._dataframe[self._dataframe.columns[0]].dropna()

    def dates(self):
        return self.timeseries.keys()

    def values(self):
        return list(self.timeseries)

    def latest(self):
        return self.timeseries.tail(1)

    def data(self):
        return [[key, value]
                for key, value in izip(self.dates(), self.values())]

    def __len__(self):
        return len(self.timeseries) if self.timeseries is not None else 0
