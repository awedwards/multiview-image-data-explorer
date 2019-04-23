"""
@author: Austin Edwards

Data model for segmentation label and color display in main gui window

"""

import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal

class SegmentationClassTableModel(QAbstractTableModel):

    def __init__(self, data, header, parent=None):

        QAbstractTableModel.__init__(self, parent)
        self._data = data
        self._header = header
        self._color_table = dict()
        self._class_loc = dict()

    class_table_update = pyqtSignal(int)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        
        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()

            if index.column() == 1:
                # sets user provided class label
                self._data[i][1] = self._color_table[i][0]

            return '{0}'.format(self._data[i][j])
        elif role == QtCore.Qt.BackgroundColorRole:
            if index.column() == 0:
                # sets user provided class color
                return self._color_table[index.row()][1]
        else:
            return QtCore.QVariant()

    def flags(self, index):
        """ Enables editing of class label column in data table """
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)

    def headerData(self, section, orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._header[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def populate_class_table(self, color_table):
        """ sets the whole data table """
        self._color_table = color_table

        data = []
        for v in color_table.values():
            data.append(["", v[0]])

        self.layoutAboutToBeChanged.emit()
        self._data = data
        self.layoutChanged.emit()

        self.class_table_update.emit([row[0] for row in color_table.values()])

    def change_color(self, row, color):
        """ Changes a single color and notifies view """
        self.layoutAboutToBeChanged.emit()
        self._color_table[row][1] = color
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return 2

    def setData(self, index, value, role=Qt.EditRole):
        """ Adjust the data (set it to <value>) depending on the given 
            index and role. 
        """
        if role != Qt.EditRole:
            return False

        if index.isValid() and (index.column() == 1):
            
            self.layoutAboutToBeChanged.emit()
            self._color_table[index.row()][0] = value    
            self.layoutChanged.emit()
            self.class_table_update.emit([row[0] for row in self._color_table.values()])
            return True

        return False
