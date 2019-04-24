# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\filterManager.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FilterManagerMainWindow(object):
    def setupUi(self, FilterManagerMainWindow):
        FilterManagerMainWindow.setObjectName("FilterManagerMainWindow")
        FilterManagerMainWindow.resize(836, 533)
        self.centralwidget = QtWidgets.QWidget(FilterManagerMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addFilterButton = QtWidgets.QPushButton(self.centralwidget)
        self.addFilterButton.setGeometry(QtCore.QRect(70, 440, 151, 23))
        self.addFilterButton.setStyleSheet("background-color: rgb(120, 201, 172);")
        self.addFilterButton.setObjectName("addFilterButton")
        self.removeFilterButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeFilterButton.setGeometry(QtCore.QRect(610, 440, 151, 23))
        self.removeFilterButton.setStyleSheet("background-color: rgb(230, 165, 187);")
        self.removeFilterButton.setObjectName("removeFilterButton")
        self.FilterManagerTableView = QtWidgets.QTableView(self.centralwidget)
        self.FilterManagerTableView.setGeometry(QtCore.QRect(70, 30, 691, 361))
        self.FilterManagerTableView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.FilterManagerTableView.setObjectName("FilterManagerTableView")
        self.checkResultTextBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.checkResultTextBox.setGeometry(QtCore.QRect(570, 480, 191, 21))
        self.checkResultTextBox.setStyleSheet("font: 7pt \"MS Shell Dlg 2\";")
        self.checkResultTextBox.setObjectName("checkResultTextBox")
        self.objectClassList = QtWidgets.QComboBox(self.centralwidget)
        self.objectClassList.setGeometry(QtCore.QRect(70, 480, 151, 22))
        self.objectClassList.setObjectName("objectClassList")
        self.filterLogicList = QtWidgets.QComboBox(self.centralwidget)
        self.filterLogicList.setGeometry(QtCore.QRect(230, 480, 101, 22))
        self.filterLogicList.setObjectName("filterLogicList")
        self.filterValueInput = QtWidgets.QLineEdit(self.centralwidget)
        self.filterValueInput.setGeometry(QtCore.QRect(340, 480, 113, 20))
        self.filterValueInput.setObjectName("filterValueInput")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(490, 480, 81, 20))
        self.label.setObjectName("label")
        self.ANDRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.ANDRadioButton.setGeometry(QtCore.QRect(70, 400, 82, 17))
        self.ANDRadioButton.setObjectName("ANDRadioButton")
        self.ORRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.ORRadioButton.setGeometry(QtCore.QRect(120, 400, 82, 17))
        self.ORRadioButton.setObjectName("ORRadioButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(440, 400, 131, 20))
        self.label_2.setObjectName("label_2")
        self.totalResultsTextBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.totalResultsTextBox.setGeometry(QtCore.QRect(570, 400, 191, 21))
        self.totalResultsTextBox.setStyleSheet("font: 7pt \"MS Shell Dlg 2\";")
        self.totalResultsTextBox.setObjectName("totalResultsTextBox")
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
        self.label.setText(_translate("FilterManagerMainWindow", "Objects in filter"))
        self.ANDRadioButton.setText(_translate("FilterManagerMainWindow", "AND"))
        self.ORRadioButton.setText(_translate("FilterManagerMainWindow", "OR"))
        self.label_2.setText(_translate("FilterManagerMainWindow", "Total objects after filtering"))

