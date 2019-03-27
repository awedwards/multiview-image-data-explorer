import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal

class fileTableModel(QAbstractTableModel):

    def __init__(self, data, header, parent=None):

        QAbstractTableModel.__init__(self, parent)
        self._data = data
        self._filelist = [f[0] for f in self._data]
        self._header = header

    file_table_data_changed = pyqtSignal(list)
    
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
    
    def add_row(self, value):

        self.layoutAboutToBeChanged.emit()
        self._data.append(value)
        self._filelist.append(value[0])
        self.layoutChanged.emit()

        self.file_table_data_changed.emit([-1])
    
    def delete_row(self, indexes):
        rows = sorted(set(index.row() for index in indexes), reverse=True)
        
        self.layoutAboutToBeChanged.emit()
        for row in rows:
            del self._data[row]
            del self._filelist[row]
        self.layoutChanged.emit()
        
        self.file_table_data_changed.emit(rows)

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        try:
            return len(self._data[0])
        except IndexError:
            return 0