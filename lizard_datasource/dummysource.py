"""Implementation of a dummy data source. It's never used for real
(not connected to any entry points) but test case classes can use the
@uses_dummy_datasource decorator to make sure they use only the dummy
data source(s)."""

import mock

class DummyDataSource(object):
    pass


def dummy_datasource_factory():
    """Return a tuple of data source instances. Currently we return just one."""
    return (DummyDataSource(),)


class DummyDatasourceEntryPoint(object):
    """Entrypoints have two things we use: a name attribute and a load()
    method that returns a factory function."""

    name = 'dummy data source'

    def load(self):
        return dummy_datasource_factory


DUMMY_ENTRYPOINT = DummyDatasourceEntryPoint()


def uses_dummy_datasource(testcase):
    """A TestCase decorator that makes sure the only data source found is the
    Dummy datasource."""

    return mock.patch(
        target='lizard_datasource.datasource.datasource_entrypoints',
        return_value=(DUMMY_ENTRYPOINT,))(testcase)
