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
            return '{0}'.format(self._data[i][j])
        elif role == QtCore.Qt.BackgroundColorRole:
            print(self._data)
            if index.column() == 0:
                return self._color_table[index.row()][1]
        else:
            return QtCore.QVariant()


    def headerData(self, section, orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._header[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def populate_class_table(self, color_table):

        self._color_table = color_table
        self.layoutAboutToBeChanged.emit()
        for v in color_table.values():
            self._data.append(["", v[0]])
        self.layoutChanged.emit()

        self.class_table_update.emit(1)

    def change_color(self, row, color):

        self.layoutAboutToBeChanged.emit()
        self._color_table[row][1] = color
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return 2

