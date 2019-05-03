"""
@author: Austin Edwards

Main window of the GUI. Talks with all of the other models and controllers to
dispay the image and quantitative data.

"""

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QAbstractItemView, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap

from views.main_view_ui import Ui_MainWindow
from views.image_manager_view import ImageManagerView
from views.filter_manager_view import FilterManagerView

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from matplotlib import pyplot as plt
import pyqtgraph as pg

import numpy as np

class MainView(QMainWindow):
    def __init__(self, model, file_table_model, filter_table_model, main_controller, image_manager_controller, filter_controller):
        
        super().__init__()

        self.all_models = model
        self._model = model.current_image_model
        self._file_table_model = file_table_model
        self._seg_class_model = model.current_seg_model
        self._filter_table_model = filter_table_model

        self._main_controller = main_controller
        self._image_manager_controller = image_manager_controller
        self._filter_controller = filter_controller

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.current_image = pg.ImageItem()
        self.current_image.setImage(self._model.image)
        self._ui.graphicsView.view.addItem(self.current_image)

        # Default segmentation mask turned off
        self.segmentation_image = pg.ImageItem()
        self._ui.graphicsView.view.addItem(self.segmentation_image)
        self.segmentation_opacity = 0.0

        # Settings for segmentation class table
        self._ui.segmentationClassList.setModel(self._seg_class_model)
        self._ui.segmentationClassList.setSelectionMode(QAbstractItemView.SingleSelection)
        self._ui.segmentationClassList.verticalHeader().setVisible(False)
        self._ui.segmentationClassList.horizontalHeader().setStretchLastSection(True)
        self._ui.segmentationClassList.horizontalHeader().setVisible(False)
        self._ui.segmentationClassList.doubleClicked.connect(self.seg_class_data_change_request)

        # Turns off default pyqtgraph visualization settings
        self._ui.graphicsView.ui.histogram.hide()
        self._ui.graphicsView.ui.roiBtn.hide()
        self._ui.graphicsView.ui.menuBtn.hide()

        self._ui.graphicsView.view.setAspectLocked(True)

        #self._ui.graphicsView.getImageItem().mouseDragEvent = self.mouseDragEvent
        #self.current_image.mouseDragEvent = self.mouseDragEvent
        #self.segmentation_image.mouseDragEvent = self.mouseDragEvent

        # I heard you like connections
        self._model.image_changed.connect(self.on_image_change)
        self._model.segmentation_image_changed.connect(self.on_seg_image_change)
        self._ui.toggleSegmentationMaskButton.clicked.connect(self.mask_button_press)
        self._ui.actionImage_Manager.triggered.connect(self.launch_image_manager)
        self._ui.imageFileNavigatorView.currentIndexChanged.connect(self.current_image_changed)
        self._ui.loadAnalysisFileButton.clicked.connect(self.load_analysis_file_clicked)
        self._ui.filterButton.clicked.connect(self.launch_filter_manager)
        self._ui.AddRegionOfInterestButton.clicked.connect(self.add_roi)
        self._ui.clusterButton.clicked.connect(self.cluster_button_press)
        self._ui.ColorByClusterButton.clicked.connect(self.color_by_cluster_clicked)
        self._image_manager_controller.change_current_image.connect(self.current_image_changed)
        self._image_manager_controller.image_manager_window_closed.connect(self.update_file_list)
        self._seg_class_model.class_table_update.connect(self._filter_table_model.class_list_changed)
        self._filter_controller.filters_changed.connect(self.filter_objects_from_seg_image)
         

        self._current_image_index = -1

    def launch_image_manager(self):
        
        """
            Launches ImageManagerView GUI when the "Image Manager" is selected from the File menu
        """
        
        self._image_manager_view = ImageManagerView(self._file_table_model, self._image_manager_controller)
        self._image_manager_view.show()

    def launch_filter_manager(self):

        """
            Launches FilterManagerView GUI when the "Manage Filters" button is pressed
        """
        if self.all_models.object_data is not None:
            self._filter_manager_view = FilterManagerView(self._filter_table_model, self._main_controller, self._filter_controller)
            self._filter_manager_view.show()

    @pyqtSlot(list)
    def update_file_list(self, value):
        """
            Detects when the image list has changed in the file table model and updates the 
            image models accordingly.
        """
        self._current_image_index = -1

        for i in range(self._ui.imageFileNavigatorView.count(),0,-1):
            self._ui.imageFileNavigatorView.removeItem(i-1)

        for entry in value:
            filename = entry.split("/")[-1]
            self._ui.imageFileNavigatorView.addItem(filename)
            self.all_models.add_image_model(filename)
            self.all_models.add_seg_model(filename)
    
    @pyqtSlot(int)
    def current_image_changed(self, value):
        """
            Detects when the user has selected a new image to view and updates the models accordingly
        """

        if (self._current_image_index != self._ui.imageFileNavigatorView.currentIndex()):
            self.all_models.current_id = self._file_table_model._filelist[self._ui.imageFileNavigatorView.currentIndex()]
            self._current_image_index = self._ui.imageFileNavigatorView.currentIndex()
            self._main_controller.update_models_from_file_table(self._file_table_model._data[self._current_image_index])
            self._model.image_scale = float(self._file_table_model._data[self._current_image_index][3])
            self._ui.segmentationMaskFileDisplay.setText(self._model.segmentation_label)
        
    @pyqtSlot(int)
    def on_image_change(self, value):
        """
            Sets a new image to the ImageItem
        """
        self.current_image.setImage( self._model.image )

    @pyqtSlot(int)
    def on_seg_image_change(self, value):
        """
            Sets a new segmentation image to the ImageItem
        """

        if self._model.has_segmentation_image:
            self.segmentation_image.setImage(self._model.segmentation_image, opacity=self.segmentation_opacity)

    def mask_button_press(self):
        """
            Toggles the segmentation mask by changing the opacity of the segmentation image
        """

        self.segmentation_opacity = 1 - self.segmentation_opacity
        self.segmentation_image.setImage(self._model.segmentation_image, opacity=self.segmentation_opacity)
    
    def seg_class_data_change_request(self):
        """
           Detects when user wants to change the segmentation class color and notifies
           the main controller 
        """

        idx = self._ui.segmentationClassList.selectionModel().selectedIndexes()[0]

        if idx.column() == 0:
            self._main_controller.change_class_color(idx.row())
    
    def load_analysis_file_clicked(self):
        """
            Detects when the "Load Analysis File" button is clicked and notifies the
            main controller to load it. Then tells the filter controller to index all of the
            objects in the image.
        """
        if len(self._file_table_model._filelist) == 0:
            no_image_loaded_error_msg = QMessageBox(self)
            no_image_loaded_error_msg.setText("Can't load analysis file")
            no_image_loaded_error_msg.setDetailedText("Please load image file before loading analysis file.")
            no_image_loaded_error_msg.show()
        else:
            [tf, filename] = self._main_controller.load_analysis_file()
            if (self._model.has_segmentation_image) and tf:
                self._filter_controller.index_objects()
                self._ui.analysisFileDisplay.setText(filename)
    
    def filter_objects_from_seg_image(self):

        results_index = self._filter_controller.combine_filters()

        if results_index is not None:
            results = results_index['object_id'].values
        else:
            results = self.all_models.object_data['object_id'].values
        
        self.all_models.filter_results = results_index
        
        self._main_controller.construct_seg_image_from_objectids(results)

    def add_roi(self):
        
        #self.setROI = not self.setROI
        defaultx = self._model.segmentation_image.shape[0]/10
        defaulty = self._model.segmentation_image.shape[1]/10
        
        roi = pg.PolyLineROI([[0,0], [0,defaultx], [defaulty,defaultx], [defaulty,0]], closed=True)
        
        label = "ROI_" + str(len(self.all_models.rois.keys()) + 1)
        self.all_models.rois[label] = roi

        self._ui.graphicsView.view.addItem(roi)
        self._filter_table_model.non_class_filterable_object_list.append(label)
        self._filter_table_model.class_list_changed([row[0] for row in self._seg_class_model._color_table.values()])
    
    def update_roi_list(self):
        return
        #self.ROIListView.setModel(self.all_models.roi_model)

    def cluster_button_press(self):
        if self.all_models.filter_results is not None:
            try:
                min_dist = float( self._ui.ClusterMinDist.text() )
                min_neighbors = int(self._ui.ClusterMinNeighbors.text() )
                self._main_controller.cluster_objects(self.all_models.filter_results, min_dist, min_neighbors)
            except ValueError: print ( "Enter parameters for clustering")
        
        