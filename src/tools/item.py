class Item(object):
    """
    Some things common to AbstractSensor,AbstractController and AbstractHardware
    """
    @property
    def name (self):
        try:
            return self._name
        except AttributeError,e:
            print e
            return ""

    @property
    def description(self):
        try:
            return self._description
        except AttributeError,e:
            print e
            return ""

    @property
    def id(self):
        try:
            return self._id
        except AttributeError,e:
            print e
            return ""
    @id.setter 
    def id(self,value):
        self._id = value

    @property
    def code(self):
        try:
            return self._code
        except AttributeError,e:
            print e
            return ""