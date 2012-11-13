"""Date utilities. Internally we ALWAYS work with UTC datetimes."""

import datetime
import pytz

UTC = pytz.utc


def to_utc(datetime_object):
    """If datetime is naive, assume it is UTC and turn it into a UTC
    date. If it has an associated timezone, translate to UTC."""

    if datetime_object.utcoffset() is None:
        return UTC.localize(datetime_object)
    else:
        return datetime_object.astimezone(UTC)


def utc(*args, **kwargs):
    """Pass args and kwargs to datetime.datetime, and turn it into a
    UTC datetime afterwards."""
    return to_utc(datetime.datetime(*args, **kwargs))
