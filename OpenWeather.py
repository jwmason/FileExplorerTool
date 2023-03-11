# openweather.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Mason Wong
# masonjw1@uci.edu
# 48567424

# key: e5e0d69e2df302b25f3f486a47e42067

"""This module retrieves data from the OpenWeather API."""

import json
from urllib import request, error
import urllib.request
import urllib.error
import WebAPI


class OpenWeather(WebAPI.WebAPI):
    """This class stores data (temperatures, coordinates, and
    weather descriptions) from OpenWeather API."""
    def __init__(self, zip: str = '95758', ccode: str = 'US'):
        self.zip = zip
        self.ccode = ccode

    def set_apikey(self, apikey: str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service

        '''
        # TODO: assign apikey value to a class data attribute that can
        # be accessed by class members
        self.apikey = apikey
        pass

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores
        the response in class data attributes.

        '''
        # TODO: use the apikey data attribute and the urllib module
        # to request data from the web api. See sample code at the begining
        # of Part 1 for a hint.TODO: assign the necessary response data to
        # the required class data attributes
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zip},{self.ccode}&appid={self.apikey}"
        web_api = self
        r_obj = web_api._download_url(url)

        if r_obj:
            self.temperature = r_obj['main']['temp']
            self.high_temperature = r_obj['main']['temp_max']
            self.low_temperature = r_obj['main']['temp_min']
            self.longitude = r_obj['coord']['lon']
            self.latitude = r_obj['coord']['lat']
            self.description = r_obj['weather'][0]['description']
            self.humidity = r_obj['main']['humidity']
            self.city = r_obj['name']
            self.sunset = r_obj['sys']['sunset']
        pass

    def transclude(self, message: str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        '''
        # TODO: write code necessary to transclude keywords in
        # the message parameter with appropriate data from API
        return message.replace('@weather', self.description)
