# lastfm.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Mason Wong
# masonjw1@uci.edu
# 48567424

"""This module retrieves data from the LastFM API."""

import WebAPI

# key: 2cdc085e470a355813e6aba66d46b6bd


class LastFM(WebAPI.WebAPI):
    """This class stores listener and playcount numbers
    from given artist from LastFM API."""
    def __init__(self, artist: str = 'Rihanna'):
        self.artist = artist
        self.listeners = None
        self.playcount = None
        self.apikey = None

    def set_apikey(self, apikey: str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service

        '''
        self.apikey = apikey

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in
        class data attributes.

        '''
        url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={self.artist}&api_key={self.apikey}&format=json"
        web_api = self
        r_obj = web_api._download_url(url)

        if r_obj:
            self.listeners = r_obj['artist']['stats']['listeners']
            self.playcount = r_obj['artist']['stats']['playcount']

    def transclude(self, message: str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        '''
        return message.replace('@lastfm', self.artist)
