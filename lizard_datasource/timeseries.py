"""Module for the Timeseries class. It is a wrapper around a pandas
timeseries."""

import pandas


class Timeseries(object):
    def __init__(
        self,
        timeseries_dict=None,
        timeseries_pandas=None,
        timeseries_times=None, timeseries_values=None):
        """
        Can be called with either:

        timeseries_dict, a dict with UTC datetimes as keys and floats
        as values.

        timeseries_pandas, a pandas timeseries.

        timeseries_times and timeseries_values, two iterables of equal
        length containing the times (UTC datetimes) and values of the
        timeseries."""
        if timeseries_dict is not None:
            self.timeseries = pandas.Series(timeseries_dict)
        elif timeseries_pandas is not None:
            self.timeseries = timeseries_pandas.copy()
        elif timeseries_times is not None and timeseries_values is not None:
            self.timeseries = pandas.Series(
                index=timeseries_times, data=timeseries_values)
        else:
            raise ValueError("Timeseries.__init__ called incorrectly.")

    def dates(self):
        return self.timeseries.keys()

    def values(self):
        return list(self.timeseries)
