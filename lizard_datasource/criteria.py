"""Defines classes for criteria (Criterion class) and options (Option,
Options, OptionList, OptionTree)."""


class Criterion(object):
    TYPE_SELECT = object()
    TYPE_TREE = object()

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

    def __unicode__(self):
        return "Criterion(identifier={0}, description={1})".format(
            self._identifier, self._description)


class AppNameCriterion(Criterion):
    def __init__(self):
        self._identifier = 'appname'
        self._description = 'Application'
        self._datatype = Criterion.TYPE_SELECT
        self._prerequisites = ()


class Option(object):
    """An option has an identifier and a description."""
    def __init__(self, identifier, description):
        self.identifier = identifier
        self.description = description

    def __unicode__(self):
        return "Option({0}, {1})".format(self.identifier, self.description)


class Options(object):
    @property
    def is_option_list(self):
        return False

    @property
    def is_option_tree(self):
        return False


class OptionList(Options):
    def __init__(self, options):
        """Needs an iterable of Options."""
        self.options = list(options)

    @property
    def is_option_list(self):
        return True

    def __unicode__(self):
        return "OptionList(...)"

    def __len__(self):
        return len(self.options)

    def __nonzero__(self):
        return bool(self.options)

    def iter_options(self):
        return iter(self.options)

    def only_option(self):
        if len(self.options) != 1:
            raise ValueError("only_option called when len isn't 1.")
        return self.options[0]

    def add(self, option_list):
        if len(option_list) > 0:
            return OptionList(self.options + option_list.options)
        else:
            return self


class OptionTree(Options):
    def __init__(self, description=None, children=None, option=None):
        """Must be called with either children or an option. The
        description is only used if there is no option."""
        self.children = list(children) if children is not None else []
        self.option = option
        self.description = description

    @property
    def is_option_tree(self):
        return True

    @property
    def has_description(self):
        return self.description is not None

    @property
    def is_leaf(self):
        return self.option is not None

    def __unicode__(self):
        if self.option:
            return "OptionTree(option={0})".format(unicode(self.option))
        return "OptionTree({0}, [{1}])".format(
            self.description or "None",
            ", ".join(unicode(c) for c in self.children))

    def __len__(self):
        if self.is_leaf:
            return 1
        else:
            return sum(len(node) for node in self.children)

    def iter_options(self):
        if self.is_leaf:
            yield self.option
        else:
            for node in self.children:
                for option in node.iter_options():
                    yield option

    def only_option(self):
        if len(self) != 1:
            raise ValueError("only_option called when len isn't 1.")
        return list(self.iter_options())[0]

    def add(self, option_tree):
        if len(option_tree) > 0:
            return OptionTree(children=[self, option_tree])
        else:
            return self


class EmptyOptions(Options):
    """Represents an empty set of options. This is not the same as
    OptionList([]) because we must be able to add other types of
    options (e.g. OptionTree) to it as well."""
    def __len__(self):
        return 0

    @property
    def description(self):
        return None

    def iter_options(self):
        return iter(())

    def add(self, options):
        return options
