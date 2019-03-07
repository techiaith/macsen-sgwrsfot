#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .apikey import CLIENT_ID, CLIENT_SECRET


import spotipy
import spotipy.oauth2 as oauth2

credentials = oauth2.SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET)

token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

def search_artist(name):
    return spotify.search(q='artist:' + name, type='artist')

