"""
@author: Austin Edwards

Control logic for integrating image and data models with the main view
and the segmentation class table models.
"""

from PyQt5.QtWidgets import QWidget, QInputDialog
from PyQt5.QtGui import QColor, QBrush, QColorDialog, QFileDialog
from PyQt5.QtCore import pyqtSignal
import h5py
import numpy as np
import pandas as pd
import scipy.io as sio
import os
from matplotlib import pyplot as plt

from skimage.transform import rescale
from sklearn.cluster import DBSCAN
from model.color_lookup_table import ColorLUT

DEFAULT_COLORS = [(0,0,0), (0,255,149), (230,0,103), (252,205,0), (0,116,241), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255)]

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
            if (len(imagefile[key].shape) > 3): return np.squeeze(imagefile[key])
            else: return np.array(imagefile[key])
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
            self._current_image_model.full_segmentation_image = self.read_image(data_row[2])
            self._current_image_model.segmentation_data = self._current_image_model.full_segmentation_image.copy()

            # gets class labels directly from segmentation image
            self.classes = np.unique(self._current_image_model.segmentation_data)
            
            # initializes the color table and segmentation mask view with default colors
            for c,i in enumerate(self.classes):
                if i == 0:
                    name = "Background"
                else:
                    name = "Class " + str(c)
                color_table[c] = ColorLUT(c, name, None, QBrush(QColor(*DEFAULT_COLORS[i])) )
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
        #image[ np.where(image - np.array(image, dtype=np.uint8) > 0.01) ] = 0
        image = np.round(image, decimals=0)

        values = np.unique(image)

        classes = self._seg_class_model._color_table.keys()

        for k in classes:
            if k in values:
                self._seg_class_model._color_table[k].index = np.where(image == k)
            else:
                self._seg_class_model._color_table[k].index = [np.array([]),np.array([])]

    def create_seg_image(self, image):
        """ Converts binary or n-ary segmentation image mask to rgb image with colors from the
            color table in the segmentation class table model
        """
        if len(image.shape) < 3:
            new_image = np.zeros([s for s in image.shape] + [3])
        else:
            new_image = np.zeros(image.shape)

        for k in self._seg_class_model._color_table.keys():
            new_image = self.set_color_in_seg_image(new_image, k)

        return new_image

    def image_rescale(self, image, scale):
        """ Rescales image given decimal scale"""
        if len(image.shape) > 3:
            image = image[0, 0, :, :, :]
        return rescale(image, scale, anti_aliasing=False, preserve_range=True, order=0)
    
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

        idx = self._seg_class_model._color_table[k].index
        color = self._seg_class_model._color_table[k].color.color()
        r = color.red()
        g = color.green()
        b = color.blue()
        if idx is not None:
            image[idx[:,0], idx[:,1], :] = (r,g,b)

        return image
    
    def load_analysis_file(self):
        
        """ Loads analysis file and calls updates to data models """

        FileDialog = QFileDialog()
        analysis_file_location = FileDialog.getOpenFileName(self, "Select object analysis data", "D:\\Austin\\", "CSV or Text Files (*csv *txt)")

        if os.path.isfile(analysis_file_location[0]):
            self._main_model.object_data = pd.read_csv(analysis_file_location[0])
            self._main_model.filter_results = self._main_model.object_data
            self.update_models_from_analysis_file()
            return (True, os.path.split(analysis_file_location[0])[-1])

        # if user cancelled loading dialog, skip indexing objects in main_view
        return (False, -1)

    def select_path_to_save_filter_results(self, data):

        """ Opens a file dialog to select path for saving object filter results """

        FileDialog = QFileDialog()
        filter_results_file_location = FileDialog.getSaveFileName(self, "Select path to save filter results","CSV Files (*.csv)")
        
        if not (filter_results_file_location[0] == ''):
            data.to_csv(filter_results_file_location[0])
        
    def update_models_from_analysis_file(self):

        """ Updates the segmentation class model with the class labels provided in analysis output file """

        class_labels = self._main_model.object_data['Predicted Class'].unique()
        for c in class_labels:
            for i in self._main_model.object_data.index:
                row = self._main_model.object_data.iloc[i]
                if row['Predicted Class'] == c:
                    cx = int( row['Center of the object_1'] )
                    cy = int( row['Center of the object_0'] )
                    self._seg_class_model.set_label_in_color_table( self._current_image_model.full_segmentation_image[cx, cy], c)
                    break

    def construct_seg_image_from_objectids(self, indexes):

        image = np.zeros([s for s in self._current_image_model.full_segmentation_image.shape] + [3])
        
        for i in indexes:
            idx = self._main_model.segmentation_index.index[i]
            k = self._main_model.segmentation_index._class[i]
            
            image[idx[0], idx[1],:] = k

        #update class locations
        self._current_image_model.segmentation_data = self.image_rescale( image, self._current_image_model.image_scale)
        self.index_class_locations(self._current_image_model.segmentation_data[:,:,0])
        self._current_image_model.segmentation_image = self.create_seg_image(self._current_image_model.segmentation_data)

    def cluster_objects(self, dataframe, min_dist, min_neighbors):

        x1 = dataframe['Center of the object_1']
        x2 = dataframe['Center of the object_0']

        db = DBSCAN(eps=min_dist, min_samples=min_neighbors).fit( np.transpose( np.vstack((x1, x2)) ) )
        
        self._main_model.cluster_labels = db.labels_
        
        lbl = [l for l in np.unique(self._main_model.cluster_labels) if l != -1]
        for l in lbl:
            self._main_model.cluster_ids.append( dataframe.iloc[np.where(db.labels_ == l)[0]]["object_id"].values )
        
        self.initialize_cluster_image()
        
        dataframe['cluster_id'] = db.labels_
        #print(np.unique(dataframe['cluster_id']))
        return dataframe

    def calculate_cluster_statistics(self, dataframe):

        return dataframe

    def initialize_cluster_image(self):

        new_image = np.zeros([s for s in self._current_image_model.full_segmentation_image.shape] + [3])

        for ob in self._main_model.filter_results['object_id'].values:

            index = self._main_model.segmentation_index.index[ob]
            # Initialize all objects as gray (to indicate no membership to a cluster)
            new_image[index[0], index[1],:] = (220,220,220)

        self.color_cluster_image(new_image)
    
    def color_cluster_image(self, image):

        # skip black
        colors = DEFAULT_COLORS[1:]
        
        for cluster in self._main_model.cluster_ids:
            select_color = np.random.randint(len(DEFAULT_COLORS))
            for ob in cluster:
                index = self._main_model.segmentation_index.index[ob]
                image[index[0], index[1],:] = DEFAULT_COLORS[select_color]
        
        self._current_image_model.cluster_image = self.image_rescale(image, self._current_image_model.image_scale)

    def str2bool(self, s):

        """ Silly way to convert a string to bool """
        
        return str(s).lower() in ("yes", "true", "t", "1")