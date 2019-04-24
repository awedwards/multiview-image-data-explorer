"""
@author: Austin Edwards

Controller for the object data and data filters.

"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
import h5py
import numpy as np
import pandas as pd
import scipy.io as sio
import os
from matplotlib import pyplot as plt
from collections import defaultdict

from skimage.transform import rescale
from skimage import measure
from model.segmentation_index import SegmentationObject, SegmentationIndex

import operator

class FilterController(QWidget):

    def __init__(self, main_model, filter_table_model, image_model):
        super().__init__()

        self._filter_table_model = filter_table_model
        self._image_model = image_model
        self._main_model = main_model

    filters_changed = pyqtSignal(int)

    def index_objects(self):
        
        """ Gets pixel locations all of the objects in the segmentation image """
        
        df = self._main_model.object_data

        nobjects = len(df.index)
        
        index = SegmentationIndex()

        boxes = np.zeros((nobjects,4))
        centers = np.zeros((nobjects, 2))
        
        boxes[:,0] = df['Bounding Box Minimum_0']
        boxes[:,1] = df['Bounding Box Minimum_1']
        boxes[:,2] = df['Bounding Box Maximum_0']
        boxes[:,3] = df['Bounding Box Maximum_1']
        boxes = boxes.astype(np.uint16)
        centers[:,0] = df['Center of the object_0']
        centers[:,1] = df['Center of the object_1']
        centers = centers.astype(np.uint16)

        for i in df.index:
            
            x1 = boxes[i,0]
            x2 = boxes[i,2]
            y1 = boxes[i,1]
            y2 = boxes[i,3]
            
            cx = centers[i,0]
            cy = centers[i,1]

            obj = SegmentationObject(i, cx, cy, list(boxes[i,:]))

            # Speed up connected component search by just using bounding box information
            sub = self._image_model.full_segmentation_data[y1:y2+1,x1:x2+1]

            # Uses connected components algorithm to find all of the pixels
            # associated with each object
            labels = measure.label(sub, background=0)
            lbl = labels[cy-y1,cx-x1]
            idx = np.where(labels == lbl)
            obj.index = np.vstack([idx[0]+y1, idx[1]+x1])
        
            index.add_object(obj)
        
        self._main_model.segmentation_index = index
    
    def get_filter_result_count(self, args):

        result = self.query(args)

        if result is not None:
            return len(result)

        return 0

    def query(self, args):

        c, f, v = args
        
        df = self._main_model.object_data
        
        if (c == "Size in pixels"):
            try:
                v = float(v)
            except ValueError:
                return None

            if f == "<":
                return df[operator.lt(df[c], v)]
            elif f == ">":
                return df[operator.gt(df[c], v)]
            elif f == "<=":
                return df[operator.le(df[c], v)]
            elif f == ">=":
                return df[operator.ge(df[c], v)]
            elif f == "=":
                return df[operator.eq(df[c], v)]
        else:
            
            if (f == "INCLUDE") or (f == "="):
                return df[df['Predicted Class']==c]
            elif f == "NOT INCLUDE":
                return df[df['Predicted Class']!=c]
        
        return None
    
    def filter_manager_window_close(self):
        
        """ Lets the main view know that the filter manager window is closed """
        self.filters_changed.emit(1)