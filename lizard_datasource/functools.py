"""Useful decorators and such."""

# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

from functools import wraps


def memoize(f):
    """Remember the results of function f and immediately return a
    remembered result if it's called with the same arguments again."""
    memo_cache = dict()

    @wraps(f)
    def memoed(*args, **kwargs):
        # Construct a key to use in the memo_cache
        key = (tuple(args), tuple(kwargs.items()))

        if key not in memo_cache:
            memo_cache[key] = f(*args, **kwargs)

        return memo_cache[key]

    return memoed
