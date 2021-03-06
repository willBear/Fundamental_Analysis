# ---------------------------------------------------------------------------------------------------------
# Author: Will Bear
# File Name: Fundamental_Analysis.py
# Version: 0.1-alpha
#
#
# Functionality:
# This PyQT5 programme is used to provide an overview of the North American Stock Indexes during
# and after trading hours. Additionally, this project allows its users to search up a stock using
# its tickers (currently limited to North American Equities & ETFs) and see its relevant information
# that may help an investor to decide whether or not he / she will purchase the stock.
#
# The information shown from the stock search functionality consist of fundamental information as
# well as technical information. On the fundamental side, the said company's growth information is
# displayed along with its percentages, all provided by Financial Modelling Prep Website.
# Technical information that are shown are the hourly moving averages, its support / resistances
# as well as pivot points. Furthermore, an Moving Average Convergence / Divergence graph is displayed
# to further aide the future investments of an investor.
#
# Lastly, this programme offers its users sector performances of the broader market both live and
# selected aggregated time to further aide its users to determine the section he/she may wish to
# invest in
# ---------------------------------------------------------------------------------------------------------

from datetime import datetime

import investpy
import pyqtgraph as pg
import requests
import urllib
import webbrowser
# Import statements for the programme
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup

# Two of the main API providers we use in this project are Alpha Vantage and Financial Modelling Prep
# For further information on these providers please visit their websites at:
#
# Alpha Vantage: https://www.alphavantage.co
# Financial Modelling Prep: https://financialmodelingprep.com/
alpha_vantage_api_key = "4NE2ALTFPGT83V3S"
financial_modelling_prep_api_key = 'a595a30dbf0ad8470cb8d0e350ccffa0'

# *********************************************************************************************************
# Class Name: Ui_MainWindow
#
# Functionality:
# This class is generated using the pyuic5 functionality that are within the PyQT5 package. UI file is
# first completed using the drag and drop UI application of QT Designer. This class is used mainly to
# serve as an application container for information that we are going to retrieve from the API providers
# as well as any input from the user
# *********************************************************************************************************
class Ui_MainWindow(object):
    # -------------------------------------------------------------------
    # Function Name: setupUi
    #
    # Functionality:
    # This function serves the purposes of setting up all widgets that
    # are in the PyQT5 application, such as assignment names, font, size
    # location etc.
    # -------------------------------------------------------------------
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1024, 768)
        MainWindow.setMouseTracking(False)
        MainWindow.setAcceptDrops(False)
        MainWindow.setAccessibleName("")
        MainWindow.setAccessibleDescription("")
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        MainWindow.setInputMethodHints(QtCore.Qt.ImhNone)
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TimeNow_Label = QtWidgets.QLabel(self.centralwidget)
        self.TimeNow_Label.setGeometry(QtCore.QRect(5, 32, 90, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.TimeNow_Label.setFont(font)
        self.TimeNow_Label.setMouseTracking(False)
        self.TimeNow_Label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TimeNow_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.TimeNow_Label.setWordWrap(True)
        self.TimeNow_Label.setObjectName("TimeNow_Label")
        self.DateNow_Label = QtWidgets.QLabel(self.centralwidget)
        self.DateNow_Label.setGeometry(QtCore.QRect(4, 10, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.DateNow_Label.setFont(font)
        self.DateNow_Label.setMouseTracking(False)
        self.DateNow_Label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.DateNow_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.DateNow_Label.setWordWrap(True)
        self.DateNow_Label.setObjectName("DateNow_Label")
        self.Index_Symbol_0 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Symbol_0.setGeometry(QtCore.QRect(100, 10, 40, 20))
        self.Index_Symbol_0.setObjectName("Index_Symbol_0")
        self.Index_Percentage_0 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Percentage_0.setGeometry(QtCore.QRect(100, 55, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Index_Percentage_0.setFont(font)
        self.Index_Percentage_0.setObjectName("Index_Percentage_0")
        self.Index_Price_0 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Price_0.setGeometry(QtCore.QRect(185, 10, 45, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.Index_Price_0.setFont(font)
        self.Index_Price_0.setObjectName("Index_Price_0")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(95, 10, 3, 61))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(230, 10, 3, 61))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.Index_Symbol_1 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Symbol_1.setGeometry(QtCore.QRect(235, 10, 40, 20))
        self.Index_Symbol_1.setObjectName("Index_Symbol_1")
        self.Index_Percentage_1 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Percentage_1.setGeometry(QtCore.QRect(235, 55, 50, 15))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Index_Percentage_1.setFont(font)
        self.Index_Percentage_1.setObjectName("Index_Percentage_1")
        self.Index_Price_1 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Price_1.setGeometry(QtCore.QRect(320, 10, 45, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.Index_Price_1.setFont(font)
        self.Index_Price_1.setObjectName("Index_Price_1")
        self.Index_Percentage_2 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Percentage_2.setGeometry(QtCore.QRect(370, 55, 50, 15))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Index_Percentage_2.setFont(font)
        self.Index_Percentage_2.setObjectName("Index_Percentage_2")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(365, 10, 3, 61))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.Index_Symbol_2 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Symbol_2.setGeometry(QtCore.QRect(370, 10, 40, 20))
        self.Index_Symbol_2.setObjectName("Index_Symbol_2")
        self.Index_Price_2 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Price_2.setGeometry(QtCore.QRect(450, 10, 45, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.Index_Price_2.setFont(font)
        self.Index_Price_2.setObjectName("Index_Price_2")
        self.Index_Percentage_3 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Percentage_3.setGeometry(QtCore.QRect(505, 55, 50, 15))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Index_Percentage_3.setFont(font)
        self.Index_Percentage_3.setObjectName("Index_Percentage_3")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(500, 10, 3, 61))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.Index_Symbol_3 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Symbol_3.setGeometry(QtCore.QRect(505, 10, 40, 20))
        self.Index_Symbol_3.setObjectName("Index_Symbol_3")
        self.Index_Price_3 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Price_3.setGeometry(QtCore.QRect(590, 10, 45, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.Index_Price_3.setFont(font)
        self.Index_Price_3.setObjectName("Index_Price_3")
        self.Index_Percentage_4 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Percentage_4.setGeometry(QtCore.QRect(640, 55, 50, 15))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Index_Percentage_4.setFont(font)
        self.Index_Percentage_4.setObjectName("Index_Percentage_4")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(635, 10, 3, 61))
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.Index_Symbol_4 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Symbol_4.setGeometry(QtCore.QRect(640, 10, 40, 20))
        self.Index_Symbol_4.setObjectName("Index_Symbol_4")
        self.Index_Price_4 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Price_4.setGeometry(QtCore.QRect(725, 10, 45, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.Index_Price_4.setFont(font)
        self.Index_Price_4.setObjectName("Index_Price_4")
        self.Index_Percentage_5 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Percentage_5.setGeometry(QtCore.QRect(775, 55, 50, 15))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Index_Percentage_5.setFont(font)
        self.Index_Percentage_5.setObjectName("Index_Percentage_5")
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setGeometry(QtCore.QRect(770, 10, 3, 61))
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.Index_Symbol_5 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Symbol_5.setGeometry(QtCore.QRect(775, 10, 40, 20))
        self.Index_Symbol_5.setObjectName("Index_Symbol_5")
        self.Index_Price_5 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Price_5.setGeometry(QtCore.QRect(860, 10, 45, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.Index_Price_5.setFont(font)
        self.Index_Price_5.setObjectName("Index_Price_5")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 75, 1024, 5))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setGeometry(QtCore.QRect(905, 10, 3, 61))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.Index_Percentage_6 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Percentage_6.setGeometry(QtCore.QRect(910, 55, 50, 15))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Index_Percentage_6.setFont(font)
        self.Index_Percentage_6.setObjectName("Index_Percentage_6")
        self.Index_Symbol_6 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Symbol_6.setGeometry(QtCore.QRect(910, 10, 40, 20))
        self.Index_Symbol_6.setObjectName("Index_Symbol_6")
        self.Index_Price_6 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Price_6.setGeometry(QtCore.QRect(980, 10, 45, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.Index_Price_6.setFont(font)
        self.Index_Price_6.setObjectName("Index_Price_6")
        self.Index_Name_0 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Name_0.setGeometry(QtCore.QRect(100, 32, 130, 21))
        self.Index_Name_0.setObjectName("Index_Name_0")
        self.Index_Name_1 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Name_1.setGeometry(QtCore.QRect(235, 32, 130, 21))
        self.Index_Name_1.setObjectName("Index_Name_1")
        self.Index_Name_2 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Name_2.setGeometry(QtCore.QRect(370, 32, 130, 21))
        self.Index_Name_2.setObjectName("Index_Name_2")
        self.Index_Name_3 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Name_3.setGeometry(QtCore.QRect(505, 32, 130, 21))
        self.Index_Name_3.setObjectName("Index_Name_3")
        self.Index_Name_4 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Name_4.setGeometry(QtCore.QRect(640, 32, 130, 21))
        self.Index_Name_4.setObjectName("Index_Name_4")
        self.Index_Name_5 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Name_5.setGeometry(QtCore.QRect(775, 32, 130, 21))
        self.Index_Name_5.setObjectName("Index_Name_5")
        self.Index_Name_6 = QtWidgets.QLabel(self.centralwidget)
        self.Index_Name_6.setGeometry(QtCore.QRect(910, 32, 130, 21))
        self.Index_Name_6.setObjectName("Index_Name_6")
        self.Sector_Name_0 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Name_0.setGeometry(QtCore.QRect(14, 710, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sector_Name_0.setFont(font)
        self.Sector_Name_0.setObjectName("Sector_Name_0")
        self.Sector_Percentage_0 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Percentage_0.setGeometry(QtCore.QRect(154, 710, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Percentage_0.setFont(font)
        self.Sector_Percentage_0.setObjectName("Sector_Percentage_0")
        self.Sector_Percentage_1 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Percentage_1.setGeometry(QtCore.QRect(154, 740, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Percentage_1.setFont(font)
        self.Sector_Percentage_1.setObjectName("Sector_Percentage_1")
        self.Sector_Name_1 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Name_1.setGeometry(QtCore.QRect(14, 740, 39, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sector_Name_1.setFont(font)
        self.Sector_Name_1.setObjectName("Sector_Name_1")
        self.Sector_Percentage_2 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Percentage_2.setGeometry(QtCore.QRect(364, 710, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Percentage_2.setFont(font)
        self.Sector_Percentage_2.setObjectName("Sector_Percentage_2")
        self.Sector_Name_2 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Name_2.setGeometry(QtCore.QRect(214, 710, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sector_Name_2.setFont(font)
        self.Sector_Name_2.setObjectName("Sector_Name_2")
        self.Sector_Percentage_3 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Percentage_3.setGeometry(QtCore.QRect(364, 740, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Percentage_3.setFont(font)
        self.Sector_Percentage_3.setObjectName("Sector_Percentage_3")
        self.Sector_Name_3 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Name_3.setGeometry(QtCore.QRect(214, 740, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sector_Name_3.setFont(font)
        self.Sector_Name_3.setObjectName("Sector_Name_3")
        self.Sector_Percentage_4 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Percentage_4.setGeometry(QtCore.QRect(564, 710, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Percentage_4.setFont(font)
        self.Sector_Percentage_4.setObjectName("Sector_Percentage_4")
        self.Sector_Name_4 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Name_4.setGeometry(QtCore.QRect(424, 710, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sector_Name_4.setFont(font)
        self.Sector_Name_4.setObjectName("Sector_Name_4")
        self.Sector_Percentage_5 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Percentage_5.setGeometry(QtCore.QRect(564, 740, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Percentage_5.setFont(font)
        self.Sector_Percentage_5.setObjectName("Sector_Percentage_5")
        self.Sector_Name_5 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Name_5.setGeometry(QtCore.QRect(424, 740, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sector_Name_5.setFont(font)
        self.Sector_Name_5.setObjectName("Sector_Name_5")
        self.Sector_Percentage_6 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Percentage_6.setGeometry(QtCore.QRect(764, 710, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Percentage_6.setFont(font)
        self.Sector_Percentage_6.setObjectName("Sector_Percentage_6")
        self.Sector_Name_6 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Name_6.setGeometry(QtCore.QRect(624, 710, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sector_Name_6.setFont(font)
        self.Sector_Name_6.setObjectName("Sector_Name_6")
        self.Sector_Percentage_7 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Percentage_7.setGeometry(QtCore.QRect(764, 740, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Percentage_7.setFont(font)
        self.Sector_Percentage_7.setObjectName("Sector_Percentage_7")
        self.Sector_Name_7 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Name_7.setGeometry(QtCore.QRect(624, 740, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sector_Name_7.setFont(font)
        self.Sector_Name_7.setObjectName("Sector_Name_7")
        self.Sector_Name_9 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Name_9.setGeometry(QtCore.QRect(824, 740, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sector_Name_9.setFont(font)
        self.Sector_Name_9.setObjectName("Sector_Name_9")
        self.Sector_Percentage_9 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Percentage_9.setGeometry(QtCore.QRect(964, 740, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Percentage_9.setFont(font)
        self.Sector_Percentage_9.setObjectName("Sector_Percentage_9")
        self.Sector_Name_8 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Name_8.setGeometry(QtCore.QRect(824, 710, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sector_Name_8.setFont(font)
        self.Sector_Name_8.setObjectName("Sector_Name_8")
        self.Sector_Percentage_8 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Percentage_8.setGeometry(QtCore.QRect(964, 710, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Percentage_8.setFont(font)
        self.Sector_Percentage_8.setObjectName("Sector_Percentage_8")
        self.Sector_Performance_Title = QtWidgets.QComboBox(self.centralwidget)
        self.Sector_Performance_Title.setGeometry(QtCore.QRect(780, 680, 231, 25))
        self.Sector_Performance_Title.setObjectName("Sector_Performance_Title")
        self.Sector_Performance_Title.addItem("")
        self.Sector_Performance_Title.addItem("")
        self.Sector_Performance_Title.addItem("")
        self.Sector_Performance_Title.addItem("")
        self.Sector_Performance_Title.addItem("")
        self.Sector_Performance_Title.addItem("")
        self.Sector_Performance_Title.addItem("")
        self.Sector_Performance_Title.addItem("")
        self.Sector_Performance_Title.addItem("")
        self.Sector_Performance_Title.addItem("")
        self.Sector_Performance_Title_2 = QtWidgets.QLabel(self.centralwidget)
        self.Sector_Performance_Title_2.setGeometry(QtCore.QRect(437, 680, 150, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Sector_Performance_Title_2.setFont(font)
        self.Sector_Performance_Title_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Sector_Performance_Title_2.setObjectName("Sector_Performance_Title_2")
        self.Marke_Open_Label = QtWidgets.QLabel(self.centralwidget)
        self.Marke_Open_Label.setGeometry(QtCore.QRect(5, 55, 90, 15))
        self.Marke_Open_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Marke_Open_Label.setObjectName("Marke_Open_Label")
        self.Search_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Search_Button.setGeometry(QtCore.QRect(105, 82, 25, 21))
        self.Search_Button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Search_Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Search_Button.setIcon(icon)
        self.Search_Button.setIconSize(QtCore.QSize(21, 21))
        self.Search_Button.setObjectName("Search_Button")
        self.Search_Bar = QtWidgets.QLineEdit(self.centralwidget)
        self.Search_Bar.setGeometry(QtCore.QRect(5, 82, 100, 20))
        self.Search_Bar.setObjectName("Search_Bar")
        self.Stock_Symbol = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Symbol.setGeometry(QtCore.QRect(150, 82, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Symbol.setFont(font)
        self.Stock_Symbol.setObjectName("Stock_Symbol")
        self.Stock_Description_Header = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Description_Header.setGeometry(QtCore.QRect(150, 130, 81, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Description_Header.setFont(font)
        self.Stock_Description_Header.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Description_Header.setObjectName("Stock_Description_Header")
        self.Stock_Description = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Description.setGeometry(QtCore.QRect(150, 150, 371, 131))
        self.Stock_Description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Stock_Description.setWordWrap(True)
        self.Stock_Description.setObjectName("Stock_Description")
        self.Stock_Image = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Image.setGeometry(QtCore.QRect(15, 130, 100, 100))
        self.Stock_Image.setScaledContents(True)
        self.Stock_Image.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Image.setObjectName("Stock_Image")
        self.Stock_Industry_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Industry_Title.setGeometry(QtCore.QRect(540, 150, 100, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Industry_Title.setFont(font)
        self.Stock_Industry_Title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Industry_Title.setObjectName("Stock_Industry_Title")
        self.Stock_Exchange_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Exchange_Title.setGeometry(QtCore.QRect(540, 170, 100, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Exchange_Title.setFont(font)
        self.Stock_Exchange_Title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Exchange_Title.setOpenExternalLinks(False)
        self.Stock_Exchange_Title.setObjectName("Stock_Exchange_Title")
        self.Stock_Industry = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Industry.setGeometry(QtCore.QRect(640, 150, 131, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Industry.setFont(font)
        self.Stock_Industry.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Industry.setObjectName("Stock_Industry")
        self.Stock_Exchange = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Exchange.setGeometry(QtCore.QRect(640, 170, 120, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Exchange.setFont(font)
        self.Stock_Exchange.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Exchange.setObjectName("Stock_Exchange")
        self.Stock_Price = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Price.setGeometry(QtCore.QRect(225, 82, 50, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Price.setFont(font)
        self.Stock_Price.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Price.setObjectName("Stock_Price")
        self.Stock_Percentage_Change = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Percentage_Change.setGeometry(QtCore.QRect(285, 82, 50, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Percentage_Change.setFont(font)
        self.Stock_Percentage_Change.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Percentage_Change.setObjectName("Stock_Percentage_Change")
        self.Stock_Volume = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Volume.setGeometry(QtCore.QRect(680, 82, 125, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Volume.setFont(font)
        self.Stock_Volume.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Volume.setObjectName("Stock_Volume")
        self.Stock_Line_1 = QtWidgets.QFrame(self.centralwidget)
        self.Stock_Line_1.setGeometry(QtCore.QRect(0, 105, 1024, 5))
        self.Stock_Line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.Stock_Line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Stock_Line_1.setObjectName("Stock_Line_1")
        self.Stock_Line_2 = QtWidgets.QFrame(self.centralwidget)
        self.Stock_Line_2.setGeometry(QtCore.QRect(0, 130, 1024, 5))
        self.Stock_Line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.Stock_Line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Stock_Line_2.setObjectName("Stock_Line_2")
        self.Stock_Name = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Name.setGeometry(QtCore.QRect(0, 110, 1024, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Name.setFont(font)
        self.Stock_Name.setStyleSheet("Background-color:rgb(128, 0, 128); Color:White")
        self.Stock_Name.setObjectName("Stock_Name")
        self.Stock_Market_Capitalization_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Market_Capitalization_Title.setGeometry(QtCore.QRect(775, 150, 81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Market_Capitalization_Title.setFont(font)
        self.Stock_Market_Capitalization_Title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Market_Capitalization_Title.setObjectName("Stock_Market_Capitalization_Title")
        self.Stock_Beta = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Beta.setGeometry(QtCore.QRect(810, 82, 80, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Beta.setFont(font)
        self.Stock_Beta.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Beta.setObjectName("Stock_Beta")
        self.Stock_Open = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Open.setGeometry(QtCore.QRect(350, 82, 100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Open.setFont(font)
        self.Stock_Open.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Open.setObjectName("Stock_Open")
        self.Stock_High = QtWidgets.QLabel(self.centralwidget)
        self.Stock_High.setGeometry(QtCore.QRect(450, 82, 100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_High.setFont(font)
        self.Stock_High.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_High.setObjectName("Stock_High")
        self.Stock_Low = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Low.setGeometry(QtCore.QRect(550, 82, 100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Low.setFont(font)
        self.Stock_Low.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Low.setObjectName("Stock_Low")
        self.Stock_Earnings_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Earnings_Title.setGeometry(QtCore.QRect(775, 170, 81, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Earnings_Title.setFont(font)
        self.Stock_Earnings_Title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Earnings_Title.setOpenExternalLinks(False)
        self.Stock_Earnings_Title.setObjectName("Stock_Earnings_Title")
        self.Stock_Market_Capitalization = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Market_Capitalization.setGeometry(QtCore.QRect(860, 150, 120, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Market_Capitalization.setFont(font)
        self.Stock_Market_Capitalization.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Market_Capitalization.setObjectName("Stock_Market_Capitalization")
        self.Stock_Earnings = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Earnings.setGeometry(QtCore.QRect(860, 170, 120, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Earnings.setFont(font)
        self.Stock_Earnings.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Earnings.setObjectName("Stock_Earnings")
        self.Stock_AverageVolume_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_AverageVolume_Title.setGeometry(QtCore.QRect(775, 190, 81, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_AverageVolume_Title.setFont(font)
        self.Stock_AverageVolume_Title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_AverageVolume_Title.setOpenExternalLinks(False)
        self.Stock_AverageVolume_Title.setObjectName("Stock_AverageVolume_Title")
        self.Stock_Average_Volume = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Average_Volume.setGeometry(QtCore.QRect(860, 190, 120, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Average_Volume.setFont(font)
        self.Stock_Average_Volume.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Average_Volume.setObjectName("Stock_Average_Volume")
        self.Stock_View_Chart = QtWidgets.QPushButton(self.centralwidget)
        self.Stock_View_Chart.setGeometry(QtCore.QRect(15, 250, 100, 31))
        self.Stock_View_Chart.setStyleSheet("Background-Color:rgb(41, 91, 128);Color:White;Font:Bold")
        self.Stock_View_Chart.setObjectName("Stock_View_Chart")
        self.Stock_Avg_Price_200_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Avg_Price_200_Title.setGeometry(QtCore.QRect(540, 190, 100, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Avg_Price_200_Title.setFont(font)
        self.Stock_Avg_Price_200_Title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Stock_Avg_Price_200_Title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Avg_Price_200_Title.setOpenExternalLinks(False)
        self.Stock_Avg_Price_200_Title.setObjectName("Stock_Avg_Price_200_Title")
        self.Stock_Avg_Price_200 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Avg_Price_200.setGeometry(QtCore.QRect(640, 190, 120, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Avg_Price_200.setFont(font)
        self.Stock_Avg_Price_200.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_Avg_Price_200.setObjectName("Stock_Avg_Price_200")
        self.Stock_Line_3 = QtWidgets.QFrame(self.centralwidget)
        self.Stock_Line_3.setGeometry(QtCore.QRect(0, 290, 1024, 5))
        self.Stock_Line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.Stock_Line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Stock_Line_3.setObjectName("Stock_Line_3")
        self.Stock_Line_4 = QtWidgets.QFrame(self.centralwidget)
        self.Stock_Line_4.setGeometry(QtCore.QRect(10, 670, 1024, 5))
        self.Stock_Line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.Stock_Line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Stock_Line_4.setObjectName("Stock_Line_4")
        self.Stock_Growth_Financia_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Financia_Title.setGeometry(QtCore.QRect(150, 300, 271, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Financia_Title.setFont(font)
        self.Stock_Growth_Financia_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Financia_Title.setObjectName("Stock_Growth_Financia_Title")
        self.Stock_Gross_Profit_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Gross_Profit_Title.setGeometry(QtCore.QRect(10, 340, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Gross_Profit_Title.setFont(font)
        self.Stock_Gross_Profit_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Gross_Profit_Title.setObjectName("Stock_Gross_Profit_Title")
        self.Stock_Growth_EBIT_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_EBIT_Title.setGeometry(QtCore.QRect(10, 360, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_EBIT_Title.setFont(font)
        self.Stock_Growth_EBIT_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_EBIT_Title.setObjectName("Stock_Growth_EBIT_Title")
        self.Stock_Growth_Operating_Income_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Operating_Income_Title.setGeometry(QtCore.QRect(10, 380, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Operating_Income_Title.setFont(font)
        self.Stock_Growth_Operating_Income_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_Operating_Income_Title.setObjectName("Stock_Growth_Operating_Income_Title")
        self.Stock_Growth_Net_Income_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Net_Income_Title.setGeometry(QtCore.QRect(10, 400, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Net_Income_Title.setFont(font)
        self.Stock_Growth_Net_Income_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_Net_Income_Title.setObjectName("Stock_Growth_Net_Income_Title")
        self.Stock_Growth_Earnings_Per_Share_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Earnings_Per_Share_Title.setGeometry(QtCore.QRect(10, 420, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Earnings_Per_Share_Title.setFont(font)
        self.Stock_Growth_Earnings_Per_Share_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_Earnings_Per_Share_Title.setObjectName("Stock_Growth_Earnings_Per_Share_Title")
        self.Stock_Growth_Dividend_Per_Share_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Dividend_Per_Share_Title.setGeometry(QtCore.QRect(10, 440, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Dividend_Per_Share_Title.setFont(font)
        self.Stock_Growth_Dividend_Per_Share_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_Dividend_Per_Share_Title.setObjectName("Stock_Growth_Dividend_Per_Share_Title")
        self.Stock_Growth_Free_Cashflow_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Free_Cashflow_Title.setGeometry(QtCore.QRect(10, 460, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Free_Cashflow_Title.setFont(font)
        self.Stock_Growth_Free_Cashflow_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_Free_Cashflow_Title.setObjectName("Stock_Growth_Free_Cashflow_Title")
        self.Stock_Growth_Debt_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Debt_Title.setGeometry(QtCore.QRect(10, 480, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Debt_Title.setFont(font)
        self.Stock_Growth_Debt_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_Debt_Title.setObjectName("Stock_Growth_Debt_Title")
        self.Stock_Growth_RD_Expense_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_RD_Expense_Title.setGeometry(QtCore.QRect(10, 500, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_RD_Expense_Title.setFont(font)
        self.Stock_Growth_RD_Expense_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_RD_Expense_Title.setObjectName("Stock_Growth_RD_Expense_Title")
        self.Stock_RSI = QtWidgets.QLabel(self.centralwidget)
        self.Stock_RSI.setGeometry(QtCore.QRect(919, 82, 81, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_RSI.setFont(font)
        self.Stock_RSI.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Stock_RSI.setObjectName("Stock_RSI")
        self.Stock_Growth_SGA_Expense_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_SGA_Expense_Title.setGeometry(QtCore.QRect(10, 520, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_SGA_Expense_Title.setFont(font)
        self.Stock_Growth_SGA_Expense_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_SGA_Expense_Title.setObjectName("Stock_Growth_SGA_Expense_Title")
        self.Stock_Growth_Longterm_Financial_Growth_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Financial_Growth_Title.setGeometry(QtCore.QRect(180, 540, 200, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Longterm_Financial_Growth_Title.setFont(font)
        self.Stock_Growth_Longterm_Financial_Growth_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Financial_Growth_Title.setObjectName("Stock_Growth_Longterm_Financial_Growth_Title")
        self.Stock_Growth_Longterm_Revenue_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Revenue_Title.setGeometry(QtCore.QRect(10, 580, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Longterm_Revenue_Title.setFont(font)
        self.Stock_Growth_Longterm_Revenue_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_Longterm_Revenue_Title.setObjectName("Stock_Growth_Longterm_Revenue_Title")
        self.Stock_Growth_Longterm_Operating_Cashflow_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Operating_Cashflow_Title.setGeometry(QtCore.QRect(10, 600, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Longterm_Operating_Cashflow_Title.setFont(font)
        self.Stock_Growth_Longterm_Operating_Cashflow_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_Longterm_Operating_Cashflow_Title.setObjectName("Stock_Growth_Longterm_Operating_Cashflow_Title")
        self.Stock_Growth_Longterm_Net_Income_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Net_Income_Title.setGeometry(QtCore.QRect(10, 620, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Longterm_Net_Income_Title.setFont(font)
        self.Stock_Growth_Longterm_Net_Income_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_Longterm_Net_Income_Title.setObjectName("Stock_Growth_Longterm_Net_Income_Title")
        self.Stock_Growth_Longterm_Shareholder_Equity_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Shareholder_Equity_Title.setGeometry(QtCore.QRect(10, 640, 135, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Longterm_Shareholder_Equity_Title.setFont(font)
        self.Stock_Growth_Longterm_Shareholder_Equity_Title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Stock_Growth_Longterm_Shareholder_Equity_Title.setObjectName("Stock_Growth_Longterm_Shareholder_Equity_Title")
        self.Stock_Growth_Date1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Date1.setGeometry(QtCore.QRect(150, 320, 90, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Date1.setFont(font)
        self.Stock_Growth_Date1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Date1.setObjectName("Stock_Growth_Date1")
        self.Stock_Growth_Date2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Date2.setGeometry(QtCore.QRect(240, 320, 90, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Date2.setFont(font)
        self.Stock_Growth_Date2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Date2.setObjectName("Stock_Growth_Date2")
        self.Stock_Growth_Date3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Date3.setGeometry(QtCore.QRect(330, 320, 90, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Date3.setFont(font)
        self.Stock_Growth_Date3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Date3.setObjectName("Stock_Growth_Date3")
        self.Stock_Growth_Longterm_Date1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Date1.setGeometry(QtCore.QRect(150, 560, 81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Longterm_Date1.setFont(font)
        self.Stock_Growth_Longterm_Date1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Date1.setObjectName("Stock_Growth_Longterm_Date1")
        self.Stock_Growth_Longterm_Date2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Date2.setGeometry(QtCore.QRect(240, 560, 81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Longterm_Date2.setFont(font)
        self.Stock_Growth_Longterm_Date2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Date2.setObjectName("Stock_Growth_Longterm_Date2")
        self.Stock_Growth_Longterm_Date3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Date3.setGeometry(QtCore.QRect(330, 560, 81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Growth_Longterm_Date3.setFont(font)
        self.Stock_Growth_Longterm_Date3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Date3.setObjectName("Stock_Growth_Longterm_Date3")
        self.Stock_Gross_Profit1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Gross_Profit1.setGeometry(QtCore.QRect(150, 340, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Gross_Profit1.setFont(font)
        self.Stock_Gross_Profit1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Gross_Profit1.setObjectName("Stock_Gross_Profit1")
        self.Stock_Growth_EBIT1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_EBIT1.setGeometry(QtCore.QRect(150, 360, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_EBIT1.setFont(font)
        self.Stock_Growth_EBIT1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_EBIT1.setObjectName("Stock_Growth_EBIT1")
        self.Stock_Growth_Operating_Income1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Operating_Income1.setGeometry(QtCore.QRect(150, 380, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Operating_Income1.setFont(font)
        self.Stock_Growth_Operating_Income1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Operating_Income1.setObjectName("Stock_Growth_Operating_Income1")
        self.Stock_Growth_Net_Income1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Net_Income1.setGeometry(QtCore.QRect(150, 400, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Net_Income1.setFont(font)
        self.Stock_Growth_Net_Income1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Net_Income1.setObjectName("Stock_Growth_Net_Income1")
        self.Stock_Growth_Earnings_Per_Share1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Earnings_Per_Share1.setGeometry(QtCore.QRect(150, 420, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Earnings_Per_Share1.setFont(font)
        self.Stock_Growth_Earnings_Per_Share1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Earnings_Per_Share1.setObjectName("Stock_Growth_Earnings_Per_Share1")
        self.Stock_Growth_Dividend_Per_Share1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Dividend_Per_Share1.setGeometry(QtCore.QRect(150, 440, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Dividend_Per_Share1.setFont(font)
        self.Stock_Growth_Dividend_Per_Share1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Dividend_Per_Share1.setObjectName("Stock_Growth_Dividend_Per_Share1")
        self.Stock_Growth_Free_Cashflow1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Free_Cashflow1.setGeometry(QtCore.QRect(150, 460, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Free_Cashflow1.setFont(font)
        self.Stock_Growth_Free_Cashflow1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Free_Cashflow1.setObjectName("Stock_Growth_Free_Cashflow1")
        self.Stock_Growth_Debt1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Debt1.setGeometry(QtCore.QRect(150, 480, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Debt1.setFont(font)
        self.Stock_Growth_Debt1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Debt1.setObjectName("Stock_Growth_Debt1")
        self.Stock_Growth_RD_Expense1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_RD_Expense1.setGeometry(QtCore.QRect(150, 500, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_RD_Expense1.setFont(font)
        self.Stock_Growth_RD_Expense1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_RD_Expense1.setObjectName("Stock_Growth_RD_Expense1")
        self.Stock_Growth_SGA_Expense1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_SGA_Expense1.setGeometry(QtCore.QRect(150, 520, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_SGA_Expense1.setFont(font)
        self.Stock_Growth_SGA_Expense1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_SGA_Expense1.setObjectName("Stock_Growth_SGA_Expense1")
        self.Stock_Gross_Profit2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Gross_Profit2.setGeometry(QtCore.QRect(240, 340, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Gross_Profit2.setFont(font)
        self.Stock_Gross_Profit2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Gross_Profit2.setObjectName("Stock_Gross_Profit2")
        self.Stock_Growth_EBIT2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_EBIT2.setGeometry(QtCore.QRect(240, 360, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_EBIT2.setFont(font)
        self.Stock_Growth_EBIT2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_EBIT2.setObjectName("Stock_Growth_EBIT2")
        self.Stock_Growth_Operating_Income2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Operating_Income2.setGeometry(QtCore.QRect(240, 380, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Operating_Income2.setFont(font)
        self.Stock_Growth_Operating_Income2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Operating_Income2.setObjectName("Stock_Growth_Operating_Income2")
        self.Stock_Growth_Net_Income2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Net_Income2.setGeometry(QtCore.QRect(240, 400, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Net_Income2.setFont(font)
        self.Stock_Growth_Net_Income2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Net_Income2.setObjectName("Stock_Growth_Net_Income2")
        self.Stock_Growth_Earnings_Per_Share2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Earnings_Per_Share2.setGeometry(QtCore.QRect(240, 420, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Earnings_Per_Share2.setFont(font)
        self.Stock_Growth_Earnings_Per_Share2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Earnings_Per_Share2.setObjectName("Stock_Growth_Earnings_Per_Share2")
        self.Stock_Growth_Dividend_Per_Share2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Dividend_Per_Share2.setGeometry(QtCore.QRect(240, 440, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Dividend_Per_Share2.setFont(font)
        self.Stock_Growth_Dividend_Per_Share2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Dividend_Per_Share2.setObjectName("Stock_Growth_Dividend_Per_Share2")
        self.Stock_Growth_Free_Cashflow2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Free_Cashflow2.setGeometry(QtCore.QRect(240, 460, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Free_Cashflow2.setFont(font)
        self.Stock_Growth_Free_Cashflow2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Free_Cashflow2.setObjectName("Stock_Growth_Free_Cashflow2")
        self.Stock_Growth_Debt2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Debt2.setGeometry(QtCore.QRect(240, 480, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Debt2.setFont(font)
        self.Stock_Growth_Debt2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Debt2.setObjectName("Stock_Growth_Debt2")
        self.Stock_Growth_RD_Expense2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_RD_Expense2.setGeometry(QtCore.QRect(240, 500, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_RD_Expense2.setFont(font)
        self.Stock_Growth_RD_Expense2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_RD_Expense2.setObjectName("Stock_Growth_RD_Expense2")
        self.Stock_Growth_SGA_Expense2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_SGA_Expense2.setGeometry(QtCore.QRect(240, 520, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_SGA_Expense2.setFont(font)
        self.Stock_Growth_SGA_Expense2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_SGA_Expense2.setObjectName("Stock_Growth_SGA_Expense2")
        self.Stock_Gross_Profit3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Gross_Profit3.setGeometry(QtCore.QRect(330, 340, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Gross_Profit3.setFont(font)
        self.Stock_Gross_Profit3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Gross_Profit3.setObjectName("Stock_Gross_Profit3")
        self.Stock_Growth_EBIT3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_EBIT3.setGeometry(QtCore.QRect(330, 360, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_EBIT3.setFont(font)
        self.Stock_Growth_EBIT3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_EBIT3.setObjectName("Stock_Growth_EBIT3")
        self.Stock_Growth_Operating_Income3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Operating_Income3.setGeometry(QtCore.QRect(330, 380, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Operating_Income3.setFont(font)
        self.Stock_Growth_Operating_Income3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Operating_Income3.setObjectName("Stock_Growth_Operating_Income3")
        self.Stock_Growth_Net_Income3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Net_Income3.setGeometry(QtCore.QRect(330, 400, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Net_Income3.setFont(font)
        self.Stock_Growth_Net_Income3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Net_Income3.setObjectName("Stock_Growth_Net_Income3")
        self.Stock_Growth_Earnings_Per_Share3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Earnings_Per_Share3.setGeometry(QtCore.QRect(330, 420, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Earnings_Per_Share3.setFont(font)
        self.Stock_Growth_Earnings_Per_Share3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Earnings_Per_Share3.setObjectName("Stock_Growth_Earnings_Per_Share3")
        self.Stock_Growth_Dividend_Per_Share3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Dividend_Per_Share3.setGeometry(QtCore.QRect(330, 440, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Dividend_Per_Share3.setFont(font)
        self.Stock_Growth_Dividend_Per_Share3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Dividend_Per_Share3.setObjectName("Stock_Growth_Dividend_Per_Share3")
        self.Stock_Growth_Free_Cashflow3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Free_Cashflow3.setGeometry(QtCore.QRect(330, 460, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Free_Cashflow3.setFont(font)
        self.Stock_Growth_Free_Cashflow3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Free_Cashflow3.setObjectName("Stock_Growth_Free_Cashflow3")
        self.Stock_Growth_Debt3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Debt3.setGeometry(QtCore.QRect(330, 480, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Debt3.setFont(font)
        self.Stock_Growth_Debt3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Debt3.setObjectName("Stock_Growth_Debt3")
        self.Stock_Growth_RD_Expense3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_RD_Expense3.setGeometry(QtCore.QRect(330, 500, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_RD_Expense3.setFont(font)
        self.Stock_Growth_RD_Expense3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_RD_Expense3.setObjectName("Stock_Growth_RD_Expense3")
        self.Stock_Growth_SGA_Expense3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_SGA_Expense3.setGeometry(QtCore.QRect(330, 520, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_SGA_Expense3.setFont(font)
        self.Stock_Growth_SGA_Expense3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_SGA_Expense3.setObjectName("Stock_Growth_SGA_Expense3")
        self.Stock_Growth_Longterm_Revenue1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Revenue1.setGeometry(QtCore.QRect(150, 580, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Revenue1.setFont(font)
        self.Stock_Growth_Longterm_Revenue1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Revenue1.setObjectName("Stock_Growth_Longterm_Revenue1")
        self.Stock_Growth_Longterm_Revenue2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Revenue2.setGeometry(QtCore.QRect(240, 580, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Revenue2.setFont(font)
        self.Stock_Growth_Longterm_Revenue2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Revenue2.setObjectName("Stock_Growth_Longterm_Revenue2")
        self.Stock_Growth_Longterm_Revenue3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Revenue3.setGeometry(QtCore.QRect(330, 580, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Revenue3.setFont(font)
        self.Stock_Growth_Longterm_Revenue3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Revenue3.setObjectName("Stock_Growth_Longterm_Revenue3")
        self.Stock_Growth_Longterm_Operating_Cashflow1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Operating_Cashflow1.setGeometry(QtCore.QRect(150, 600, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Operating_Cashflow1.setFont(font)
        self.Stock_Growth_Longterm_Operating_Cashflow1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Operating_Cashflow1.setObjectName("Stock_Growth_Longterm_Operating_Cashflow1")
        self.Stock_Growth_Longterm_Operating_Cashflow2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Operating_Cashflow2.setGeometry(QtCore.QRect(240, 600, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Operating_Cashflow2.setFont(font)
        self.Stock_Growth_Longterm_Operating_Cashflow2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Operating_Cashflow2.setObjectName("Stock_Growth_Longterm_Operating_Cashflow2")
        self.Stock_Growth_Longterm_Operating_Cashflow3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Operating_Cashflow3.setGeometry(QtCore.QRect(330, 600, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Operating_Cashflow3.setFont(font)
        self.Stock_Growth_Longterm_Operating_Cashflow3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Operating_Cashflow3.setObjectName("Stock_Growth_Longterm_Operating_Cashflow3")
        self.Stock_Growth_Longterm_Net_Income1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Net_Income1.setGeometry(QtCore.QRect(150, 620, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Net_Income1.setFont(font)
        self.Stock_Growth_Longterm_Net_Income1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Net_Income1.setObjectName("Stock_Growth_Longterm_Net_Income1")
        self.Stock_Growth_Longterm_Shareholder_Equity1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Shareholder_Equity1.setGeometry(QtCore.QRect(150, 640, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Shareholder_Equity1.setFont(font)
        self.Stock_Growth_Longterm_Shareholder_Equity1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Shareholder_Equity1.setObjectName("Stock_Growth_Longterm_Shareholder_Equity1")
        self.Stock_Growth_Longterm_Net_Income2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Net_Income2.setGeometry(QtCore.QRect(240, 620, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Net_Income2.setFont(font)
        self.Stock_Growth_Longterm_Net_Income2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Net_Income2.setObjectName("Stock_Growth_Longterm_Net_Income2")
        self.Stock_Growth_Longterm_Shareholder_Equity2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Shareholder_Equity2.setGeometry(QtCore.QRect(240, 640, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Shareholder_Equity2.setFont(font)
        self.Stock_Growth_Longterm_Shareholder_Equity2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Shareholder_Equity2.setObjectName("Stock_Growth_Longterm_Shareholder_Equity2")
        self.Stock_Growth_Longterm_Net_Income3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Net_Income3.setGeometry(QtCore.QRect(330, 620, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Net_Income3.setFont(font)
        self.Stock_Growth_Longterm_Net_Income3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Net_Income3.setObjectName("Stock_Growth_Longterm_Net_Income3")
        self.Stock_Growth_Longterm_Shareholder_Equity3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Growth_Longterm_Shareholder_Equity3.setGeometry(QtCore.QRect(330, 640, 90, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Growth_Longterm_Shareholder_Equity3.setFont(font)
        self.Stock_Growth_Longterm_Shareholder_Equity3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Growth_Longterm_Shareholder_Equity3.setObjectName("Stock_Growth_Longterm_Shareholder_Equity3")
        self.Stock_Growth_Switch_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Stock_Growth_Switch_Button.setGeometry(QtCore.QRect(10, 300, 113, 32))
        self.Stock_Growth_Switch_Button.setObjectName("Stock_Growth_Switch_Button")
        self.Stock_Technical_S3_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_S3_Title.setGeometry(QtCore.QRect(530, 320, 45, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Technical_S3_Title.setFont(font)
        self.Stock_Technical_S3_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_S3_Title.setObjectName("Stock_Technical_S3_Title")
        self.Stock_Technical_S2_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_S2_Title.setGeometry(QtCore.QRect(580, 320, 45, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Technical_S2_Title.setFont(font)
        self.Stock_Technical_S2_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_S2_Title.setObjectName("Stock_Technical_S2_Title")
        self.Stock_Technical_S1_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_S1_Title.setGeometry(QtCore.QRect(630, 320, 45, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Technical_S1_Title.setFont(font)
        self.Stock_Technical_S1_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_S1_Title.setObjectName("Stock_Technical_S1_Title")
        self.Stock_Technical_Pivot_Point_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_Pivot_Point_Title.setGeometry(QtCore.QRect(685, 320, 70, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Technical_Pivot_Point_Title.setFont(font)
        self.Stock_Technical_Pivot_Point_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_Pivot_Point_Title.setObjectName("Stock_Technical_Pivot_Point_Title")
        self.Stock_Technical_R1_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_R1_Title.setGeometry(QtCore.QRect(765, 320, 45, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Technical_R1_Title.setFont(font)
        self.Stock_Technical_R1_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_R1_Title.setObjectName("Stock_Technical_R1_Title")
        self.Stock_Technical_R2_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_R2_Title.setGeometry(QtCore.QRect(815, 320, 45, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Technical_R2_Title.setFont(font)
        self.Stock_Technical_R2_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_R2_Title.setObjectName("Stock_Technical_R2_Title")
        self.Stock_Technical_R3_Title = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_R3_Title.setGeometry(QtCore.QRect(865, 320, 45, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Stock_Technical_R3_Title.setFont(font)
        self.Stock_Technical_R3_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_R3_Title.setObjectName("Stock_Technical_R3_Title")
        self.Stock_Technical_S3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_S3.setGeometry(QtCore.QRect(530, 340, 45, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Technical_S3.setFont(font)
        self.Stock_Technical_S3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_S3.setObjectName("Stock_Technical_S3")
        self.Stock_Technical_S2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_S2.setGeometry(QtCore.QRect(580, 340, 45, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Technical_S2.setFont(font)
        self.Stock_Technical_S2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_S2.setObjectName("Stock_Technical_S2")
        self.Stock_Technical_S1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_S1.setGeometry(QtCore.QRect(630, 340, 45, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Technical_S1.setFont(font)
        self.Stock_Technical_S1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_S1.setObjectName("Stock_Technical_S1")
        self.Stock_Technical_Pivot_Point = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_Pivot_Point.setGeometry(QtCore.QRect(685, 340, 70, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Technical_Pivot_Point.setFont(font)
        self.Stock_Technical_Pivot_Point.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_Pivot_Point.setObjectName("Stock_Technical_Pivot_Point")
        self.Stock_Technical_R1 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_R1.setGeometry(QtCore.QRect(765, 340, 45, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Technical_R1.setFont(font)
        self.Stock_Technical_R1.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_R1.setObjectName("Stock_Technical_R1")
        self.Stock_Technical_R2 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_R2.setGeometry(QtCore.QRect(815, 340, 45, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Technical_R2.setFont(font)
        self.Stock_Technical_R2.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_R2.setObjectName("Stock_Technical_R2")
        self.Stock_Technical_R3 = QtWidgets.QLabel(self.centralwidget)
        self.Stock_Technical_R3.setGeometry(QtCore.QRect(865, 340, 45, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Stock_Technical_R3.setFont(font)
        self.Stock_Technical_R3.setAlignment(QtCore.Qt.AlignCenter)
        self.Stock_Technical_R3.setObjectName("Stock_Technical_R3")

        # We first initialize the x and y axis of the PyQTgraph , x-axis needs to be in date time
        # and we need assign it to a separate class, for both axis, we show the grid to have better
        # viewing experiences
        date_axis = TimeAxisItem(orientation='bottom')
        y_axis = pg.AxisItem(orientation='left')

        # Show grid with opacity = 255
        y_axis.setGrid(255)
        date_axis.setGrid(255)

        # Instead of normally assigning as graphic view, we would assign this widget as a plot widget
        # with axis assigned with variables above
        self.Stock_Technical_MACD = pg.PlotWidget(self.centralwidget, axisItems={'bottom': date_axis, 'left': y_axis})
        self.Stock_Technical_MACD.setGeometry(QtCore.QRect(430, 370, 571, 291))
        self.Stock_Technical_MACD.setObjectName("Stock_Technical_MACD")

        # Set the background colour to be white
        self.Stock_Technical_MACD.setBackground('w')

        self.Sector_Performance_Title_2.raise_()
        self.TimeNow_Label.raise_()
        self.DateNow_Label.raise_()
        self.Index_Symbol_0.raise_()
        self.Index_Percentage_0.raise_()
        self.Index_Price_0.raise_()
        self.line_2.raise_()
        self.line_3.raise_()
        self.Index_Symbol_1.raise_()
        self.Index_Percentage_1.raise_()
        self.Index_Price_1.raise_()
        self.Index_Percentage_2.raise_()
        self.line_4.raise_()
        self.Index_Symbol_2.raise_()
        self.Index_Price_2.raise_()
        self.Index_Percentage_3.raise_()
        self.line_5.raise_()
        self.Index_Symbol_3.raise_()
        self.Index_Price_3.raise_()
        self.Index_Percentage_4.raise_()
        self.line_6.raise_()
        self.Index_Symbol_4.raise_()
        self.Index_Price_4.raise_()
        self.Index_Percentage_5.raise_()
        self.line_7.raise_()
        self.Index_Symbol_5.raise_()
        self.Index_Price_5.raise_()
        self.line.raise_()
        self.line_8.raise_()
        self.Index_Percentage_6.raise_()
        self.Index_Symbol_6.raise_()
        self.Index_Price_6.raise_()
        self.Index_Name_0.raise_()
        self.Index_Name_1.raise_()
        self.Index_Name_2.raise_()
        self.Index_Name_3.raise_()
        self.Index_Name_4.raise_()
        self.Index_Name_5.raise_()
        self.Index_Name_6.raise_()
        self.Sector_Name_0.raise_()
        self.Sector_Percentage_0.raise_()
        self.Sector_Percentage_1.raise_()
        self.Sector_Name_1.raise_()
        self.Sector_Percentage_2.raise_()
        self.Sector_Name_2.raise_()
        self.Sector_Percentage_3.raise_()
        self.Sector_Name_3.raise_()
        self.Sector_Percentage_4.raise_()
        self.Sector_Name_4.raise_()
        self.Sector_Percentage_5.raise_()
        self.Sector_Name_5.raise_()
        self.Sector_Percentage_6.raise_()
        self.Sector_Name_6.raise_()
        self.Sector_Percentage_7.raise_()
        self.Sector_Name_7.raise_()
        self.Sector_Name_9.raise_()
        self.Sector_Percentage_9.raise_()
        self.Sector_Name_8.raise_()
        self.Sector_Percentage_8.raise_()
        self.Sector_Performance_Title.raise_()
        self.Marke_Open_Label.raise_()
        self.Search_Button.raise_()
        self.Search_Bar.raise_()
        self.Stock_Symbol.raise_()
        self.Stock_Description_Header.raise_()
        self.Stock_Image.raise_()
        self.Stock_Industry_Title.raise_()
        self.Stock_Exchange_Title.raise_()
        self.Stock_Industry.raise_()
        self.Stock_Exchange.raise_()
        self.Stock_Price.raise_()
        self.Stock_Percentage_Change.raise_()
        self.Stock_Volume.raise_()
        self.Stock_Line_1.raise_()
        self.Stock_Line_2.raise_()
        self.Stock_Name.raise_()
        self.Stock_Market_Capitalization_Title.raise_()
        self.Stock_Beta.raise_()
        self.Stock_Open.raise_()
        self.Stock_High.raise_()
        self.Stock_Low.raise_()
        self.Stock_Earnings_Title.raise_()
        self.Stock_Market_Capitalization.raise_()
        self.Stock_Earnings.raise_()
        self.Stock_AverageVolume_Title.raise_()
        self.Stock_Average_Volume.raise_()
        self.Stock_View_Chart.raise_()
        self.Stock_Avg_Price_200_Title.raise_()
        self.Stock_Line_3.raise_()
        self.Stock_Line_4.raise_()
        self.Stock_Growth_Financia_Title.raise_()
        self.Stock_Gross_Profit_Title.raise_()
        self.Stock_Growth_EBIT_Title.raise_()
        self.Stock_Growth_Operating_Income_Title.raise_()
        self.Stock_Growth_Net_Income_Title.raise_()
        self.Stock_Growth_Earnings_Per_Share_Title.raise_()
        self.Stock_Growth_Dividend_Per_Share_Title.raise_()
        self.Stock_Growth_Free_Cashflow_Title.raise_()
        self.Stock_Growth_Debt_Title.raise_()
        self.Stock_Growth_RD_Expense_Title.raise_()
        self.Stock_RSI.raise_()
        self.Stock_Growth_SGA_Expense_Title.raise_()
        self.Stock_Growth_Longterm_Financial_Growth_Title.raise_()
        self.Stock_Growth_Longterm_Revenue_Title.raise_()
        self.Stock_Growth_Longterm_Operating_Cashflow_Title.raise_()
        self.Stock_Growth_Longterm_Net_Income_Title.raise_()
        self.Stock_Growth_Longterm_Shareholder_Equity_Title.raise_()
        self.Stock_Growth_Date1.raise_()
        self.Stock_Growth_Date2.raise_()
        self.Stock_Growth_Date3.raise_()
        self.Stock_Growth_Longterm_Date1.raise_()
        self.Stock_Growth_Longterm_Date2.raise_()
        self.Stock_Growth_Longterm_Date3.raise_()
        self.Stock_Gross_Profit1.raise_()
        self.Stock_Growth_EBIT1.raise_()
        self.Stock_Growth_Operating_Income1.raise_()
        self.Stock_Growth_Net_Income1.raise_()
        self.Stock_Growth_Earnings_Per_Share1.raise_()
        self.Stock_Growth_Dividend_Per_Share1.raise_()
        self.Stock_Growth_Free_Cashflow1.raise_()
        self.Stock_Growth_Debt1.raise_()
        self.Stock_Growth_RD_Expense1.raise_()
        self.Stock_Growth_SGA_Expense1.raise_()
        self.Stock_Gross_Profit2.raise_()
        self.Stock_Growth_EBIT2.raise_()
        self.Stock_Growth_Operating_Income2.raise_()
        self.Stock_Growth_Net_Income2.raise_()
        self.Stock_Growth_Earnings_Per_Share2.raise_()
        self.Stock_Growth_Dividend_Per_Share2.raise_()
        self.Stock_Growth_Free_Cashflow2.raise_()
        self.Stock_Growth_Debt2.raise_()
        self.Stock_Growth_RD_Expense2.raise_()
        self.Stock_Growth_SGA_Expense2.raise_()
        self.Stock_Gross_Profit3.raise_()
        self.Stock_Growth_EBIT3.raise_()
        self.Stock_Growth_Operating_Income3.raise_()
        self.Stock_Growth_Net_Income3.raise_()
        self.Stock_Growth_Earnings_Per_Share3.raise_()
        self.Stock_Growth_Dividend_Per_Share3.raise_()
        self.Stock_Growth_Free_Cashflow3.raise_()
        self.Stock_Growth_Debt3.raise_()
        self.Stock_Growth_RD_Expense3.raise_()
        self.Stock_Growth_SGA_Expense3.raise_()
        self.Stock_Growth_Longterm_Revenue1.raise_()
        self.Stock_Growth_Longterm_Revenue2.raise_()
        self.Stock_Growth_Longterm_Revenue3.raise_()
        self.Stock_Growth_Longterm_Operating_Cashflow1.raise_()
        self.Stock_Growth_Longterm_Operating_Cashflow2.raise_()
        self.Stock_Growth_Longterm_Operating_Cashflow3.raise_()
        self.Stock_Growth_Longterm_Net_Income1.raise_()
        self.Stock_Growth_Longterm_Shareholder_Equity1.raise_()
        self.Stock_Growth_Longterm_Net_Income2.raise_()
        self.Stock_Growth_Longterm_Shareholder_Equity2.raise_()
        self.Stock_Growth_Longterm_Net_Income3.raise_()
        self.Stock_Growth_Longterm_Shareholder_Equity3.raise_()
        self.Stock_Description.raise_()
        self.Stock_Growth_Switch_Button.raise_()
        self.Stock_Avg_Price_200.raise_()
        self.Stock_Technical_S3_Title.raise_()
        self.Stock_Technical_S2_Title.raise_()
        self.Stock_Technical_S1_Title.raise_()
        self.Stock_Technical_Pivot_Point_Title.raise_()
        self.Stock_Technical_R1_Title.raise_()
        self.Stock_Technical_R2_Title.raise_()
        self.Stock_Technical_R3_Title.raise_()
        self.Stock_Technical_S3.raise_()
        self.Stock_Technical_S2.raise_()
        self.Stock_Technical_S1.raise_()
        self.Stock_Technical_Pivot_Point.raise_()
        self.Stock_Technical_R1.raise_()
        self.Stock_Technical_R2.raise_()
        self.Stock_Technical_R3.raise_()
        self.Stock_Technical_MACD.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        # This list contains all the widgets that we need to hide/show when the user searches up a stock
        self.stock_widgets = {self.Stock_Symbol, self.Stock_Description_Header, self.Stock_Description,
                              self.Stock_Image,
                              self.Stock_Industry_Title, self.Stock_Exchange_Title, self.Stock_Industry,
                              self.Stock_Exchange,
                              self.Stock_Price, self.Stock_Percentage_Change, self.Stock_Volume, self.Stock_Line_1,
                              self.Stock_Line_2, self.Stock_Name, self.Stock_Market_Capitalization_Title,
                              self.Stock_Beta,
                              self.Stock_Open, self.Stock_High, self.Stock_Low, self.Stock_Earnings_Title,
                              self.Stock_Market_Capitalization,
                              self.Stock_Earnings, self.Stock_AverageVolume_Title, self.Stock_Average_Volume,
                              self.Stock_View_Chart,
                              self.Stock_Avg_Price_200_Title, self.Stock_Avg_Price_200, self.Stock_Line_3,
                              self.Stock_Line_4,
                              self.Stock_Growth_Financia_Title, self.Stock_Gross_Profit_Title,
                              self.Stock_Growth_EBIT_Title,
                              self.Stock_Growth_Operating_Income_Title, self.Stock_Growth_Net_Income_Title,
                              self.Stock_Growth_Earnings_Per_Share_Title, self.Stock_Growth_Dividend_Per_Share_Title,
                              self.Stock_Growth_Free_Cashflow_Title, self.Stock_Growth_Debt_Title,
                              self.Stock_Growth_RD_Expense_Title,
                              self.Stock_RSI, self.Stock_Growth_SGA_Expense_Title,
                              self.Stock_Growth_Longterm_Financial_Growth_Title,
                              self.Stock_Growth_Longterm_Revenue_Title,
                              self.Stock_Growth_Longterm_Operating_Cashflow_Title,
                              self.Stock_Growth_Longterm_Net_Income_Title,
                              self.Stock_Growth_Longterm_Shareholder_Equity_Title,
                              self.Stock_Growth_Date1, self.Stock_Growth_Date2, self.Stock_Growth_Date3,
                              self.Stock_Growth_Longterm_Date1,
                              self.Stock_Growth_Longterm_Date2, self.Stock_Growth_Longterm_Date3,
                              self.Stock_Gross_Profit1,
                              self.Stock_Growth_EBIT1, self.Stock_Growth_Operating_Income1,
                              self.Stock_Growth_Net_Income1,
                              self.Stock_Growth_Earnings_Per_Share1, self.Stock_Growth_Dividend_Per_Share1,
                              self.Stock_Growth_Free_Cashflow1,
                              self.Stock_Growth_Debt1, self.Stock_Growth_RD_Expense1, self.Stock_Growth_SGA_Expense1,
                              self.Stock_Gross_Profit2,
                              self.Stock_Growth_EBIT2, self.Stock_Growth_Operating_Income2,
                              self.Stock_Growth_Net_Income2,
                              self.Stock_Growth_Earnings_Per_Share2, self.Stock_Growth_Dividend_Per_Share2,
                              self.Stock_Growth_Free_Cashflow2,
                              self.Stock_Growth_Debt2, self.Stock_Growth_RD_Expense2, self.Stock_Growth_SGA_Expense2,
                              self.Stock_Gross_Profit3,
                              self.Stock_Growth_EBIT3, self.Stock_Growth_Operating_Income3,
                              self.Stock_Growth_Net_Income3, self.Stock_Growth_Earnings_Per_Share3,
                              self.Stock_Growth_Dividend_Per_Share3, self.Stock_Growth_Free_Cashflow3,
                              self.Stock_Growth_Debt3,
                              self.Stock_Growth_RD_Expense3, self.Stock_Growth_SGA_Expense3,
                              self.Stock_Growth_Longterm_Revenue1,
                              self.Stock_Growth_Longterm_Revenue2, self.Stock_Growth_Longterm_Revenue3,
                              self.Stock_Growth_Longterm_Operating_Cashflow1,
                              self.Stock_Growth_Longterm_Operating_Cashflow2,
                              self.Stock_Growth_Longterm_Operating_Cashflow3,
                              self.Stock_Growth_Longterm_Net_Income1, self.Stock_Growth_Longterm_Shareholder_Equity1,
                              self.Stock_Growth_Longterm_Net_Income2, self.Stock_Growth_Longterm_Shareholder_Equity2,
                              self.Stock_Growth_Longterm_Net_Income3, self.Stock_Growth_Longterm_Shareholder_Equity3,
                              self.Stock_Technical_S3_Title, self.Stock_Technical_S2_Title, self.Stock_Technical_S1_Title,
                              self.Stock_Technical_Pivot_Point_Title, self.Stock_Technical_R1_Title, self.Stock_Technical_R2_Title,
                              self.Stock_Technical_R3_Title, self.Stock_Technical_S3, self.Stock_Technical_S2, self.Stock_Technical_S1,
                              self.Stock_Technical_Pivot_Point,self.Stock_Technical_R1,self.Stock_Technical_R2,self.Stock_Technical_R3,
                              self.Stock_Technical_MACD,self.Stock_Growth_Switch_Button}

        # Run through every widget in the list and hide it
        for widget in self.stock_widgets:
            widget.setVisible(False)

        # Whenever the search button is pressed, we would run the search stocks function
        self.Search_Button.clicked.connect(self.Search_Stocks)

        # Whenever the view chart button is pressed, we would call a function to open the web browser
        self.Stock_View_Chart.clicked.connect(self.OpenTradingView)

        # We have a timer that updates every second and updates the current time of the clock
        self.timer_painter = QtCore.QTimer()
        self.timer_painter.timeout.connect(self.UpdateTime)
        self.timer_painter.start(1000)

        # Set up another timer that updates all the banner indices
        self.stock_update_timer = QtCore.QTimer()
        self.stock_update_timer.timeout.connect(self.UpdateBanner)
        self.stock_update_timer.start(10000)

        # Singleshot Timers that sets up a timer and populates all formation, timed loop updates are then followed
        QtCore.QTimer.singleShot(1000, self.UpdateBanner)
        QtCore.QTimer.singleShot(1000, self.PopulateSectorPerformances)

        # Whenever the index of the performance title is changed, we would run populate Sector Performances Function
        self.Sector_Performance_Title.currentIndexChanged.connect(self.PopulateSectorPerformances)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # -------------------------------------------------------------------
    # Function Name: UpdateTime
    #
    # Description:
    # This function is run every 1 second to update the date
    # and time labels on the top left of the main window.This function is
    # called from the QT timer expiry at the bottom of the setupUI
    # function.
    # -------------------------------------------------------------------
    def UpdateTime(self):
        current_time = datetime.now()

        # To Debug the current time
        # print(current_time.strftime("%H:%M:%S"))

        # Update the text label with current time, one for date and another for current time
        self.TimeNow_Label.setText(current_time.strftime("%H:%M:%S"))
        self.DateNow_Label.setText(current_time.strftime("%b %d %Y"))

    # -------------------------------------------------------------------
    # Function Name: Search_Stocks
    #
    # Description:
    # This function is called whenever a ticker is searched
    # and it relies on Alphavantage and FinancialModellingPrep JSON to
    # have data returned, labels are then generated and refreshed
    # -------------------------------------------------------------------
    def Search_Stocks(self):

        # Get rid of white spaces if there are any
        ticker_string = self.Search_Bar.text()
        ticker_string = ticker_string.strip()

        # Assigns a variable that other functions can use
        # TODO: Past ticker_string instead into other defs
        self.search_symbol = ticker_string

        # We set up the URL that we will need to use for the comppany profile
        url = "https://financialmodelingprep.com/api/v3/company/profile/" + ticker_string + \
              '?apikey=' + financial_modelling_prep_api_key
        session = requests.session()
        request = session.get(url, timeout=5)

        # Store the JSON data into variable for later processing
        company_data = request.json()

        # In addition to the company profile, we also obtain the latest quote information on
        # the searched equity
        quote_url = "https://financialmodelingprep.com/api/v3/quote/" + ticker_string + '?apikey=' + financial_modelling_prep_api_key
        session = requests.session()
        request = session.get(quote_url, timeout=5)
        quote_data = request.json()

        # Debug Messages
        # print(type(company_profile['mktCap']))
        # print(quote_data)

        # We now need to test the integrity of the data that we have received. We check for the amount of dictionary
        # pairs in the returned message, if it has less than 2 key-value pairs, something is wrong!
        #print(company_data)
        #print(quote_data)
        if len(company_data) < 2:
            return

        # We do basic parsing of the company data and get rid of any data we do not need
        company_profile = company_data['profile']
        self.Stock_Name.setText('  ' + str(company_profile['companyName']))
        self.Stock_Symbol.setText(company_data['symbol'])
        self.Stock_Description.setText(company_profile['description'])

        # Take the Image URL from information passed down from Financial Modelling Prep
        image_url = company_profile['image']

        # We would use the URL module and read the image file, convert it to byte
        data = urllib.request.urlopen(image_url).read()
        image = QtGui.QImage()
        image.loadFromData(data)

        # We set the company image to have the converted image
        self.Stock_Image.setPixmap(QtGui.QPixmap(image))

        # Update the label widgets with information we obtained from the API provider
        self.Stock_Price.setText(str(company_profile['price']))

        percentage_change = company_profile['changesPercentage']
        percentage_change = percentage_change[1:-1]
        self.Stock_Percentage_Change.setText(percentage_change)

        self.Stock_Volume.setText('Vol: ' + company_profile['volAvg'])
        self.Stock_Low.setText('L: ' + str(quote_data[0]['dayLow']))
        self.Stock_High.setText('H: ' + str(quote_data[0]['dayHigh']))
        self.Stock_Open.setText('O: ' + str(quote_data[0]['open']))

        beta = company_profile['beta']
        beta = beta[0:4]
        self.Stock_Beta.setText('Beta: ' + beta)
        self.Stock_Market_Capitalization.setText(company_profile['mktCap'])
        self.Stock_Exchange.setText(quote_data[0]['exhange'])
        self.Stock_Industry.setText(company_profile['industry'])
        self.Stock_Avg_Price_200.setText(str(quote_data[0]['priceAvg200'])[0:7])
        self.Stock_Average_Volume.setText(str(quote_data[0]['avgVolume']))
        self.Stock_Earnings.setText(quote_data[0]['earningsAnnouncement'][0:10])
        self.Stock_Exchange_Variable = quote_data[0]['exhange']

        # After we have updated the information, we would now need change the colour
        # of the widget based on the string
        # TODO: Perhaps changing another way to detect negative for faster processing

        if (quote_data[0]['changesPercentage']) < 0:
            self.Stock_Price.setStyleSheet('Color:RED')
            self.Stock_Percentage_Change.setStyleSheet('Color:RED')
            self.Stock_Name.setStyleSheet('Background-Color:RED;Color:WHITE')
        else:
            self.Stock_Price.setStyleSheet('Color:GREEN')
            self.Stock_Percentage_Change.setStyleSheet('Color:GREEN')
            self.Stock_Name.setStyleSheet('Background-Color:GREEN;Color:WHITE')

        # Now we manipulate data to fit our needs for growth of data
        # We first make arrays for efficiency of these information in
        # later in a loop
        date_array_widgets = [self.Stock_Growth_Date1, self.Stock_Growth_Date2, self.Stock_Growth_Date3]
        gross_profit_widgets = [self.Stock_Gross_Profit1, self.Stock_Gross_Profit2, self.Stock_Gross_Profit3]
        ebit_widgets = [self.Stock_Growth_EBIT1, self.Stock_Growth_EBIT2, self.Stock_Growth_EBIT3]
        operating_income_widgets = [self.Stock_Growth_Operating_Income1, self.Stock_Growth_Operating_Income2,
                                    self.Stock_Growth_Operating_Income3]
        net_income_widgets = [self.Stock_Growth_Net_Income1, self.Stock_Growth_Net_Income2,
                              self.Stock_Growth_Net_Income3]
        earnings_per_share_widgets = [self.Stock_Growth_Earnings_Per_Share1, self.Stock_Growth_Earnings_Per_Share2,
                                      self.Stock_Growth_Earnings_Per_Share3]
        dividend_per_share_widgets = [self.Stock_Growth_Dividend_Per_Share1, self.Stock_Growth_Dividend_Per_Share2,
                                      self.Stock_Growth_Dividend_Per_Share3]
        free_cash_flow_widgets = [self.Stock_Growth_Free_Cashflow1, self.Stock_Growth_Free_Cashflow2,
                                  self.Stock_Growth_Free_Cashflow3]
        debt_growth_widgets = [self.Stock_Growth_Debt1, self.Stock_Growth_Debt2, self.Stock_Growth_Debt3]
        rd_expense_widgets = [self.Stock_Growth_RD_Expense1, self.Stock_Growth_RD_Expense2,
                              self.Stock_Growth_RD_Expense3]
        sga_widgets = [self.Stock_Growth_SGA_Expense1, self.Stock_Growth_SGA_Expense2, self.Stock_Growth_SGA_Expense3]

        base_url = "https://financialmodelingprep.com/api/v3/financial-statement-growth/" + \
                   ticker_string + "?period=annual" + '?apikey=' + financial_modelling_prep_api_key

        session = requests.session()
        request = session.get(base_url, timeout=5)
        growth_ratio = request.json()

        # Debug Statements
        # print(growth_ratio)
        # print(len(growth_ratio['growth']))
        # print(growth_ratio['growth'][0])

        # We will now run a for loop that loops through the growth data set and take the most recent 3 earnings
        # report, parse the data and put it at it respective place after parsing through calling another function
        growth_index = 0

        for growth_period in growth_ratio['growth']:
            date_array_widgets[growth_index].setText((growth_period['date']))
            gross_profit_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['Gross Profit Growth']))
            ebit_widgets[growth_index].setText(self.Convert_to_Percentage_String(growth_period['EBIT Growth']))
            operating_income_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['Operating Income Growth']))
            net_income_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['Net Income Growth']))
            earnings_per_share_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['EPS Growth']))
            dividend_per_share_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['Dividends per Share Growth']))
            free_cash_flow_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['Free Cash Flow growth']))
            debt_growth_widgets[growth_index].setText(self.Convert_to_Percentage_String(growth_period['Debt Growth']))
            rd_expense_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['R&D Expense Growth']))
            sga_widgets[growth_index].setText(self.Convert_to_Percentage_String(growth_period['SG&A Expenses Growth']))

            # We only need the first 3 data sets that are given by the data, once we detect we reach the fourth
            # data set, we would break out of the for loop
            growth_index = growth_index + 1

            if (growth_index > 2):
                break
        # All earnings data are loaded, we now parse and load data into long term financial data
        most_recent_report = growth_ratio['growth'][0]
        print(most_recent_report)
        # First we parse long term revenue growths
        self.Stock_Growth_Longterm_Revenue1.setText(
            self.Convert_to_Percentage_String(most_recent_report['3Y Revenue Growth (per Share)']))
        self.Stock_Growth_Longterm_Revenue2.setText(
            self.Convert_to_Percentage_String(most_recent_report['5Y Revenue Growth (per Share)']))
        self.Stock_Growth_Longterm_Revenue3.setText(
            self.Convert_to_Percentage_String(most_recent_report['10Y Revenue Growth (per Share)']))
        # Then we parse and add Operating Cash flow
        self.Stock_Growth_Longterm_Operating_Cashflow1.setText(
            self.Convert_to_Percentage_String(most_recent_report['3Y Operating CF Growth (per Share)']))
        self.Stock_Growth_Longterm_Operating_Cashflow2.setText(
            self.Convert_to_Percentage_String(most_recent_report['5Y Operating CF Growth (per Share)']))
        self.Stock_Growth_Longterm_Operating_Cashflow3.setText(
            self.Convert_to_Percentage_String(most_recent_report['10Y Operating CF Growth (per Share)']))
        # Then we parse and add Net Income
        self.Stock_Growth_Longterm_Net_Income1.setText(
            self.Convert_to_Percentage_String(most_recent_report['3Y Net Income Growth (per Share)']))
        self.Stock_Growth_Longterm_Net_Income2.setText(
            self.Convert_to_Percentage_String(most_recent_report['5Y Net Income Growth (per Share)']))
        self.Stock_Growth_Longterm_Net_Income3.setText(
            self.Convert_to_Percentage_String(most_recent_report['10Y Net Income Growth (per Share)']))
        # Then we parse and add Shareholder Equity
        self.Stock_Growth_Longterm_Shareholder_Equity1.setText(
            self.Convert_to_Percentage_String(most_recent_report['3Y Shareholders Equity Growth (per Share)']))
        self.Stock_Growth_Longterm_Shareholder_Equity2.setText(
            self.Convert_to_Percentage_String(most_recent_report['5Y Shareholders Equity Growth (per Share)']))
        self.Stock_Growth_Longterm_Shareholder_Equity3.setText(
            self.Convert_to_Percentage_String(most_recent_report['10Y Shareholders Equity Growth (per Share)']))

        # Call the Populate MACD Function to retrieve data from alpha vantage
        self.Populate_MACD_Graph()

        # Call the Populate Pivot Point Function
        self.Populate_Pivot_Points()

        # Now since all the data has been loaded, we would set the visibility of all widgets to be visible and refresh
        # widgets that are changed to see labels be updated
        for widget in self.stock_widgets:
            widget.show()
            widget.repaint()

    # -------------------------------------------------------------------
    # Function Name: Populate_Pivot_Points
    #
    # Description:
    # This function is called from the Search_Stocks
    # function.Using the investpy module, we would get investing.com
    # url for the company. Then, we would use beautiful soup package
    # to retrieve the technical pivot points of the equity. Lastly,
    # we would update the labels in the technical section to its data
    #
    # TODO:
    # Add functionality for stocks that aren't in the United States
    # -------------------------------------------------------------------
    def Populate_Pivot_Points(self):

        # Use the investpy package to retrieve investing.com information
        company_profile = investpy.get_stock_company_profile(stock=self.search_symbol,
                                                             country='United States')
        # Debug statement
        # print(company_profile)

        company_profile_url = company_profile['url']

        # Add string to the url for technical information
        technical_url = company_profile_url[:-15] + 'technical'

        response = requests.get(technical_url, headers={'User-Agent': 'Mozilla/5.0'})

        # Retrieve the data from above and store it into lxml file
        soup = BeautifulSoup(response.text, 'lxml')

        # Find the header <div id = technicalContent>
        data_table = soup.find_all('div', {'id': 'techinalContent'})
        # print(data_table)

        # We now have the technicalContent, perform further parsing and find all table elements
        cols = [td.text for td in data_table[0].select('td')]

        # print(cols)

        # We initializa a empty list
        parsed_list = []

        # Parse data that we receive from web scraping into array
        for text in cols:
            parsed_text = text.strip()
            if '\t' or '\n' in text:
                parsed_text = text.replace('\n', '')
                parsed_text = parsed_text.replace('\t', '')
            parsed_list.append(parsed_text)

        # print(parsed_list)

        # Add all widgets that need their labels changed into an array for updating in for loop
        pivot_point_widgets = [self.Stock_Technical_S3,self.Stock_Technical_S2,self.Stock_Technical_S1,
                               self.Stock_Technical_Pivot_Point,self.Stock_Technical_R1,self.Stock_Technical_R2,
                               self.Stock_Technical_R3]

        # Initiate for loop variables below for control
        found_pivot = False
        found_RSI = False
        pivot_index = 0

        # We traverse through each element in the data, if we found the matching data, we would then
        # update the corresponding labels
        for element in parsed_list:
            # Traverse through each element and check for flags that are set, if true then update labels
            if found_pivot and pivot_index < 6:
                pivot_point_widgets[pivot_index].setText(element)
                pivot_index = pivot_index + 1
            elif found_RSI:
                self.Stock_RSI.setText('RSI(14):' + element[0:4])
                break
            # If the element is what we need, then we would set the flag to be true and take data in
            if element == 'Classic':
                found_pivot = True
            elif element == 'RSI(14)':
                found_RSI = True

    def Search_Stocks(self):

        # Get rid of white spaces if there are any
        ticker_string = self.Search_Bar.text()
        ticker_string = ticker_string.strip()

        # Assigns a variable that other functions can use
        # TODO: Past ticker_string instead into other defs
        self.search_symbol = ticker_string

        # We set up the URL that we will need to use for the comppany profile
        url = "https://financialmodelingprep.com/api/v3/company/profile/" + ticker_string + \
              '?apikey=' + financial_modelling_prep_api_key
        session = requests.session()
        request = session.get(url, timeout=5)

        # Store the JSON data into variable for later processing
        company_data = request.json()

        # In addition to the company profile, we also obtain the latest quote information on
        # the searched equity
        quote_url = "https://financialmodelingprep.com/api/v3/quote/" + ticker_string + '?apikey=' + financial_modelling_prep_api_key
        session = requests.session()
        request = session.get(quote_url, timeout=5)
        quote_data = request.json()

        # Debug Messages
        # print(type(company_profile['mktCap']))
        # print(quote_data)

        # We now need to test the integrity of the data that we have received. We check for the amount of dictionary
        # pairs in the returned message, if it has less than 2 key-value pairs, something is wrong!
        # print(company_data)
        # print(quote_data)
        if len(company_data) < 2:
            return

        # We do basic parsing of the company data and get rid of any data we do not need
        company_profile = company_data['profile']
        self.Stock_Name.setText('  ' + str(company_profile['companyName']))
        self.Stock_Symbol.setText(company_data['symbol'])
        self.Stock_Description.setText(company_profile['description'])

        # Take the Image URL from information passed down from Financial Modelling Prep
        image_url = company_profile['image']

        # We would use the URL module and read the image file, convert it to byte
        data = urllib.request.urlopen(image_url).read()
        image = QtGui.QImage()
        image.loadFromData(data)

        # We set the company image to have the converted image
        self.Stock_Image.setPixmap(QtGui.QPixmap(image))

        # Update the label widgets with information we obtained from the API provider
        self.Stock_Price.setText(str(company_profile['price']))

        percentage_change = company_profile['changesPercentage']
        percentage_change = percentage_change[1:-1]
        self.Stock_Percentage_Change.setText(percentage_change)

        self.Stock_Volume.setText('Vol: ' + company_profile['volAvg'])
        self.Stock_Low.setText('L: ' + str(quote_data[0]['dayLow']))
        self.Stock_High.setText('H: ' + str(quote_data[0]['dayHigh']))
        self.Stock_Open.setText('O: ' + str(quote_data[0]['open']))

        beta = company_profile['beta']
        beta = beta[0:4]
        self.Stock_Beta.setText('Beta: ' + beta)
        self.Stock_Market_Capitalization.setText(company_profile['mktCap'])
        self.Stock_Exchange.setText(quote_data[0]['exhange'])
        self.Stock_Industry.setText(company_profile['industry'])
        self.Stock_Avg_Price_200.setText(str(quote_data[0]['priceAvg200'])[0:7])
        self.Stock_Average_Volume.setText(str(quote_data[0]['avgVolume']))
        self.Stock_Earnings.setText(quote_data[0]['earningsAnnouncement'][0:10])
        self.Stock_Exchange_Variable = quote_data[0]['exhange']

        # After we have updated the information, we would now need change the colour
        # of the widget based on the string
        # TODO: Perhaps changing another way to detect negative for faster processing

        if (quote_data[0]['changesPercentage']) < 0:
            self.Stock_Price.setStyleSheet('Color:RED')
            self.Stock_Percentage_Change.setStyleSheet('Color:RED')
            self.Stock_Name.setStyleSheet('Background-Color:RED;Color:WHITE')
        else:
            self.Stock_Price.setStyleSheet('Color:GREEN')
            self.Stock_Percentage_Change.setStyleSheet('Color:GREEN')
            self.Stock_Name.setStyleSheet('Background-Color:GREEN;Color:WHITE')

        # Now we manipulate data to fit our needs for growth of data
        # We first make arrays for efficiency of these information in
        # later in a loop
        date_array_widgets = [self.Stock_Growth_Date1, self.Stock_Growth_Date2, self.Stock_Growth_Date3]
        gross_profit_widgets = [self.Stock_Gross_Profit1, self.Stock_Gross_Profit2, self.Stock_Gross_Profit3]
        ebit_widgets = [self.Stock_Growth_EBIT1, self.Stock_Growth_EBIT2, self.Stock_Growth_EBIT3]
        operating_income_widgets = [self.Stock_Growth_Operating_Income1, self.Stock_Growth_Operating_Income2,
                                    self.Stock_Growth_Operating_Income3]
        net_income_widgets = [self.Stock_Growth_Net_Income1, self.Stock_Growth_Net_Income2,
                              self.Stock_Growth_Net_Income3]
        earnings_per_share_widgets = [self.Stock_Growth_Earnings_Per_Share1, self.Stock_Growth_Earnings_Per_Share2,
                                      self.Stock_Growth_Earnings_Per_Share3]
        dividend_per_share_widgets = [self.Stock_Growth_Dividend_Per_Share1, self.Stock_Growth_Dividend_Per_Share2,
                                      self.Stock_Growth_Dividend_Per_Share3]
        free_cash_flow_widgets = [self.Stock_Growth_Free_Cashflow1, self.Stock_Growth_Free_Cashflow2,
                                  self.Stock_Growth_Free_Cashflow3]
        debt_growth_widgets = [self.Stock_Growth_Debt1, self.Stock_Growth_Debt2, self.Stock_Growth_Debt3]
        rd_expense_widgets = [self.Stock_Growth_RD_Expense1, self.Stock_Growth_RD_Expense2,
                              self.Stock_Growth_RD_Expense3]
        sga_widgets = [self.Stock_Growth_SGA_Expense1, self.Stock_Growth_SGA_Expense2, self.Stock_Growth_SGA_Expense3]

        base_url = "https://financialmodelingprep.com/api/v3/financial-statement-growth/" + \
                   ticker_string + "?period=annual" + '?apikey=' + financial_modelling_prep_api_key

        session = requests.session()
        request = session.get(base_url, timeout=5)
        growth_ratio = request.json()

        # Debug Statements
        # print(growth_ratio)
        # print(len(growth_ratio['growth']))
        # print(growth_ratio['growth'][0])

        # We will now run a for loop that loops through the growth data set and take the most recent 3 earnings
        # report, parse the data and put it at it respective place after parsing through calling another function
        growth_index = 0

        for growth_period in growth_ratio['growth']:
            date_array_widgets[growth_index].setText((growth_period['date']))
            gross_profit_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['Gross Profit Growth']))
            ebit_widgets[growth_index].setText(self.Convert_to_Percentage_String(growth_period['EBIT Growth']))
            operating_income_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['Operating Income Growth']))
            net_income_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['Net Income Growth']))
            earnings_per_share_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['EPS Growth']))
            dividend_per_share_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['Dividends per Share Growth']))
            free_cash_flow_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['Free Cash Flow growth']))
            debt_growth_widgets[growth_index].setText(self.Convert_to_Percentage_String(growth_period['Debt Growth']))
            rd_expense_widgets[growth_index].setText(
                self.Convert_to_Percentage_String(growth_period['R&D Expense Growth']))
            sga_widgets[growth_index].setText(self.Convert_to_Percentage_String(growth_period['SG&A Expenses Growth']))

            # We only need the first 3 data sets that are given by the data, once we detect we reach the fourth
            # data set, we would break out of the for loop
            growth_index = growth_index + 1

            if (growth_index > 2):
                break
        # All earnings data are loaded, we now parse and load data into long term financial data
        most_recent_report = growth_ratio['growth'][0]
        print(most_recent_report)
        # First we parse long term revenue growths
        self.Stock_Growth_Longterm_Revenue1.setText(
            self.Convert_to_Percentage_String(most_recent_report['3Y Revenue Growth (per Share)']))
        self.Stock_Growth_Longterm_Revenue2.setText(
            self.Convert_to_Percentage_String(most_recent_report['5Y Revenue Growth (per Share)']))
        self.Stock_Growth_Longterm_Revenue3.setText(
            self.Convert_to_Percentage_String(most_recent_report['10Y Revenue Growth (per Share)']))
        # Then we parse and add Operating Cash flow
        self.Stock_Growth_Longterm_Operating_Cashflow1.setText(
            self.Convert_to_Percentage_String(most_recent_report['3Y Operating CF Growth (per Share)']))
        self.Stock_Growth_Longterm_Operating_Cashflow2.setText(
            self.Convert_to_Percentage_String(most_recent_report['5Y Operating CF Growth (per Share)']))
        self.Stock_Growth_Longterm_Operating_Cashflow3.setText(
            self.Convert_to_Percentage_String(most_recent_report['10Y Operating CF Growth (per Share)']))
        # Then we parse and add Net Income
        self.Stock_Growth_Longterm_Net_Income1.setText(
            self.Convert_to_Percentage_String(most_recent_report['3Y Net Income Growth (per Share)']))
        self.Stock_Growth_Longterm_Net_Income2.setText(
            self.Convert_to_Percentage_String(most_recent_report['5Y Net Income Growth (per Share)']))
        self.Stock_Growth_Longterm_Net_Income3.setText(
            self.Convert_to_Percentage_String(most_recent_report['10Y Net Income Growth (per Share)']))
        # Then we parse and add Shareholder Equity
        self.Stock_Growth_Longterm_Shareholder_Equity1.setText(
            self.Convert_to_Percentage_String(most_recent_report['3Y Shareholders Equity Growth (per Share)']))
        self.Stock_Growth_Longterm_Shareholder_Equity2.setText(
            self.Convert_to_Percentage_String(most_recent_report['5Y Shareholders Equity Growth (per Share)']))
        self.Stock_Growth_Longterm_Shareholder_Equity3.setText(
            self.Convert_to_Percentage_String(most_recent_report['10Y Shareholders Equity Growth (per Share)']))

        # Call the Populate MACD Function to retrieve data from alpha vantage
        self.Populate_MACD_Graph()

        # Call the Populate Pivot Point Function
        self.Populate_Pivot_Points()

        # Now since all the data has been loaded, we would set the visibility of all widgets to be visible and refresh
        # widgets that are changed to see labels be updated
        for widget in self.stock_widgets:
            widget.show()
            widget.repaint()

    # -------------------------------------------------------------------
    # Function Name: Populate_MACD_Graph
    #
    # Description:
    # This function is called from the Search_Stocks function, using the
    # API call from alpha vantage, we would receive relevant data. Then
    # we process the data and plots it into pyqtgraph
    #
    # TODO:
    # Add colour scheme for bars, green for positive and red for negative
    # Add current stock prices
    # -------------------------------------------------------------------
    def Populate_MACD_Graph(self):
        technical_url = 'https://www.alphavantage.co/query?function=MACD&symbol=' + self.search_symbol + \
                        '&interval=daily&series_type=open&apikey=' + alpha_vantage_api_key

        req_ob = requests.get(technical_url)

        # result contains list of nested dictionaries
        result = req_ob.json()

        last_refresh_date = result['Meta Data']['3: Last Refreshed']
        print("Last Refresh Date is:" + last_refresh_date)

        interval = result['Meta Data']['4: Interval']
        print("The interval of refresh is :" + last_refresh_date)

        macd_data = result['Technical Analysis: MACD']

        # Declare Four Variables that we need to plot into the graph
        date_array = []
        macd_array = []
        macd_signal_array = []
        macd_hist_array = []
        # print('The type of data of macd_data is:' + str(type(macd_data)))

        index = 0
        # Go through this loop and store everything into an array later for plotting
        for data in macd_data:
            if index < 200:
                # print('The type of data is: ' + str(type(date))+ ' and the value is:' + str(date))

                # First convert the string to datetime function
                date = datetime.strptime(data, '%Y-%m-%d')

                # Store the respective variables into an array
                date_array.append(date)
                macd_array.append(float(macd_data[data]['MACD']))
                macd_signal_array.append(float(macd_data[data]['MACD_Signal']))
                macd_hist_array.append(float(macd_data[data]['MACD_Hist']))
                index = index + 1
            else:
                break

        # Seperately plot two lines into the pyqtgraph widget, one for MACD Signal and one for MACD
        for i in range(2):
            if i == 0:
                # First plot the MACD values
                y_data = macd_array
            elif i == 1:
                # Then we plot the MACD Signals
                y_data = macd_signal_array

            # Now we plot our values onto the widget
            self.Stock_Technical_MACD.plot(x=[x.timestamp() for x in date_array], y=y_data, pen=(i, 2), width = 2)

        # Initialize the bar chart
        bar = pg.BarGraphItem(x=[x.timestamp() for x in date_array], height=macd_hist_array, width=0.3, brush='r')

        # Add the bar chart onto the graph widget itself with the addItem function
        self.Stock_Technical_MACD.addItem(bar)

    # -------------------------------------------------------------------
    # Function Name: Convert_to_Percentage_String
    #
    # Description: This function is called to convert string numbers into
    # its perspective float and parses it to have 5 significant figures
    # and returns data that are parsed
    # -------------------------------------------------------------------
    def Convert_to_Percentage_String(self, string_input):
        # We first convert the string to float
        string_float = float(string_input)
        # if the float value is less than 0, there would already be an - sign, add %
        # else we would add the + sign and cut off one less character
        if string_float < 0:
            return_string = str(string_float * 100)[0:6] + "%"
        else:
            return_string = '+' + str(string_float * 100)[0:5] + "%"

        return return_string

    # -------------------------------------------------------------------
    # Function Name: OpenTradingView
    #
    # Description: This function is ran everytime a stock is searched up
    # and whenever this button is shown, we open the webpage to trading
    # view interface on our browser.
    # -------------------------------------------------------------------
    def OpenTradingView(self):
        #
        tradingview_url = "https://www.tradingview.com/symbols/" + self.Stock_Exchange_Variable + '-' \
                          + self.Stock_Symbol.text()

        webbrowser.open(tradingview_url)

    # -------------------------------------------------------------------
    # Function Name: UpdateBanner
    #
    # Description: This function is run every 30 seconds to update the
    # banner on the top of main window application that refreshes by
    # making a query to financialmodellingprep.com, multiple quotes.
    # When we receive a correct result from the website, we would update
    # the banners to have its information filled in.
    #
    # TODO:
    # Change colour based on the percentaged changed being + or -
    # Background colour flash for every update
    # Improve mass updating of banners to shave processing time
    # -------------------------------------------------------------------

    def UpdateBanner(self):
        # Fetch Real Time Data and Stores Previous Day Price
        # -------------------------------------------------------------------
        # ETFs Shown on Header:
        # SPY - SPDR S&P 500 ETF Trust -
        # QQQ - Invesco QQQ Trust
        # IWM - iShares Russell 2000 ETF
        # DIA - SPDR Dow Jones Industrial Average ETF Trust
        # ^VIX - CBOE Volatility Index
        # GLD - SPDR Gold Shares
        # WTI - Crude Oil Index
        # -------------------------------------------------------------------
        banner_indices = ['SPY', 'QQQ', 'IWM', 'DIA', '^VIX', 'GLD', 'WTI']

        # Iterate through the array of tickers and add it to the quote string
        # We are requesting multiple quotes from
        quote_string = ','.join(banner_indices)

        # The URL that we will concatenate with quote_string, makes the request
        # and stores the result into closing_price_data
        url = "https://financialmodelingprep.com/api/v3/quote/" + quote_string + '?apikey=' + financial_modelling_prep_api_key
        session = requests.session()
        request = session.get(url, timeout=5)
        closing_price_data = request.json()

        # Add the all widgets into an array
        colour_change_widgets = [self.Index_Percentage_0, self.Index_Percentage_1, self.Index_Percentage_2,
                                 self.Index_Percentage_3,
                                 self.Index_Percentage_4, self.Index_Percentage_5, self.Index_Percentage_6]

        print(closing_price_data)
        # We would parse the data by looping through the nested dictionary and
        # insert the content of each dictionary into its rightful place
        for key in closing_price_data:
            if key['symbol'] == banner_indices[0]:
                self.Index_Symbol_0.setText(key['symbol'])
                self.Index_Price_0.setText(str(key['price']))
                # We take out the one word pre-fix to the ETF name
                self.Index_Name_0.setText(str(key['name']).split(' ', 1)[1])
                self.Index_Percentage_0.setText(str(key['changesPercentage']) + "%")
            elif key['symbol'] == banner_indices[1]:
                self.Index_Symbol_1.setText(key['symbol'])
                self.Index_Price_1.setText(str(key['price']))
                self.Index_Name_1.setText(str(key['name']).split(' ', 1)[1])
                self.Index_Percentage_1.setText(str(key['changesPercentage']) + "%")
            elif key['symbol'] == banner_indices[2]:
                self.Index_Symbol_2.setText(key['symbol'])
                self.Index_Price_2.setText(str(key['price']))
                self.Index_Name_2.setText(str(key['name']).split(' ', 1)[1])
                self.Index_Percentage_2.setText(str(key['changesPercentage']) + "%")
            elif key['symbol'] == banner_indices[3]:
                self.Index_Symbol_3.setText(key['symbol'])
                self.Index_Price_3.setText(str(key['price']))
                self.Index_Name_3.setText(str(key['name']).split(' ', 1)[1])
                self.Index_Percentage_3.setText(str(key['changesPercentage']) + "%")
            elif key['symbol'] == banner_indices[4]:
                self.Index_Symbol_4.setText(key['symbol'])
                self.Index_Price_4.setText(str(key['price']))
                self.Index_Name_4.setText(str(key['name']).split(' ', 1)[1])
                self.Index_Percentage_4.setText(str(key['changesPercentage']) + "%")
            elif key['symbol'] == banner_indices[5]:
                self.Index_Symbol_5.setText(key['symbol'])
                self.Index_Price_5.setText(str(key['price']))
                self.Index_Name_5.setText(str(key['name']).split(' ', 1)[1])
                self.Index_Percentage_5.setText(str(key['changesPercentage']) + "%")
            elif key['symbol'] == banner_indices[6]:
                self.Index_Symbol_6.setText(key['symbol'])
                self.Index_Price_6.setText(str(key['price']))
                self.Index_Name_6.setText(str(key['name']).split(' ', 1)[1])
                self.Index_Percentage_6.setText(str(key['changesPercentage']) + "%")
        # Go through every single percentage changed that needs colour adjusted and make red for losses
        # and green for anything that's above 0.00%
        for w in colour_change_widgets:
            if '-' in w.text():
                w.setStyleSheet("color:red")
            else:
                w.setStyleSheet("color:green")

    # -------------------------------------------------------------------
    # Function Name: PopulateSectorPerformances
    #
    # Description: This function is called to populate the performances of
    #              each sector performance in real time
    #
    # TODO:
    # Change colour based on the percentaged changed being + or -
    # Background colour flash for every update
    # Improve mass updating of banners to shave processing time
    # -------------------------------------------------------------------

    def PopulateSectorPerformances(self):
        # Fetch Real Time Data and Stores Previous Day Price
        # -------------------------------------------------------------------
        # Sectors Interested:
        # Slot 0 - Consumer Discretionary
        # Slot 1 - Energy
        # Slot 2 - Communication Services
        # Slot 3 - Information Technology
        # Slot 4 - Consumer Staples
        # Slot 5 - Health Care
        # Slot 6 - Materials
        # Slot 7 - Utilities
        # Slot 8 - Industrials
        # Slot 9 - Financials
        # Based on the selected index of the performance, we would update the
        # titles and data associated with the sector performance
        # -------------------------------------------------------------------
        print("The index changed is: " + str(self.Sector_Performance_Title.currentIndex()))

        sector_indices = ['Consumer Discretionary', 'Energy', 'Communication Services', 'Information Technology',
                          'Consumer Staples', 'Health Care', 'Materials', 'Utilities', 'Industrials', 'Financials']

        # This index maps the timeline to the dictionary passed by the json requests by alpha vantage
        timeline_indice = ['Rank A: Real-Time Performance', 'Rank B: 1 Day Performance', 'Rank C: 5 Day Performance',
                           'Rank D: 1 Month Performance', 'Rank E: 3 Month Performance',
                           'Rank F: Year-to-Date (YTD) Performance',
                           'Rank G: 1 Year Performance', 'Rank H: 3 Year Performance', 'Rank I: 5 Year Performance',
                           'Rank J: 10 Year Performance']

        colour_change_widgets = [self.Sector_Percentage_0, self.Sector_Percentage_1, self.Sector_Percentage_2,
                                 self.Sector_Percentage_3,
                                 self.Sector_Percentage_4, self.Sector_Percentage_5, self.Sector_Percentage_6,
                                 self.Sector_Percentage_7,
                                 self.Sector_Percentage_8, self.Sector_Percentage_9]

        # base_url variable that stores the base url
        base_url = "https://www.alphavantage.co/query?function=SECTOR"

        # main_url variable that stores complete url with API key
        main_url = base_url + "&apikey=" + alpha_vantage_api_key

        # get method of requests module
        # return response object
        req_ob = requests.get(main_url)

        # result contains list of nested dictionaries
        result = req_ob.json()

        parsed_dictionary = result[timeline_indice[self.Sector_Performance_Title.currentIndex()]]

        for key in parsed_dictionary:
            if key == sector_indices[0]:
                self.Sector_Name_0.setText(key)
                self.Sector_Percentage_0.setText(parsed_dictionary[key])
            elif key == sector_indices[1]:
                self.Sector_Name_1.setText(key)
                self.Sector_Percentage_1.setText(parsed_dictionary[key])
            elif key == sector_indices[2]:
                self.Sector_Name_2.setText(key)
                self.Sector_Percentage_2.setText(parsed_dictionary[key])
            elif key == sector_indices[3]:
                self.Sector_Name_3.setText(key)
                self.Sector_Percentage_3.setText(parsed_dictionary[key])
            elif key == sector_indices[4]:
                self.Sector_Name_4.setText(key)
                self.Sector_Percentage_4.setText(parsed_dictionary[key])
            elif key == sector_indices[5]:
                self.Sector_Name_5.setText(key)
                self.Sector_Percentage_5.setText(parsed_dictionary[key])
            elif key == sector_indices[6]:
                self.Sector_Name_6.setText(key)
                self.Sector_Percentage_6.setText(parsed_dictionary[key])
            elif key == sector_indices[7]:
                self.Sector_Name_7.setText(key)
                self.Sector_Percentage_7.setText(parsed_dictionary[key])
            elif key == sector_indices[8]:
                self.Sector_Name_8.setText(key)
                self.Sector_Percentage_8.setText(parsed_dictionary[key])
            elif key == sector_indices[9]:
                self.Sector_Name_9.setText(key)
                self.Sector_Percentage_9.setText(parsed_dictionary[key])

        status_url = "https://financialmodelingprep.com/api/v3/is-the-market-open"+ '?apikey=' + financial_modelling_prep_api_key
        session = requests.session()
        request = session.get(status_url, timeout=5)
        market_status = request.json()
        print(type(market_status['isTheStockMarketOpen']))
        print(market_status['isTheStockMarketOpen'])

        if (market_status['isTheStockMarketOpen'] == True):
            self.Marke_Open_Label.setText("Market Open")
            self.Marke_Open_Label.setStyleSheet('Background-Color:GREEN;COLOR:WHITE')
        else:
            self.Marke_Open_Label.setText("Market Closed")
            self.Marke_Open_Label.setStyleSheet('Background-Color:RED;COLOR:WHITE')

        for w in colour_change_widgets:
            if '-' in w.text():
                w.setStyleSheet("color:red")
            else:
                w.setStyleSheet("color:green")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Will\'s Stock Screener"))
        self.TimeNow_Label.setText(_translate("MainWindow", "00:00:00"))
        self.DateNow_Label.setText(_translate("MainWindow", "Apr 14 2020"))
        self.Index_Symbol_0.setText(_translate("MainWindow", "SPY"))
        self.Index_Percentage_0.setText(_translate("MainWindow", "-0.00%"))
        self.Index_Price_0.setText(_translate("MainWindow", "100.00"))
        self.Index_Symbol_1.setText(_translate("MainWindow", "QQQ"))
        self.Index_Percentage_1.setText(_translate("MainWindow", "-0.00%"))
        self.Index_Price_1.setText(_translate("MainWindow", "100.00"))
        self.Index_Percentage_2.setText(_translate("MainWindow", "-0.00%"))
        self.Index_Symbol_2.setText(_translate("MainWindow", "IWM"))
        self.Index_Price_2.setText(_translate("MainWindow", "100.00"))
        self.Index_Percentage_3.setText(_translate("MainWindow", "-0.00%"))
        self.Index_Symbol_3.setText(_translate("MainWindow", "DIA"))
        self.Index_Price_3.setText(_translate("MainWindow", "100.00"))
        self.Index_Percentage_4.setText(_translate("MainWindow", "-0.00%"))
        self.Index_Symbol_4.setText(_translate("MainWindow", "^VIX"))
        self.Index_Price_4.setText(_translate("MainWindow", "100.00"))
        self.Index_Percentage_5.setText(_translate("MainWindow", "-0.00%"))
        self.Index_Symbol_5.setText(_translate("MainWindow", "GLD"))
        self.Index_Price_5.setText(_translate("MainWindow", "100.00"))
        self.Index_Percentage_6.setText(_translate("MainWindow", "-0.00%"))
        self.Index_Symbol_6.setText(_translate("MainWindow", "WTI"))
        self.Index_Price_6.setText(_translate("MainWindow", "100.00"))
        self.Index_Name_0.setText(_translate("MainWindow", "S&P 500 ETF Trust"))
        self.Index_Name_1.setText(_translate("MainWindow", "QQQ Trust"))
        self.Index_Name_2.setText(_translate("MainWindow", "Russell 2000 ETF"))
        self.Index_Name_3.setText(_translate("MainWindow", "Dow Jones Industrial"))
        self.Index_Name_4.setText(_translate("MainWindow", "Volatility Index"))
        self.Index_Name_5.setText(_translate("MainWindow", "Gold Shares"))
        self.Index_Name_6.setText(_translate("MainWindow", "Offshore, Inc."))
        self.Sector_Name_0.setText(_translate("MainWindow", "Consumer Discretionary"))
        self.Sector_Percentage_0.setText(_translate("MainWindow", "-0.00%"))
        self.Sector_Percentage_1.setText(_translate("MainWindow", "-0.00%"))
        self.Sector_Name_1.setText(_translate("MainWindow", "Energy"))
        self.Sector_Percentage_2.setText(_translate("MainWindow", "-0.00%"))
        self.Sector_Name_2.setText(_translate("MainWindow", "Communication Services"))
        self.Sector_Percentage_3.setText(_translate("MainWindow", "-0.00%"))
        self.Sector_Name_3.setText(_translate("MainWindow", "Information Technology"))
        self.Sector_Percentage_4.setText(_translate("MainWindow", "-0.00%"))
        self.Sector_Name_4.setText(_translate("MainWindow", "Consumer Staples"))
        self.Sector_Percentage_5.setText(_translate("MainWindow", "-0.00%"))
        self.Sector_Name_5.setText(_translate("MainWindow", "Health Care"))
        self.Sector_Percentage_6.setText(_translate("MainWindow", "-0.00%"))
        self.Sector_Name_6.setText(_translate("MainWindow", "Materials"))
        self.Sector_Percentage_7.setText(_translate("MainWindow", "-0.00%"))
        self.Sector_Name_7.setText(_translate("MainWindow", "Utilities"))
        self.Sector_Name_9.setText(_translate("MainWindow", "Financials"))
        self.Sector_Percentage_9.setText(_translate("MainWindow", "-0.00%"))
        self.Sector_Name_8.setText(_translate("MainWindow", "Industrials"))
        self.Sector_Percentage_8.setText(_translate("MainWindow", "-0.00%"))
        self.Sector_Performance_Title.setItemText(0, _translate("MainWindow", "Real-Time Performance"))
        self.Sector_Performance_Title.setItemText(1, _translate("MainWindow", "1 Day Performance"))
        self.Sector_Performance_Title.setItemText(2, _translate("MainWindow", "5 Day Performance"))
        self.Sector_Performance_Title.setItemText(3, _translate("MainWindow", "1 Month Performance"))
        self.Sector_Performance_Title.setItemText(4, _translate("MainWindow", "3 Month Performance"))
        self.Sector_Performance_Title.setItemText(5, _translate("MainWindow", "Year-to-Date (YTD) Performance"))
        self.Sector_Performance_Title.setItemText(6, _translate("MainWindow", "1 Year Performance"))
        self.Sector_Performance_Title.setItemText(7, _translate("MainWindow", "3 Year Performance"))
        self.Sector_Performance_Title.setItemText(8, _translate("MainWindow", "5 Year Performance"))
        self.Sector_Performance_Title.setItemText(9, _translate("MainWindow", "10 Year Performance"))
        self.Sector_Performance_Title_2.setText(_translate("MainWindow", "Sector Performance"))
        self.Marke_Open_Label.setText(_translate("MainWindow", "Open"))
        self.Search_Bar.setPlaceholderText(_translate("MainWindow", "Tickers..."))
        self.Stock_Symbol.setText(_translate("MainWindow", "AAPL"))
        self.Stock_Description_Header.setText(_translate("MainWindow", "Description:"))
        self.Stock_Description.setText(_translate("MainWindow", "Apple Inc is designs, manufactures and markets mobile communication and media devices and personal computers, and sells a variety of related software, services, accessories, networking solutions and third-party digital content and applications."))
        self.Stock_Image.setText(_translate("MainWindow", "[img]"))
        self.Stock_Industry_Title.setText(_translate("MainWindow", "Industry:"))
        self.Stock_Exchange_Title.setText(_translate("MainWindow", "Exchange:"))
        self.Stock_Industry.setText(_translate("MainWindow", "Online Media"))
        self.Stock_Exchange.setText(_translate("MainWindow", "NASDAQ"))
        self.Stock_Price.setText(_translate("MainWindow", "69.00"))
        self.Stock_Percentage_Change.setText(_translate("MainWindow", "+0.15"))
        self.Stock_Volume.setText(_translate("MainWindow", "Vol: "))
        self.Stock_Name.setText(_translate("MainWindow", "AAPL"))
        self.Stock_Market_Capitalization_Title.setText(_translate("MainWindow", "Market Cap:"))
        self.Stock_Beta.setText(_translate("MainWindow", "Beta:"))
        self.Stock_Open.setText(_translate("MainWindow", "Open:"))
        self.Stock_High.setText(_translate("MainWindow", "H:"))
        self.Stock_Low.setText(_translate("MainWindow", "L:"))
        self.Stock_Earnings_Title.setText(_translate("MainWindow", "Earnings:"))
        self.Stock_Market_Capitalization.setText(_translate("MainWindow", "1.3 Billion"))
        self.Stock_Earnings.setText(_translate("MainWindow", "13-Apr-2020"))
        self.Stock_AverageVolume_Title.setText(_translate("MainWindow", "Avg Volume:"))
        self.Stock_Average_Volume.setText(_translate("MainWindow", "1234567890"))
        self.Stock_View_Chart.setText(_translate("MainWindow", "View Chart"))
        self.Stock_Avg_Price_200_Title.setText(_translate("MainWindow", "Price Avg 200:"))
        self.Stock_Avg_Price_200.setText(_translate("MainWindow", "243.22"))
        self.Stock_Growth_Financia_Title.setText(_translate("MainWindow", "Annual Financial Growth"))
        self.Stock_Gross_Profit_Title.setText(_translate("MainWindow", "Gross Profit:"))
        self.Stock_Growth_EBIT_Title.setText(_translate("MainWindow", "EBIT:"))
        self.Stock_Growth_Operating_Income_Title.setText(_translate("MainWindow", "Operating income:"))
        self.Stock_Growth_Net_Income_Title.setText(_translate("MainWindow", "Net Income:"))
        self.Stock_Growth_Earnings_Per_Share_Title.setText(_translate("MainWindow", "Earnings per Share:"))
        self.Stock_Growth_Dividend_Per_Share_Title.setText(_translate("MainWindow", "Dividend per Share"))
        self.Stock_Growth_Free_Cashflow_Title.setText(_translate("MainWindow", "Free Cashflow :"))
        self.Stock_Growth_Debt_Title.setText(_translate("MainWindow", "Debt Growth:"))
        self.Stock_Growth_RD_Expense_Title.setText(_translate("MainWindow", "R & D Expense:"))
        self.Stock_RSI.setText(_translate("MainWindow", "RSI(14):"))
        self.Stock_Growth_SGA_Expense_Title.setText(_translate("MainWindow", "SG&A:"))
        self.Stock_Growth_Longterm_Financial_Growth_Title.setText(_translate("MainWindow", "Long-Term Financial Growth"))
        self.Stock_Growth_Longterm_Revenue_Title.setText(_translate("MainWindow", "Revenue:"))
        self.Stock_Growth_Longterm_Operating_Cashflow_Title.setText(_translate("MainWindow", "Operating Cashflow:"))
        self.Stock_Growth_Longterm_Net_Income_Title.setText(_translate("MainWindow", "Net Income:"))
        self.Stock_Growth_Longterm_Shareholder_Equity_Title.setText(_translate("MainWindow", "Shareholder Equity:"))
        self.Stock_Growth_Date1.setText(_translate("MainWindow", "13-Apr-2020"))
        self.Stock_Growth_Date2.setText(_translate("MainWindow", "13-Apr-2019"))
        self.Stock_Growth_Date3.setText(_translate("MainWindow", "13-Apr-2018"))
        self.Stock_Growth_Longterm_Date1.setText(_translate("MainWindow", "3 Years"))
        self.Stock_Growth_Longterm_Date2.setText(_translate("MainWindow", "5 Years"))
        self.Stock_Growth_Longterm_Date3.setText(_translate("MainWindow", "10 Years"))
        self.Stock_Gross_Profit1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_EBIT1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Operating_Income1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Net_Income1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Earnings_Per_Share1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Dividend_Per_Share1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Free_Cashflow1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Debt1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_RD_Expense1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_SGA_Expense1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Gross_Profit2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_EBIT2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Operating_Income2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Net_Income2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Earnings_Per_Share2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Dividend_Per_Share2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Free_Cashflow2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Debt2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_RD_Expense2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_SGA_Expense2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Gross_Profit3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_EBIT3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Operating_Income3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Net_Income3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Earnings_Per_Share3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Dividend_Per_Share3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Free_Cashflow3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Debt3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_RD_Expense3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_SGA_Expense3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Revenue1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Revenue2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Revenue3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Operating_Cashflow1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Operating_Cashflow2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Operating_Cashflow3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Net_Income1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Shareholder_Equity1.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Net_Income2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Shareholder_Equity2.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Net_Income3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Longterm_Shareholder_Equity3.setText(_translate("MainWindow", "+00.00%"))
        self.Stock_Growth_Switch_Button.setText(_translate("MainWindow", "Quarterly"))
        self.Stock_Technical_S3_Title.setText(_translate("MainWindow", "S3"))
        self.Stock_Technical_S2_Title.setText(_translate("MainWindow", "S2"))
        self.Stock_Technical_S1_Title.setText(_translate("MainWindow", "S1"))
        self.Stock_Technical_Pivot_Point_Title.setText(_translate("MainWindow", "Pivot Point"))
        self.Stock_Technical_R1_Title.setText(_translate("MainWindow", "R1"))
        self.Stock_Technical_R2_Title.setText(_translate("MainWindow", "R2"))
        self.Stock_Technical_R3_Title.setText(_translate("MainWindow", "R3"))
        self.Stock_Technical_S3.setText(_translate("MainWindow", "132.32"))
        self.Stock_Technical_S2.setText(_translate("MainWindow", "132.32"))
        self.Stock_Technical_S1.setText(_translate("MainWindow", "132.32"))
        self.Stock_Technical_Pivot_Point.setText(_translate("MainWindow", "132.32"))
        self.Stock_Technical_R1.setText(_translate("MainWindow", "132.32"))
        self.Stock_Technical_R2.setText(_translate("MainWindow", "132.32"))
        self.Stock_Technical_R3.setText(_translate("MainWindow", "132.32"))

# *********************************************************************************************************
# Class Name: TimeAxisItem
#
# Functionality:
# This class is used solely for changing the x-axis for pyqtgraph from numeric values to datetime values 
# *********************************************************************************************************
class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value) for value in values]

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
