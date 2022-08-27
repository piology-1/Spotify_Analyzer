from cmath import log
from email.utils import parseaddr
from utils import *
from authentication import authenticate
import requests
from io import BytesIO
from prettyprinter import pprint

''' --- GUI Imports --- '''
import sys
from PIL import Image, ImageTk
# from PySide6 import *
# from PySide6.QtWidgets import *  # z.B. PySide6.QtWidgets.QVBoxLayout
# from PySide6.QtGui import *  # QFont
# from PySide6.QtCore import *

from PyQt5 import *
from PyQt5.QtWidgets import *  # z.B. PySide6.QtWidgets.QVBoxLayout
from PyQt5.QtGui import *  # QFont
from PyQt5.QtCore import *

''' --- constants --- '''
WIN_WIDTH, WIN_HEIGHT = 1900, 1000  # default window geometry
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
        data = get_all_top_artists(sp=sp)
        rows = len(data['artists'])*2  # Artist Name AND Followers
        pic_width, pic_height = 150, 150  # px

        artist_layout = QGridLayout(self)
        artist_index = 0
        follower_index = 0
        for index in range(rows):
            if index % 2 == 0:  # even rows
                """ Visualize top Artists """
                curr_artist = str(data['artists'][artist_index])

                artist_Label = QLabel(
                    f"{artist_index + 1}. {curr_artist}", self)
                artist_Label.setFont(QFont("Helvetica", 25))
                artist_Label.setStyleSheet(
                    "font-weight: bold; background: transparent")

                """ Visualize pictures """
                pic_url = data['img_url'][artist_index]
                picture = QImage()
                # it comes with size(640, 640)
                picture.loadFromData(requests.get(url=pic_url).content)
                picture_resized = picture.scaled(pic_width, pic_height)
                image_label = QLabel(self)
                image_label.setPixmap(QPixmap(picture_resized))
                image_label.setStyleSheet("background: transparent")

                # SONG LEFT, PICTURE RIGHT
                artist_layout.addWidget(artist_Label, index, 0, Qt.AlignLeft)
                artist_layout.addWidget(
                    image_label, index, 1, 2, 1, Qt.AlignCenter)

                artist_index += 1
            else:  # uneven rows
                """ Visualize amount of Followers from the top Artists """
                followers = str(data['amount_of_followers'][follower_index])
                # \t for indentation
                follower_Label = QLabel(f"\tFollowers - {followers}", self)
                follower_Label.setFont(QFont("Helvetica", 15))
                follower_Label.setStyleSheet("background: transparent")

                # ARTIST LEFT, PICTURE RIGHT
                artist_layout.addWidget(follower_Label, index, 0, Qt.AlignLeft)

                follower_index += 1

            self.setLayout(artist_layout)


class TopSongsTab(QWidget):
    """
        This class handels all the Widgets, Data and Information regarding the all Time
        Songs of the User
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        data = get_all_top_tracks(sp=sp)
        rows = len(data['songs'])*2  # songname AND Artist Name per track
        pic_width, pic_height = 150, 150  # px

        song_layout = QGridLayout(self)
        song_index = 0
        artist_index = 0
        for index in range(rows):
            if index % 2 == 0:  # even rows

                """ Visualize top Tracks """
                curr_track = str(data['songs'][song_index])
                track_Label = QLabel(f"{song_index + 1}. {curr_track}", self)
                track_Label.setFont(QFont("Helvetica", 25))
                track_Label.setStyleSheet(
                    "font-weight: bold; background: transparent")

                # """ Visualize top Tracks duration"""
                # curr_track_id = str(data['song_id'][song_index])
                # duration = track_played_min(
                #     sp=sp, song_id=curr_track_id)  # [min]
                # track_duration_Label = QLabel(
                #     f"Your listened to this song for {duration} minutes", self)
                # track_duration_Label.setFont(QFont("Helvetica", 20))
                # track_duration_Label.setStyleSheet("background: transparent")
                # song_layout.addWidget(
                #     track_duration_Label, index, 1, Qt.AlignLeft)
                # TODO: Problem is in utils.py track_played_min(sp=sp, song_id=curr_track_id) -> NOT returning in minutes???!!!

                """ Visualize pictures """
                pic_url = data['img_url'][song_index]
                picture = QImage()
                # it comes with size(640, 640)
                picture.loadFromData(requests.get(url=pic_url).content)
                picture_resized = picture.scaled(pic_width, pic_height)
                image_label = QLabel(self)
                image_label.setPixmap(QPixmap(picture_resized))
                image_label.setStyleSheet("background: transparent")

                # SONG LEFT, PICTURE RIGHT
                song_layout.addWidget(track_Label, index, 0, Qt.AlignLeft)
                song_layout.addWidget(image_label, index,
                                      1, 2, 1, Qt.AlignCenter)

                song_index += 1
            else:  # uneven rows
                """ Visualize top Tracks artists """
                artist = str(data['artists'][artist_index])
                # \t for indentation
                artist_Label = QLabel(f"\t{artist}", self)
                artist_Label.setFont(QFont("Helvetica", 15))
                artist_Label.setStyleSheet("background: transparent")

                # ARTIST LEFT, PICTURE RIGHT
                song_layout.addWidget(artist_Label, index, 0, Qt.AlignLeft)

                artist_index += 1

        self.setLayout(song_layout)


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

        # info_text = f"I'm glad, that you're interested in this Spotify Analyzer.\nThis Application will show you:\n\t- Your all time favorite Tracks\n\t- Your all time favorite Artists\n\t- Your all recently played Songs\n\t- The possibility, to add Songs to the queue\n\nHave fun and enjoy\n\t~Piology"
        # info_Label = QLabel(info_text, self)
        # info_Label.setStyleSheet("background: transparent")
        # # TODO: https://doc.qt.io/qtforpython/overviews/richtext-layouts.html

        info_Label = QLabel(
            f"I'm glad, that you're interested in this Spotify Analyzer. This Application will show you:", self)
        info_Label.setFont(QFont("Helvetica", 20))
        info_Label.setStyleSheet("background: transparent")
        # making label multi line (don't need \n anymore, except I want a next Line)
        info_Label.setWordWrap(True)

        # downloading the profile pic
        user_picture_url = data['profile_img']
        user_picture = QImage()
        user_picture.loadFromData(requests.get(url=user_picture_url).content)
        picture_resized = user_picture.scaled(600, 600)
        image_label = QLabel(self)
        image_label.setPixmap(QPixmap(user_picture))
        # image_label.show() # I don't need this, I guess ?! the Layout Manager takes cae of this?!
        image_label.setStyleSheet("background: transparent")
        # TODO: cloud make the profile picture Circular (https://www.geeksforgeeks.org/pyqt5-how-to-create-circular-image-from-any-image/)

        ''' Layoout Manager '''
        info_layout = QGridLayout(self)
        # main_layout.addWidget(QWidget, row, column, rowSpan, columnSpan, alignment)
        info_layout.addWidget(welcome_text_Label, 0, 0, 1, 2, Qt.AlignLeft)
        info_layout.addWidget(info_Label, 1, 0, 1, 2,
                              Qt.AlignLeft)  # is wrapped
        info_layout.addWidget(image_label, 0, 3, 2, 1, Qt.AlignLeft)

        ''' currently playing '''
        current_track_data = get_currently_playing_song(sp=sp)
        # TODO: How can I update this, when the Application is already open and the user starts listen to a song?
        if current_track_data['is_playing']:
            current_song = current_track_data['song']
            current_song_artist = current_track_data['artist']
            current_song_image = QImage()
            current_song_image.loadFromData(
                requests.get(url=current_track_data['img_url']).content)
            current_song_image_resized = current_song_image.scaled(250, 250)

            song_label = QLabel(f"Current Song: {current_song}", self)
            song_label.setWordWrap(True)
            song_label.setFont(QFont("Helvetica", 25))
            song_label.setStyleSheet(
                "font-weight: bold; background: transparent")
            artist_label = QLabel(f"\t{current_song_artist}")
            artist_label.setFont(QFont("Helvetica", 20))
            artist_label.setStyleSheet("background: transparent")
            img_label = QLabel(self)
            img_label.setPixmap(QPixmap(current_song_image_resized))
            img_label.setStyleSheet("background: transparent")

            info_layout.addWidget(song_label, 2, 1, Qt.AlignLeft)
            info_layout.addWidget(artist_label, 3, 1, Qt.AlignLeft)
            info_layout.addWidget(img_label, 2, 0, 2, 1, Qt.AlignRight)
        else:
            no_song_playing_label = QLabel("No Song playing right now", self)
            no_song_playing_label.setFont(QFont("Helvetica", 30))
            no_song_playing_label.setStyleSheet("background: transparent")
            info_layout.addWidget(no_song_playing_label,
                                  2, 0, 2, 2, Qt.AlignCenter)

        ''' Logout Button '''
        logout = QPushButton(QIcon("imgs/Spotify_logo.png"), "Log out", self)
        logout.setFont(QFont("comicsans", 15))
        # TODO: change Size
        logout.setStyleSheet("QPushButton{"
                             f"background: {BLACK}; border-style: outset; border-width: 3px;"
                             "border-radius: 10px; border-color: white; color: white; "
                             "min-width: 50px; padding: 6px;"
                             "}"
                             "QPushButton::hover{"
                             f"background-color: {SPOTIFY_GREEN};"
                             "}")
        # TODO: logout.connect(self.spotify_logout)

        info_layout.addWidget(logout, 0, 4, Qt.AlignTop)

        # creating Button to link to the Tabs
        # top_songs_button = QPushButton("Yout top Songs of all time", self)
        # top_artists_button = QPushButton("Yout top Artists of all time", self)

        # main_layout.addWidget(buttons_for_tabs, 2, 0, Qt.AlignTop) # can't add Buttongroup, because it's no Widget
        # info_layout.addWidget(top_songs_button, 2, 0, Qt.AlignTop)
        # info_layout.addWidget(top_artists_button, 3, 0, Qt.AlignTop)

        self.setLayout(info_layout)

    def go_to_tab(self, tab_index):
        pass

    def create_circular_image(self):
        pass

    def spotify_logout(self):
        pass


class MainWindow(QMainWindow):   # It dosn't really work with QMainWindow
    """
        This class handels all the Widgets, Tabs etc.
    """

    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)

        ''' init geoemetry '''
        self.setWindowTitle("Spotify Analyzer")
        self.setGeometry(50, 50, WIN_WIDTH, WIN_HEIGHT)
        spotify_logo = QIcon("imgs/Spotify_logo.png")
        self.setWindowIcon(spotify_logo)
        self.setStyleSheet(f"background: {BLACK}")

        ''' ------------------------------------------------------------------ '''
        self.tab_widget = QTabWidget()  # creating a Tabwidget
        # setting the tabWidget as the main window’s central widget
        self.setCentralWidget(self.tab_widget)

        # TODO: Do I need a QTabWidget() and a QTabBar()?
        # tab_bar = QTabBar()
        # tab_bar = all_tabs.tabBar()
        # tab_bar = all_tabs.tabBar() # is this eequal to tab_bar = QTabBar()?
        tab_bar = self.tab_widget.tabBar()

        # creating a Area, where a Scroll bar is added, when the space isn't enough
        songs_scrollbar = QScrollArea()
        songs_scrollbar.setWidgetResizable(True)
        top_songs_tab = TopSongsTab(self)  # instance of TopSongsTab
        # setting the scrollbar to the Tab(s)
        songs_scrollbar.setWidget(top_songs_tab)

        artist_scrollbar = QScrollArea()
        artist_scrollbar.setWidgetResizable(True)
        top_artists_tab = TopArtistsTab(self)
        artist_scrollbar.setWidget(top_artists_tab)

        #  adding all Tabs to the TabWidget
        self.tab_widget.addTab(InfoTab(self), QIcon(
            "imgs/info_icon.png"), "General Infos")
        self.tab_widget.addTab(songs_scrollbar, "Your all Time Fav's")
        self.tab_widget.addTab(artist_scrollbar, "Your favorite Artists")

        self.tab_widget.setMovable(True)

        self.tab_widget.setTabsClosable(True)

        # self.tab_widget.tabCloseRequested(self.close_Tab)

        self.tab_widget.setTabShape(QTabWidget.TabShape.Triangular)
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setUsesScrollButtons(True)

        tab_bar.setStyleSheet(
            f"background: {SPOTIFY_GREEN}; color: white; border: 5px")  # making the Tab Bar green
        self.tab_widget.setStyleSheet(
            "background-image: url(imgs/Spotify_color_gradient.png)")  # making the page of the tabs green/black

        # creating a layout for flexible usage
        # QHBoxLayout(self.tab_widget) was necessary     QHBoxLayout() is not working
        main_layout = QHBoxLayout(self.tab_widget)
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
sys.exit(app.exec_())  # exec_ for PyQt5
