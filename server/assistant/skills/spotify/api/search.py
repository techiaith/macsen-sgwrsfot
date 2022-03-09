#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from .apikey import CLIENT_ID, CLIENT_SECRET

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def search_artist(name):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    return sp.search(q='artist:' + name, type='artist')

if __name__ == '__main__':
    print (search_artist(sys.argv[1]))
