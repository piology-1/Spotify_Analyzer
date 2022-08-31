from turtle import position
from prettyprinter import pprint
from authentication import authenticate
import requests


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


def get_current_user(sp):
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
        'profile_img': user['images'][0]['url']
    }

    return data  # dict()


def get_all_top_tracks(sp):
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


def track_played_min(sp, song_id):
    '''
        This function returns the duration, that a specific song was played returned in minutes
        params:
            - sp: Spotify (object)
            - song_id: the id of the track or song
    '''

    track_audio_data = sp.audio_analysis(track_id=song_id)

    all_time_duration_min = track_audio_data['track']['duration']  # [min]
    return int(all_time_duration_min)


def get_all_top_artists(sp):
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


def get_recently_played(sp, amount_of_tracks=20):
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
        'uri': []
    }

    for item in rec_played['items']:
        data['songs'].append(item['track']['name'])
        data['artists'].append(item['track']['artists'][0]['name'])
        data['date'].append(convert_date(date=item['played_at']))
        data['songs'].append(item['track']['uri'])

    return data  # dict()


def get_tracks_from_favoritesongs(sp):
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
        'uri': []
    }

    data['amount'] = fav_songs['total']
    for song in fav_songs['items']:
        data['songs'].append(song['track']['name'])
        data['artists'].append(song['track']['album']['artists'][0]['name'])
        data['uri'].append(song['track']['uri'])

    return data  # dict()


def add_track_to_queue(song_uri, sp):
    '''
        This function adds a song to the queue of the user
        params:
            - sp: Spotify (object)
            - song_uri (str): The uri of the song, which should be added to queue
    '''

    sp.add_to_queue(uri=song_uri)


def get_currently_playing_song(sp):
    currently_playing = sp.current_user_playing_track()

    if currently_playing['is_playing']:
        data = {
            'song': currently_playing['item']['name'],
            'artist': currently_playing['item']['artists'][0]['name'],
            'img_url': currently_playing['item']['album']['images'][0]['url'],
            'is_playing': currently_playing['is_playing']  # True or False
        }

        return data

    else:
        return None


def play_next_track(sp):
    """
        This function skips to the next track.
        A Device should be active and open spotify
    """
    # sp.next_track()
    try:
        sp.next_track()
    except:
        print("Couldn't skip, because no Device is currently active!")


def play_previous_track(sp):
    """
        This function skips to the previous track.
        A Device should be active and open spotify
    """
    try:
        sp.previous_track()
    except:
        print("Couldn't skip, because no Device is currently active!")


def pause_current_track(sp):
    """
        This function pauses track.
        A Device should be active and open spotify
    """
    try:
        sp.pause_playback()
    except:
        print("Couldn't pause, because no Device is currently active!")


def start_current_track(sp):
    """
        This function starts track.
        A Device should be active and open spotify
    """
    try:
        sp.start_playback(position_ms=0)
    except:
        print("Couldn't start, because no Device is currently active!")


def set_repeat_mode(sp):
    """
        This function sets the state in repeatmode.
        A Device should be active and open spotify
    """
    sp.repeat(state="track")


def set_shuffle_mode(sp):
    """
        This function sets the state in shufflemode.
        A Device should be active and open spotify
    """
    sp.shuffle(state=True)  # "true"


def control_volume(sp, volume_percent):
    """
        This function sets the volume to the given percentage value
        A Device should be active and open spotify
    """
    sp.volume(volume_percent=volume_percent)


# sp = authenticate()
# start_current_track(sp=sp)
# pause_current_track(sp=sp)
# play_previous_track(sp=sp)
# pprint(get_current_user(sp=sp))
"""
# sp = authenticate()
# track_played_min(sp=sp, song_id="50eJOxJiGmJ7PBZaTKpje1")
# pprint(get_all_top_tracks(sp=sp))
# 
# profile_url = get_current_user(sp=sp)['profile_img']
# response = requests.get(url=profile_url)
# profile_img = Image.open(BytesIO(response.content))
# data = get_all_top_tracks(sp=sp)

# for song_index in range(len(data['songs'])):
#     pprint(data['songs'][song_index])

# for song in data['songs']:
#     pprint(song)

# pprint(data.keys())
# get_all_top_tracks(sp=sp)
"""
