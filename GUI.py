import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import ttk
from tkinter import *
from utils import *
from authentication import authenticate
from prettyprinter import pprint
from PIL import Image, ImageTk
import requests
from io import BytesIO

# constants
WIN_WIDTH, WIN_HEIGHT = 1100, 600
TASKBAR_HEIGHT = 40
SPOTIFY_GREEN = "#1DB954"
BLACK = "#000000"
sp = authenticate()


class InfoTab(ttk.Frame):
    def __init__(self, container):
        super().__init__()

        self.info_tab = ttk.Frame(self, border=True, borderwidth=15)
        #print(self.info_tab.winfo_width(), self.info_tab.winfo_height())

    def show_info_to_screen(self):
        self.data = get_current_user(sp=sp)

        self.user = self.data["name"]  # getting the currrent user name

        self.info_Text = ttk.Label(
            self,  # we are adding this to our Frame, which is the Info Tab
            text=f"Hello {self.user}, nice to see you!",
            font=("Helvetica", 32, "bold"),
            anchor="center",
            background=SPOTIFY_GREEN,
            foreground=BLACK,
            padding=0,
            width=WIN_WIDTH,
            borderwidth=20

        ).pack(fill="both", expand=True)
        # .place(relx=0, rely=0, width=WIN_WIDTH)
        # .grid(column=0, row=0, rowspan=2, sticky=tk.N)
        # .pack(fill="both", expand=True)

        self.info = f"Hello {self.user},\nI'm Glad, that you're interested in this Spotify Analyzer.\nThis Application will show you:\n\t- Your all time favorite Tracks\n\t- Your all time favorite Artists\n\t- Your all recently played Songs\n\t- The possibility, to add Songs to the queue\n\nHave fun and enjoy\n\t~Piology"

        # downloading the profile pic
        self.profile_url = self.data['profile_img']
        self.response = requests.get(url=self.profile_url)
        self.picture = Image.open(fp=BytesIO(self.response.content), mode="r")
        self.img_resized = self.picture.resize((300, 300), Image.ANTIALIAS)

        self.profile_img = ImageTk.PhotoImage(self.img_resized)

        self.info_Label = ttk.Label(self,
                                    text=self.info,
                                    font=("Times New Roman", 25, "bold"),
                                    anchor=NW,
                                    background=SPOTIFY_GREEN,
                                    foreground=BLACK,
                                    padding=5,
                                    width=WIN_WIDTH,
                                    image=self.profile_img,
                                    compound=RIGHT).pack()

        # self.profile_pic = ttk.Label(
        #     self,
        #     image=self.profile_img,  # adding the profile pic to the Label
        #     anchor=NE  # Northeast
        # ).pack(fill="both", expand=True)
        # .place(relx=800, rely=500)
        # .grid(column=1, row=50, rowspan=1, sticky=tk.N)
        # .pack(fill="both", expand=True)


class TopSongsTab(ttk.Frame):
    def __init__(self, container):
        super().__init__()

        self.top_tracks = ttk.Frame(self)

        """
        # configure columns
        # self.columnconfigure(index=0, weight=1)
        # self.columnconfigure(index=1, weight=1)

        # # configure columns
        # self.rowconfigure(index=0, weight=4)
        # self.rowconfigure(index=1, weight=4)
        # self.rowconfigure(index=2, weight=4)
        # self.rowconfigure(index=3, weight=4)
        # self.rowconfigure(index=4, weight=4)
        # self.rowconfigure(index=5, weight=4)
        # self.rowconfigure(index=6, weight=4)
        # self.rowconfigure(index=7, weight=4)
        # self.rowconfigure(index=8, weight=4)
        # self.rowconfigure(index=9, weight=4)
        # self.rowconfigure(index=10, weight=4)
        # self.rowconfigure(index=11, weight=4)
        # self.rowconfigure(index=12, weight=4)
        # self.rowconfigure(index=13, weight=4)
        # self.rowconfigure(index=14, weight=4)
        # self.rowconfigure(index=15, weight=4)
        # self.rowconfigure(index=16, weight=4)
        # self.rowconfigure(index=17, weight=4)
        # self.rowconfigure(index=18, weight=4)
        # self.rowconfigure(index=19, weight=4)
        """

    def show_data(self):
        data = get_all_top_tracks(sp=sp)

        self.song_index = 0
        for track_row_ctn in range(0, 20, 2):
            self.track = str(data['songs'][self.song_index])
            self.track_output_text = f"{self.song_index+1}. {self.track}"
            self.track_output = ttk.Label(self,
                                          text=self.track_output_text,
                                          font=(("Arial Black", 20, "bold")),
                                          background=SPOTIFY_GREEN,
                                          foreground=BLACK,
                                          anchor=W
                                          ).grid(row=track_row_ctn, column=0)

            self.song_index += 1

        self.artist_index = 0
        for artist_row_ctn in range(1, 21, 2):
            self.artist = str(data['artists'][self.artist_index])
            self.artist_output_text = f"\t\t{self.artist}"

            self.artist_output = ttk.Label(self,
                                           text=self.artist_output_text,
                                           font=(("Arial Black", 15, "bold")),
                                           background=SPOTIFY_GREEN,
                                           foreground=BLACK,
                                           anchor=W
                                           ).grid(row=artist_row_ctn, column=0)

            self.artist_index += 1

        self.img_index = 0
        for img_row_ctn in range(0, 20, 2):
            # downloading the pic's from the albums
            self.pic_url = data['img_url'][self.img_index]
            self.pic_response = requests.get(url=self.pic_url)
            # original size is (640, 640)
            self.picture = Image.open(fp=BytesIO(
                self.pic_response.content), mode="r")
            self.pic_resized = self.picture.resize((100, 100), Image.ANTIALIAS)
            self.album_cover = ImageTk.PhotoImage(self.pic_resized)

            self.album_output = ttk.Label(self,
                                          image=self.album_cover,
                                          anchor=E,

                                          ).grid(row=img_row_ctn, column=1, rowspan=2)

            self.img_index += 1


class TopArtistsTab(ttk.Frame):
    def __init__(self, container):
        super().__init__()

        self.top_artists = ttk.Frame(self)

    def show_data(self):
        pass


class MainApplication(tk.Tk):   # App class inherits from the tk.Tk

    def __init__(self):
        super().__init__()

        # configure the main window
        self.title("Spotify Analyzer")

        # changing the icon from the window
        spotify_logo = tk.PhotoImage(file="imgs/Spotify_logo.png")
        self.wm_iconphoto(False, spotify_logo)

        # center the Window to the screen
        x = (self.winfo_screenwidth()/2) - (WIN_WIDTH/2)
        y = (self.winfo_screenheight()/2) - \
            (WIN_HEIGHT/2) - TASKBAR_HEIGHT

        # x,y coordinates of the top left of the Window#
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{int(x)}+{int(y)}")

        # creating multiple Tabs

        # the Notebook holds the tabs
        self.tab_control = ttk.Notebook(
            self, height=TASKBAR_HEIGHT, width=WIN_WIDTH)

        self.info_tab = InfoTab(container=self.tab_control)
        self.tab_control.add(self.info_tab, text="General Info")

        self.top_tracks = TopSongsTab(container=self.tab_control)
        self.tab_control.add(self.top_tracks, text="Your all Time Fav's")

        self.top_artists = TopArtistsTab(container=self.tab_control)
        self.tab_control.add(self.top_artists, text="The Top Artists")

        self.tab_control.pack(fill=tk.BOTH, expand=True)

        self.info_tab.show_info_to_screen()
        self.top_tracks.show_data()


# app = MainApplication()
# app.mainloop()

# bsp_test_song_uri = get_all_top_tracks(sp)['uri'][4]
# add_track_to_queue(bsp_test_song_uri)
