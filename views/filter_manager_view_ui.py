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
        FilterManagerMainWindow.resize(836, 544)
        self.centralwidget = QtWidgets.QWidget(FilterManagerMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addFilterButton = QtWidgets.QPushButton(self.centralwidget)
        self.addFilterButton.setGeometry(QtCore.QRect(70, 400, 151, 23))
        self.addFilterButton.setStyleSheet("background-color: rgb(120, 201, 172);")
        self.addFilterButton.setObjectName("addFilterButton")
        self.removeFilterButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeFilterButton.setGeometry(QtCore.QRect(610, 400, 151, 23))
        self.removeFilterButton.setStyleSheet("background-color: rgb(230, 165, 187);")
        self.removeFilterButton.setObjectName("removeFilterButton")
        self.FilterManagerTableView = QtWidgets.QTableView(self.centralwidget)
        self.FilterManagerTableView.setGeometry(QtCore.QRect(70, 30, 691, 361))
        self.FilterManagerTableView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.FilterManagerTableView.setObjectName("FilterManagerTableView")
        self.checkResultTextBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.checkResultTextBox.setGeometry(QtCore.QRect(70, 430, 691, 41))
        self.checkResultTextBox.setObjectName("checkResultTextBox")
        self.objectClassList = QtWidgets.QComboBox(self.centralwidget)
        self.objectClassList.setGeometry(QtCore.QRect(70, 490, 151, 22))
        self.objectClassList.setObjectName("objectClassList")
        self.filterLogicList = QtWidgets.QComboBox(self.centralwidget)
        self.filterLogicList.setGeometry(QtCore.QRect(230, 490, 101, 22))
        self.filterLogicList.setObjectName("filterLogicList")
        self.filterValueInput = QtWidgets.QLineEdit(self.centralwidget)
        self.filterValueInput.setGeometry(QtCore.QRect(340, 490, 113, 20))
        self.filterValueInput.setObjectName("filterValueInput")
        self.checkLogic = QtWidgets.QPushButton(self.centralwidget)
        self.checkLogic.setGeometry(QtCore.QRect(470, 490, 75, 23))
        self.checkLogic.setStyleSheet("background-color: rgb(172, 199, 241);")
        self.checkLogic.setObjectName("checkLogic")
        FilterManagerMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FilterManagerMainWindow)
        self.statusbar.setObjectName("statusbar")
        FilterManagerMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(FilterManagerMainWindow)
        QtCore.QMetaObject.connectSlotsByName(FilterManagerMainWindow)

    def retranslateUi(self, FilterManagerMainWindow):
        _translate = QtCore.QCoreApplication.translate
        FilterManagerMainWindow.setWindowTitle(_translate("FilterManagerMainWindow", "MainWindow"))
        self.addFilterButton.setText(_translate("FilterManagerMainWindow", "Add filter"))
        self.removeFilterButton.setText(_translate("FilterManagerMainWindow", "Remove filter"))
        self.checkLogic.setText(_translate("FilterManagerMainWindow", "Check"))

