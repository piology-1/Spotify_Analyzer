from gzip import READ
from turtle import title
from xml.etree.ElementTree import PI
from utils import *
from authentication import authenticate
import requests
from io import BytesIO
import os
from prettyprinter import pprint

''' --- GUI Imports --- '''
import sys
from PIL import Image, ImageTk
# from PySide6 import *
# from PySide6.QtWidgets import *  # z.B. PySide6.QtWidgets.QVBoxLayout
# from PySide6.QtGui import *  # QFont
# from PySide6.QtCore import *

from PyQt5 import *
from PyQt5.QtWidgets import *  # z.B. PyQt5.QtWidgets.QVBoxLayout
from PyQt5.QtGui import *  # QFont
from PyQt5.QtCore import *

''' --- constants --- '''
WIN_WIDTH, WIN_HEIGHT = 1900, 1000  # default window geometry
TASKBAR_HEIGHT = 40
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_BLUE = "#10267D"
LIGHT_BLUE = "#486682"
LIGHT_RED = "#BA303A"
LIGHT_GREY = "#7F8285"
WHITE = "#FFFFFF"
BLACK = "#000000"
GREY = "#6B6A69"
PINK = "#611038"


sp = authenticate()


class SavedFavSongs(QWidget):
    """
        This class handels all the Widgets, Data and Information regarding the favorite
        Artists of the User
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        data = get_tracks_from_favoritesongs(sp=sp)
        rows = len(data['songs'])*2  # songname AND Artist name per track
        pic_width, pic_height = 150, 150  # px

        song_layout = QGridLayout(self)

        title = QLabel("Your saved favorite songs\n", self)
        title.setFont(QFont("Helvetica", 35))
        title.setStyleSheet(
            "font-weight: bold; background: transparent")
        song_layout.addWidget(title, 0, 0, 1, 2, Qt.AlignCenter)

        song_index = 0
        artist_index = 0
        for index in range(2, rows+2, 1):
            if index % 2 == 0:  # even rows

                """ Visualize top Tracks """
                curr_track = str(data['songs'][song_index])
                track_Label = QLabel(f"{song_index + 1}. {curr_track}", self)
                # track_Label.setMaximumSize()
                track_Label.setWordWrap(True)
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

                artist_Label = QLabel(f"\t{artist}", self)
                artist_Label.setFont(QFont("Helvetica", 15))
                artist_Label.setStyleSheet("background: transparent")

                # ARTIST LEFT, PICTURE RIGHT
                song_layout.addWidget(artist_Label, index, 0, Qt.AlignLeft)

                artist_index += 1

        self.setLayout(song_layout)


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
        title = QLabel("Your top artists of all time\n", self)
        title.setFont(QFont("Helvetica", 35))
        title.setStyleSheet(
            "font-weight: bold; background: transparent")
        artist_layout.addWidget(title, 0, 0, 1, 2, Qt.AlignCenter)

        # artist_layout.addWidget(QLine(), 1, 0, 1, 2, Qt.AlignCenter)

        artist_index = 0
        follower_index = 0
        # index = 1
        for index in range(2, rows+2, 1):
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
                # it comes with the size of (640, 640)
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
        rows = len(data['songs'])*2  # songname AND Artist name per track
        pic_width, pic_height = 150, 150  # px

        song_layout = QGridLayout(self)

        title = QLabel("Your top tracks of all time\n", self)
        title.setFont(QFont("Helvetica", 35))
        title.setStyleSheet(
            "font-weight: bold; background: transparent")
        song_layout.addWidget(title, 0, 0, 1, 2, Qt.AlignCenter)

        song_index = 0
        artist_index = 0
        for index in range(2, rows+2, 1):
            if index % 2 == 0:  # even rows

                """ Visualize top Tracks """
                curr_track = str(data['songs'][song_index])
                track_Label = QLabel(f"{song_index + 1}. {curr_track}", self)
                track_Label.setWordWrap(True)
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

        ''' MAIN INFO Layoout Manager '''
        main_info_layout = QGridLayout(self)

        data = get_current_user(sp=sp)

        user = data["name"]
        welcome_text_Label = QLabel(f"Hello {user}!", self)
        welcome_text_Label.setFont(QFont("Helvetica", 40))
        welcome_text_Label.setStyleSheet(
            "font-weight: bold; background: transparent")
        # main_layout.addWidget(QWidget, row, column, rowSpan, columnSpan, alignment)
        main_info_layout.addWidget(
            welcome_text_Label, 0, 0, Qt.AlignCenter)
        # TODO: https://doc.qt.io/qtforpython/overviews/richtext-layouts.html

        """ Info Text Manager """
        info_text_layout = QHBoxLayout()  # not self as an argument

        # downloading the profile pic
        user_picture_url = data['profile_img']
        user_picture = QImage()
        user_picture.loadFromData(requests.get(url=user_picture_url).content)
        picture_resized = user_picture.scaled(600, 600)
        image_label = QLabel(self)
        image_label.setPixmap(QPixmap(user_picture))
        # image_label.show() # I don't need this, I guess ?! the Layout Manager takes care of this?!
        image_label.setStyleSheet("background: transparent")
        info_text_layout.addWidget(image_label)
        # TODO: cloud make the profile picture Circular (https://www.geeksforgeeks.org/pyqt5-how-to-create-circular-image-from-any-image/)

        info_Label = QLabel(
            f"I'm glad, that you're interested in this Spotify Analyzer. I need to stretch the Information text, so I will just write a litte bit more, if thats okay for you. Hope so. See ya. Push yoursef\nBest, Piology", self)
        info_Label.setFont(QFont("Helvetica", 20))
        # making label multi line (don't need manual edited \n anymore, except I want a next Line)
        info_Label.setWordWrap(True)
        info_Label.setStyleSheet("background: transparent")
        info_text_layout.addWidget(info_Label)

        main_info_layout.addLayout(info_text_layout, 1, 0, Qt.AlignLeft)

        ''' currently playing '''
        currently_playing_layout = QHBoxLayout()

        current_track_data = get_currently_playing_song(sp=sp)
        if (not current_track_data) or (not current_track_data['is_playing']):
            no_song_playing_label = QLabel("No Song playing right now", self)
            no_song_playing_label.setFont(QFont("Helvetica", 30))
            no_song_playing_label.setStyleSheet("background: transparent")
            currently_playing_layout.addWidget(no_song_playing_label)

        else:
            current_song = current_track_data['song']
            current_song_artist = current_track_data['artist']
            current_song_image = QImage()
            current_song_image.loadFromData(
                requests.get(url=current_track_data['img_url']).content)
            current_song_image_resized = current_song_image.scaled(250, 250)

            song_artist_label = QLabel(
                f"Current Song:\n{current_song} - {current_song_artist}", self)
            song_artist_label.setWordWrap(True)
            song_artist_label.setFont(QFont("Helvetica", 20))
            song_artist_label.setStyleSheet(
                "font-weight: bold; background: transparent")
            currently_playing_layout.addWidget(song_artist_label)

            img_label = QLabel(self)
            img_label.setPixmap(QPixmap(current_song_image_resized))
            img_label.setStyleSheet("background: transparent")
            currently_playing_layout.addWidget(img_label)
        # TODO: How can I update this, when the Application is already open and the user starts listen to a song?

        main_info_layout.addLayout(
            currently_playing_layout, 2, 0, Qt.AlignLeft)
        ''' Controll over songs area '''
        music_layout = QHBoxLayout()

        self.suffle_status = False  # True: on, False: off
        self.repeat_status = False  # True: on, False: off

        shuffle = QPushButton(QIcon("icons/shuffle.svg"), "", self)
        shuffle.setMinimumSize(75, 75)
        shuffle.setToolTip("Shuffle Mode")
        if not self.suffle_status:
            shuffle.setStyleSheet(f"""QPushButton{{
                                  background: transparent; border-style: outset;
                                  border-radius: 37; border: 2px solid white;
                                  }}
                                  QPushButton::hover{{
                                  background-color: {LIGHT_BLUE};
                                  }}
                                  QToolTip{{
                                  border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                                  border-radius: 5px; opacity: 200; color: {WHITE}
                                  }}""")
        else:
            shuffle.setStyleSheet(f"""QPushButton{{
                                  background-color: #041a10; border-style: outset;
                                  border-radius: 37; border: 2px solid white;
                                  }}
                                  QPushButton::hover{{
                                  background-color: #041a10;
                                  }}
                                  QToolTip{{
                                  border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                                  border-radius: 5px; opacity: 200; color: {WHITE};
                                  }}""")
        shuffle.clicked.connect(self.toggle_shuffle_status)
        music_layout.addWidget(shuffle)

        repeat = QPushButton(QIcon("icons/repeat.svg"), "", self)
        repeat.setMinimumSize(75, 75)
        repeat.setToolTip("Repeat Mode")
        # TODO: if repeat on, then ... and so on
        repeat.setStyleSheet(f"""QPushButton{{
                             background: transparent; border-style: outset;
                             border-radius: 37; border: 2px solid white;
                             }}
                             QPushButton::hover{{
                             background-color: {LIGHT_BLUE};
                             }}
                             QToolTip{{
                             border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                             border-radius: 5px; opacity: 200; color: {WHITE};
                             }}""")
        # repeat.clicked.connect(self.toggle_repeat_status)
        music_layout.addWidget(repeat)

        previous_track = QPushButton(
            QIcon("icons/skip-back.svg"), "", self)
        previous_track.setMinimumSize(100, 100)
        previous_track.setToolTip("Skip Back")
        # setting radius and border
        previous_track.setStyleSheet(f"""QPushButton{{
                                     background: transparent; border-style: outset;
                                     border-radius: 50; border : 4px solid white;
                                     }}
                                     QPushButton::hover{{
                                     background-color: {LIGHT_BLUE};
                                     }}
                                     QToolTip{{
                                     border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                                     border-radius: 5px; opacity: 200; color: {WHITE}
                                     }}""")
        previous_track.clicked.connect(self.skip_back)
        music_layout.addWidget(previous_track)

        pause = QPushButton(QIcon("icons/pause.svg"), "", self)
        pause.setMinimumSize(100, 100)
        pause.setToolTip("Pause Track")
        pause.setStyleSheet(f"""QPushButton{{
                            background: transparent; border-style: outset;
                            border-radius: 50; border : 4px solid white;
                            }}
                            QPushButton::hover{{
                            background-color: {LIGHT_BLUE};
                            }}
                            QToolTip{{
                            border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                            border-radius: 5px; opacity: 200; color: {WHITE};
                            }}""")
        pause.clicked.connect(self.pause_track)
        music_layout.addWidget(pause)

        play = QPushButton(QIcon("icons/play.svg"), "", self)
        play.setMinimumSize(100, 100)
        play.setToolTip("Play Track")
        play.setStyleSheet(f"""QPushButton{{
                           background: transparent; border-style: outset;
                           border-radius: 50; border : 4px solid white;
                           }}
                           QPushButton::hover{{
                           background-color: {LIGHT_BLUE};
                           }}
                           QToolTip{{
                           border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                           border-radius: 5px; opacity: 200; color: {WHITE};
                           }}""")
        play.clicked.connect(self.play_track)
        music_layout.addWidget(play)

        next_track = QPushButton(
            QIcon("icons/skip-forward.svg"), "", self)
        next_track.setMinimumSize(100, 100)
        next_track.setToolTip("Skip Forward")
        next_track.setStyleSheet(f"""QPushButton{{
                                 background: transparent; border-style: outset;
                                 border-radius: 50; border : 4px solid white;
                                 }}
                                 QPushButton::hover{{
                                 background-color: {LIGHT_BLUE};
                                 }}
                                 QToolTip{{
                                 border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                                 border-radius: 5px; opacity: 200; color: {WHITE};
                                 }}""")
        next_track.clicked.connect(self.skip_track)
        music_layout.addWidget(next_track)

        add_track_to_favs = QPushButton(QIcon("icons/heart.svg"), "", self)
        add_track_to_favs.setMinimumSize(75, 75)
        fav_songs_data = get_tracks_from_favoritesongs(sp=sp)
        fav_songs_uris = fav_songs_data['uri']  # list
        curr_song_uri = self.get_curr_song_uri()
        if curr_song_uri not in fav_songs_uris:
            add_track_to_favs.setToolTip("Add current song to Fav's")
            add_track_to_favs.setStyleSheet(f"""QPushButton{{
                                            background: transparent; border-style: outset;
                                            border-radius: 37; border: 2px solid white;
                                            }}
                                            QPushButton::hover{{
                                            background-color: {LIGHT_BLUE};
                                            }}
                                            QToolTip{{
                                            border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                                            border-radius: 5px; opacity: 200; color: {WHITE};
                                            }}""")
        else:
            add_track_to_favs.setToolTip("Already in your Fav Library")
            add_track_to_favs.setStyleSheet(  # is allready in favs
                f"""QPushButton{{
                                            background-color: {LIGHT_RED}; border-style: outset;
                                            border-radius: 37; border: 2px solid white;
                                            }}
                                            QPushButton::hover{{
                                            background-color: {LIGHT_RED};
                                            }}
                                            QToolTip{{
                                            border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                                            border-radius: 5px; opacity: 200; color: {WHITE};
                                            }}""")
        # add current song to fav library
        add_track_to_favs.clicked.connect(self.add_curr_track_to_fav_library)
        music_layout.addWidget(add_track_to_favs)

        add_track_to_queue = QPushButton(
            QIcon("icons/add_track_to_queue.svg"), "", self)
        add_track_to_queue.setMinimumSize(75, 75)
        add_track_to_queue.setToolTip("Add current song to queue")
        add_track_to_queue.setStyleSheet(f"""QPushButton{{
                                         background: transparent; border-style: outset;
                                         border-radius: 37; border: 2px solid white;
                                         }}
                                         QPushButton::hover{{
                                         background-color: {LIGHT_BLUE};
                                         }}
                                         QToolTip{{
                                         border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                                         border-radius: 5px; opacity: 200; color: {WHITE};
                                         }}""")
        add_track_to_queue.clicked.connect(
            self.add_curr_track_to_queue)  # add current song to queue
        music_layout.addWidget(add_track_to_queue)
        main_info_layout.addLayout(music_layout, 3, 0, Qt.AlignLeft)

        volume_control_layout = QHBoxLayout()
        volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        volume_slider.setMaximumSize(400, 20)
        height = 4
        volume_slider.setStyleSheet(f'''
        QSlider {{
            margin-top: {height+1}px;
            margin-bottom: {height+1}px;
            background: transparent;
        }}
        QSlider::groove:horizontal {{
            height: {height}px;
            background: {SPOTIFY_GREEN};
            margin: {height // 4}px 0;
        }}
        QSlider::handle:horizontal {{
            background: {WHITE};
            border: {height} solid {WHITE};
            width: {height * 3};
            margin: {height * 2 * -1} 0;
            border-radius: {height * 2 + height // 2}px;
        }}
        QSlider::add-page:horizontal {{
            background: {GREY};
            height: {height}px;
            margin: {height // 4}px 0;
        }}
        ''')
        # volume_slider.valueChanged.connect(self.change_value)
        volume_control_layout.addWidget(volume_slider)
        main_info_layout.addLayout(volume_control_layout, 4, 0, Qt.AlignLeft)

        # creating Button to link to the Tabs
        # top_songs_button = QPushButton("Yout top Songs of all time", self)
        # top_artists_button = QPushButton("Yout top Artists of all time", self)

        # main_layout.addWidget(buttons_for_tabs, 2, 0, Qt.AlignTop) # can't add Buttongroup, because it's no Widget
        # info_layout.addWidget(top_songs_button, 2, 0, Qt.AlignTop)
        # info_layout.addWidget(top_artists_button, 3, 0, Qt.AlignTop)

        ''' Logout Button '''
        logout = QPushButton(QIcon("icons/log-out.svg"), "\tLog out", self)
        logout.setFont(QFont("comicsans", 15))
        logout.setMinimumSize(250, 50)
        logout.setToolTip("Log-out")  # hover_message
        # TODO: change Size
        logout.setStyleSheet(f"""QPushButton{{
                             background: {BLACK}; border-style: outset; border-width: 3px;
                             border-radius: 10px; border-color: white; color: white;
                             padding: 6px;
                             }}
                             QPushButton::hover{{
                             background-color: {SPOTIFY_GREEN};
                             }}
                             QToolTip{{
                             border: 2px solid {WHITE}; padding: 5px; background: {GREY};
                             border-radius: 5px; opacity: 200; color: {WHITE};
                             }}""")
        # TODO: logout.clicked.connect(self.spotify_logout)
        main_info_layout.addWidget(logout, 0, 1, Qt.AlignRight)

        self.setLayout(main_info_layout)

    def toggle_shuffle_status(self):
        # toggle self.suffle_status
        if self.suffle_status:
            self.suffle_status = False
        else:
            self.suffle_status = True

        set_shuffle_mode(sp=sp, status=self.suffle_status)  # default: False

    def toggle_repeat_status(self):
        if self.repeat_status:
            self.repeat_status = False
        else:
            self.repeat_status = True

        # set_repeat_mode(sp=sp, status=self.repeat_status)

    def skip_back(self):  # previous_track
        # response = play_previous_track(sp=sp)  # True, 404, False
        if play_previous_track(sp=sp):
            pass
        else:  # Es ist soo schlecht. GHiewr gehts mit dem Fester nicht ???!?? WTF is goinjkg on???? kskdnaskfn ksldfiuosed hfkljdsfg sfdg fsdg bsd ghosdrhg foisudrhg
            self.call_no_active_device_found_error()

        """if respone:
            # everything is fine: connected to a akip was successfull
            pass
        elif respone == 404:
            self.call_no_active_device_found_error()
        else:
            self.call_unkown_error_found()"""

    def pause_track(self):
        if pause_current_track(sp=sp):
            pass
        elif pause_current_track(sp=sp) == 403:
            # Error 404: A track is already playing
            # go on, nothing should happen
            pass
        elif pause_current_track(sp=sp) == 404:
            self.call_no_active_device_found_error()
        else:
            self.call_unkown_error_found()

    def play_track(self):
        if start_current_track(sp=sp):
            pass
        elif start_current_track(sp=sp) == 403:
            pass
        elif start_current_track(sp=sp) == 404:
            self.call_no_active_device_found_error()
        else:
            self.call_unkown_error_found()

    def skip_track(self):  # next track
        if play_next_track(sp=sp):
            pass
        else:
            self.call_no_active_device_found_error()

    def get_curr_song_uri(self):
        curr_song_data = get_currently_playing_song(sp=sp)
        return curr_song_data['song_uri']

    def add_curr_track_to_queue(self):
        curr_song_uri = self.get_curr_song_uri()
        add_track_to_queue(sp=sp, song_uri=curr_song_uri)
        # TODO: need to handle: curr_song_uri = curr_song_data['song_uri']
        # TypeError: 'bool' object is not subscriptable
        # currently only working, when device is active

    def add_curr_track_to_fav_library(self):  # song_uri=get_curr_song_uri
        curr_song_uri = self.get_curr_song_uri()
        add_track_to_fav_songs(sp=sp, track_uri=[curr_song_uri])

    def change_value(self, value):
        '''
            volume_slider.valueChanged.connect(self.change_value) returns a int between 0 and 99
        '''
        print(value)

    def go_to_tab(self, tab_index):
        pass

    def create_circular_image(self):
        pass

    def spotify_logout(self):
        if os.path.exists(".cache"):
            os.remove(".cache")

    def call_no_active_device_found_error(self):
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setWindowTitle("Conection Error")
        error_msg.setText("No active device found!")
        error_msg.setInformativeText(
            "We couldn not connect to your device, because there is no one active at the moment\nMake sure you have turend a device on!")
        error_msg.exec_()

    def call_unkown_error_found(self):
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setWindowTitle("Unkown Error")
        error_msg.setText("Unkown error accoured")
        error_msg.setInformativeText(
            "An undefined and unkown error accoured.\n Please try later again!")
        error_msg.exec_()


class MainWindow(QMainWindow):
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

        # TODO: Do I need a QTabWidget() AND a QTabBar()?
        # tab_bar = QTabBar()
        # tab_bar = all_tabs.tabBar()
        # tab_bar = all_tabs.tabBar() # is this eequal to tab_bar = QTabBar()?
        tab_bar = self.tab_widget.tabBar()

        # creating an Area, where a Scroll bar is added, when the space isn't enough
        top_songs_scrollbar = QScrollArea()
        top_songs_scrollbar.setWidgetResizable(True)
        top_songs_tab = TopSongsTab(self)  # instance of TopSongsTab
        # setting the scrollbar to the Tab(s)
        top_songs_scrollbar.setWidget(top_songs_tab)

        top_artist_scrollbar = QScrollArea()
        top_artist_scrollbar.setWidgetResizable(True)
        top_artist_scrollbar.setWidget(TopArtistsTab(self))

        fav_songs_scrollbar = QScrollArea()
        fav_songs_scrollbar.setWidgetResizable(True)
        fav_songs_scrollbar.setWidget(SavedFavSongs(self))

        #  adding all Tabs to the TabWidget
        self.tab_widget.addTab(InfoTab(self), QIcon(
            "icons/info.svg"), "General Infos")
        self.tab_widget.addTab(top_songs_scrollbar, QIcon(
            "icons/top_tracks.svg"), "Your all Time Fav's")
        self.tab_widget.addTab(top_artist_scrollbar, QIcon(
            "icons/top_artists.svg"), "Your favorite Artists")
        self.tab_widget.addTab(fav_songs_scrollbar, QIcon(
            "icons/heart.svg"), "Your saved favorite Songs")

        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(True)  # changed Icon below
        # self.tab_widget.tabCloseRequested(self.close_Tab)

        self.tab_widget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setUsesScrollButtons(True)

        # setting the background of the tabbar transparent
        tab_bar.setStyleSheet("background: transparent")
        curr_win_width, curr_win_height = self.width(), self.height()
        # styling the Tabs and the tabpage

        self.tab_widget.setStyleSheet(
            # making the page of the tabs green/black
            # top lef and bottom right
            # factors in % 1==completely width and height and so on
            f"""QWidget {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {SPOTIFY_GREEN}, stop: 1 {BLACK});
                    }}
                QTabWidget::tab-bar {{
                    alignment: center;
                    }}"""
            # The tab widget frame at the top, shifts the tabs in the border
            f"""QTabWidget::pane {{
                    border-top: 5px solid {WHITE};
                    position: absolute; top: -20px;
                    }}"""
            # making the Tabs in the Tab Bar green
            f"""QTabBar::tab {{
                    background:  {SPOTIFY_GREEN};
                    border: 2px solid {WHITE};
                    border-top-left-radius: 10px; border-top-right-radius: 10px;
                    padding: 8px;
                    font: Arial; color: {WHITE};
                    }}
                QTabBar::tab:selected {{
                    background:  {SPOTIFY_BLUE};
                    border-top: 5px solid {WHITE};
                    }}"""
            # QTabBar::tab:selected, # same as the pane
            f"""QTabBar::tab:hover {{
                    border: 5px solid {GREY};
                    }}
                QTabBar::close-button {{
                    image: url(icons/close_x.svg);
                    }}
                QTabBar::close-button:hover {{
                    image: url(icons/close_x_hover.svg);
                    }}"""
        )

        # creating a layout for flexible usage
        # QHBoxLayout(self.tab_widget) was necessary     QHBoxLayout() is not working
        main_layout = QHBoxLayout(self.tab_widget)
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

        self.show()

    def close_Tab(self, current_Index):
        """
            callback Function, when the Tabs getting closed
            TODO: adding functionality, to add the tabs again(maybe from the Info Tab?)
            TODO: Making the Info Tab uncloseable

        """
        self.tab_widget.removeTab(current_Index)  # removes the current Tab


app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())  # exec_ for PyQt5
