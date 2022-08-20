from authentication import authenticate
from utils import *   # get everything
from prettyprinter import pprint
from GUI import MainApplication


def main():

    app = MainApplication()
    app.mainloop()

    # bsp_test_song_uri = get_all_top_tracks(sp)['uri'][4]
    # add_track_to_queue(bsp_test_song_uri)


if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()
