from PyQt5.QtWidgets import QMainWindow

from views.filter_manager_view_ui import Ui_FilterManagerMainWindow

class FilterManagerView(QMainWindow):
    def __init__(self, model, main_controller):
        
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        self._ui = Ui_FilterManagerMainWindow()
        self._ui.setupUi(self)

    def closeEvent(self, event):        
        event.accept()
