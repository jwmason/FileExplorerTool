# lastfm.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Mason Wong
# masonjw1@uci.edu
# 48567424

"""This module retrieves data from the LastFM API."""

import json
from urllib import request,error
import urllib.request, urllib.error


# key: 2cdc085e470a355813e6aba66d46b6bd

class LastFM:
    """This class stores listener and playcount numberes from given artist from LastFM API."""
    def __init__(self, artist: str):
        self.artist = artist


    def set_apikey(self, apikey:str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
    
        '''
        #TODO: assign apikey value to a class data attribute that can be accessed by class members
        self.apikey = apikey
        pass


    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
            
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        #TODO: assign the necessary response data to the required class data attributes
        url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={self.artist}&api_key={self.apikey}&format=json"
        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            r_obj = json.loads(json_results)
            
            print(r_obj)
            self.listeners = r_obj['artist']['stats']['listeners']
            self.playcount = r_obj['artist']['stats']['playcount']

        except urllib.error.HTTPError as e:
            if e.code == 404 or e.code == 503:
                print('Error, the remote API is unavailable')
            else:
                print('Failed to download contents of URL')
                print('Status code: {}'.format(e.code))
        except urllib.error.URLError:
            print('Error with local connection to the Internet')
        except ValueError:
            print('Error with invalid data formatting from the remote API')
        except SyntaxError:
            print('Error with invalid data formatting from the remote API')
        finally:
            response.close()
