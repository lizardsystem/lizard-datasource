from unittest import TestCase

from lizard_datasource import criteria


class TestCriterion(TestCase):
    def test_trivial_constructor_works(self):
        criterion = criteria.Criterion("test", "this is a test")
        self.assertEquals(criterion.identifier, "test")
        self.assertEquals(criterion.description, "this is a test")
        self.assertEquals(criterion.datatype, criteria.Criterion.TYPE_SELECT)
        self.assertEquals(criterion.prerequisites, ())

    def test_passing_datatype_works(self):
        criterion = criteria.Criterion(
            "test", "this is a test",
            datatype=criteria.Criterion.TYPE_TREE)
        self.assertEquals(criterion.datatype, criteria.Criterion.TYPE_TREE)

    def test_passing_preqreqs_works(self):
        criterion = criteria.Criterion(
            "test", "this is a test",
            prerequisites=("some identifier",))
        self.assertEquals(criterion.prerequisites, ("some identifier",))

    def test_criteria_with_same_identifiers_are_equal(self):
        criterion1 = criteria.Criterion("test", "some string")
        criterion2 = criteria.Criterion("test", "some other string")
        self.assertEquals(criterion1, criterion2)

    def test_criteria_with_different_identifiers_are_not_equal(self):
        criterion1 = criteria.Criterion("test1", "some string")
        criterion2 = criteria.Criterion("test2", "some other string")
        self.assertNotEquals(criterion1, criterion2)

    def test_criteria_can_be_placed_in_sets_same_ids_same_in_set(self):
        criterion1 = criteria.Criterion("test", "some string")
        criterion2 = criteria.Criterion("test", "some other string")
        s = set((criterion1, criterion2))
        self.assertEquals(len(s), 1)

    def test_criteria_in_set_different_ids_different_in_set(self):
        criterion1 = criteria.Criterion("test1", "some string")
        criterion2 = criteria.Criterion("test2", "some other string")
        s = set((criterion1, criterion2))
        self.assertEquals(len(s), 2)


class TestOption(TestCase):
    def test_if_option_is_hashable(self):
        option1 = criteria.Option(
            identifier="some_identifier",
            description="Some description.")
        d = {option1: 3}
        option2 = criteria.Option(
            identifier="some_identifier",
            description="Some description.")
        self.assertEquals(d.get(option2), 3)


class TestOptionList(TestCase):
    def test_we_can_initialize_an_empty_optionlist(self):
        ol = criteria.OptionList(())
        self.assertEquals(len(ol), 0)
        self.assertFalse(ol.is_option_tree)
        self.assertTrue(ol.is_option_list)

    def test_has_unicode(self):
        ol = criteria.OptionList([
                criteria.Option("string1", "string2")])
        self.assertTrue(unicode(ol))

    def test_len_works(self):
        ol = criteria.OptionList((
                criteria.Option("test", "test"),
                criteria.Option("test2", "test2")))
        self.assertEquals(len(ol), 2)

    def test_only_option_does_return_it(self):
        option = criteria.Option("test", "test")
        ol = criteria.OptionList((option,))
        self.assertTrue(ol.only_option() is option)

    def test_empty_is_false(self):
        ol = criteria.OptionList(())
        self.assertFalse(ol)

    def test_otherwise_true(self):
        ol = criteria.OptionList((
                criteria.Option("test", "test"),))
        self.assertTrue(ol)

    def test_only_option_raises(self):
        ol = criteria.OptionList(())
        self.assertRaises(ValueError, lambda: ol.only_option())

    def test_iter_options_works(self):
        op1 = criteria.Option("test1", "test1")
        op2 = criteria.Option("test2", "test2")
        ol = criteria.OptionList([op1, op2])

        i = ol.iter_options()
        self.assertTrue(i.next() is op1)
        self.assertTrue(i.next() is op2)
        self.assertRaises(StopIteration, lambda: i.next())

    def test_add_empty_options_returns_original(self):
        op1 = criteria.Option("test1", "test1")
        op2 = criteria.Option("test2", "test2")
        ol = criteria.OptionList([op1, op2])
        self.assertTrue(ol is ol.add(criteria.EmptyOptions()))

    def test_add_works(self):
        op1 = criteria.Option("test1", "test1")
        op2 = criteria.Option("test2", "test2")
        ol1 = criteria.OptionList([op1])
        ol2 = criteria.OptionList([op2])

        ol3 = ol1.add(ol2)
        self.assertEquals(len(ol3), 2)
        self.assertFalse(ol3 is ol1)


class TestOptionTree(TestCase):
    def test_no_arguments_gives_empty_option_tree(self):
        ot = criteria.OptionTree()
        self.assertTrue(ot.is_option_tree)
        self.assertFalse(ot.is_option_list)
        self.assertEquals(len(ot), 0)
        self.assertFalse(ot.has_description)
        self.assertFalse(ot.is_leaf)

    def test_unicode_empty(self):
        ot = criteria.OptionTree()
        self.assertTrue(unicode(ot))

    def test_unicode_leaf(self):
        option = criteria.Option("test", "test")
        ot = criteria.OptionTree(option=option)
        self.assertTrue(unicode(ot))

    def test_unicode_children(self):
        option = criteria.Option("test", "test")
        leaf = criteria.OptionTree(option=option)
        ot = criteria.OptionTree(children=(leaf,))
        self.assertTrue(unicode(ot))

    def test_len(self):
        option = criteria.Option("test", "test")
        leaf1 = criteria.OptionTree(option=option)
        leaf2 = criteria.OptionTree(option=option)
        ot = criteria.OptionTree(children=(leaf1, leaf2))
        self.assertEquals(len(ot), 2)

    def test_iteration(self):
        option = criteria.Option("test", "test")
        leaf1 = criteria.OptionTree(option=option)
        leaf2 = criteria.OptionTree(option=option)
        ot = criteria.OptionTree(children=(leaf1, leaf2))

        i = 0
        for opt in ot.iter_options():
            i += 1
            self.assertTrue(opt is option)
        self.assertEquals(i, 2)

    def test_only_option(self):
        option = criteria.Option("test", "test")
        leaf = criteria.OptionTree(option=option)
        ot = criteria.OptionTree(children=(leaf,))
        self.assertTrue(ot.only_option() is option)

    def test_only_option_raises(self):
        ot = criteria.OptionTree(())
        self.assertRaises(ValueError, lambda: ot.only_option())

    def test_add(self):
        option1 = criteria.Option("test1", "test1")
        option2 = criteria.Option("test2", "test2")
        leaf1 = criteria.OptionTree(option=option1)
        leaf2 = criteria.OptionTree(option=option2)
        ot1 = criteria.OptionTree(children=(leaf1,))
        ot2 = criteria.OptionTree(children=(leaf2,))

        ot3 = ot1.add(ot2)
        self.assertEquals(len(ot3), 2)
        self.assertEquals(len(ot3.children), 2)
        self.assertTrue(ot3.children[0] is ot1)
        self.assertTrue(ot3.children[1] is ot2)

        i = ot3.iter_options()
        self.assertTrue(i.next() is option1)
        self.assertTrue(i.next() is option2)
        self.assertRaises(StopIteration, lambda: i.next())

    def test_add_empty_options_returns_self(self):
        option = criteria.Option("test1", "test1")
        leaf = criteria.OptionTree(option=option)
        ot = criteria.OptionTree(children=(leaf,))
        self.assertTrue(ot is ot.add(criteria.EmptyOptions()))


class TestEmptyOptions(TestCase):
    def test_emptyoptions_is_neither_a_list_nor_a_tree(self):
        eo = criteria.EmptyOptions()
        self.assertFalse(eo.is_option_tree)
        self.assertFalse(eo.is_option_list)

    def test_emptyoptions_has_no_description(self):
        eo = criteria.EmptyOptions()
        self.assertEquals(eo.description, None)

    def test_emptyoptions_length_is_0(self):
        eo = criteria.EmptyOptions()
        self.assertEquals(len(eo), 0)

    def test_iter_options_works_but_immediately_stops(self):
        eo = criteria.EmptyOptions()
        self.assertEquals(list(eo.iter_options()), [])

    def test_add_returns_other_options_object(self):
        eo = criteria.EmptyOptions()
        something = object()
        self.assertEquals(eo.add(something), something)

    def test_emptyoptions_is_false(self):
        eo = criteria.EmptyOptions()
        self.assertFalse(eo)
