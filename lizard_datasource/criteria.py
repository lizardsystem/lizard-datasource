class Criterion(object):
    TYPE_SELECT = object()

    def __init__(self, identifier, description,
                 datatype=TYPE_SELECT, prerequisites=()):
        self._identifier = identifier
        self._description = description
        self._datatype = datatype
        self._prerequisites = prerequisites

    @property
    def identifier(self):
        return self._identifier

    @property
    def description(self):
        return self._description

    @property
    def datatype(self):
        return self._datatype

    @property
    def prerequisites(self):
        return self._prerequisites

    def __eq__(self, other):
        return getattr(other, '_identifier', None) == self._identifier

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._identifier)


class AppNameCriterion(Criterion):
    def __init__(self):
        self._identifier = 'appname'
        self._description = 'Application'
        self._datatype = Criterion.TYPE_SELECT
        self._prerequisites = ()
