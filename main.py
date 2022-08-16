from authentication import authenticate
from utils import *   # get everything
from prettyprinter import pprint


def main():
    sp = authenticate()

    get_categories(sp, print_results=False)
    get_favorite_songs(sp, print_results=False)
    pprint(get_recently_played(sp))
    get_current_user_saved_episodes(sp)


if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()
