"""Module for the Location class. So what if that's Java-ish, it keeps
modules reasonably short and readable."""


class Location(object):
    def __init__(self, identifier, latitude, longitude, **kwargs):
        self.identifier = identifier
        self.latitude = latitude
        self.longitude = longitude
        self.extra_args = kwargs.copy()

    def to_dict(self):
        d = self.extra_args.copy()
        d['identifier'] = self.identifier
        d['latitude'] = self.latitude
        d['longitude'] = self.longitude

    def description(self):
        for key in ('description', 'name'):
            if key in self.extra_args:
                return self.extra_args[key]
            return self.identifier
