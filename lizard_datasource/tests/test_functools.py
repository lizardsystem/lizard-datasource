"""Tests for lizard_datasource.functools"""

from django.test import TestCase

from lizard_datasource import functools


class TestMemoized(TestCase):
    def test_returns_same_object_for_same_input(self):
        @functools.memoize
        def helper(arg):
            return object()

        o1 = helper(1)
        o2 = helper(1)

        self.assertTrue(o1 is o2)

    def test_returns_different_object_for_different_input(self):
        @functools.memoize
        def helper(arg):
            return object()

        o1 = helper(1)
        o2 = helper(2)
        self.assertFalse(o1 is o2)
