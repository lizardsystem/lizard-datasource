from unittest import TestCase

from lizard_datasource import dummy_datasource


class TestDummyDatasource(TestCase):
    def setUp(self):
        self.ds = dummy_datasource.DummyDataSource()

    def test_has_two_criteria(self):
        criteria = self.ds.criteria()
        self.assertEquals(len(criteria), 2)

    def test_has_option_for_first_criterion(self):
        criteria = self.ds.criteria()
        for criterion in criteria:
            if criterion.identifier == 'appname':
                break

        options = self.ds.options_for_criterion(criterion)
        self.assertTrue(options.is_option_list)
        self.assertEquals(len(options), 1)

