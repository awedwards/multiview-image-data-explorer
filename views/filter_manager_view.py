"""
@author: Austin Edwards

View window for creating new data filters.

"""

from PyQt5.QtWidgets import QMainWindow

from views.filter_manager_view_ui import Ui_FilterManagerMainWindow

class FilterManagerView(QMainWindow):
    def __init__(self, model, main_controller, filter_controller):
        
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._filter_controller = filter_controller

        self._ui = Ui_FilterManagerMainWindow()
        self._ui.setupUi(self)

        self.objectClassList

    def closeEvent(self, event):        
        event.accept()