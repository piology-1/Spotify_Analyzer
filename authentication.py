""" Websites:
        https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
        https://developer.spotify.com/documentation/general/guides/authorization/app-settings/
        https://developer.spotify.com/dashboard/applications/92cce333b3da417a95d8ca738477b241
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


def authenticate():
    # getting the environment variables
    client_id = os.environ.get('client_id', 'client_id not found')
    client_secret = os.environ.get('client_secret', 'client_secret not found')

    # storing all possible scopes
    scopes = 'ugc-image-upload, user-modify-playback-state, user-follow-modify, user-read-recently-played,user-read-playback-position, playlist-read-collaborative, app-remote-control, user-read-playback-state, user-read-email, streaming user-top-read, playlist-modify-public, user-library-modify, user-follow-read, user-read-currently-playing, user-library-read, playlist-read-private, user-read-private, playlist-modify-private'

    auth_manage = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                               redirect_uri="http://localhost:8888/callback", scope=scopes, open_browser=True)

    return spotipy.Spotify(auth_manager=auth_manage)
