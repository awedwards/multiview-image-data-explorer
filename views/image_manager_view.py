"""
    @author: Austin Edwards

    View for displaying, adding, and removing ImageManagerFileTable data

"""

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QHeaderView

from views.image_manager_view_ui import Ui_ImageManagerMainWindow
from controllers.image_manager_ctrl import ImageManagerController
import numpy as np
import pandas as pd

class ImageManagerView(QMainWindow):
    def __init__(self, model, main_controller):
        
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        self._ui = Ui_ImageManagerMainWindow()
        self._ui.setupUi(self)
        self._ui.addImageButton.clicked.connect(self._main_controller.request_image_files)
        self._ui.removeImageButton.clicked.connect(self.remove_images)

        self._ui.imageManagerTableView.setSelectionBehavior(QTableWidget.SelectRows)
        self._ui.imageManagerTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self._ui.imageManagerTableView.setModel(self._model)

    def remove_images(self):
        """ Sends selected indexes to delete to file table model """
        print("REMOVE")
        self._model.delete_row(self._ui.imageManagerTableView.selectedIndexes())

    def closeEvent(self, event):
        """ Lets the controller know that the window has been closed so that the current image can be updated """
        
        event.accept()
        
        if len(self._model._filelist) > 0:
            self._main_controller.file_manager_window_close()
