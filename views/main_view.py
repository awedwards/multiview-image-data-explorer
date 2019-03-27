from PyQt5.QtWidgets import QMainWindow, QGraphicsScene
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap

from views.main_view_ui import Ui_MainWindow
from views.image_manager_view import ImageManagerView

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from matplotlib import pyplot as plt
import pyqtgraph as pg

import numpy as np

class MainView(QMainWindow):
    def __init__(self, model, file_table_model, main_controller, image_manager_controller):
        
        super().__init__()

        self._model = model
        self._file_table_model = file_table_model

        self._main_controller = main_controller
        self._image_manager_controller = image_manager_controller

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._scene = QGraphicsScene()
        #self._scene.setSceneRect(0,0,self._model.h,self._model.w)

        self.figure = Figure()
        #self.figure.tight_layout()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setGeometry(-100,-100,self._model.h,self._model.w)

        self.axis = self.figure.add_subplot(111)
        self.axis.set_axis_off()
        
        self.axis.imshow(self._model.image)
        
        
        self._scene.addWidget(self.canvas)

        for item in self._scene.items():
            item.setPos(50,0)

        self._ui.imageDisplayView.setScene(self._scene)
        self._ui.imageDisplayView.show()
        self._model.image_changed.connect(self.on_image_change)

        self._ui.actionImage_Manager.triggered.connect(self.launchImageManager)
        self._image_manager_controller.change_current_image.connect(self.current_image_changed)
        self._file_table_model.file_table_data_changed.connect(self.file_list_changed)
        
        self._current_image_index = -1

    def launchImageManager(self):
 
        self._image_manager_view = ImageManagerView(self._file_table_model, self._image_manager_controller)
        self._image_manager_view.show()

    @pyqtSlot(list)
    def file_list_changed(self, value):

        try:
            if (value[0] == -1):
                filename = self._file_table_model._filelist[-1].split("/")[-1]
                self._ui.imageFileNavigatorView.addItem(filename)
            else:
                for row in value:
                    self._ui.imageFileNavigatorView.removeItem(row)
    
        except IndexError:
            pass

    @pyqtSlot(int)
    def current_image_changed(self, value):
       
        self._current_image_index = self._ui.imageFileNavigatorView.currentIndex()
 #print(self._file_table_model._filelist[self._current_image_index])
        self._main_controller.read_image( self._file_table_model._filelist[self._current_image_index])

    @pyqtSlot(pg.ImageWindow)
    def on_image_change(self, value):

        print("image changed, view")
        axes = self.figure.gca()
        axes.imshow(self._model.image)

        canvas = FigureCanvas(self.figure)

        self._scene.addWidget(canvas)
        self._ui.imageDisplayView.setScene(self._scene)
        self._ui.imageDisplayView.show()
