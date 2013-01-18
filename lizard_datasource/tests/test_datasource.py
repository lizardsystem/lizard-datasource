import mock

from unittest import TestCase

from lizard_datasource import datasource
from lizard_datasource import dummy_datasource
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
    def test_has_identifier(self):
        ds = datasource.CombinedDataSource([
                dummy_datasource.DummyDataSource(),
                dummy_datasource.DummyDataSource()
                ])
        self.assertTrue(ds.identifier)

    def test_has_description(self):
        ds = datasource.CombinedDataSource([
                dummy_datasource.DummyDataSource(),
                dummy_datasource.DummyDataSource()
                ])
        self.assertTrue(ds.description)

    def test_originating_app_is_lizard_datasource(self):
        # Change the return value of the dummy data source, so that it is
        # clear that the originating app is set by the combined datasource
        with mock.patch(
          'lizard_datasource.dummy_datasource.DummyDataSource.originating_app',
            return_value="changed"):
            ds = datasource.CombinedDataSource([
                    dummy_datasource.DummyDataSource(),
                    dummy_datasource.DummyDataSource()
                    ])
            self.assertEquals(ds.originating_app, 'lizard_datasource')

    def test_datasource_model_raises_exception(self):
        # The combined data source has no state, so if something tries to use
        # its datasource model, that's an error
        self.assertRaises(
            ValueError,
            lambda: datasource.CombinedDataSource([]).datasource_model)

    def test_is_visible(self):
        # Since it can't be turned off by changing the datasource model, and it
        # should always be there, visible should always be True.
        self.assertTrue(datasource.CombinedDataSource([]).visible)

    def test_datasource_layer_raises_exception(self):
        # The combined data source has no state, so if something tries to use
        # its datasource model, that's an error
        self.assertRaises(
            ValueError,
            lambda: datasource.CombinedDataSource([]).datasource_layer)

    def test_set_choices_sets_in_all_data_sources(self):
        cm = datasource.ChoicesMade()
        dm = dummy_datasource.DummyDataSource()

        combined = datasource.CombinedDataSource([dm])
        combined.set_choices_made(cm)
        self.assertEquals(dm.get_choices_made(), cm)

    def test_get_choices_returns_value_set_with_set(self):
        cm = datasource.ChoicesMade()
        dm = dummy_datasource.DummyDataSource()

        combined = datasource.CombinedDataSource([dm])
        combined.set_choices_made(cm)
        self.assertEquals(combined.get_choices_made(), cm)

    def test_criteria_returns_combination(self):
        # dm1 and dm2 have the same criteria
        dm1 = dummy_datasource.DummyDataSource()
        dm2 = dummy_datasource.DummyDataSource()

        # combined should return a list combining both
        combined = datasource.CombinedDataSource([dm1, dm2])

        criteria = combined.criteria()
        self.assertEquals(len(criteria), len(dm1.criteria()))

        for criterion in dm1.criteria():
            self.assertTrue(criterion in criteria)
        for criterion in dm2.criteria():
            self.assertTrue(criterion in criteria)

    def test_options_for_criterion(self):
        # Construct two datasources returning different option lists.
        option1 = criteria.Option("test1", "test1")
        option2 = criteria.Option("test2", "test2")
        ol1 = criteria.OptionList([option1])
        ol2 = criteria.OptionList([option2])

        options = [ol1, ol2]

        def side_effect(*args, **kwargs):
            return options.pop(0)

        with mock.patch(
  'lizard_datasource.dummy_datasource.DummyDataSource.options_for_criterion',
            side_effect=side_effect):
            ds1 = dummy_datasource.DummyDataSource()
            ds2 = dummy_datasource.DummyDataSource()

            cds = datasource.CombinedDataSource([ds1, ds2])

            self.assertEquals(
                len(cds.options_for_criterion(mock.MagicMock())), 2)


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
