import re
from authentication import authenticate
from utils import *   # get everything
from prettyprinter import pprint
from prettyprinter import pprint
from authentication import authenticate
from collections import Counter

# sp = authenticate()


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
        'name': None,
        'email': None,
        'country': None,
        'uri': None,
        'profile_url': None,
        'membership': None
    }

    data['name'] = user['display_name']
    data['email'] = user['email']
    data['country'] = user['country']
    data['uri'] = user['uri']
    data['profile_url'] = user['external_urls']['spotify']
    data['membership'] = user['product']  # f.ex. premium

    return data  # dict()


def get_all_top_tracks(sp=sp):
    '''
        This function returns all kind of data regarding the current user's top tracks
        params:
            - sp: Spotify (object)
    '''

    top_songs = sp.current_user_top_tracks(time_range='long_term')
    data = {'songs': [],
            'artists': [],
            'uri': []
            }

    for item in top_songs['items']:
        # pprint(item['preview_url']) # gives a url, where a slice of the song can be played

        data['songs'].append(item['name'])
        data['artists'].append(item['artists'][0]['name'])
        data['uri'].append(item['uri'])

    return data  # dict()


def get_all_top_artists(sp=sp):
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
            'uri': []
            }

    for item in top_artists['items']:
        data['artists'].append(item['name'])
        data['amount_of_followers'].append(item['followers']['total'])
        data['genres'].append(item['genres'])
        data['uri'].append(item['uri'])

    return data  # dict()


def get_recently_played(sp=sp, amount_of_tracks=20):
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


def get_tracks_from_favoritesongs(sp=sp):
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

    # adds the amount of tracks, added in favorite Songs
    data['amount'] = fav_songs['total']
    for song in fav_songs['items']:
        data['songs'].append(song['track']['name'])
        data['artists'].append(song['track']['album']['artists'][0]['name'])
        data['uri'].append(song['track']['uri'])

    return data  # dict()


def add_track_to_queue(song_uri, sp=sp):
    '''
        This function adds a song to the queue of the user
        params:
            - sp: Spotify (object)
            - song_uri (str): The uri of the song, which should be added to queue
    '''

    sp.add_to_queue(uri=song_uri)


def main():
    sp = authenticate()

    get_current_user(sp)
    get_all_top_tracks(sp)
    get_all_top_artists(sp)
    get_recently_played(sp)
    get_tracks_from_favoritesongs(sp)

    # bsp_test_song_uri = get_all_top_tracks(sp)['uri'][4]
    # add_track_to_queue(bsp_test_song_uri)


if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()
