"""
@author: Austin Edwards

Controller for Image File Manager

"""
import os, sys

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QListWidgetItem, QHeaderView, QInputDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class ImageManagerController(QWidget):
    
    def __init__(self, model):
        super().__init__()
        
        self._model = model
    
    image_manager_window_closed = pyqtSignal(list)
    change_current_image = pyqtSignal(int)
     
    def test_command(self):
        print("ADD")
    def request_image_files(self):
        ''' User dialog to add new images to the ImageManager table '''
        print("ADD")
        items = ["", "False", "", 1]
        item_check = False
        # HDF5 Only for now
        fname = self.createH5FileDialog()[0]
        
        if len(fname) > 0:
            defaultDir = os.path.join(*fname.split("/")[:-1])
        else:
            # User cancelled dialog
            return
        # If file exists, ask for segmentation file and scale
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
        """ Lets the main view know that the file manager window is closed and updates the current image """
        self._model.file_table_data_changed.emit([-1])
        print("CLOSED")
        self.image_manager_window_closed.emit(self._model._filelist)
        self.change_current_image.emit(1)
    
    def getScale(self):
        """ Asks user for rescale factor """
        i, okPressed = QInputDialog.getDouble(self, "Enter factor for image rescale (1 if no change)","Scale:", 1, 0.01, 1, 2)
        if okPressed:
            return i
        else: return 1
