"""
@author: Austin Edwards

View window for creating new data filters.

"""

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QHeaderView
from PyQt5.QtCore import pyqtSlot
from views.filter_manager_view_ui import Ui_FilterManagerMainWindow

class FilterManagerView(QMainWindow):
    def __init__(self, filter_model, main_controller, filter_controller):
        
        super().__init__()
        
        self._filter_model = filter_model
        self._main_controller = main_controller
        self._filter_controller = filter_controller

        self._ui = Ui_FilterManagerMainWindow()
        self._ui.setupUi(self)

        self.current_query = None
        self._ui.objectClassList.currentTextChanged.connect(self.get_selected_values)
        self._ui.filterLogicList.currentTextChanged.connect(self.get_selected_values)
        self._ui.filterValueInput.textEdited.connect(self.get_selected_values)

        # These should only need to be triggered when a new view is created.
        # Don't need to update them if things change while window is closed.

        for v in self._filter_model.filter_object_list:
            self._ui.objectClassList.addItem(v)
        
        for v in self._filter_model.function_list:
            self._ui.filterLogicList.addItem(v)
        
        self._ui.addFilterButton.clicked.connect(self.add_current_query)
        self._ui.removeFilterButton.clicked.connect(self.remove_filter)

        self._ui.FilterManagerTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._ui.FilterManagerTableView.setSelectionBehavior(QTableWidget.SelectRows)
        self._ui.FilterManagerTableView.setModel(self._filter_model)

        self._filter_controller.filters_changed.connect(self.update_total_objects_filtered)
        self._ui.ORRadioButton.toggled.connect(self.check_or_button)
        self._ui.ANDRadioButton.toggled.connect(self.check_or_button)

        self._ui.ANDRadioButton.setChecked(True)
        
    def closeEvent(self, event):
        self._filter_controller.filter_manager_window_close()
        
        event.accept()
    
    def get_selected_values(self):

        obj_class = self._filter_model.filter_object_list[ self._ui.objectClassList.currentIndex() ]
        logic = self._filter_model.function_list[ self._ui.filterLogicList.currentIndex() ]
        value = str(self._ui.filterValueInput.text())
        self.current_query = [obj_class, logic, value]
        count = self._filter_controller.get_filter_result_count(self.current_query)
        self._ui.checkResultTextBox.setText(str(count))
    
    def add_current_query(self):

        if self.current_query is not None:
            self._filter_model.add_row(self.current_query)
        
        self.update_total_objects_filtered()
    
    def remove_filter(self):
        
        self._filter_model.delete_row(self._ui.FilterManagerTableView.selectedIndexes())
        self.update_total_objects_filtered()
    
    def update_total_objects_filtered(self):

        result = self._filter_controller.combine_filters()

        if result is None:
            total = len(self._filter_controller._main_model.object_data)
        else:
            total = len(result)

        self._ui.totalResultsTextBox.setText(str(total))
    
    def check_or_button(self):

        self._filter_model.OR = self._ui.ORRadioButton.isChecked()
        self.update_total_objects_filtered()