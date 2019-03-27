import os, sys

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QListWidgetItem, QHeaderView
from PyQt5.QtCore import pyqtSignal

class ImageManagerController(QWidget):
    
    def __init__(self, model):
        super().__init__()
        
        self._model = model

    change_current_image = pyqtSignal(int)

    def request_image_files(self):

        items = ["", "False", ""]
        item_check = False

        fname = self.createFileDialog()

        if os.path.isfile(fname[0]):

            item_check = True

            items[0] = fname[0]
            maskfname = self.createFileDialog(message="Select segmentation mask file")
            
            tf = os.path.isfile(maskfname[0])
            items[1] = str(tf)

            if tf and (len(maskfname[0]) > 0):
                items[2] = maskfname[0]
            else:
                item_check = False
        
        if item_check:
            self._model.add_row(items)

    def createFileDialog(self, message="Open file", defaultDir="E:\\Data\\Austin", filetype="Image files (*hdf5 *h5)"):

        FileDialog = QFileDialog()
        return FileDialog.getOpenFileName(self, message, defaultDir, filetype)

    def file_manager_window_close(self):
        
        self.change_current_image.emit(1)
