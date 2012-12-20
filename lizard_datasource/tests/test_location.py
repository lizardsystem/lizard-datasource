"""Tests for lizard_datasource.location"""

from lizard_datasource import location

from django.test import TestCase


class TestLocation(TestCase):
    def test_to_dict_has_extra_args_too(self):
        l = location.Location(
            'identifier', 0.0, 1.0, somearg="whee")
        d = l.to_dict()
        self.assertEquals(d['identifier'], 'identifier')
        self.assertEquals(d['latitude'], 0.0)
        self.assertEquals(d['longitude'], 1.0)
        self.assertEquals(d['somearg'], "whee")
        self.assertTrue("color" not in d)

    def test_color_is_added_to_dict_too(self):
        l = location.Location(
            'identifier', 0.0, 1.0, color="ffffff", somearg="whee")
        d = l.to_dict()
        self.assertEquals(d['color'], 'ffffff')

    def test_description_returns_description(self):
        l = location.Location(
            'identifier', 0.0, 1.0, description="test")
        self.assertEquals(l.description(), "test")

    def test_otherwise_it_returns_name(self):
        l = location.Location(
            'identifier', 0.0, 1.0, name="test")
        self.assertEquals(l.description(), "test")

    def test_and_if_all_else_fails_it_returns_identifier(self):
        l = location.Location(
            'identifier', 0.0, 1.0)
        self.assertEquals(l.description(), "identifier")

    def test_has_unicode_and_it_contains_the_identifier(self):
        l = location.Location(
            'identifier', 0.0, 1.0)
        u = unicode(l)
        self.assertTrue('identifier' in u)

    def test_repr_is_unicode(self):
        l = location.Location(
            'identifier', 0.0, 1.0)
        self.assertEquals(unicode(l), repr(l))
