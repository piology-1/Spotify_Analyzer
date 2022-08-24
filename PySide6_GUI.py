from ctypes import alignment
from random import triangular
from tkinter import CENTER, TOP
from utils import *
from authentication import authenticate
import requests
from io import BytesIO
from prettyprinter import pprint

''' --- GUI Imports --- '''
import sys
from PIL import Image, ImageTk
from PySide6 import *
from PySide6.QtWidgets import *  # z.B. PySide6.QtWidgets.QVBoxLayout
from PySide6.QtGui import *  # QFont

''' --- constants --- '''
WIN_WIDTH, WIN_HEIGHT = 1100, 600  # default window geometry
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
        pass


class TopSongsTab(QWidget):
    """
        This class handels all the Widgets, Data and Information regarding the all Time
        Songs of the User
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        pass


class InfoTab(QWidget):
    """
        This class handels all the Widgets, Data and Information for the general Information Tab
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setStyleSheet(
            "background-image: url(imgs/Spotify_color_gradient.png)")
        data = get_current_user(sp=sp)
        user = data["name"]
        welcome_text_Label = QLabel(f"Hello {user}!", self)
        welcome_text_Label.setFont(QFont("Helvetica", 40))
        welcome_text_Label.setStyleSheet(
            "font-weight: bold; background: transparent")

        info_text = f"I'm glad, that you're interested in this Spotify Analyzer.\nThis Application will show you:\n\t- Your all time favorite Tracks\n\t- Your all time favorite Artists\n\t- Your all recently played Songs\n\t- The possibility, to add Songs to the queue\n\nHave fun and enjoy\n\t~Piology"
        info_Label = QLabel(info_text, self)
        info_Label.setStyleSheet("background: transparent")

        # downloading the profile pic
        user_picture_url = data['profile_img']
        user_picture = QImage()
        user_picture.loadFromData(requests.get(url=user_picture_url).content)
        picture_resized = user_picture.scaled(600, 600)
        image_label = QLabel(self)
        image_label.setPixmap(QPixmap(user_picture))
        image_label.show()
        image_label.setStyleSheet("background: transparent")
        # TODO: cloud make the profile picture Circular (https://www.geeksforgeeks.org/pyqt5-how-to-create-circular-image-from-any-image/)

        # main_layout.addRow(image_label)
        # QFormLayout(self) with addRow(QLabel(), QLineEdit()) provides an entry Box to the QLabel

        main_layout = QGridLayout(self)
        # main_layout.addWidget(QWidget, row, column, rowSpan, columnSpan, alignment)
        main_layout.addWidget(welcome_text_Label, 0, 0, 1, 2, Qt.AlignCenter)
        main_layout.addWidget(info_Label, 1, 0, Qt.AlignTop)
        main_layout.addWidget(image_label, 1, 1, Qt.AlignCenter)
        # main_layout.addStretch(1)
        self.setLayout(main_layout)


class MainWindow(QMainWindow):   # It dosn't really work with QMainWindow
    """
        This class handels all the Widgets, Tabs etc.
    """

    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)

        ''' init geoemetry '''
        self.setWindowTitle("Spotify Analyzer")
        # self.setGeometry(50, 50, WIN_WIDTH, WIN_HEIGHT)
        spotify_logo = QIcon("imgs/Spotify_logo.png")
        self.setWindowIcon(spotify_logo)
        self.setStyleSheet(f"background: {BLACK}")

        ''' ------------------------------------------------------------------ '''

        self.tab_widget = QTabWidget()  # creating a Tabwidget

        # setting the tabWidget as the main window’s central widget
        self.setCentralWidget(self.tab_widget)

        # TODO: Do I need a QTabWidget() and a QTabBar()?
        #tab_bar = QTabBar()
        #tab_bar = all_tabs.tabBar()
        # tab_bar = all_tabs.tabBar() # is this eequal to tab_bar = QTabBar()?
        tab_bar = self.tab_widget.tabBar()

        #  adding all Tabs to the TabWidget
        self.tab_widget.addTab(InfoTab(self), QIcon(
            "imgs/info_icon.png"), "General Infos")
        self.tab_widget.addTab(TopSongsTab(self), "Your all Time Fav's")
        self.tab_widget.addTab(TopArtistsTab(self), "Your favorite Artists")

        self.tab_widget.setMovable(True)

        self.tab_widget.setTabsClosable(True)
        # self.tab_widget.tabCloseRequested(self.close_Tab)

        self.tab_widget.setTabShape(QTabWidget.TabShape.Triangular)
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setUsesScrollButtons(True)

        tab_bar.setStyleSheet(
            f"background: {SPOTIFY_GREEN}; color: white; border: 5px")
        self.tab_widget.setStyleSheet(
            "background-image: url(imgs/Spotify_color_gradient.png)")

        # creating a layout for flexible usage
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

        self.show()

    def close_Tab(self, current_Index):
        """
            callback Function, when the Tabs getting closed
            TODO: adding functionality, to add the tabs again (maybe from the Info Tab?)
            TODO: Making the Info Tab uncloseable

        """
        self.tab_widget.removeTab(current_Index)  # removes the current Tab


app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())
