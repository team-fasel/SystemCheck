# -*- coding: utf-8 -*-

""" Generic UI Models


"""

# define authorship information
__authors__ = ['Lars Fasel']
__author__ = ','.join(__authors__)
__credits__ = []
__copyright__ = 'Copyright (c) 2017'
__license__ = 'GNU AGPLv3'



import logging
from typing import Any
from sqlalchemy_utils.functions import get_type
from systemcheck import models
from PyQt5 import QtCore, QtGui, QtWidgets
from pprint import pformat


class SettingsModel(QtCore.QAbstractItemModel):

    def __init__(self, abstractItem):
        super().__init__()
        self.logger = logging.getLogger('{}.{}'.format(__name__, self.__class__.__name__))
        self._abstractItem = abstractItem


    def columnCount(self, parent=None, *args, **kwargs)->int:

        return self._abstractItem._qt_column_count()

    def rowCount(self, parent=None, *args, **kwargs)->int:

        return 1

    def data(self, index: QtCore.QModelIndex, role:int=QtCore.Qt.DisplayRole)->Any:
        column = index.column()
        if not index.isValid():
            return False

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self._abstractItem._qt_data_colnr(index.column())


    def flags(self, index:QtCore.QModelIndex)->int:
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def setData(self, index:QtCore.QModelIndex, value: Any, role=QtCore.Qt.EditRole)->bool:
        """ setData Method to make the model modifiable """

        if index.isValid():
            if role == QtCore.Qt.EditRole:
                self._abstractItem._qt_set_value_by_colnr(index.column(), value)

            return True
        return False

    def index(self, row:int, column:int, parent=None)->QtCore.QModelIndex:

        index = self.createIndex(0, column, QtCore.QModelIndex())

        return index

    def parent(self):
        return QtCore.QModelIndex()

class SettingsTableModel(QtCore.QAbstractTableModel):

    def __init__(self, abstractItem):
        super().__init__()
        self.logger = logging.getLogger('{}.{}'.format(__name__, self.__class__.__name__))
        self._abstractItem = abstractItem


    def columnCount(self, parent=None, *args, **kwargs)->int:

        return 2

    def rowCount(self, parent=None, *args, **kwargs)->int:

        return self._abstractItem._qt_column_count()

    def data(self, index: QtCore.QModelIndex, role: int)->Any:

        if not index.isValid():
            return False

        table_column = index.column()
        table_row=index.row()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:

            if table_column==0:
                # The Label
                table_row=self._abstractItem.__qtmap__[table_row]
                return table_row.info.get('qt_label')
            elif table_column==1:
                # The actual value
                name=self._abstractItem.__qtmap__[table_row].name
                if name is None:
                    self.logger.error('No Name configured in model. Column: %s', pformat(self._abstractItem.__qtmap__[table_row]))
                value = getattr(self._abstractItem, name)
                return value

            return self._abstractItem._qt_data_colnr(index.column())

        if role == QtCore.Qt.FontRole and index.column()==0:
            font = QtGui.QFont()
            font.setBold(True)
            return font

    def flags(self, index:QtCore.QModelIndex)->int:

        flags = QtCore.Qt.ItemIsEnabled
        if index.column() != 0:
            flags= flags | QtCore.Qt.ItemIsEditable

        return flags

    def setData(self, index:QtCore.QModelIndex, value: Any, role=QtCore.Qt.EditRole)->bool:
        """ setData Method to make the model modifiable """

        if not index.isValid():
            return False

        if role == QtCore.Qt.EditRole:
            table_column=index.column()
            table_row=index.row()

            if table_column==1:
                self._abstractItem._qt_set_value_by_colnr(table_row, value)
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role=None):
        if role==QtCore.Qt.DisplayRole:
            if section==0:
                return 'Parameter'
            elif section==1:
                return 'Value'

    def parent(self):
        return QtCore.QModelIndex()
