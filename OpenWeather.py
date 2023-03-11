# openweather.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Mason Wong
# masonjw1@uci.edu
# 48567424

# key: e5e0d69e2df302b25f3f486a47e42067

"""This module retrieves data from the OpenWeather API."""

import unittest
import WebAPI

class OpenWeather(WebAPI.WebAPI):
    """This class stores data (temperatures, coordinates, and
    weather descriptions) from OpenWeather API."""
    def __init__(self, zip: str = '95758', ccode: str = 'US'):
        self.zip = zip
        self.ccode = ccode
        self.apikey = None
        self.temperature = None
        self.high_temperature = None
        self.low_temperature = None
        self.longitude = None
        self.latitude = None
        self.description = None
        self.humidity = None
        self.city = None
        self.sunset = None

    def set_apikey(self, apikey: str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service

        '''
        self.apikey = apikey

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores
        the response in class data attributes.

        '''
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

    def transclude(self, message: str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        '''
        return message.replace('@weather', self.description)


class TestOpenWeather(unittest.TestCase):
    """This is a class that tests Openweather"""
    def test_set_apikey(self):
        """Tests apikey"""
        apikey = 'e5e0d69e2df302b25f3f486a47e42067'
        ow = OpenWeather()
        ow.set_apikey(apikey)
        assert ow.apikey == apikey

    def test_load_data(self):
        """Tests load data"""
        ow = OpenWeather()
        ow.set_apikey('e5e0d69e2df302b25f3f486a47e42067')
        ow.load_data()
        assert ow.temperature is not None
        assert ow.high_temperature is not None
        assert ow.low_temperature is not None
        assert ow.longitude is not None
        assert ow.latitude is not None
        assert ow.description is not None
        assert ow.humidity is not None
        assert ow.city is not None
        assert ow.sunset is not None

    def test_transclude(self):
        """Test transclude function"""
        ow = OpenWeather()
        ow.description = 'sunny'
        message = 'The weather is @weather'
        assert ow.transclude(message) == 'The weather is sunny'
