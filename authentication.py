# ---  Websites:
# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
# https://developer.spotify.com/documentation/general/guides/authorization/app-settings/
# https://developer.spotify.com/dashboard/applications/92cce333b3da417a95d8ca738477b241
### ----------------------------------------------------------------------------------------------- ###
from requests import Request, Response, post
import requests
#from rest_framework import status, R

client_id = "92cce333b3da417a95d8ca738477b241"
Client_Secret = "7bbf053307e54547be82030359eb072c"

scopes = 'ugc-image-upload user-modify-playback-state user-follow-modify user-read-recently-played user-read-playback-position playlist-read-collaborative app-remote-control user-read-playback-state user-read-email streaming user-top-read playlist-modify-public user-library-modify user-follow-read user-read-currently-playing user-library-read playlist-read-private user-read-private playlist-modify-private'


def get_url():
    # generates a url for us (output: string)
    url = Request('GET', 'https://accounts.spotify.com/authorize', params={
        'scope': scopes,
        'response_type': 'code',
        'redirect_uri': 'https://mySpotifyAPI.com/home',
        'client_id': client_id
    }).prepare().url

    return url


url = get_url()
print(url)
response = requests.get(url)
print(response)
