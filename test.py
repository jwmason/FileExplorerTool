from OpenWeather import OpenWeather
from LastFM import LastFM
import WebAPI

def test_api(message:str, apikey:str, webapi:WebAPI):
  webapi.set_apikey(apikey)
  webapi.load_data()
  result = webapi.transclude(message)
  print(result)


open_weather = OpenWeather('95758', 'US') #notice there are no params here...HINT: be sure to use parameter defaults!!!
lastfm = LastFM('KanyeWest')

test_api("Testing the weather: @weather", 'e5e0d69e2df302b25f3f486a47e42067', open_weather)
# expected output should include the original message transcluded with the default weather value for the @weather keyword.

test_api("Testing lastFM: @lastfm", '2cdc085e470a355813e6aba66d46b6bd', lastfm)
# expected output include the original message transcluded with the default music data assigned to the @lastfm keyword