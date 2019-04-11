from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QHeaderView
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

from model.image_model import ImageModel
from model.segmentation_class_table_model import SegmentationClassTableModel
class Model(QObject):

    def __init__(self):
        super().__init__()
        
        self.images = {}
        self.images[""] = ImageModel()
        self.seg_models = {}
        self.seg_models[""] = SegmentationClassTableModel(data=[], header=["Color", "Class"])
        self.current_id = ""
            
    @property
    def current_id(self):
        return self.__current_id
    
    @current_id.setter
    def current_id(self, value):
        self.__current_id = value
        try:
            self.current_image_model = self.images[value]
            self.current_seg_model = self.seg_models[value]
        except KeyError:
            pass 
    
    def add_image_model(self, key):
        self.images[key] = ImageModel()
    
    def add_seg_model(self, key):
        self.seg_models[key] = SegmentationClassTableModel(data=[], header=["Color", "Class"])