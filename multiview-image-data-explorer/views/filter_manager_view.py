"""
@author: Austin Edwards

View window for creating new data filters.

"""

from PyQt5.QtWidgets import QTreeWidgetItem, QMainWindow
from PyQt5.QtCore import pyqtSlot, Qt
from views.filter_manager_view_ui import Ui_FilterManagerMainWindow

class FilterManagerView(QMainWindow):
    def __init__(self, filter_model, main_controller, filter_controller):
        
        super().__init__()
        
        self._filter_model = filter_model
        self._main_controller = main_controller
        self._filter_controller = filter_controller

        self._ui = Ui_FilterManagerMainWindow()
        self._ui.setupUi(self)

        self.class_queries = []
        self.non_class_queries = []
        self.query_results = self._filter_model._data

        object_list = QTreeWidgetItem(self._ui.filterObjectsList)
        object_list.setText(0,"Class Objects")
        
        object_list.setFlags(object_list.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        
        for ob in self._filter_model.class_filterable_object_list:
            item = QTreeWidgetItem(object_list)
            item.setText(0,ob)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)

        feature_list = QTreeWidgetItem(self._ui.filterObjectsList)
        feature_list.setText(0,"Features")
        for f in self._filter_model.non_class_filterable_object_list:
            item = QTreeWidgetItem(feature_list)
            item.setText(0,f)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)

        self._ui.resetFilterSettingsButton.clicked.connect(self.reset_filter_settings)
        self._ui.applyFilterButton.clicked.connect(self.construct_queries)

        self._ui.totalResultsTextBox.setText(str(len(self._filter_model._data)))

    def construct_queries(self):
        
        # Clear previous results
        self.class_queries = []
        self.non_class_queries = []

        # Class objects
        object_list = self._ui.filterObjectsList.topLevelItem(0)
        for j in range(object_list.childCount()):
            child = object_list.child(j)
            if (child.checkState(0) == Qt.Checked):
                c = child.text(0)
                f = "INCLUDE"
                v = ""
                self.class_queries.append((c,f,v))
             

        object_list = self._ui.filterObjectsList.topLevelItem(1)
        for j in range(object_list.childCount()):
            child = object_list.child(j)
            if (child.checkState(0) == Qt.Checked):
                c = child.text(0)
                f = "INCLUDE"
                v = ""
                self.non_class_queries.append((c,f,v))
        
        self.query_results = self._filter_controller.combine_filters(self.class_queries, self.non_class_queries)
        self._ui.totalResultsTextBox.setText(str(len(self.query_results)))

    def reset_filter_settings(self):
        return

    def closeEvent(self, event):
        self._filter_model.query_results = self.query_results
        self._filter_controller.filter_manager_window_close()
        
        event.accept()