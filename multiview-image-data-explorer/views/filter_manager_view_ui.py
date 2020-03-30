# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filterManager.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FilterManagerMainWindow(object):
    def setupUi(self, FilterManagerMainWindow):
        FilterManagerMainWindow.setObjectName("FilterManagerMainWindow")
        FilterManagerMainWindow.resize(836, 365)
        self.centralwidget = QtWidgets.QWidget(FilterManagerMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.applyFilterButton = QtWidgets.QPushButton(self.centralwidget)
        self.applyFilterButton.setGeometry(QtCore.QRect(70, 320, 151, 23))
        self.applyFilterButton.setStyleSheet("background-color: rgb(120, 201, 172);")
        self.applyFilterButton.setObjectName("applyFilterButton")
        self.resetFilterSettingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetFilterSettingsButton.setGeometry(QtCore.QRect(70, 290, 151, 23))
        self.resetFilterSettingsButton.setStyleSheet("background-color: rgb(230, 165, 187);")
        self.resetFilterSettingsButton.setObjectName("resetFilterSettingsButton")
        self.totalObjectsLabel = QtWidgets.QLabel(self.centralwidget)
        self.totalObjectsLabel.setGeometry(QtCore.QRect(440, 290, 131, 20))
        self.totalObjectsLabel.setObjectName("totalObjectsLabel")
        self.totalResultsTextBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.totalResultsTextBox.setGeometry(QtCore.QRect(570, 290, 191, 21))
        self.totalResultsTextBox.setStyleSheet("font: 7pt \"MS Shell Dlg 2\";")
        self.totalResultsTextBox.setObjectName("totalResultsTextBox")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(70, 10, 691, 271))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 689, 269))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.filterObjectsList = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents)
        self.filterObjectsList.setGeometry(QtCore.QRect(0, 0, 691, 271))
        self.filterObjectsList.setObjectName("filterObjectsList")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        FilterManagerMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FilterManagerMainWindow)
        self.statusbar.setObjectName("statusbar")
        FilterManagerMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(FilterManagerMainWindow)
        QtCore.QMetaObject.connectSlotsByName(FilterManagerMainWindow)

    def retranslateUi(self, FilterManagerMainWindow):
        _translate = QtCore.QCoreApplication.translate
        FilterManagerMainWindow.setWindowTitle(_translate("FilterManagerMainWindow", "MainWindow"))
        self.applyFilterButton.setText(_translate("FilterManagerMainWindow", "Apply"))
        self.resetFilterSettingsButton.setText(_translate("FilterManagerMainWindow", "Reset to default"))
        self.totalObjectsLabel.setText(_translate("FilterManagerMainWindow", "Total objects after filtering"))

