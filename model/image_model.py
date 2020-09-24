"""
    @author: Austin Edwards

    Data model for storing image and segmentation data

"""

from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QHeaderView
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

import pyqtgraph as pg
import numpy as np

import os

class ImageModel(QObject):

    def __init__(self):
        super().__init__()
        
        self.image = np.zeros((500,500))
        self.has_segmentation_image = False
        
        self.segmentation_data = np.zeros(self.__image.shape)
        self.full_segmentation_image = self.segmentation_data.copy()
        self.segmentation_image = self.segmentation_data.copy()
        self.segmentation_label = "None"
        self.cluster_image = self.segmentation_data.copy()
        self.segmentation_classes = []
        self.mask_on = False
        #self.image_scale = 1.0
        
    image_changed = pyqtSignal(int)
    segmentation_image_changed = pyqtSignal(int)
    
    @property
    def image(self):
        return self.__image
    
    @image.setter
    def image(self, value):
        self.__image = value
        self.image_changed.emit(1)

    @property
    def segmentation_image(self):
        return self.__segmentation_image
    
    @segmentation_image.setter
    def segmentation_image(self, value):
        self.__segmentation_image = value
        self.segmentation_image_changed.emit(1)

    @property
    def segmentation_label(self):
        return self.__segmentation_label

    @segmentation_label.setter
    def segmentation_label(self, value):

        if self.has_segmentation_image:
            if (self.image.shape == self.segmentation_image.shape):
                self.__segmentation_label = value
        else:
            self.__segmentation_label = "None"

    @property
    def image_to_view(self):
        return self.__image_to_view
    
    @image_to_view.setter
    def image_to_view(self, value):
        
        self.__image_to_view = value
        self.image_changed.emit(value)

    def add_class_label(self, classid, classlabel, classcolor):

        self.segmentation_classes[classid] = (classlabel, classcolor)
        
