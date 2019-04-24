"""
@author: Austin Edwards

View window for creating new data filters.

"""

from PyQt5.QtWidgets import QMainWindow
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

        # These should only need to be triggered when a new view is created.
        # Don't need to update them if things change while window is closed.

        for v in self._filter_model.filter_object_list:
            self._ui.objectClassList.addItem(v)
        
        for v in self._filter_model.function_list:
            self._ui.filterLogicList.addItem(v)
        
        self._ui.checkLogic.clicked.connect(self.get_selected_values)
        
        self.current_query = ["", "", ""]

    def closeEvent(self, event):        
        event.accept()
    
    def get_selected_values(self):

        obj_class = self._filter_model.filter_object_list[ self._ui.objectClassList.currentIndex() ]
        logic = self._filter_model.function_list[ self._ui.filterLogicList.currentIndex() ]
        value = str(self._ui.filterValueInput.text())
        self.current_query = [obj_class, logic, value]
        count = self._filter_controller.get_filter_result_count(self.current_query)

        self._ui.checkResultTextBox.setText(" ".join(self.current_query) + ", count: " + str(count))
        