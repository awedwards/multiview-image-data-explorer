# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1031, 928)
        MainWindow.setStyleSheet("background-color: rgb(245,245,245);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.imageFileNavigatorView = QtWidgets.QComboBox(self.centralwidget)
        self.imageFileNavigatorView.setGeometry(QtCore.QRect(410, 660, 181, 22))
        self.imageFileNavigatorView.setStyleSheet("background-color: rgb(255,255,255);")
        self.imageFileNavigatorView.setObjectName("imageFileNavigatorView")
        self.toggleSegmentationMaskButton = QtWidgets.QPushButton(self.centralwidget)
        self.toggleSegmentationMaskButton.setGeometry(QtCore.QRect(10, 680, 111, 23))
        self.toggleSegmentationMaskButton.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(120, 201, 172);")
        self.toggleSegmentationMaskButton.setObjectName("toggleSegmentationMaskButton")
        self.segmentationMaskFileDisplay = QtWidgets.QLineEdit(self.centralwidget)
        self.segmentationMaskFileDisplay.setGeometry(QtCore.QRect(10, 660, 113, 20))
        self.segmentationMaskFileDisplay.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.segmentationMaskFileDisplay.setObjectName("segmentationMaskFileDisplay")
        self.loadAnalysisFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadAnalysisFileButton.setGeometry(QtCore.QRect(410, 690, 111, 23))
        self.loadAnalysisFileButton.setStyleSheet("background-color: rgb(252, 205, 64);")
        self.loadAnalysisFileButton.setObjectName("loadAnalysisFileButton")
        self.analysisFileDisplay = QtWidgets.QLineEdit(self.centralwidget)
        self.analysisFileDisplay.setGeometry(QtCore.QRect(410, 720, 131, 20))
        self.analysisFileDisplay.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.analysisFileDisplay.setObjectName("analysisFileDisplay")
        self.filterButton = QtWidgets.QPushButton(self.centralwidget)
        self.filterButton.setGeometry(QtCore.QRect(830, 800, 181, 31))
        self.filterButton.setStyleSheet("background-color: rgb(172, 199, 241);")
        self.filterButton.setObjectName("filterButton")
        self.segmentationClassList = QtWidgets.QTableView(self.centralwidget)
        self.segmentationClassList.setGeometry(QtCore.QRect(130, 660, 256, 192))
        self.segmentationClassList.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.segmentationClassList.setObjectName("segmentationClassList")
        self.graphicsView = ImageView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 1011, 641))
        self.graphicsView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.graphicsView.setObjectName("graphicsView")
        self.filterListView = QtWidgets.QListView(self.centralwidget)
        self.filterListView.setGeometry(QtCore.QRect(820, 660, 201, 131))
        self.filterListView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.filterListView.setObjectName("filterListView")
        self.ROIListView = QtWidgets.QListWidget(self.centralwidget)
        self.ROIListView.setGeometry(QtCore.QRect(600, 660, 201, 131))
        self.ROIListView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ROIListView.setObjectName("ROIListView")
        self.AddRegionOfInterestButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddRegionOfInterestButton.setGeometry(QtCore.QRect(600, 800, 101, 21))
        self.AddRegionOfInterestButton.setStyleSheet("background-color: rgb(120, 201, 172);")
        self.AddRegionOfInterestButton.setObjectName("AddRegionOfInterestButton")
        self.RemoveRegionOfInterestButton = QtWidgets.QPushButton(self.centralwidget)
        self.RemoveRegionOfInterestButton.setGeometry(QtCore.QRect(710, 800, 91, 23))
        self.RemoveRegionOfInterestButton.setStyleSheet("background-color: rgb(230, 165, 187);")
        self.RemoveRegionOfInterestButton.setObjectName("RemoveRegionOfInterestButton")
        self.clusterButton = QtWidgets.QPushButton(self.centralwidget)
        self.clusterButton.setGeometry(QtCore.QRect(410, 760, 75, 23))
        self.clusterButton.setStyleSheet("background-color: rgb(172, 199, 241);")
        self.clusterButton.setObjectName("clusterButton")
        self.ClusterMinDist = QtWidgets.QLineEdit(self.centralwidget)
        self.ClusterMinDist.setGeometry(QtCore.QRect(410, 810, 113, 20))
        self.ClusterMinDist.setObjectName("ClusterMinDist")
        self.ClusterMinNeighbors = QtWidgets.QLineEdit(self.centralwidget)
        self.ClusterMinNeighbors.setGeometry(QtCore.QRect(410, 850, 113, 20))
        self.ClusterMinNeighbors.setObjectName("ClusterMinNeighbors")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(410, 790, 141, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(410, 830, 171, 16))
        self.label_2.setObjectName("label_2")
        self.ColorByClusterButton = QtWidgets.QPushButton(self.centralwidget)
        self.ColorByClusterButton.setGeometry(QtCore.QRect(490, 760, 101, 23))
        self.ColorByClusterButton.setStyleSheet("background-color: rgb(172, 199, 241);")
        self.ColorByClusterButton.setObjectName("ColorByClusterButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLoad_Project = QtWidgets.QAction(MainWindow)
        self.actionLoad_Project.setObjectName("actionLoad_Project")
        self.actionSave_Project = QtWidgets.QAction(MainWindow)
        self.actionSave_Project.setObjectName("actionSave_Project")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionImage_Manager = QtWidgets.QAction(MainWindow)
        self.actionImage_Manager.setObjectName("actionImage_Manager")
        self.actionNew_Project = QtWidgets.QAction(MainWindow)
        self.actionNew_Project.setObjectName("actionNew_Project")
        self.actionNight_mode = QtWidgets.QAction(MainWindow)
        self.actionNight_mode.setObjectName("actionNight_mode")
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionLoad_Project)
        self.menuFile.addAction(self.actionSave_Project)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionImage_Manager)
        self.menuView.addAction(self.actionNight_mode)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toggleSegmentationMaskButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Click to toggle the segmentation mask overlay (if exists)</p></body></html>"))
        self.toggleSegmentationMaskButton.setText(_translate("MainWindow", "Object Mask"))
        self.segmentationMaskFileDisplay.setText(_translate("MainWindow", "No mask"))
        self.loadAnalysisFileButton.setText(_translate("MainWindow", "Load analysis file"))
        self.analysisFileDisplay.setText(_translate("MainWindow", "No analysis file"))
        self.filterButton.setText(_translate("MainWindow", "Configure filters"))
        self.AddRegionOfInterestButton.setText(_translate("MainWindow", "Add ROI"))
        self.RemoveRegionOfInterestButton.setText(_translate("MainWindow", "Delete ROI"))
        self.clusterButton.setText(_translate("MainWindow", "Cluster"))
        self.label.setText(_translate("MainWindow", "Min dist between neighbors"))
        self.label_2.setText(_translate("MainWindow", "Min number of objects per cluster"))
        self.ColorByClusterButton.setText(_translate("MainWindow", "Color by Cluster"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionLoad_Project.setText(_translate("MainWindow", "Load Project"))
        self.actionSave_Project.setText(_translate("MainWindow", "Save Project"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))
        self.actionImage_Manager.setText(_translate("MainWindow", "Image Manager"))
        self.actionNew_Project.setText(_translate("MainWindow", "New Project"))
        self.actionNight_mode.setText(_translate("MainWindow", "Toggle night mode"))

from pyqtgraph import ImageView
