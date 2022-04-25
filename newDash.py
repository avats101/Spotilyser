import operator
import requests
import json
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64
import chart_studio.plotly as py
import plotly.offline as po
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from matplotlib.collections import PatchCollection


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

#################### TOP ARTISTS ###################################

if pd.read_csv("top_artists.csv").empty:

    def findTopArtist(country):
        r = lastfm_get({
        'method': 'geo.gettopartists'
        }, country)

        artists = dict()
  
        for i in range(50):
            artists[r.json()['topartists']['artist'][i]['name']] = r.json()['topartists']['artist'][i]['listeners']

        sortedArtists = sorted(artists.items(), key=operator.itemgetter(1))
        return sortedArtists[-1]

    country = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Chad', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guernsey', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malaysia', 'Maldives', 'Mali', 'Mauritius', 'Mexico', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Russian Federation', 'Saudi Arabia', 'Serbia', 'Seychelles', 'Singapore', 'Slovakia', 'South Africa', 'Spain', 'Sri Lanka', 'Swaziland', 'Sweden', 'Switzerland', 'Taiwan', 'Tajikistan', 'Thailand', 'Togo', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Yemen', 'Zambia', 'Zimbabwe']
    codes = ['AFG', 'ALB', 'DZA', 'AND', 'AGO', 'AIA', 'ARG', 'ARM', 'ABW', 'AUS', 'AUT', 'AZE', 'BHR', 'BGD', 'BRB', 'BLR', 'BEL', 'BLZ', 'BEN', 'BMU', 'BTN', 'BOL', 'BIH', 'BWA', 'BRA', 'BGR', 'BDI', 'KHM', 'CMR', 'CAN', 'CYM', 'TCD', 'CHL', 'CHN', 'COL', 'CRI', 'HRV', 'CUB', 'CYP', 'CZE', 'DNK', 'DJI', 'DMA', 'ECU', 'EGY', 'SLV', 'EST', 'ETH', 'FJI', 'FIN', 'FRA', 'GAB', 'GEO', 'DEU', 'GHA', 'GIB', 'GRC', 'GRL', 'GRD', 'GUM', 'GTM', 'GGY', 'HTI', 'HND', 'HKG', 'HUN', 'ISL', 'IND', 'IDN', 'IRQ', 'IRL', 'ISR', 'ITA', 'JAM', 'JPN', 'JEY', 'JOR', 'KAZ', 'KEN', 'KWT', 'KGZ', 'LVA', 'LBN', 'LTU', 'LUX', 'MDG', 'MYS', 'MDV', 'MLI', 'MUS', 'MEX', 'MCO', 'MNG', 'MNE', 'MAR', 'NAM', 'NPL', 'NLD', 'NZL', 'NGA', 'NOR', 'OMN', 'PAK', 'PAN', 'PER', 'PHL', 'POL', 'PRT', 'PRI', 'QAT', 'RUS', 'SAU', 'SRB', 'SYC', 'SGP', 'SVK', 'ZAF', 'ESP', 'LKA', 'SWZ', 'SWE', 'CHE', 'TWN', 'TJK', 'THA', 'TGO', 'TUN', 'TUR', 'TKM', 'UGA', 'UKR', 'ARE', 'GBR', 'USA', 'URY', 'UZB', 'VUT', 'VEN', 'YEM', 'ZMB', 'ZWE']

    API_KEY = '4d5b0e0d0fb5a1304821593a75aa70e2'
    USER_AGENT = 'Arohan'

    data = dict()

    for i in country:
        data[i] = findTopArtist(i)

    df1 = pd.DataFrame(list(data.keys()), columns=['Country'])
    df2 = pd.DataFrame(list(data.values()), columns=["Artist", "Listeners"])
    df3 = pd.DataFrame(codes, columns = ["Code"])

    df = pd.concat([df1, df2, df3], axis=1)
    df.to_csv("top_artists.csv", index=False)
#po.init_notebook_mode(connected = True)
else:
    df=pd.read_csv("top_artists.csv")
data = dict(type='choropleth', 
            locations = df['Code'], 
            z = df['Listeners'], 
            text = df['Artist'])

layout = dict(geo = dict(projection = {'type':'robinson'}))

x = go.Figure(data = [data], layout = layout)

#######################################################################


#################### TOP SONGS ###################################
if pd.read_csv("top_artists.csv").empty:
  def findTopSong(country):
    r = lastfm_get({
      'method': 'geo.gettoptracks'
    }, country)

    songs = dict()
  
    for i in range(50):
      songs[r.json()['tracks']['track'][i]['name']] = r.json()['tracks']['track'][i]['listeners']
  
    sortedSongs = sorted(songs.items(), key=operator.itemgetter(1))
    return sortedSongs[-1]

  country = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Chad', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guernsey', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malaysia', 'Maldives', 'Mali', 'Mauritius', 'Mexico', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Russian Federation', 'Saudi Arabia', 'Serbia', 'Seychelles', 'Singapore', 'Slovakia', 'South Africa', 'Spain', 'Sri Lanka', 'Swaziland', 'Sweden', 'Switzerland', 'Taiwan', 'Tajikistan', 'Thailand', 'Togo', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Yemen', 'Zambia', 'Zimbabwe']
  codes = ['AFG', 'ALB', 'DZA', 'AND', 'AGO', 'AIA', 'ARG', 'ARM', 'ABW', 'AUS', 'AUT', 'AZE', 'BHR', 'BGD', 'BRB', 'BLR', 'BEL', 'BLZ', 'BEN', 'BMU', 'BTN', 'BOL', 'BIH', 'BWA', 'BRA', 'BGR', 'BDI', 'KHM', 'CMR', 'CAN', 'CYM', 'TCD', 'CHL', 'CHN', 'COL', 'CRI', 'HRV', 'CUB', 'CYP', 'CZE', 'DNK', 'DJI', 'DMA', 'ECU', 'EGY', 'SLV', 'EST', 'ETH', 'FJI', 'FIN', 'FRA', 'GAB', 'GEO', 'DEU', 'GHA', 'GIB', 'GRC', 'GRL', 'GRD', 'GUM', 'GTM', 'GGY', 'HTI', 'HND', 'HKG', 'HUN', 'ISL', 'IND', 'IDN', 'IRQ', 'IRL', 'ISR', 'ITA', 'JAM', 'JPN', 'JEY', 'JOR', 'KAZ', 'KEN', 'KWT', 'KGZ', 'LVA', 'LBN', 'LTU', 'LUX', 'MDG', 'MYS', 'MDV', 'MLI', 'MUS', 'MEX', 'MCO', 'MNG', 'MNE', 'MAR', 'NAM', 'NPL', 'NLD', 'NZL', 'NGA', 'NOR', 'OMN', 'PAK', 'PAN', 'PER', 'PHL', 'POL', 'PRT', 'PRI', 'QAT', 'RUS', 'SAU', 'SRB', 'SYC', 'SGP', 'SVK', 'ZAF', 'ESP', 'LKA', 'SWZ', 'SWE', 'CHE', 'TWN', 'TJK', 'THA', 'TGO', 'TUN', 'TUR', 'TKM', 'UGA', 'UKR', 'ARE', 'GBR', 'USA', 'URY', 'UZB', 'VUT', 'VEN', 'YEM', 'ZMB', 'ZWE']

  API_KEY = '4d5b0e0d0fb5a1304821593a75aa70e2'
  USER_AGENT = 'Arohan'
  
  dataSongs = dict()

  for i in country:
    dataSongs[i] = findTopSong(i)

  dfs1 = pd.DataFrame(list(dataSongs.keys()), columns=['Country'])
  dfs2 = pd.DataFrame(list(dataSongs.values()), columns=["Songs", "Listeners"])
  dfs3 = pd.DataFrame(codes, columns = ["Code"])

  dfs = pd.concat([dfs1, dfs2, dfs3], axis=1)
  dfs.to_csv("top_songs.csv", index=False)

else:
    dfs=pd.read_csv("top_songs.csv")

dataSongs = dict(type='choropleth', 
            locations = dfs['Code'], 
            z = dfs['Listeners'], 
            text = dfs['Songs'])

layoutSongs = dict(title = 'Country wise top songs', 
              geo = dict(projection = {'type':'robinson'}))

y = go.Figure(data = [dataSongs], layout = layoutSongs)

##############################################################


##################  TOP GENRES ##############################
def getTopGenre():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
        scope="user-follow-read user-read-recently-played user-read-playback-position user-top-read user-read-email user-read-private user-library-read",
        redirect_uri="http://example.com",
        client_id='204d99eaea4044d08a4d5c06444cb58a',
        client_secret='ac11837bbd6e410da35bcbd3a1b05a7c',
        show_dialog=True,
        cache_path="token.txt"
        )
    )
    result = sp.current_user_top_artists()

    genres = []
    unique = set()

    for i in range(20):
        for j in result['items'][i]['genres']:
            genres.append(j)
            unique.add(j)

    topGenres = dict()

    for i in unique:
        topGenres[i] = genres.count(i)

    return sorted(topGenres.items(), key=operator.itemgetter(1))

def nested_circles(data, labels=None, c=None, ax=None, cmap=None, norm=None, textkw={}):
    ax = ax or plt.gca()
    data = np.array(data)
    R = np.sqrt(data/data.max())
    p = [plt.Circle((0,r), radius=r) for r in R[::-1]]
    arr = data[::-1] if c is None else np.array(c[::-1])
    col = PatchCollection(p, cmap=cmap, norm=norm, array=arr)

    ax.add_collection(col)
    ax.axis("off")
    ax.set_aspect("equal")
    ax.autoscale()

    if labels is not None:
        kw = dict(color="white", va="center", ha="center")
        kw.update(textkw)
        ax.text(0, R[0], labels[0], **kw)
        for i in range(1, len(R)):
            ax.text(0, R[i]+R[i-1], labels[i], **kw)
    return col

dfg = pd.DataFrame(getTopGenre(), columns=["Genre", "Count"])

count = list(dfg['Count'])[-4:]
labels = list(dfg['Genre'])[-4:]
circles = nested_circles(count, labels=labels, cmap="tab10", textkw=dict(color = "black", fontsize=14))
plt.title("Your top genres")
#plt.show()
#z = go.Figure(data = circles)

#plot not showing in dash

##################################################################

app = Dash(__name__)
app.layout = html.Div(children=[
  html.Div(children=[
    dcc.Graph(figure = x)
    ]),
  html.Div(children=[
    dcc.Graph(figure = y)
    ]),
  #html.Div(children=[
  #  dcc.Graph(figure = z)
  #  ])
  ])

if __name__ == "__main__":
    app.run_server(debug=True)
