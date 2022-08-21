from turtle import color
from utils import *
from authentication import authenticate
import requests
from io import BytesIO
from PIL import Image, ImageTk
from prettyprinter import pprint

''' --- GUI Imports --- '''
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
# QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *  # QFont


''' --- constants --- '''
# WIN_WIDTH, WIN_HEIGHT = 1100, 600
# SCREEN_SIZE = QtWidgets.QDesktopWidget().screenGeometry(-1)
# WIN_WIDTH, WIN_HEIGHT = SCREEN_SIZE.width(), SCREEN_SIZE.height()

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

        self.top_artists_tab = QWidget()
        self.data = get_all_top_artists(sp=sp)
        self.show_data()

    def show_data(self):
        one_data_height = 175  # px
        pic_width, pic_height = 150, 150  # px
        padding_between_songs = 20  # px
        border_padding = 100  # px
        y_starting_point = 25  # px
        followers_padding = 100  # px

        for index in range(0, 10, 1):  # top 10
            """ Visualize top Artists """
            self.top_artist = str(self.data['artists'][index])
            self.top_artist_output_text = f"{index+1}. {self.top_artist}"
            self.top_artist_Label = QLabel(self.top_artist_output_text, self)
            self.top_artist_Label.setFont(QFont("Helvetica", 50))
            self.top_artist_Label.setStyleSheet(
                "font-weight: bold; background: transparent")
            self.top_artist_Label.adjustSize()
            self.top_artist_Label.move(
                (border_padding), (y_starting_point))

            """ Visualize amount of Followers from the top Artists """
            self.artists_followers = str(
                self.data['amount_of_followers'][index])
            self.follower_output_text = f"Followers - {self.artists_followers}"
            self.followers_Label = QLabel(self.follower_output_text, self)
            self.followers_Label.setFont(QFont("Helvetica", 25))
            self.followers_Label.setStyleSheet("background: transparent")
            self.followers_Label.adjustSize()
            self.followers_Label.move(
                (border_padding + followers_padding), (y_starting_point + self.top_artist_Label.height()))

            """ Visualize pictures """
            self.pic_url = self.data['img_url'][index]
            self.picture = QImage()
            self.picture.loadFromData(requests.get(url=self.pic_url).content)
            self.picture_resized = self.picture.scaled(pic_width, pic_height)
            self.image_label = QLabel(self)
            self.image_label.setPixmap(QPixmap(self.picture_resized))
            self.image_label.show()
            self.image_label.adjustSize()
            self.image_label.move(WIN_WIDTH - pic_width -
                                  border_padding, y_starting_point)
            # TODO: cloud make the profile picture Circular (https://www.geeksforgeeks.org/pyqt5-how-to-create-circular-image-from-any-image/)
            # TODO: could make the visualisation alternierend (Picture, text)

            y_starting_point += (one_data_height + padding_between_songs)


class TopSongsTab(QWidget):
    """
        This class handels all the Widgets, Data and Information regarding the all Time
        Songs of the User
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.top_songs_tab = QWidget()
        self.data = get_all_top_tracks(sp=sp)
        self.show_data()

    def show_data(self):
        one_data_height = 175  # px
        pic_width, pic_height = 150, 150  # px
        padding_between_songs = 20  # px
        border_padding = 100  # px
        y_starting_point = 25  # px
        # px   [or insert \t\t in self.artist_output_text]
        artist_indention = 100  # px

        for index in range(0, 10, 1):  # top 10
            """ Visualize top Tracks """
            self.track = str(self.data['songs'][index])
            self.track_output_text = f"{index+1}. {self.track}"
            self.track_Label = QLabel(self.track_output_text, self)
            self.track_Label.setFont(QFont("Helvetica", 30))
            self.track_Label.setStyleSheet(
                "font-weight: bold; background: transparent")
            self.track_Label.adjustSize()
            self.track_Label.move(border_padding, y_starting_point)

            """ Visualize top Tracks artists """
            self.artist = str(self.data['artists'][index])
            self.artist_output_text = f"{self.artist}"
            self.artist_Label = QLabel(self.artist_output_text, self)
            self.artist_Label.setFont(QFont("Helvetica", 20))
            self.artist_Label.setStyleSheet("background: transparent")
            self.artist_Label.adjustSize()
            self.artist_Label.move(
                (border_padding + artist_indention), (y_starting_point + self.track_Label.height()))

            """ Visualize pictures """
            self.pic_url = self.data['img_url'][index]
            self.picture = QImage()
            self.picture.loadFromData(requests.get(url=self.pic_url).content)
            self.picture_resized = self.picture.scaled(pic_width, pic_height)
            self.image_label = QLabel(self)
            self.image_label.setPixmap(QPixmap(self.picture_resized))
            self.image_label.adjustSize()
            self.image_label.show()
            self.image_label.move(WIN_WIDTH - pic_width -
                                  border_padding, y_starting_point)
            # TODO: cloud make the profile picture Circular (https://www.geeksforgeeks.org/pyqt5-how-to-create-circular-image-from-any-image/)
            # TODO: could make the visualisation alternierend (Picture, text)

            y_starting_point += (one_data_height + padding_between_songs)


class InfoTab(QWidget):
    """
        This class handels all the Widgets, Data and Information for the general Information Tab
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.info_tab = QWidget()
        self.data = get_current_user(sp=sp)
        self.user = self.data["name"]  # getting the currrent user name

        self.show_welcome_text()
        self.show_info()
        self.adjustSize()

    def show_welcome_text(self):
        """
            This function handels the Welchome Text
        """

        # creating a label widget
        self.welcome_text = QLabel(
            f"Hello {self.user}, nice to see you!", self)
        # setting font and size
        self.welcome_text.setFont(QFont("Helvetica", 31))
        self.welcome_text.setStyleSheet(
            "font-weight: bold; background: transparent")

        self.welcome_text.adjustSize()  # adjusting the size of label

        # moving the label to the center
        self.width_center = int(WIN_WIDTH/2 - self.welcome_text.width()/2)
        self.welcome_text.move(self.width_center, 0)

    def show_info(self):
        """
            This function handels the Info text
        """
        self.info_text = f"Hello {self.user},\nI'm Glad, that you're interested in this Spotify Analyzer.\nThis Application will show you:\n\t- Your all time favorite Tracks\n\t- Your all time favorite Artists\n\t- Your all recently played Songs\n\t- The possibility, to add Songs to the queue\n\nHave fun and enjoy\n\t~Piology"

        self.info_Label = QLabel(self.info_text, self)
        self.info_Label.setFixedWidth(WIN_WIDTH)
        self.info_Label.setFont(QFont("Arial", 25))
        self.info_Label.setStyleSheet("background: transparent")
        self.info_Label.adjustSize()
        self.info_Label.move(0, 200)

        # downloading the profile pic
        self.profile_url = self.data['profile_img']
        self.picture = QImage()
        self.picture.loadFromData(requests.get(url=self.profile_url).content)
        self.picture_resized = self.picture.scaled(600, 600)
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap(self.picture_resized))
        self.image_label.show()
        self.image_label.adjustSize()
        self.image_label.move(WIN_WIDTH-700, 70)
        # TODO: cloud make the profile picture Circular (https://www.geeksforgeeks.org/pyqt5-how-to-create-circular-image-from-any-image/)


class TabControl(QWidget):
    """
        This class handels all the different Tabs
    """

    def __init__(self, parent: QWidget = None):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        """ Initialize tab screen and tab Bar """
        self.all_tabs = QTabWidget()
        # TODO: Do I need a QTabWidget() and a QTabBar()?
        # self.tab_bar = QTabBar()
        self.tab_bar = self.all_tabs.tabBar()
        # self.tab_bar = self.all_tabs.tabBar() # is this eequal to self.tab_bar = QTabBar()?

        self.set_position()  # North, West, East, South
        self.set_Tab_shape()  # Triangular or Rounded
        self.add_all_tabs()

        """ Making the Tabs moveable """
        self.all_tabs.setMovable(True)

        # makes the current Tab green
        self.tab_bar.setStyleSheet(
            f"background: {SPOTIFY_GREEN}; color: white; border: 5px")

        """ resizing the Tab Bar """
        # TODO: making the Tabs in the Tab Bar bigger and other color
        # self.tab_bar.resize(WIN_HEIGHT, 20)
        # self.tab_bar.setFixedSize(WIN_HEIGHT, 20)
        # print(self.tab_bar.size())
        # print(self.all_tabs.size())
        # self.all_tabs.setBaseSize(WIN_WIDTH, WIN_HEIGHT)
        # self.all_tabs.resize(WIN_WIDTH, 20)
        # QTabBar.setFixedWidth(self, int(WIN_WIDTH/3)) == self.all_tabs.setFixedWidth(int(WIN_WIDTH/3))

        self.set_image_as_background()

        ''' closing the current Tab '''
        self.all_tabs.setTabsClosable(True)
        self.all_tabs.tabCloseRequested.connect(self.close_Tab)

        """ Makeing the Tabs scrollable, if to many """
        self.all_tabs.setUsesScrollButtons(True)

        self.layout.addWidget(self.all_tabs)
        self.setLayout(self.layout)

    def set_position(self):
        """
            whether the Tabs are on the North, South, West or East
            default: QTabWidget.North
        """
        self.all_tabs.setTabPosition(QTabWidget.North)

    def set_Tab_shape(self):
        """
            setting the Shape of the Tabs to Rounded or Triangular
            default: QTabWidget.Rounded
        """
        self.tab_shape = QtWidgets.QTabWidget.Triangular
        self.all_tabs.setTabShape(self.tab_shape)

    def add_all_tabs(self):
        """
            Adding all Tabs to the QTabWidget()
        """
        self.all_tabs.addTab(InfoTab(self), QIcon(
            "imgs/info_icon.png"), "General Infos")
        self.all_tabs.addTab(TopSongsTab(self), "Your all Time Fav's")
        self.all_tabs.addTab(TopArtistsTab(self), "Your favorite Artists")

    def set_image_as_background(self):
        """
            setting the background of the Tabs to a color-gradient in the colors of Spotify
            TODO: making the Size for every resolution equal
        """
        # self.spotify_background = QtGui.QIcon(
        #     "imgs/Spotify_color_gradient.png")
        # self.spotify_background.availableSizes()
        self.all_tabs.setStyleSheet(
            "background-image: url(imgs/Spotify_color_gradient.png)")

    def close_Tab(self, currentIndex):
        """
            callback Function, when the Tabs getting closed
            TODO: adding functionality, to add the tabs again (maybe from the Info Tab?)
            TODO: Making the Info Tab uncloseable

        """
        self.all_tabs.removeTab(currentIndex)  # removes the current Tab


class MainWindow(QMainWindow):   # App class inherits from the tk.Tk
    """
        This class handels all the Widgets, Tabs etc.
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        self.init_geometry()
        self.init_Tabs()
        self.show()  # to show the Window on the screen

    def init_geometry(self):
        """ configure the main window """
        self.setWindowTitle("Spotify Analyzer")

        """ center the Window to the screen """
        self.screen_size = QtWidgets.QDesktopWidget().screenGeometry(-1)
        x = (self.screen_size.width()/2) - (WIN_WIDTH/2)
        y = (self.screen_size.height()/2) - (WIN_HEIGHT/2) - TASKBAR_HEIGHT
        self.setGeometry(0, 0, self.screen_size.width(),
                         self.screen_size.height())

        """ changing the icon from the window """
        self.spotify_logo = QtGui.QIcon("imgs/Spotify_logo.png")
        self.setWindowIcon(self.spotify_logo)

        """ changing the background color of the Window """
        self.setStyleSheet(f"background: {BLACK}")

    def init_Tabs(self):
        self.table_widget = TabControl(self)
        self.setCentralWidget(self.table_widget)


app = QApplication(sys.argv)
SCREEN_SIZE = QtWidgets.QDesktopWidget().screenGeometry(-1)
WIN_WIDTH, WIN_HEIGHT = SCREEN_SIZE.width(), SCREEN_SIZE.height()
window = MainWindow()
sys.exit(app.exec_())
