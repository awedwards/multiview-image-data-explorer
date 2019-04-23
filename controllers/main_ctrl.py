"""
@author: Austin Edwards

Control logic for integrating image and data models with the main view
and the segmentation class table models.
"""

from PyQt5.QtWidgets import QWidget, QInputDialog
from PyQt5.QtGui import QColor, QBrush, QColorDialog, QFileDialog
import h5py
import numpy as np
import pandas as pd
import scipy.io as sio
import os
from matplotlib import pyplot as plt

from skimage.transform import rescale
DEFAULT_COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255)]

class ImageDisplayController(QWidget):
    
    def __init__(self, main_model):
        super().__init__()

        self._main_model = main_model
        self._current_image_model = self._main_model.current_image_model
        self._seg_class_model = self._main_model.current_seg_model
        self.classes = []
    
    def read_image(self, fname):
        """ Reads image. H5 format only, for now """

        try:
            imagefile = h5py.File(fname, 'r')
            for k in list(imagefile.keys()):
                if "data" in k:
                    key=k
                    break
            return imagefile[key]
            #return np.squeeze(imagefile[key])
        except IOError:
            print("Can't read image")
    
        return

    def update_models_from_file_table(self, data_row):
        
        """ Updates image models after segmentation data is read."""

        self._current_image_model.image = self.image_rescale( self.read_image(data_row[0]), float(data_row[3]))
        
        if self.str2bool(data_row[1]):

            self._current_image_model.has_segmentation_image = True

            # saves a copy of the original segmentation image before rescaling
            color_table = dict()
            self._current_image_model.full_segmentation_data = self.read_image(data_row[2])
            self._current_image_model.segmentation_data = np.squeeze(self._current_image_model.full_segmentation_data).copy()
            
            # gets class labels directly from segmentation image
            self.classes = np.unique(self._current_image_model.segmentation_data)
            
            # initializes the color table and segmentation mask view with default colors
            for c,i in enumerate(self.classes):
                color_table[i] = ["Class " + str(c), QBrush(QColor(*DEFAULT_COLORS[i]))]
            self._seg_class_model.populate_class_table(color_table)

            # rescales segmentation image and saves object pixel locations for fast color updates
            self._current_image_model.segmentation_data = self._current_image_model.segmentation_data.astype(np.float64)
            self._current_image_model.segmentation_data = self.image_rescale( self._current_image_model.segmentation_data, float(data_row[3]))
            self.index_class_locations(self._current_image_model.segmentation_data)
            
            # creates an RGB segmentation image with default colors
            self._current_image_model.segmentation_image = self.create_seg_image(self._current_image_model.segmentation_data)
            self._current_image_model.segmentation_label = data_row[2]

    def index_class_locations(self, image):

        """ Saves all of the pixel locations in the segmentation image for each class in
            the segmentation class model
        """

        values = np.unique(np.round(image, decimals=0))
        nclasses = len(self._seg_class_model._color_table.keys())

        if (nclasses != len(values)):
            print("Error scaling segmentation image")
            raise(ValueError)

        for k in np.arange(nclasses):
            v = int(values[k])
            self._seg_class_model._class_loc[k] = np.where(image == values[v])

    def create_seg_image(self, image):
        """ Converts binary or n-ary segmentation image mask to rgb image with colors from the
            color table in the segmentation class table model
        """
        new_image = np.zeros([s for s in image.shape] + [3])

        for k,v in self._seg_class_model._color_table.items():
            new_image = self.set_color_in_seg_image(new_image, k)

        return new_image

    def image_rescale(self, image, scale):
        """ Rescales image given decimal scale"""
        if len(image.shape) > 3:
            image = image[0, 0, :, :, :]
        return rescale(image, scale, anti_aliasing=False, preserve_range=True)
    
    def change_class_color(self, row):
        """ Gets new color from user for segmentation class using a color wheel"""
        color = QColorDialog.getColor()
        if color.isValid():
            self._seg_class_model.change_color(row, QBrush(color))
            self._current_image_model.segmentation_image = self.create_seg_image(self._current_image_model.segmentation_data)

    def set_color_in_seg_image(self, image, k):
        """ Sets new color by retrieving the index of all pixels at class k and setting
            them to a new rgb color
        """
        idx = self._seg_class_model._class_loc[k]
        color = self._seg_class_model._color_table[k][1].color()
        r = color.red()
        g = color.green()
        b = color.blue()

        image[idx[0], idx[1], :] = (r,g,b)

        return image
    
    def load_analysis_file(self):
        
        """ Loads analysis file and calls updates to data models """

        FileDialog = QFileDialog()
        analysis_file_location = FileDialog.getOpenFileName(self, "Select object analysis data")

        if os.path.isfile(analysis_file_location[0]):
            self._main_model.object_data = pd.read_csv(analysis_file_location[0])
        
        self.update_models_from_analysis_file()

    def update_models_from_analysis_file(self):

        """ Updates the segmentation class model with the class labels provided in analysis output file """

        class_labels = self._main_model.object_data['Predicted Class'].unique()
        for c in class_labels:
            for i in self._main_model.object_data.index:
                row = self._main_model.object_data.iloc[i]
                if row['Predicted Class'] == c:
                    cx = row['Center of the object_1']
                    cy = row['Center of the object_0']
                    self._seg_class_model._color_table[ self._current_image_model.full_segmentation_data[cx, cy] ][0] = c
                    break

    def str2bool(self, s):

        """ Silly way to convert a string to bool """
        
        return str(s).lower() in ("yes", "true", "t", "1")