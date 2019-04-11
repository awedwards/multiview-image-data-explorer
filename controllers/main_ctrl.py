from PyQt5.QtCore import QObject
from PyQt5.QtGui import QColor, QBrush, QColorDialog
import h5py
import numpy as np
import scipy.io as sio
from matplotlib import pyplot as plt

from skimage.transform import rescale
DEFAULT_COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255)]

class ImageDisplayController(QObject):
    
    def __init__(self, main_model):
        super().__init__()

        self._main_model = main_model
        self._current_image_model = self._main_model.current_image_model
        self._seg_class_model = self._main_model.current_seg_model
        self.classes = []
    
    def read_image(self, fname):
        
        try:
            imagefile = h5py.File(fname, 'r')
            for k in list(imagefile.keys()):
                if "data" in k:
                    key=k
                    break
            return np.squeeze(imagefile[key])
        except IOError:
            print("Can't read image")
    
        return

    def update_models_from_file_table(self, data_row):

        self._current_image_model.image = self.image_rescale( self.read_image(data_row[0]), float(data_row[3]))
        
        if data_row[1]:

            self._current_image_model.has_segmentation_image = True

            color_table = dict()
            self._current_image_model.segmentation_data = self.read_image(data_row[2])
            self.classes = np.unique(self._current_image_model.segmentation_data).astype(np.uint8)
            
            for c,i in enumerate(self.classes):
                color_table[i] = ["Class " + str(c), QBrush(QColor(*DEFAULT_COLORS[i]))]
            
            self._seg_class_model.populate_class_table(color_table)
            self._current_image_model.segmentation_data = self._current_image_model.segmentation_data.astype(np.float64)
            self._current_image_model.segmentation_data = self.image_rescale( self._current_image_model.segmentation_data, float(data_row[3]))
            self.index_class_locations(self._current_image_model.segmentation_data)
            
            self._current_image_model.segmentation_image = self.create_seg_image(self._current_image_model.segmentation_data)
            self._current_image_model.segmentation_label = data_row[2]

    def index_class_locations(self, image):

        values = np.unique(np.round(image, decimals=0))
        nclasses = len(self._seg_class_model._color_table.keys())

        if (nclasses != len(values)):
            print("Error scaling segmentation image")
            raise(ValueError)

        for k in np.arange(nclasses):
            v = int(values[k])
            self._seg_class_model._class_loc[k] = np.where(image == values[v])

    def create_seg_image(self, image):
       
        new_image = np.zeros([s for s in image.shape] + [3])

        for k,v in self._seg_class_model._color_table.items():
            new_image = self.set_color_in_seg_image(new_image, k)

        return new_image

    def image_rescale(self, image, scale):
        '''rescale image'''
        
        return rescale(image, scale, anti_aliasing=False, preserve_range=True)
    
    def change_class_color(self, row):
        
        color = QColorDialog.getColor()
        if color.isValid():
            self._seg_class_model.change_color(row, QBrush(color))
            self._current_image_model.segmentation_image = self.create_seg_image(self._current_image_model.segmentation_data)
    
    def change_class_label(self, row):

        # ADD LATER
        return

    def set_color_in_seg_image(self, image, k):

        idx = self._seg_class_model._class_loc[k]
        color = self._seg_class_model._color_table[k][1].color()
        r = color.red()
        g = color.green()
        b = color.blue()

        image[idx[0], idx[1], :] = (r,g,b)

        return image