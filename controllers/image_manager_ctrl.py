import os, sys

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QListWidgetItem, QHeaderView, QInputDialog
from PyQt5.QtCore import pyqtSignal

class ImageManagerController(QWidget):
    
    def __init__(self, model):
        super().__init__()
        
        self._model = model

    change_current_image = pyqtSignal(int)

    def request_image_files(self):
        ''' User dialog to add a new image to the ImageManager table '''

        items = ["", "False", "", 1]
        item_check = False
        fname = self.createH5FileDialog()[0]
        
        if len(fname) > 0:
            defaultDir = os.path.join(*fname.split("/")[:-1])
        else:
            # User cancelled dialog
            return

        if os.path.isfile(fname):

            item_check = True

            items[0] = fname
            maskfname = self.createH5FileDialog(defaultDir = defaultDir, message="Select segmentation mask file")[0]
            
            tf = os.path.isfile(maskfname)
            items[1] = str(tf)
            
            if (len(maskfname) > 0):
                if tf:
                    items[2] = maskfname
                else: item_check = False

        items[3] = self.getScale()

        if item_check:
            self._model.add_row(items)

    def createH5FileDialog(self, message="Open file", defaultDir="E:\\Data\\Austin", filetype="Image files (*hdf5 *h5)"):
        ''' Creates FileDialog object to ask for h5 files''' 
        FileDialog = QFileDialog()
        return FileDialog.getOpenFileName(self, message, defaultDir, filetype)

    def file_manager_window_close(self):        
        self.change_current_image.emit(1)
    
    def getScale(self):
        i, okPressed = QInputDialog.getDouble(self, "Enter image scale","Scale:", 1, 0, 1, 2)
        if okPressed:
            return i
        else: return 1