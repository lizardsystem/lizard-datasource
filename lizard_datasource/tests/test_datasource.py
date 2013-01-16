import mock

from unittest import TestCase

from lizard_datasource import datasource
from lizard_datasource import criteria


class TestChoicesMade(TestCase):
    def test_init_with_json(self):
        cm = datasource.ChoicesMade(json="""{"test": "value"}""")
        self.assertTrue('test' in cm)

    def test_init_with_dict(self):
        cm = datasource.ChoicesMade(dict={"test": "value"})
        self.assertTrue('test' in cm)

    def test_init_with_kwargs(self):
        cm = datasource.ChoicesMade(test="value")
        self.assertTrue('test' in cm)

    def test_init_dict_and_json_arent_special_if_not_used_alone(self):
        cm = datasource.ChoicesMade(test="value", dict="whee")
        self.assertTrue('dict' in cm)
        cm = datasource.ChoicesMade(test="value", json="whee")
        self.assertTrue('json' in cm)

    def test_getitem(self):
        cm = datasource.ChoicesMade(test="value")
        self.assertEquals(cm['test'], 'value')

    def test_get_returns_option(self):
        cm = datasource.ChoicesMade(test="value")
        self.assertEquals(cm.get('test'), 'value')

    def test_get_returns_default(self):
        cm = datasource.ChoicesMade()
        self.assertEquals(cm.get('test', 'value'), 'value')

    def test_get_default_default_is_none(self):
        cm = datasource.ChoicesMade()
        self.assertEquals(cm.get('test'), None)

    def test_add_returns_new_choicesmade(self):
        cm = datasource.ChoicesMade()
        cm2 = cm.add("test", "value")
        self.assertFalse(cm is cm2)

    def test_add_contains_old_and_new_values(self):
        cm = datasource.ChoicesMade(test="value")
        cm = cm.add("test2", "alsovalue")
        self.assertEquals(cm['test'], 'value')
        self.assertEquals(cm['test2'], 'alsovalue')

    def test_add_criterion_option(self):
        cm = datasource.ChoicesMade()
        criterion = criteria.Criterion(
            identifier="test", description="Some test criterion")
        option = criteria.Option(
            identifier="value", description="Some test value")

        cm = cm.add_criterion_option(criterion, option)
        self.assertEquals(cm.get('test'), 'value')

    def test_forget_returns_new(self):
        cm = datasource.ChoicesMade(test="value")
        cm2 = cm.forget("test")
        self.assertFalse(cm is cm2)

    def test_forget_removes_value(self):
        cm = datasource.ChoicesMade(test="value")
        cm = cm.forget("test")
        self.assertFalse("test" in cm)

    def test_forget_silent_if_key_doesnt_exist(self):
        cm = datasource.ChoicesMade()
        cm.forget("test")

    def test_json_sorts_keys(self):
        cm = datasource.ChoicesMade(test="value", a="b")
        self.assertEquals(cm.json(),
                          """{"a": "b", "test": "value"}""")
        cm = datasource.ChoicesMade(a="value", b="value")

    def test_unicode_gives_useful_repr(self):
        cm = datasource.ChoicesMade(test="value")
        from lizard_datasource.datasource import ChoicesMade
        ChoicesMade  # pyflakes
        cm2 = eval(unicode(cm))
        self.assertEquals(cm.json(), cm2.json())

    def test_repr_gives_useful_repr(self):
        cm = datasource.ChoicesMade(test="value")
        from lizard_datasource.datasource import ChoicesMade
        ChoicesMade  # pyflakes
        cm2 = eval(repr(cm))
        self.assertEquals(cm.json(), cm2.json())

    def test_we_can_loop_over_keys(self):
        cm = datasource.ChoicesMade(a="value", b="value")
        i = iter(cm)
        self.assertEquals(i.next(), "a")
        self.assertEquals(i.next(), "b")
        self.assertRaises(StopIteration, lambda: i.next())

    def test_items_returns_items_list(self):
        cm = datasource.ChoicesMade(a="value", b="value")
        l = cm.items()

        self.assertTrue(isinstance(l, list))
        self.assertEquals(len(l), 2)
        self.assertTrue(("a", "value") in l)
        self.assertTrue(("b", "value") in l)


class TestCombinedDatasource(TestCase):
    pass


class TestDataSourceFunction(TestCase):
    def test_if_there_are_no_datasources_returns_none(self):
        with mock.patch('lizard_datasource.datasource.get_datasources',
                        return_value=[]):
            self.assertEquals(datasource.datasource(), None)

    def test_if_there_is_one_datasource_it_is_returned(self):
        m = object()
        with mock.patch('lizard_datasource.datasource.get_datasources',
                        return_value=[m]):
            self.assertTrue(datasource.datasource() is m)

    def test_a_combined_datasource_is_returned(self):
        m1, m2 = object(), object()
        with mock.patch('lizard_datasource.datasource.get_datasources',
                        return_value=[m1, m2]):
            self.assertTrue(isinstance(
                    datasource.datasource(),
                    datasource.CombinedDataSource))
