"""What to test about management commands? I just mock the functions
they call and see if they commands run without error."""

import mock
from unittest import TestCase

from lizard_datasource.management.commands import cache_latest_values


class TestCacheLatestValues(TestCase):
    def test_run(self):
        command = cache_latest_values.Command()
        return_value = [mock.MagicMock()]
        with mock.patch(
            'lizard_datasource.datasource.datasources_from_entrypoints',
            return_value=return_value) as mocked1:
            with mock.patch('lizard_datasource.scripts.cache_latest_values'
                            ) as mocked2:
                command.handle()
                self.assertTrue(mocked1.called)
                self.assertTrue(mocked2.called)
                mocked2.assert_called_with(return_value[0])
