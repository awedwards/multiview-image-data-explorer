from PyQt5.QtWidgets import QWidget
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

class FilterController(QWidget):

    def __init__(self, main_model, filter_table_model, image_model):

        self._filter_table_model = filter_table_model
        self._image_model = image_model
        self._main_model = main_model

    def index_objects(self):

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

            sub = self._image_model.full_segmentation_data[y1:y2+1,x1:x2+1]

            labels = measure.label(sub, background=0)
            lbl = labels[cy-y1,cx-x1]
            idx = np.where(labels == lbl)
            obj.index = np.vstack([idx[0]+y1, idx[1]+x1])
        
            index.add_object(obj)
        
        self._main_model.segmentation_index = index