import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal

class filterTableModel(QAbstractTableModel):

    def __init__(self, data, header, parent=None):

        QAbstractTableModel.__init__(self, parent)
        self._data = data
        self._header = header
        self.non_class_filterable_object_list = ["Size in pixels"]
        self.function_list = ["INCLUDE", "NOT INCLUDE", "<", "<=", ">", ">=", "="]
        self.OR = False
        
    fliter_object_list_changed_signal = pyqtSignal(list)
    
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

    def class_list_changed(self, value):
        
        self.filter_object_list = []

        for item in self.non_class_filterable_object_list:
            self.filter_object_list.append(item)
        for v in value:
            self.filter_object_list.append(v)
        self.fliter_object_list_changed_signal.emit(self.filter_object_list)

    def add_row(self, value):
        if value not in self._data:
            self.layoutAboutToBeChanged.emit()
            self._data.append(value)
            self.layoutChanged.emit()

    def delete_row(self, indexes):

        rows = sorted(set(index.row() for index in indexes), reverse=True)
        
        self.layoutAboutToBeChanged.emit()
        for row in rows:
            del self._data[row]
        self.layoutChanged.emit()