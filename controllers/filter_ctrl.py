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
from matplotlib import path
from collections import defaultdict

from skimage.transform import rescale
from skimage import measure
from model.segmentation_index import SegmentationObject, SegmentationIndex

import operator
from functools import reduce
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
        
        ids = df['object_id']

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
            id_ = ids[i]

            # Speed up connected component search by just using bounding box information
            sub = self._image_model.full_segmentation_image[y1:y2+1,x1:x2+1]

            # Uses connected components algorithm to find all of the pixels
            # associated with each object
            labels = measure.label(sub, background=0)
            lbl = labels[cy-y1,cx-x1]
            idx = np.where(labels == lbl)

            # only index is saved right now, not objects
            obj = SegmentationObject(id_, cx, cy, list(boxes[i,:]), self._image_model.full_segmentation_image[cy, cx])
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
        roi_class = False

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
            if c in self._main_model.rois.keys():
                    
                path = self.roi_to_path(self._main_model.rois[c])
                x = df['Center of the object_1'].values
                y = df['Center of the object_0'].values
                centers = np.transpose(np.vstack([x, y]))
                contains_centers = path.contains_points(centers)
                roi_class = True
            
            if (f == "INCLUDE") or (f == "="):
                if roi_class:
                    return df.loc[contains_centers]
                else:
                    return df[df['Predicted Class']==c]
            elif f == "NOT INCLUDE":
                if roi_class:
                    return df.loc[ [not x for x in contains_centers] ]
                return df[df['Predicted Class']!=c]
        
        return None
    
    def roi_to_path(self, roi):

        return path.Path([x/self._image_model.image_scale for x in roi.getState()['points']])

    def filter_manager_window_close(self):
        
        """ Lets the main view know that the filter manager window is closed """
        self.filters_changed.emit(1)
    
    def combine_filters(self):

        results = [self.query(df) for df in self._filter_table_model._data]
        
        if len(results) == 0:
            return None
        elif len(results) == 1:
            return results[0]
        else:
            if self._filter_table_model.OR:
                return reduce(lambda  left,right: pd.merge(left,right,
                                                how='outer'), results)
            else:
                return reduce(lambda  left,right: pd.merge(left,right,
                                                how='inner'), results)