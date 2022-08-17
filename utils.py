from prettyprinter import pprint
from authentication import authenticate
from collections import Counter

sp = authenticate()


def convert_date(date):
    day = str(date)[8:10]
    month = str(date)[5:7]
    year = str(date)[0:4]
    return f"{day}.{month}.{year}"


def get_categories(sp, print_results=True):
    categories = sp.categories()
    all_categories = []

    # List
    for categorie in categories['categories']['items']:
        catego = categorie['name']
        if print_results:
            pprint(f"- {str(catego)}")
        all_categories.append(catego)
    return all_categories


def get_favorite_songs(sp, print_results=True):
    '''
        return just the songs in the favorite categories
        param: print_results prints all kind of Data regarding to the song
    '''
    fav_songs = sp.current_user_saved_tracks()
    if print_results:
        print("There are currently " +
              str(fav_songs['total']) + " Songs added to your Favorite Songs list:")

    # pprint(fav_songs.keys())
    # pprint(type(fav_songs['items'])) # is a list
    favorite_songs = []
    song_cnt = 1
    for song in fav_songs['items']:

        # song_uri = song['track']['uri']
        # print(song_uri)
        # sp.add_to_queue(uri="spotify:track:6SYu5mwFpG3AmoudfJrt33")
        break
        title = song['track']['name']

        artist = None
        feat = 0
        has_a_feat = False
        artist = song['track']['album']['artists'][0]['name']
        if len(song['track']['artists']) > 1:
            feat = len(song['track']['artists']) - 1
            has_a_feat = True

        '''pprint(artist)
        pprint(song['track']['album']['artists'][0]['name'])
        pprint(len(song['track']['artists']))
        len_of_artist = len(song['track']['artists'])
        if len_of_artist == 1:
            artist = song['track']['artists'][0]['name']
        else:
            artist_1, artist_2 = None, None
            for i in range(len_of_artist):
                if i == 0:
                    artist_1 = song['track']['artists'][0]['name']
                elif i == 2:
                    artist_2 = song['track']['artists'][1]['name']
            artist = f"{artist_1} feat. {artist_2}"
            for i in song['track']['artists']:
                # pprint(i.keys())
                artist = f"{i['name']} feat. {i['name']}"
                len_of_artist -= 1
                if len_of_artist == 0:
                    break
        pprint(artist)
        pprint(song['track']['album']['artists'][0]['name'])

        album = song['track']['album']['name']
        '''

        duration_min = 0
        rest_sec = 0
        duration_ms = int(song['track']['duration_ms'])
        duration_min = duration_ms / (1000 * 60)
        rest_sec = (duration_min - int(duration_min)) * 60

        date_added = convert_date(date=song['added_at'])

        if print_results:
            if has_a_feat:
                output = f"\t{song_cnt}. {title} from {artist}, Duration: {int(duration_min)}:{int(rest_sec)} min ---> added at: {date_added}\t\t This song has {feat} features"
            else:
                output = f"\t{song_cnt}. {title} from {artist}, Duration: {int(duration_min)}:{int(rest_sec)} min ---> added at: {date_added}"
            print(output)
        # data = f"{title} from {artist}"
        favorite_songs.append(title)
        song_cnt += 1

    return favorite_songs


def get_recently_played(sp, amount_of_tracks=20):
    rec_played = sp.current_user_recently_played(limit=amount_of_tracks)
    data = {
        'songs': [],
        'artists': [],
        'date': []
    }

    for item in rec_played['items']:
        data['songs'].append(item['track']['name'])
        data['artists'].append(item['track']['artists'][0]['name'])
        data['date'].append(convert_date(date=item['played_at']))

    return data


def get_current_user_saved_episodes(sp):
    saved_episodes = sp.current_user_saved_episodes()


def get_all_top_tracks(sp):
    data = {'songs': [],
            'uri': [],
            'artists': []
            }
