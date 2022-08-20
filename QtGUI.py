from decimal import Rounded
from utils import *
from authentication import authenticate
from prettyprinter import pprint

''' --- GUI Imports --- '''
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel


''' --- constants --- '''
WIN_WIDTH, WIN_HEIGHT = 1100, 600
TASKBAR_HEIGHT = 40
SPOTIFY_GREEN = "#1DB954"
BLACK = "#000000"
sp = authenticate()


class TopArtistsTab(QWidget):
    """
        This class handels all the Widgets, Data and Information regarding the favorite
        Artists of the User
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.info_tab = QWidget()


class TopSongsTab(QWidget):
    """
        This class handels all the Widgets, Data and Information regarding the all Time
        Songs of the User
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.info_tab = QWidget()


class InfoTab(QWidget):
    """
        This class handels all the Widgets, Data and Information for the Information Tab
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.info_tab = QWidget()


class TabControl(QWidget):
    """
        This class handels all the different Tabs
    """

    def __init__(self, parent: QWidget = None):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.all_tabs = QTabWidget()
        self.all_tabs.resize(100, 100)

        # Adding all tabs
        self.all_tabs.addTab(InfoTab(self), "General Infos")
        self.all_tabs.addTab(TopSongsTab(self), "Your all Time Fav's")
        self.all_tabs.addTab(TopArtistsTab(self), "Your favorite Artists")

        # Add tabs to widget
        self.layout.addWidget(self.all_tabs)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):   # App class inherits from the tk.Tk
    """
        This class handels all the Widgets, Tabs etc.
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        self.init_geometry()
        self.init_Tabs()
        self.show()

    def init_geometry(self):
        # configure the main window
        self.setWindowTitle("Spotify Analyzer")

        # center the Window to the screen
        self.screen_size = QtWidgets.QDesktopWidget().screenGeometry(-1)
        x = (self.screen_size.width()/2) - (WIN_WIDTH/2)
        y = (self.screen_size.height()/2) - (WIN_HEIGHT/2) - TASKBAR_HEIGHT
        self.setGeometry(x, y, WIN_WIDTH, WIN_HEIGHT)

        # changing the icon from the window
        self.spotify_logo = QtGui.QIcon("imgs/Spotify_logo.png")
        self.setWindowIcon(self.spotify_logo)

        # changing the background color
        self.setStyleSheet(f"background:{BLACK}")

    def init_Tabs(self):
        self.table_widget = TabControl(self)
        self.setCentralWidget(self.table_widget)


app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
