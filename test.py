import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from prettyprinter import pprint
import requests

client_id = "92cce333b3da417a95d8ca738477b241"
client_Secret = "7bbf053307e54547be82030359eb072c"

scopes = 'ugc-image-upload, user-modify-playback-state, user-follow-modify, user-read-recently-played,user-read-playback-position, playlist-read-collaborative, app-remote-control, user-read-playback-state, user-read-email, streaming user-top-read, playlist-modify-public, user-library-modify, user-follow-read, user-read-currently-playing, user-library-read, playlist-read-private, user-read-private, playlist-modify-private'

auth_manage = SpotifyOAuth(client_id=client_id, client_secret=client_Secret,
                           redirect_uri="http://localhost:8888/callback", scope=scopes, open_browser=True)

#token = util.prompt_for_user_token(scope=scopes, client_id=client_id, client_secret=client_Secret,  redirect_uri="http://localhost:8888/callback", show_dialog=True)
# , oauth_manager=auth_manage,

token = auth_manage.get_access_token(code='code')
# pprint(token)
sp = spotipy.Spotify(auth=token['access_token'])
# auth_manager=auth_manage,

# https://accounts.spotify.com/authorize

favorite_songs = sp.current_user_saved_tracks()
#rec_played = sp.current_user_recently_played()
#saved_episodes = sp.current_user_saved_episodes()
#data = sp.categories()

url = favorite_songs['href']
# Making a GET request
request = requests.get(url=url)

pprint(request.content)
