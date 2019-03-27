from PyQt5.QtCore import QObject
from skimage.transform import rescale
import h5py
import numpy as np
from matplotlib import pyplot as plt

class ImageDisplayController(QObject):
    
    def __init__(self, model):
        super().__init__()

        self._model = model
        
        self._scale = 0.25

    def read_image(self, fname):
        
        try:

            imagefile = h5py.File(fname, 'r')
            self._model.image = self.image_rescale(np.squeeze(imagefile['data']))
            #f = plt.figure(figsize=(20,20))
            #plt.imshow(self.image_rescale(np.squeeze(imagefile['data'])))

        except IOError:
            print("Can't read image")

    def image_rescale(self, image):
        '''rescale image'''
        
        return rescale(image, self._scale, anti_aliasing=False)