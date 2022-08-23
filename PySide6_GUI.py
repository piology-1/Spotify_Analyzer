from ast import main
from utils import *
from authentication import authenticate
import requests
from io import BytesIO
from PIL import Image, ImageTk
from prettyprinter import pprint

''' --- GUI Imports --- '''
import sys
from PySide6 import *
from PySide6.QtWidgets import *
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

        data = get_current_user(sp=sp)
        user = data["name"]
        welcome_text_Label = QLabel(f"Hello, nice to see you!")

        info_text = f"Hello,\nI'm glad, that you're interested in this Spotify Analyzer.\nThis Application will show you:\n\t- Your all time favorite Tracks\n\t- Your all time favorite Artists\n\t- Your all recently played Songs\n\t- The possibility, to add Songs to the queue\n\nHave fun and enjoy\n\t~Piology"
        info_Label = QLabel(info_text)

        main_layout = QHBoxLayout()
        main_layout.addWidget(welcome_text_Label)
        main_layout.addWidget(info_Label)
        main_layout.addStretch(1)
        self.setLayout(main_layout)


class MainWindow(QMainWindow):   # It dosn't really work with QMainWindow
    """
        This class handels all the Widgets, Tabs etc.
    """

    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)

        ''' init geoemtry '''
        self.setWindowTitle("Spotify Analyzer")
        # self.setGeometry(50, 50, WIN_WIDTH, WIN_HEIGHT)
        spotify_logo = QIcon("imgs/Spotify_logo.png")
        self.setWindowIcon(spotify_logo)
        self.setStyleSheet(f"background: {BLACK}")

        ''' ------------------------------------------------------------------ '''

        tab_widget = QTabWidget()  # creating a Tabwidget
        # setting the tabWidget as the main window’s central widget
        self.setCentralWidget(tab_widget)

        #  all Tabs to the TabWidget
        tab_widget.addTab(InfoTab(self), QIcon(
            "imgs/info_icon.png"), "General Infos")
        tab_widget.addTab(TopSongsTab(self), "Your all Time Fav's")
        tab_widget.addTab(TopArtistsTab(self), "Your favorite Artists")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

        self.show()


app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())
