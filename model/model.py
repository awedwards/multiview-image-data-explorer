from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QHeaderView
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

import pyqtgraph as pg

import numpy as np

class Model(QObject):

    def __init__(self):
        super().__init__()

        self.w, self.h, self.c = (631, 721, 3)

        self.image = np.zeros((self.w, self.h, self.c))
        #self.image = self.convert_numpy_to_QPixmap(np.zeros((self.w, self.h, self.c)))
        self._segmentation_image = np.zeros((100,100,3))
        
    image_changed = pyqtSignal(pg.ImageWindow)
    segmentation_image_changed = pyqtSignal(pg.ImageWindow)
    
    @property
    def image(self):
        return self.__image
    
    @image.setter
    def image(self, value):
        
        print("image changed , model")
        try:
            self.__image = pg.image(value)
            #self.__image = self.convert_numpy_to_QPixmap(value)
        except AttributeError:
            self.__image = value

        self.image_changed.emit(self.__image)

    @property
    def segmentation_image(self):
        return self._segmentation_image
    
    @segmentation_image.setter
    def segmentation_image(self, value):
        self._segmentation_image = value
        self.segmentation_image_changed.emit(value)
    
    def convert_numpy_to_QPixmap(self, data):

        height, width, channel = data.shape
        bytesPerLine = channel * width
        return QPixmap(QImage(data, width, height, bytesPerLine, QImage.Format_RGB888))