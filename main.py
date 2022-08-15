# from __future__ import print_function
# import sys
# import spotipy
# import spotipy.util as util

# scope = 'user-library-read'

# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Usage: %s username" % (sys.argv[0],))
#     sys.exit()

# token = util.prompt_for_user_token(username, scope)

# if token:
#     sp = spotipy.Spotify(auth=token)
#     results = sp.current_user_saved_tracks()
#     for item in results['items']:
#         track = item['track']
#         print(track['name'] + ' - ' + track['artists'][0]['name'])
# else:
#     print("Can't get token for", username)
import os
import pprint

# getting the EMVs
# result = os.getenv('client_id','EMV not found')
client_id = os.environ.get('client_id','client_id not found')
print(client_id)
# env_var = os.environ
  
# # Print the list of user's
# # environment variables
# print("User's Environment variable:")
# pprint.pprint(dict(env_var['client_id']), width = 1)