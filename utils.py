from prettyprinter import pprint
from authentication import authenticate
import requests
import spotipy


def convert_date(date):
    '''
        This function converts a Data given in '2022-08-17T14:27:25.085Z' to '17.08.2022'
        params:
            - date: string in the Form of '2022-08-17T14:27:25.085Z'
    '''
    day = str(date)[8:10]
    month = str(date)[5:7]
    year = str(date)[0:4]
    return f"{day}.{month}.{year}"


def get_current_user(sp) -> dict:
    '''
        This function returns all kind of information regarding the current user
        params:
            - sp: Spotify (object)
    '''

    user = sp.current_user()

    data = {
        'name': user['display_name'],
        'email': user['email'],
        'country': user['country'],
        'uri': user['uri'],
        'profile_url': user['external_urls']['spotify'],
        'membership': user['product'],  # f.ex. premium
        'profile_img': user['images'][0]['url'],
        'id': user['id']
    }

    return data  # dict()


def get_all_top_tracks(sp) -> dict:
    '''
        This function returns all kind of data regarding the current user's top tracks
        params:
            - sp: Spotify (object)
    '''

    top_songs = sp.current_user_top_tracks(time_range='long_term')

    data = {'songs': [],
            'artists': [],
            'uri': [],
            'img_url': [],
            'song_id': []
            }

    for item in top_songs['items']:
        data['songs'].append(item['name'])
        data['artists'].append(item['artists'][0]['name'])
        data['uri'].append(item['uri'])
        # the max width and height (640, 640)
        data['img_url'].append(item['album']['images'][0]['url'])
        data['song_id'].append(item['id'])

    return data  # dict()


def track_played_min(sp, song_id) -> dict:
    '''
        This function returns the duration, that a specific song was played returned in minutes
        params:
            - sp: Spotify (object)
            - song_id: the id of the track or song
    '''

    track_audio_data = sp.audio_analysis(track_id=song_id)

    all_time_duration_min = track_audio_data['track']['duration']  # [min]
    return int(all_time_duration_min)


def get_all_top_artists(sp) -> dict:
    '''
        This function returns all kind of data regarding the current user's top artists
        params:
            - sp: Spotify (object)
    '''

    top_artists = sp.current_user_top_artists(
        time_range="long_term")  # long_term = 50 tracks (['total'])
    data = {'artists': [],
            'amount_of_followers': [],
            'genres': [],
            'uri': [],
            'img_url': []
            }

    for item in top_artists['items']:
        data['artists'].append(item['name'])
        data['amount_of_followers'].append(item['followers']['total'])
        data['genres'].append(item['genres'])
        data['uri'].append(item['uri'])
        data['img_url'].append(item['images'][0]['url'])

    return data  # dict()


def get_recently_played(sp, amount_of_tracks=20) -> dict:
    '''
        This function returns all kind of data regarding the recently played tracks
        params:
            - sp: Spotify (object)
            - amount_of_tracks (int): default=20
    '''

    rec_played = sp.current_user_recently_played(limit=amount_of_tracks)
    data = {
        'songs': [],
        'artists': [],
        'date': [],
        'uri': [],
        'img_url': []
    }

    for item in rec_played['items']:
        data['songs'].append(item['track']['name'])
        data['artists'].append(item['track']['artists'][0]['name'])
        data['date'].append(convert_date(date=item['played_at']))
        data['uri'].append(item['track']['uri'])
        data['img_url'].append(item['track']['album']['images'][0]['url'])

    return data  # dict()


def get_tracks_from_favoritesongs(sp) -> dict:
    '''
        This returns all kind of data from the tracks, which are added in the 'favorite Songs' categorie
        params:
            - sp: Spotify (object)
    '''

    fav_songs = sp.current_user_saved_tracks()
    data = {
        'amount': None,
        'songs': [],
        'artists': [],
        'uri': [],
        'img_url': []
    }

    data['amount'] = fav_songs['total']
    for song in fav_songs['items']:
        data['songs'].append(song['track']['name'])
        data['artists'].append(song['track']['album']['artists'][0]['name'])
        data['uri'].append(song['track']['uri'])
        data['img_url'].append(song['track']['album']['images'][0]['url'])

    return data  # dict()


def add_track_to_queue(sp, song_uri):
    '''
        This function adds a song to the queue of the user
        params:
            - sp: Spotify (object)
            - song_uri (str): The uri of the song, which should be added to queue
    '''
    try:
        sp.add_to_queue(uri=song_uri)
        return True
    except spotipy.exceptions.SpotifyException as e:
        """
            Error 404: No active device found            
        """
        return e.http_status
    except Exception:
        return False


def add_track_to_fav_songs(sp, track_uri=[]):
    """
        This function adds a song to the favoritue library of the user
        params:
            - sp: Spotify (object)
            - track_uri (lst): needds to be a list of track URIs, URLs or IDs 
    """
    # could add list of uri's as well
    sp.current_user_saved_tracks_add(tracks=track_uri)


def get_currently_playing_song(sp) -> dict:
    currently_playing = sp.current_user_playing_track()

    try:
        data = {
            'song': currently_playing['item']['name'],
            'artist': currently_playing['item']['artists'][0]['name'],
            'img_url': currently_playing['item']['album']['images'][0]['url'],
            'is_playing': currently_playing['is_playing'],  # True or False
            'song_uri': currently_playing['item']['uri']
        }

        return data

    except TypeError:
        return False


def set_shuffle_mode(sp, status=False):
    """
        This function sets the state in shufflemode.
        A Device should be active and open spotify
        params:
            - status: Wheter Shuffle mode is on or not (True or False)
    """
    sp.shuffle(state=status)  # state: Shuffle Mode on or not "true" or "false"


def set_repeat_mode(sp):
    """
        This function sets the state in repeatmode.
        A Device should be active and open spotify
    """
    sp.repeat(state="track")


def play_previous_track(sp):  # skip back to prevoius song
    """
        This function skips to the previous track.
        A Device should be active and open spotify
    """
    try:
        """ Skip back was successfull """
        sp.previous_track()
        return True
    except Exception:
        """ unkown error """
        return False

    # except spotipy.exceptions.SpotifyException as e:
    #     """ Error 404: No active device found """
    #     return e.http_status  # int


def pause_current_track(sp):
    """
        This function pauses track.
        A Device should be active and open spotify
    """
    try:
        sp.pause_playback()
        return True
    except spotipy.exceptions.SpotifyException as e:
        """
            Error 404: No active device found
            Error 403: Device is currently active and a track is already playing
        """
        return e.http_status
    except Exception:
        return False


def start_current_track(sp):
    """
        This function starts track.
        A Device should be active and open spotify
    """
    try:
        sp.start_playback(position_ms=0)
        return True
    except spotipy.exceptions.SpotifyException as e:
        """
            Error 404: No active device found
            Error 403: Device is currently active and a track is already playing
        """
        return e.http_status

    # TODO: need to handle: HTTP Error for PUT to https://api.spotify.com/v1/me/player/play with Params: {} returned 403 due to Player command failed: Restriction violated in console
    # except Exception as errh:
    #     print("do I get here???")
        # print("Http Error:", errh.with_traceback(errh))


def play_next_track(sp):  # skip to next song
    """
        This function skips to the next track.
        A Device should be active and open spotify
    """
    try:
        sp.next_track()
        return True
    except Exception:
        return False


def control_volume(sp, volume_percent):
    """
        This function sets the volume to the given percentage value
        A Device should be active and open spotify
    """
    # ERROR: Player command failed: Cannot control device volume, reason: VOLUME_CONTROL_DISALLOW
    sp.volume(volume_percent=volume_percent)


def create_playlist(sp, songs, playlist_name="", visability_status="public", collaborate=False, playlist_description=""):
    """
        This function creates a new playlist

        params:
            - songs: a list of track URIs, URLs or IDs
            - playlist_name: The name of the playlist            
            - visability_status: decides, wheter the playlist is public (True) or private (False)
            - collaborate: decides, wheter the playlist is aditable with another person or only by one user
            - playlist_description: The description of the playlist

            ### - track_pos: the position to add the tracks
    """

    # TODO: playlist is akways public (True or false doesn't work)
    status = True  # default is public (True)
    if visability_status == "private":
        status = False

    curr_user = get_current_user(sp=sp)
    # creating an empty playlist
    playlist = sp.user_playlist_create(
        user=curr_user['id'], name=playlist_name, public=status, collaborative=collaborate, description=playlist_description)

    # adding tracks to the playlist
    sp.user_playlist_add_tracks(
        user=curr_user['id'], playlist_id=playlist['id'], tracks=songs, position=None)


"""
def get_playlist_data(sp, playlist_id)

    data = {
        'name':None,
        'id': playlist_id,
        'url': None,
        'cover_img':None
    }
    # getting the image of Playlistcover
    playlist_img = sp.playlist_cover_image(
        playlist_id=playlist['id'])[0]['url']
"""

sp = authenticate()
# pprint(get_all_top_tracks(sp=sp))
