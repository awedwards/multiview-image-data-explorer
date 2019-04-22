import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal

class filterTableModel(QAbstractTableModel):

    def __init__(self, data, header, parent=None):

        QAbstractTableModel.__init__(self, parent)
        self._data = data
        self._header = header

        self.classList = []
        self.functionList = ["INCLUDE", "NOT INCLUDE", "<", ">", "="]

    class_list_changed = pyqtSignal(list)
    
    def data(self, index, role=QtCore.Qt.DisplayRole):

        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return '{0}'.format(self._data[i][j])
        else:
            return QtCore.QVariant()

    def headerData(self, section, orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._header[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)
    
    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        try:
            return len(self._data[0])
        except IndexError:
            return 0