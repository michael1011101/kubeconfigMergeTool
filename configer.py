import os
import yaml

class BaseReader(object):
    name = ''
    value = ''

    def __init__(self, name, attr, value):
        self.name = name
        self.attr = attr
        self.value = value
        self.__dict = None
    
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if self.name == other.name and self.value == other.value:
            return True
        else:
            return False

    @property
    def dict(self):
        if self.__dict is None:
            self.__dict = {
                'name': self.name,
                self.attr: self.value
            }
        return self.__dict