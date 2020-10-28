#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from .apikey import CLIENT_ID, CLIENT_SECRET

import spotipy
import spotipy.oauth2 as oauth2

credentials = oauth2.SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET)

def search_artist(name):
    token = credentials.get_access_token()
    spotify = spotipy.Spotify(auth=token)
    return spotify.search(q='artist:' + name, type='artist')

if __name__ == '__main__':
    print (search_artist(sys.argv[1]))
