# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MultiviewImageExplorer\resources\imageManager.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_ImageManagerMainWindow(object):
    def setupUi(self, ImageManagerMainWindow):
        ImageManagerMainWindow.setObjectName("ImageManagerMainWindow")
        ImageManagerMainWindow.resize(1200, 477)
        self.centralwidget = QtWidgets.QWidget(ImageManagerMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.addImageButton.setGeometry(QtCore.QRect(70, 400, 151, 23))
        #self.addImageButton.contentsMargins.setLeft(70)
        #self.addImageButton.contentsMargins.setTop(400)
        #self.addImageButton.contentsMargins.setRight(151)
        #self.addImageButton.contentsMargins.setBottom(23)

        self.addImageButton.setStyleSheet("background-color: rgb(120, 201, 172);")
        if sys.platform == 'darwin':
            self.addImageButton.setStyleSheet("margin: 0px")
        
        self.addImageButton.setObjectName("addImageButton")
        self.addSegmentationMaskButton = QtWidgets.QPushButton(self.centralwidget)
        self.addSegmentationMaskButton.setGeometry(QtCore.QRect(230, 400, 151, 23))
        self.addSegmentationMaskButton.setStyleSheet("background-color: rgb(172, 199, 241);")
        self.addSegmentationMaskButton.setObjectName("addSegmentationMaskButton")
        
        if sys.platform == 'darwin':
            self.addSegmentationMaskButton.setStyleSheet("margin: 0px")
        
        self.removeImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeImageButton.setGeometry(QtCore.QRect(610, 400, 151, 23))
        self.removeImageButton.setStyleSheet("background-color: rgb(230, 165, 187);")
        self.removeImageButton.setObjectName("removeImageButton")

        if sys.platform == 'darwin':
            self.removeImageButton.setStyleSheet("margin: 0px")

        self.imageManagerTableView = QtWidgets.QTableView(self.centralwidget)
        self.imageManagerTableView.setGeometry(QtCore.QRect(70, 30, 1030, 361))
        self.imageManagerTableView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.imageManagerTableView.setObjectName("imageManagerTableView")
        ImageManagerMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ImageManagerMainWindow)
        self.statusbar.setObjectName("statusbar")
        ImageManagerMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ImageManagerMainWindow)
        QtCore.QMetaObject.connectSlotsByName(ImageManagerMainWindow)

    def retranslateUi(self, ImageManagerMainWindow):
        _translate = QtCore.QCoreApplication.translate
        ImageManagerMainWindow.setWindowTitle(_translate("ImageManagerMainWindow", "MainWindow"))
        self.addImageButton.setText(_translate("ImageManagerMainWindow", "Add image"))
        self.addSegmentationMaskButton.setText(_translate("ImageManagerMainWindow", "Add segmentation mask"))
        self.removeImageButton.setText(_translate("ImageManagerMainWindow", "Remove image"))

