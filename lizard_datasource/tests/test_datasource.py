import json

from unittest import TestCase

from lizard_datasource import datasource


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

    def test_add_returns_new_choicesmade(self):
        cm = datasource.ChoicesMade()
        cm2 = cm.add("test", "value")
        self.assertFalse(cm is cm2)

    def test_add_contains_old_and_new_values(self):
        cm = datasource.ChoicesMade(test="value")
        cm = cm.add("test2", "alsovalue")
        self.assertEquals(cm['test'], 'value')
        self.assertEquals(cm['test2'], 'alsovalue')

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

