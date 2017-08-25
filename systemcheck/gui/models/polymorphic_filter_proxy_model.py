from PyQt5 import QtWidgets, QtCore, QtGui

class PolyMorphicFilterProxyModel(QtCore.QSortFilterProxyModel):


    def __init__(self, filterClasses:list):
        super().__init__()
        self.__filterClasses = filterClasses


    def filterAcceptsRow(self, rowNr:int, parent:QtCore.QModelIndex):

        model = self.sourceModel()
        index = model.index(rowNr, self.filterKeyColumn(), parent)

        node=index.internalPointer()

        if type(node) in self.__filterClasses:
            return True
        return False

