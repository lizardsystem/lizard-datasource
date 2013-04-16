"""Module for the Timeseries class. It is a wrapper around a pandas
DataFrame."""

import logging
import pandas

from itertools import izip

from pandas import DataFrame
from pandas import Series

logger = logging.getLogger(__name__)


class Timeseries(object):
    def __init__(self, data):

        """
        Can be called with either:

        A DataFrame. Preferred.

        timeseries_dict, a dict with UTC datetimes as keys and floats
        as values.

        A list of such dicts.

        This works like a pandas DataFrame, except we keep track of
        the order of column names."""

        if isinstance(data, DataFrame):
            self._dataframe = data
            self._columns = tuple(data.columns)
        elif isinstance(data, dict):
            series = Series(data)
            self._dataframe = DataFrame({'data': series})
            self._columns = ('data',)
        else:
            self._dataframe = DataFrame(dict([
                        ('data_{0}'.format(i), series)
                        for i, series in enumerate(data)]))
            self._columns = tuple(
                'data_{0}'.format(i) for i, series in enumerate(data))

    def add(self, timeseries):
        """Add the columns from timeseries to the dataframe of this
        timeseries."""
        self._dataframe = self._dataframe.combineAdd(timeseries._dataframe)
        self._columns = self.columns + timeseries.columns

    @property
    def dataframe(self):
        return self._dataframe

    @property
    def timeseries(self):
        """Return the first of the series in dataframe"""
        return self._dataframe[self._columns[0]].dropna()

    def get_series(self, columnname):
        return self._dataframe[columnname].dropna()

    @property
    def columns(self):
        return self._columns

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
        return len(self._dataframe) if self._dataframe is not None else 0
