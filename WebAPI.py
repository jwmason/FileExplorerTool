# webapi.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Mason Wong
# masonjw1@uci.edu
# 48567424

"""This module is the parent class for both web apis
(OpenWeather and LastFM) that prevents redundant code"""

from abc import ABC, abstractmethod
import urllib.request
import urllib.error
import json


class WebAPI(ABC):
    """This is the parent class for the Web API."""
    def __init__(self):
        self.apikey = None

    def _download_url(self, url: str) -> dict:
        """This function implements web api request codes
        in a way that supports all types of web APIs."""
        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            r_obj = json.loads(json_results)
            return r_obj
        except urllib.error.HTTPError as e:
            if e.code in (404, 503):
                print('Error, the remote API is unavailable')
            else:
                print('Failed to download contents of URL')
                print(f'Status code: {e.code}')
        except urllib.error.URLError:
            print('Error with local connection to the Internet')
        except ValueError:
            print('Error with invalid data formatting from the remote API')
        except SyntaxError:
            print('Error with invalid data formatting from the remote API')

    def set_apikey(self, apikey: str) -> None:
        """Sets api key"""
        self.apikey = apikey

    @abstractmethod
    def load_data(self):
        """This abstract function loads data"""


    @abstractmethod
    def transclude(self, message: str) -> str:
        """This abstract method transcludes message"""
