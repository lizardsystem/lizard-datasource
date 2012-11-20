"""Module for the Location class. So what if that's Java-ish, it keeps
modules reasonably short and readable."""


class Location(object):
    def __init__(self, identifier, latitude, longitude, color=None, **kwargs):
        self._identifier = identifier
        self._latitude = latitude
        self._longitude = longitude
        self._extra_args = kwargs.copy()
        self.color = color

    def to_dict(self):
        d = self.extra_args.copy()
        d['identifier'] = self.identifier
        d['latitude'] = self.latitude
        d['longitude'] = self.longitude

    def description(self):
        for key in ('description', 'name'):
            if key in self._extra_args:
                return self._extra_args[key]
            return self.identifier

    @property
    def identifier(self):
        return self._identifier

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    def __unicode__(self):
        return "Location '{0}' ({1}, {2})".format(
            self.identifier, self.latitude, self.longitude)
