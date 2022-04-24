API_KEY = '4d5b0e0d0fb5a1304821593a75aa70e2'
USER_AGENT = 'Arohan'

import requests

def lastfm_get(payload, COUNTRY):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['country'] = COUNTRY
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

#find most popular artist in a particular country
import operator

def findTopArtist(country):
  r = lastfm_get({
    'method': 'geo.gettopartists'
  }, country)

  artists = dict()
  
  for i in range(50):
    artists[r.json()['topartists']['artist'][i]['name']] = r.json()['topartists']['artist'][i]['listeners']
  
  sortedArtists = sorted(artists.items(), key=operator.itemgetter(1))
  return sortedArtists[-1]

country = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Chad', 'Chile', 'China', 'Colombia', 'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg', 'Macao', 'Madagascar', 'Malaysia', 'Maldives', 'Mali', 'Mauritius', 'Mexico', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands','New Zealand', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Russian Federation', 'Saudi Arabia', 'Serbia', 'Seychelles', 'Singapore', 'Slovakia', 'South Africa', 'Spain', 'Sri Lanka', 'Swaziland', 'Sweden', 'Switzerland', 'Taiwan', 'Tajikistan', 'Thailand', 'Togo', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Yemen', 'Zambia', 'Zimbabwe']

data = dict()

for i in country:
  data[i] = findTopArtist(i)


import pandas as pd

df1 = pd.DataFrame(list(data.keys()), columns=['Country'])
df2 = pd.DataFrame(list(data.values()), columns=["Artist", "Listeners"])

df = pd.concat([df1, df2], axis=1)

df.head()


# Commented out IPython magic to ensure Python compatibility.
import chart_studio.plotly as py
import plotly.offline as po
import plotly.graph_objs as pg
import matplotlib.pyplot as plt
# %matplotlib inline

po.init_notebook_mode(connected = True)

data = dict(type='choropleth', 
            locations = df['Country'], 
            z = df['Listeners'], 
            text = df['Artist'])

layout = dict(title = 'Country wise top artists', geo = dict(projection = {'type':'robinson'}, showlakes = True, lakecolor = 'rgb(0,191,255)'))

x = pg.Figure(data = [data], layout = layout)

po.iplot(x)
x.show()