class Item(object):

    @property
    def name (self):
        try:
            return self._name
        except AttributeError:
            return ""

    @property
    def description(self):
        try:
            return self._description
        except AttributeError:
            return ""

    @property
    def id(self):
        try:
            return self._id
        except AttributeError:
            return ""