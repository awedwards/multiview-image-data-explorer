import sys

from PyQt5 import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QFileDialog, QWidget, QMenuBar

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path 
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt

import h5py

import numpy as np

import pandas as pd

from skimage.transform import rescale

class ImageDisplayController(QWidget):
    
    def __init__(self, parent=None):
        super(ImageDisplay, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure(figsize=(20,20))
        self.ax = self.figure.add_subplot(111)
        self.image = np.zeros((100,100,3))
        
        self.regions = {}
        self.selected_regions = []
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Button to load image, connected to `load_image` method
        self.load_button = QPushButton('Load image')
        self.load_button.clicked.connect(self.load_image)
        
        # Button to load image, connected to `load_image` method
        self.add_region_button = QPushButton('Add region')
        self.add_region_button.setCheckable(True)
        self.add_region_button.clicked.connect(self.add_region)
        
        # Button to filter object file based on selected regions
        self.filter_objects = QPushButton('Filter objects')
        self.filter_objects.clicked.connect(self.filter_and_save)
        
        self.build_menu()
        
        # Widget to handle region selector
        self.cid = self.canvas.mpl_connect('button_press_event', self.select_region)
        
        self.scale=0.25
        
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.menu)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.load_button)
        layout.addWidget(self.add_region_button)
        layout.addWidget(self.filter_objects)
        
        self.setLayout(layout)
        
        self.show()
    
    def build_menu(self):

        self.menu = QMenuBar()
        self.menu.addMenu('File')
        self.menu.addMenu('Edit')
        self.menu.addMenu('View')

    def load_image(self):
        ''' load image from file '''
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'E:\\Data\\Austin', 'Image files (*hdf5))')
        self.imagefile = h5py.File(fname[0], 'r')
        
        self.image_rescale(np.squeeze(self.imagefile['data']))
        self.draw()
        
    def image_rescale(self, image):
        '''rescale image'''
        
        self.image = rescale(image, self.scale, anti_aliasing=False)
            
    def add_region(self):
        '''A button that connects to the mouse connection swapper so regions can
           be drawn'''
        self.swap_mouse_connections()
        self.draw()
    
    def swap_mouse_connections(self):
        '''Swaps mouse-click connection between (already drawn) region selector
           and region drawer'''
        if self.add_region_button.isChecked():
            self.canvas.mpl_disconnect(self.cid)
            self.lasso = LassoSelector(self.ax, onselect=self.onselect)            
        else:
            self.cid = self.canvas.mpl_connect('button_press_event', self.select_region)
            self.lasso = None      
    
    def keyPressEvent(self, event):
        '''Deletes selected regions'''
        if (event.key() == Qt.Key_Delete) or (event.key() == Qt.Key_Backspace):
            
            regions_to_delete = self.selected_regions.copy()
            
            for pathid in regions_to_delete:
                del self.regions[pathid]
                self.selected_regions.remove(pathid)
                
        self.draw()
    
    def select_region(self, event):
        '''select region by clicking on it'''
        
        x, y = event.xdata, event.ydata
        
        for pathid in self.regions.keys():
            path = self.regions[pathid]
            
            if path.contains_point((x,y)):
                if (pathid not in self.selected_regions):
                    self.selected_regions.append(pathid)
                else:
                    self.selected_regions.remove(pathid)
            
        self.draw()

    def draw(self):
        
        # Display image
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.imshow(self.image)
        
        # Draw regions
        for pathid in self.regions.keys():
            
            path = self.regions[pathid]
            if pathid in self.selected_regions:
                patch = PathPatch(path, facecolor='r', alpha=0.25)
            else:
                patch = PathPatch(path, facecolor='b', alpha=0.25)
                
            self.ax.add_patch(patch)
        
        # Make sure mouse is connected properly
        self.swap_mouse_connections()
            
        # refresh canvas
        self.canvas.draw()
            
    def onselect(self, verts):
        
        path = Path(verts)
        self.regions[ len( self.regions.keys() ) ] = path
        self.draw()
        
    def filter_and_save(self):
        
        fname = QFileDialog.getOpenFileName(self, 'Open object file', 'E:\\Data\\Austin', 'Data files (*.csv *.txt)')
        
        try:
            df = pd.read_csv(fname[0])
        except FileNotFoundError:
            # Does not print if user cancelled open action
            if len(fname[0]) > 0:
                print("Object file " + fname[0] + " does not exist")
            return
       
        object_locations = np.transpose(np.vstack((df['Center of the object_0'], df['Center of the object_1'])))
        idx = [False]*object_locations.shape[0]
        for path in self.regions.values():
            verts = path.vertices / self.scale
            rescaled_path = Path(verts)
            idx = np.logical_or(idx, rescaled_path.contains_points(object_locations))
            
        filtered = df.loc[idx]
        print(len(filtered))