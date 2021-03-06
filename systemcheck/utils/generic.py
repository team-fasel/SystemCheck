# -*- coding: utf-8 -*-

""" Generic Utiltities

This file contains some generic utilities that are used across the application.



"""

# define authorship information
__authors__     = ['Lars Fasel']
__author__      = ','.join(__authors__)
__credits__     = []
__copyright__   = 'Copyright (c) 2017'
__license__     = 'GNU AGPLv3'

# maintanence information
__maintainer__  = 'Lars Fasel'
__email__       = 'systemcheck@team-fasel.com'

from configparser import ConfigParser
import sys
import os
import datetime
import re

def main_is_frozen():
    """ Determines whether scripts are executed using pyInstaller or actual scripts.
    :return: True if using py2exe or pyinstaller or False if using scripts"""

    return (hasattr(sys, '_MEIPASS'))

def get_absolute_path(relative_path):
    """ Returns the absolute path for the relative path taking into account the freeze status """

    if main_is_frozen():
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(sys.argv[0]), relative_path)

def get_absolute_systemcheck_path(relative_path=None):
    """ Returns the absolute path for the relative path taking into account the freeze status """
    import systemcheck
    if main_is_frozen():
        path1=sys._MEIPASS
    else:
        path1=os.path.dirname(systemcheck.__file__)

    if relative_path is None:
        return path1
    return os.path.join(path1, relative_path)

def get_lower_interval(parameters:dict, basetime):
    """ Calculate the lower date for the success_count function """
    if parameters.get('INTERVALTYPE') == 'D':
        dateFrom = basetime + datetime.timedelta(days=-int(parameters['INTERVAL']))
    elif parameters['INTERVALTYPE'] == 'H':
        dateFrom = basetime + datetime.timedelta(hours=-int(parameters['INTERVAL']))
    elif parameters['INTERVALTYPE'] == 'S':
        dateFrom = basetime + datetime.timedelta(seconds=-int(parameters['INTERVAL']))
    elif parameters['INTERVALTYPE'] == 'W':
        dateFrom = basetime + datetime.timedelta(weeks=-int(parameters['INTERVAL']))
    elif parameters['INTERVALTYPE'] == 'Y':
        dateFrom = basetime + datetime.timedelta(years=-int(parameters['INTERVAL']))

    return dateFrom


def get_user_attributes(cls, exclude_methods:bool=True)-> list:
    """ Get Attributes of a Class

    :param cls: Class Object
    :param exclude_methods: Exclude Methods
    :return:
    """
    base_attrs = dir(type('dummy', (object,), {}))
    this_cls_attrs = dir(cls)
    res = []
    for attr in this_cls_attrs:
        if base_attrs.count(attr) or (callable(getattr(cls,attr)) and exclude_methods):
            continue
        res += [attr]
    return res

class Result(object):
    '''
    Alternative implementation for error handling.

    This class contains the result of a successful execution.

    '''

    def __init__(self, message=None, data=None, fail=False):
        self.__data = data
        self.__message = message
        self.fail = fail

    @property
    def result(self):
        return {'data': self.__data, 'message': self.__message, 'fail': self.fail}

    @property
    def message(self):
        return self.__message

    @property
    def data(self):
        return self.__data

    def __repr__(self):
        string = '< {}: message: {}, data: {}, fail: {}'.format(self.__class__.__name__, self.message, self.data, self.fail)
        return string


class Fail(Result):
    """
    Failure Object
    """

    def __init__(self, message=None, data=None):
        fail = True
        super().__init__(message, data, fail)

def underscore_to_camelcase(value):
    """ Convert the value camel_case to CamelCase """
    def camelcase():
        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(c.next()(x) if x else '_' for x in value.split("_"))

def camelcase_to_underscore(value):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()