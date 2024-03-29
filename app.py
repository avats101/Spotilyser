import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
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
from tkinter import *
from tkinter import filedialog
import dash_bootstrap_components as dbc
import dash
import plotly.offline as po
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import operator
import requests
import webbrowser
import pickle
import key
from sklearn import preprocessing


def get_directory():
    root = Tk()
    path = filedialog.askdirectory(title="Choose path to spotify data folder")
    root.destroy()
    return path

path = get_directory()+"/"

df1 = pd.read_json(path+"/StreamingHistory0.json", encoding='utf-8')
df2 = pd.read_json(path+"/StreamingHistory1.json", encoding='utf-8')
df3 = pd.read_json(path+"/StreamingHistory2.json", encoding='utf-8')
df4 = pd.read_json(path+"/StreamingHistory3.json", encoding='utf-8')
# df5 = pd.read_json(path+"/StreamingHistory4.json", encoding='utf-8')
# stream_df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
stream_df = pd.concat([df1, df2], ignore_index=True)
#Add dfs according to the number of input JSON files.

# stream_df.to_csv("spotify_data.csv")

stream_df['Play-Time'] = pd.to_datetime(stream_df['endTime'])
stream_df['year'] = pd.DatetimeIndex(stream_df['Play-Time']).year
stream_df['month'] = pd.DatetimeIndex(stream_df['Play-Time']).month
stream_df['day'] = pd.DatetimeIndex(stream_df['Play-Time']).day
stream_df['weekday'] = pd.DatetimeIndex(stream_df['Play-Time']).weekday
stream_df['time'] = pd.DatetimeIndex(stream_df['Play-Time']).time
stream_df['hours'] = pd.DatetimeIndex(stream_df['Play-Time']).hour
stream_df['day-name'] = stream_df['Play-Time'].apply(lambda x: x.day_name())
stream_df['count'] = 1

stream_df['Time-Played (hh-mm-ss)'] = pd.to_timedelta(stream_df['msPlayed'], unit='ms')


def hours(td):
    return td.seconds / 3600


def minutes(td):
    return (td.seconds / 60) % 60


stream_df['Listening Time (Hours)'] = stream_df['Time-Played (hh-mm-ss)'].apply(hours).round(3)
stream_df['Listening Time (Minutes)'] = stream_df['Time-Played (hh-mm-ss)'].apply(minutes).round(3)

stream_df.drop(columns=['endTime', "Time-Played (hh-mm-ss)", "msPlayed"], inplace=True)

stream_df.describe()


sns.set_style('darkgrid')
plt.style.use('seaborn-darkgrid')

matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'

unique_artists = stream_df['artistName'].nunique()
total_artists = stream_df['artistName'].count()
unique_artists_per = unique_artists / total_artists * 100

unique_artists_list = np.array([unique_artists, total_artists - unique_artists])
unique_artists_list_labels = ["Unique Artists", "Non-Unique Artists"]
fig, ax = plt.subplots(figsize=(12, 6))
ax.pie(unique_artists_list, labels=unique_artists_list_labels, autopct='%1.1f%%', explode=[0.05, 0.05], startangle=180,
       shadow=True)
plt.title("Unique Artist Percentage")
# plt.show()

# ***** Plotly Code *****
# p1 = px.pie(values=unique_artists_list, names=unique_artists_list_labels, title="Unique Artist Pecentage")
# p1.show()
p1 = go.Figure(data=go.Pie(values=unique_artists_list, labels=unique_artists_list_labels, textinfo='label+percent',
                           insidetextorientation='radial', pull=0.2, rotation=90))
# p1.show()
# ***** Plotly Code *****

top_10_artist_df = stream_df.groupby(["artistName"])[
    ["Listening Time (Hours)", "Listening Time (Minutes)", "count"]].sum().sort_values(by="Listening Time (Minutes)",
                                                                                       ascending=False)
top_10_artist_time_df = stream_df.groupby(["artistName"])[
    ["Listening Time (Hours)", "Listening Time (Minutes)", "count"]].sum().sort_values(by="Listening Time (Minutes)",
                                                                                       ascending=False)

fig, ax = plt.subplots(figsize=(12, 8))
ax.bar(top_10_artist_time_df.head(10).index, top_10_artist_time_df["Listening Time (Hours)"].head(10), color='green')
ax.set( xlabel="Artists", ylabel="No. of Hours Songs Played")
plt.xticks(rotation=75)
# plt.show()

# ***** Plotly Code *****

b1 = go.Figure(
    data=go.Bar(x=top_10_artist_time_df.head(10).index, y=top_10_artist_time_df["Listening Time (Hours)"].head(10),
                hoverinfo="x+text", hovertext=top_10_artist_time_df["Listening Time (Hours)"].head(10),
                marker_color="cyan"))
b1.update_layout(xaxis_tickangle=-75)
# b1.show()

# ***** Plotly Code *****

top_10_artist_count_df = stream_df.groupby(["artistName"])[
    ["Listening Time (Hours)", "Listening Time (Minutes)", "count"]].sum().sort_values(by="count", ascending=False)

fig, ax = plt.subplots(figsize=(12, 8))
ax.bar(top_10_artist_count_df.head(10).index, top_10_artist_count_df["count"].head(10), color='orange')
ax.set(title="My Top 10 Favourite Artist (based on Counts)", xlabel="Artists", ylabel="No. of Times Songs Played")
plt.xticks(rotation=75)
# plt.show()


# ***** Plotly Code *****

b2 = go.Figure(
    data=go.Bar(x=top_10_artist_count_df.head(10).index, y=top_10_artist_count_df["count"].head(10), hoverinfo="x+text",
                hovertext=top_10_artist_count_df["count"].head(10), marker_color="cyan"))
b2.update_layout(xaxis_tickangle=-75)
# b2.show()

# ***** Plotly Code *****


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 5))

ax1.bar(top_10_artist_time_df.head(10).index, top_10_artist_time_df["Listening Time (Hours)"].head(10), color="green")
ax1.set(title="My Top 10 Favourite Artist (based on Hours)", xlabel="Artists", ylabel="No. of Hours Songs Played")
ax1.tick_params(labelrotation=75)
ax1.axhline(top_10_artist_time_df["Listening Time (Hours)"][:100].mean(), linestyle="--", color="black")

ax2.bar(top_10_artist_count_df.head(10).index, top_10_artist_count_df["count"].head(10), color="orange")
ax2.set(title="My Top 10 Favourite Artist (based on Counts)", xlabel="Artists", ylabel="No. of Times Songs Played")
ax2.tick_params(labelrotation=75)
ax2.axhline(top_10_artist_count_df["count"][:100].mean(), linestyle="--", color="black")
# plt.show()

unique_songs = stream_df["trackName"].nunique()
total_songs = stream_df["trackName"].count()
unique_songs_percentage = unique_songs / total_songs * 100

unique_songs_list = np.array([unique_songs, total_songs - unique_songs])
unique_songs_list_labels = [" Unique Songs", "Non Unique Songs"]

fig, ax = plt.subplots(figsize=(12, 6))
ax.pie(unique_songs_list, labels=unique_songs_list_labels, autopct='%1.1f%%', explode=[0.05, 0.05], startangle=180,
       shadow=True)
plt.title("Unique Songs Percentage")
# plt.show()

# ***** Plotly Code *****

p2 = go.Figure(data=go.Pie(values=unique_songs_list, labels=unique_songs_list_labels, textinfo='label+percent',
                           insidetextorientation='radial', pull=0.2, rotation=90))
# p2.show()

# ***** Plotly Code *****


top_10_songs_time_df = stream_df.groupby(["trackName"])[
    ["Listening Time (Hours)", "Listening Time (Minutes)", "count"]].sum().sort_values(by="Listening Time (Minutes)",
                                                                                       ascending=False)
top_10_songs_count_df = stream_df.groupby(["trackName"])[
    ["Listening Time (Hours)", "Listening Time (Minutes)", "count"]].sum().sort_values(by="count", ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 5))

ax1.bar(top_10_songs_time_df.head(10).index, top_10_songs_time_df["Listening Time (Hours)"].head(10), color="olive")
ax1.set(title="My Top 10 Favourite Songs", xlabel="TrackName", ylabel="No. of Hours Songs Played")
ax1.tick_params(labelrotation=90)
ax1.axhline(top_10_songs_time_df["Listening Time (Hours)"][:100].mean(), linestyle="--", color="r")

# ***** Plotly Code *****

b3 = go.Figure(
    data=go.Bar(x=top_10_songs_time_df.head(10).index, y=top_10_songs_time_df["Listening Time (Hours)"].head(10),
                hoverinfo="x+text",
                hovertext=top_10_songs_time_df["Listening Time (Hours)"].head(10), marker_color="cyan"))
b3.update_layout(xaxis_tickangle=-75)
# b3.show()

# ***** Plotly Code *****


ax2.bar(top_10_songs_count_df.head(10).index, top_10_songs_count_df["count"].head(10), color="gray")
ax2.set(title="My Top 10 Favourite Songs", xlabel="TrackName", ylabel="No. of Times Songs Played")
ax2.tick_params(labelrotation=90)
ax2.axhline(top_10_songs_count_df["count"][:100].mean(), linestyle="--", color="r")
# plt.show()

# ***** Plotly Code *****

b4 = go.Figure(
    data=go.Bar(x=top_10_songs_count_df.head(10).index, y=top_10_songs_count_df["count"].head(10), hoverinfo="x+text",
                hovertext=top_10_songs_count_df["count"].head(10), marker_color="cyan"))
b4.update_layout( xaxis_tickangle=-75)
# b4.show()

# ***** Plotly Code *****

fig, ax = plt.subplots(figsize=(12, 6))
ax.pie(stream_df["day-name"].value_counts(), labels=stream_df["day-name"].value_counts().index, autopct='%1.1f%%',
       startangle=180, shadow=True)
ax.set(title="Day wise % of Spotify Streaming")
# plt.show()

# ***** Plotly Code *****

p3 = go.Figure(
    data=go.Pie(values=stream_df["day-name"].value_counts(), labels=stream_df["day-name"].value_counts().index,
                textinfo='label+percent',
                insidetextorientation='radial', pull=0.2, rotation=90))
# p3.show()

# ***** Plotly Code *****


fig, ax = plt.subplots(figsize=(12, 8))
ax.set(title="Average Distribution of Streaming Over Day Hours", xlabel="Hours (in 24 hour format)",
       ylabel="Songs Played")
sns.histplot(stream_df["hours"], bins=24, kde=True, color="darkgreen")
# plt.show()

# ***** Plotly Code *****

h1 = go.Figure(data=[go.Histogram(x=stream_df['hours'], nbinsx=24, texttemplate="%{y}")])
h1.update_layout(
    xaxis_title_text="Hours (in 24 Hour Format)",
    yaxis_title_text="Songs Played"
)
# h1.show()

# ***** Plotly Code *****

fig, ax = plt.subplots(figsize=(12, 6))

ax = sns.countplot(y=stream_df["month"], ax=ax)
ax.set(title="Average Spotify Usage over Years", xlabel="Songs Played in Counts", ylabel="Months (1-12)")
# plt.show()


# ***** Plotly Code *****

# print(list(Counter(stream_df['month']).values()))
# print(list(Counter(stream_df['month']).keys()))
b5 = go.Figure(
    data=go.Bar(x=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                y=list(Counter(stream_df['month']).values()), hoverinfo="x+y", marker_color="cyan"))
b5.update_layout(
    xaxis_tickangle=-75,
    xaxis_title_text="Months",
    yaxis_title_text="Songs Played Count"
)
# b5.show()

# ***** Plotly Code *****


time_spent_hours = stream_df["Listening Time (Hours)"].sum()  # Summation of all

date_df = stream_df["Play-Time"]  # Making a new dataset of time only

time_difference = (date_df.iloc[list(stream_df.shape)[0]-1] - date_df.iloc[0]) / np.timedelta64(1,"D")  # Calulating total possible days in days

time_difference_hours = time_difference * 24  # Converting that in hours by multiplying with 24

time_spent_percentage = time_spent_hours / time_difference_hours * 100

hours_spent_list = np.array([time_spent_hours, time_difference_hours - time_spent_hours])
hours_spent_list_labels = [" Actual Hours Spent", "Possible Hours"]

fig, ax = plt.subplots(figsize=(12, 6))
ax.pie(hours_spent_list, labels=hours_spent_list_labels, autopct='%1.1f%%', explode=[0.2, 0.2], startangle=180,
       shadow=True)
plt.title("Hours Spent Percentage")
# plt.show()

total_songs = stream_df["trackName"].count()  # Total Songs played

average_songs_played_daily = (total_songs / time_difference).round()

stream_df["date"] = stream_df["Play-Time"].dt.date  # Creating a new column with date

most_songs = stream_df.groupby(["date"])[["count"]].sum().sort_values(by="count", ascending=False)

fig, ax = plt.subplots(figsize=(15, 8))
ax.scatter(most_songs.index, most_songs["count"]);
ax.set(title="Maximum number of songs played in a day", xlabel="Date", ylabel="Count");
ax.axhline(most_songs["count"].mean(), linestyle="-", color="r");
# plt.show()

fav_artist = stream_df.groupby(["artistName"])["count"].count()
fav_artist.sort_values(ascending=False).head(100)

fig, ax = plt.subplots(figsize=(20, 15))
wordcloud = WordCloud(width=1000, height=600, max_words=400, relative_scaling=1,
                      normalize_plurals=False).generate_from_frequencies(fav_artist)
ax.imshow(wordcloud, interpolation='bilinear')
plt.axis(False)
# plt.show()

fav_songs = stream_df.groupby(["trackName"])["count"].count()

fig, ax = plt.subplots(figsize=(20, 15))
wordcloud = WordCloud(width=1000, height=600, max_words=400, relative_scaling=1,
                      normalize_plurals=False).generate_from_frequencies(fav_songs)
ax.imshow(wordcloud, interpolation='bilinear')
plt.axis(False)
# plt.show()

active_usage = stream_df.groupby(['hours', 'day-name'])['artistName'].size().reset_index()
active_usage_pivot = active_usage.pivot("hours", 'day-name', 'artistName')

days = ["Monday", 'Tuesday', "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

fig, ax = plt.subplots(figsize=(15, 12))
ax = sns.heatmap(active_usage_pivot[days].fillna(0), robust=True, cmap="Blues", ax=ax)
ax.set(title="Heat Map of Spotify Usage", xlabel="Days of the Week", ylabel="Time(in 24 hrs format)")
# plt.show()

# ***** Plotly Code *****

# print(active_usage_pivot[days].fillna(0))
hm = go.Figure(data=go.Heatmap(
    z=active_usage_pivot[days].fillna(0),
    x=days,
    y=[str(i) for i in range(0, 24)],
    colorscale="Reds"
))
hm.update_layout(
    xaxis_title_text="Day",
    yaxis_title_text="Time (24 Hour Format)"
)
# hm.show()

# ***** Plotly Code *****

fig, ax = plt.subplots(figsize=(12, 8))
ax = sns.countplot(x=stream_df["day-name"], ax=ax)
plt.xticks(rotation=75)
ax.set(title="Average Spotify Usage over Week", xlabel="Days of the Week", ylabel="Counts of Songs Played")
# plt.show()

extra_df = stream_df.copy()
extra_df['is_weekend'] = extra_df["day-name"].isin(['Sunday', 'Saturday'])
weekday_vs_weekend = extra_df.groupby(['is_weekend'])[['count']].sum()

weekday_vs_weekend["Percentage"] = weekday_vs_weekend["count"] / weekday_vs_weekend["count"].sum() * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))
ax1 = sns.barplot(x=["False", "True"], y="count", data=weekday_vs_weekend, ax=ax1)
ax1.set(title="Weekday vs Weekend", xlabel="Is it Weekend", ylabel="Counts of Songs Played");

ax2 = sns.barplot(x=["False", "True"], y="Percentage", data=weekday_vs_weekend, color="Olive", ax=ax2)
ax2.set(title="Weekday vs Weekend (Percentage)", xlabel="Is it Weekend", ylabel="Percentage of Songs Played");
# plt.show()

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Pie Chart 1
# p1 = px.pie(values=unique_artists_list, names=unique_artists_list_labels, title="Unique Artist Pecentage")
p1 = go.Figure(data=go.Pie(values=unique_artists_list, labels=unique_artists_list_labels, textinfo='label+percent',
                           insidetextorientation='radial', pull=0.2, rotation=90))

# Pie Chart 2
p2 = go.Figure(data=go.Pie(values=unique_songs_list, labels=unique_songs_list_labels, textinfo='label+percent',
                           insidetextorientation='radial', pull=0.2, rotation=90))

# Pie Chart 3
p3 = go.Figure(
    data=go.Pie(values=stream_df["day-name"].value_counts(), labels=stream_df["day-name"].value_counts().index,
                textinfo='label+percent',
                insidetextorientation='radial', pull=0.2, rotation=90))


# p3.show()
# tot = sum(list(stream_df["day-name"].value_counts()))
# perc = list(stream_df["day-name"].value_counts())
# perc=np.divide(perc,tot)
# print(perc)


# Polar ScatterPlot 1
ps = go.Figure(
    go.Scatterpolar(
        theta=stream_df["day-name"].value_counts().index,
        mode='markers',
        r=stream_df["day-name"].value_counts(),
        fill='toself',
    )
)
ps.update_layout(
    title="",
    polar={'radialaxis': {'visible': False}},
    autosize=True
)
# ps.show()


# Bar Chart 1
b1 = go.Figure(
    data=go.Bar(x=top_10_artist_time_df.head(10).index, y=top_10_artist_time_df["Listening Time (Hours)"].head(10),
                hoverinfo="x+text", hovertext=top_10_artist_time_df["Listening Time (Hours)"].head(10),
                marker_color="cyan"))
b1.update_layout(xaxis_tickangle=-75)

# Bar Chart 2
b2 = go.Figure(
    data=go.Bar(x=top_10_artist_count_df.head(10).index, y=top_10_artist_count_df["count"].head(10), hoverinfo="x+text",
                hovertext=top_10_artist_count_df["count"].head(10), marker_color="cyan"))
b2.update_layout(xaxis_tickangle=-75)

# Bar Chart 3
b3 = go.Figure(
    data=go.Bar(x=top_10_songs_time_df.head(10).index, y=top_10_songs_time_df["Listening Time (Hours)"].head(10),
                hoverinfo="x+text",
                hovertext=top_10_songs_time_df["Listening Time (Hours)"].head(10), marker_color="cyan"))
b3.update_layout(xaxis_tickangle=-75)

# Bar Chart 4
b4 = go.Figure(
    data=go.Bar(x=top_10_songs_count_df.head(10).index, y=top_10_songs_count_df["count"].head(10), hoverinfo="x+text",
                hovertext=top_10_songs_count_df["count"].head(10), marker_color="cyan"))
b4.update_layout(xaxis_tickangle=-75)

# Bar Chart 5
# print(list(Counter(stream_df['month']).values()))
# print(list(Counter(stream_df['month']).keys()))
b5 = go.Figure(
    data=go.Bar(x=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                y=list(Counter(stream_df['month']).values()), hoverinfo="x+y", marker_color="cyan"))
b5.update_layout(
    xaxis_tickangle=-75,
    xaxis_title_text="Months",
    yaxis_title_text="Songs Played Count"
)

# Heat Map 1
hm = go.Figure(data=go.Heatmap(
    z=active_usage_pivot[days].fillna(0),
    x=days,
    y=[str(i) for i in range(0, 24)],
    colorscale="Reds"
))
hm.update_layout(
    xaxis_title_text="Day",
    yaxis_title_text="Time (24 Hour Format)"
)

# WordCloud 1
wca = WordCloud(background_color="black", width=1000, height=600, max_words=400, relative_scaling=1,
                normalize_plurals=False).generate_from_frequencies(fav_artist).to_image()
ax.imshow(wca, interpolation='bilinear')
plt.axis(False)

# WordCloud 2
wct = WordCloud(background_color="black", width=1000, height=600, max_words=400, relative_scaling=1,
                normalize_plurals=False).generate_from_frequencies(fav_songs).to_image()
ax.imshow(wct, interpolation='bilinear')
plt.axis(False)

API_KEY = key.lastfm
USER_AGENT=key.user

#top artists and songs
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

if pd.read_csv("top_songs.csv").empty:
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

layoutSongs = dict(geo = dict(projection = {'type':'robinson'}))

y = go.Figure(data = [dataSongs], layout = layoutSongs)

# Bubble plot for top Genres
def getTopGenre():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
        scope="user-follow-read user-read-recently-played user-read-playback-position user-top-read user-read-email user-read-private user-library-read",
        redirect_uri="http://example.com",
        client_id=key.spotipy_id,
        client_secret=key.spotipy_secret,
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
#plt.savefig('..assets/genre.png')


#############################################################################################################
###################################### SENTIMENT ANALYSIS ###################################################
#############################################################################################################
def getAccessToken():
    auth_url = 'https://accounts.spotify.com/api/token'
    clientID = key.spotipy_id
    clientSecret = key.spotipy_secret

    data = {
        'grant_type': 'client_credentials',
        'client_id': clientID,
        'client_secret': clientSecret,
    }

    auth_response = requests.post(auth_url, data = data)
    access_token = auth_response.json().get('access_token')
    return access_token

def getAudioID(name):
  endpoint = "https://api.spotify.com/v1/search?q=track:" + name + "&type=track"

  headers = {
        'Authorization': 'Bearer {}'.format(getAccessToken())
    }

  response = requests.get(endpoint, headers = headers)
  if len(response.json().get('tracks').get('items')) != 0 and response.json() is not None:
    return response.json().get('tracks').get('items')[0].get('id')
  else:
    return 'noIDfound'
  # print(response.json())

def getAudioFeatures(id):
  endpoint = "https://api.spotify.com/v1/audio-features/" + id

  headers = {
        'Authorization': 'Bearer {}'.format(getAccessToken())
    }

  response = requests.get(endpoint, headers = headers)

  return response.json()

loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
result = loaded_model

#top_10_songs_count_df = top_10_songs_count_df.dropna(inplace = True)

top10songs = top_10_songs_count_df.index.tolist()
top10songs = top10songs[:10]

features = []
for i in top10songs:
    song = getAudioFeatures(getAudioID(i))
    features.append(song)  

acousticness = []
danceability = []
liveness = []
loudness = []
speechiness = []
valence = []

for i in features:
  acousticness.append(i.get('acousticness'))
  danceability.append(i.get('danceability'))
  liveness.append(i.get('liveness'))
  loudness.append(i.get('loudness'))
  speechiness.append(i.get('speechiness'))
  valence.append(i.get('valence'))

mood10 = pd.DataFrame(list(zip(acousticness, danceability, liveness, loudness, speechiness, valence)), columns=['Acousticness', 'Danceability', 'Liveness', 'Loudness', 'Speechiness', 'Valence',])

arrl = np.array(loudness)
min_max_scaler = preprocessing.MinMaxScaler()
loudness_scaled = min_max_scaler.fit_transform(arrl.reshape(-1,1))
mood10['Loudness'] = pd.DataFrame(loudness_scaled)

mood10 = mood10.dropna()
print(mood10)
print(type(mood10))

y_pred = result.predict(mood10)
definitionsSong = ['Happy','Romantic','Sad']
reversefactorSong = dict(zip(range(4),definitionsSong))
predSong = np.vectorize(reversefactorSong.get)(y_pred)

ct = Counter(predSong)
mood = ct.most_common(1)[0][0]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "auto",
    "padding": "2rem 1rem",
    "background-color": "#191414",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Spotilyser", className="display-4"),
        html.Hr(),
        html.P(
            "", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Unique Artists/Tracks", href="/page-1", active="exact"),
                dbc.NavLink("Top 10 Artists", href="/page-2", active="exact"),
                dbc.NavLink("Top 10 Tracks", href="/page-3", active="exact"),
                dbc.NavLink("Weekly Streaming", href="/page-4", active="exact"),
                dbc.NavLink("Daily Streaming ", href="/page-5", active="exact"),
                dbc.NavLink("Monthly Streaming", href="/page-6", active="exact"),
                dbc.NavLink("Active Hours", href="/page-7", active="exact"),
                dbc.NavLink("Favourite Artists", href="/page-8", active="exact"),
                dbc.NavLink("Favourite Tracks", href="/page-9", active="exact"),
                dbc.NavLink("Favourite Genres", href="/page-10", active="exact"),
                dbc.NavLink("Countrywise Top Artist", href="/page-11", active="exact"),
                dbc.NavLink("Countrywise Top Track", href="/page-12", active="exact"),
                dbc.NavLink("Overall Mood of Top 10 Songs", href="/page-13", active="exact")  
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(style={
            "text-align": "left", 'float':"left",'margin-top':'100px'},children=[
            html.Img(src="../assets/logo.png", width="100", height="100", style={'float':"left",'margin-right':"50px"}),
            html.H1("Welcome to Spotilyser : An Analysis of Spotify Usage"),
            html.H2("All your Stats at one glance!"),
            html.P("Spotilyser is the ultimate amalgamation of visual analytics and your music taste. These two things on the plate create real magic. This wrap includes all the songs users have been listening to, in the past year, the genre they were the most into and their most favourite artists along with minutes streamed and other data. It included the top musicians that users have listened to. Every year, millions of data is generated by Spotify users, using this dashboard many users could gain visual insights for their listening habits. The reason people love this form of analysis is its too personal and can be generated within few seconds.",style={'margin-left':"150px",'width':'60%','font-size':'20px'})]) 
    elif pathname == "/page-1":
        return html.Div(className="charts",children=[dcc.Dropdown(
                    id='unique-dd',
                    options=[
                        {'label': 'Percentage Of Unique Artists Listened To', 'value': 'artist'},
                        {'label': 'Percentage Of Unique Tracks Listened To', 'value': 'track'}
                    ],
                    value='artist',
                    style={
                "width": "50%",
                "margin": "auto"
                }
                    ),

                    dcc.Graph(id='unique-plot')
                    ])
    elif pathname == "/page-2":
        return html.Div(className="charts",children=[
        dcc.Dropdown(
            id='top-artist-dd',
            options=[
                {'label': 'Top 10 Artists Based On Listening Time', 'value': 'listen-time'},
                {'label': 'Top 10 Artists Based On Listening Count', 'value': 'listen-count'}
            ],
            value='listen-time',
            style={
                "width": "50%",
                "margin": "auto"
                }
        ),
        dcc.Graph(id='top-artist-plot')
    ])
    elif pathname == "/page-3":
        return html.Div(className="charts",children=[
        dcc.Dropdown(
            id='top-track-dd',
            options=[
                {'label': 'Top 10 Tracks Based On Listening Time', 'value': 'listen-time'},
                {'label': 'Top 10 Tracks Based On Listening Count', 'value': 'listen-count'}
            ],
            value='listen-time',
            style={
                "width": "50%",
                "margin": "auto"
                }
        ),
        dcc.Graph(id='top-track-plot')
    ])
    elif pathname == "/page-4":
        return html.Div(className="charts",children=[

        # html.H1("Daywise Percentage Of Listening Time"),
        # dcc.Graph(
        #     id='daywise-time',
        #     figure=p3),
        html.H1("Daywise Distribution Of Listening Time"),
        dcc.Graph(
            id='daywise-time',
            figure=ps

        )
    ])
    elif pathname == "/page-5":
        return html.Div(className="charts",children=[
        html.H1("Daytime Streaming Hours"),
        dcc.Graph(
            id='hourwise-time',
            figure=h1
        )
    ])
    elif pathname == "/page-6":
        return html.Div(className="charts",children=[
        html.H1("Distribution Of Spotify Streaming Over The Year"),
        dcc.Graph(
            id='year-dist',
            figure=b5
        )
    ])
    elif pathname == "/page-7":
        return html.Div(className="charts",children=[
        html.H1("HeatMap Of Listening Time"),
        dcc.Graph(
            id='listen-heatmap',
            figure=hm
        )
    ])
    elif pathname == "/page-8":
        return html.Div(className="charts",children=[
        html.H1("WordCloud Of Favourite Artists"),
        html.Img(id='img-wc-artist')
    ])
    elif pathname == "/page-9":
        return html.Div(className="charts",children=[
        html.H1("WordCloud Of Favourite Tracks"),
        html.Img(id='img-wc-tracks')
    ])
    elif pathname == "/page-10":
        return html.Div(className="charts",children=[
        html.H1("Bubble Plot Of Top Genres"),
        html.Img(src='../assets/genre.png',style={'width':'auto','height':'auto'})
        ])
    elif pathname == "/page-11":
        return html.Div(className="charts",children=[
        html.H1("Chloropleth Map of Countrywise Top Artist"),
        dcc.Graph(figure = x)
        ])
    elif pathname == "/page-12":
        return html.Div(className="charts",children=[
        html.H1("Chloropleth Map of Countrywise Top Track"),
        dcc.Graph(figure = y)
        ])
    elif pathname == "/page-13":
        #picsrc = ''
        if mood == "Happy":
            picsrc = '../assets/happy.png'
        elif mood == "Sad":
            picsrc = '../assets/sad.png'
        elif mood == "Romantic":
            picsrc = '../assets/romantic.jpg'
        return html.Div(className="charts", children=[
        html.H1("Predicted Mood for Top 10 Songs"),
        html.H2(mood),
        html.Img(src=picsrc,style={'width':'350px','height':'auto'})
        ])
    
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(Output('img-wc-artist', 'src'), [Input('img-wc-artist', 'id')])
def make_image(b):
    img = BytesIO()
    wca.save(img, format="PNG")
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


@app.callback(Output('img-wc-tracks', 'src'), [Input('img-wc-tracks', 'id')])
def make_image(b):
    img = BytesIO()
    wct.save(img, format="PNG")
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

@app.callback(Output(component_id='top-artist-plot', component_property='figure'),
              [Input(component_id='top-artist-dd', component_property='value')])
def top_artist(top_artist_dd_value):
    # print(top_artist_dd_value)
    if top_artist_dd_value == 'listen-time':
        b1 = go.Figure(
            data=go.Bar(x=top_10_artist_time_df.head(10).index,
                        y=top_10_artist_time_df["Listening Time (Hours)"].head(10),
                        hoverinfo="x+text", hovertext=top_10_artist_time_df["Listening Time (Hours)"].head(10),
                        marker_color="cyan"))
        b1.update_layout(xaxis_tickangle=-75)
        return b1
    elif top_artist_dd_value == 'listen-count':
        b2 = go.Figure(
            data=go.Bar(x=top_10_artist_count_df.head(10).index, y=top_10_artist_count_df["count"].head(10),
                        hoverinfo="x+text",
                        hovertext=top_10_artist_count_df["count"].head(10), marker_color="cyan"))
        b2.update_layout(xaxis_tickangle=-75)
        return b2


@app.callback(Output(component_id='top-track-plot', component_property='figure'),
              [Input(component_id='top-track-dd', component_property='value')])
def top_track(top_track_dd_value):
    # print(top_track_dd_value)
    if top_track_dd_value == 'listen-time':
        b3 = go.Figure(
            data=go.Bar(x=top_10_songs_time_df.head(10).index,
                        y=top_10_songs_time_df["Listening Time (Hours)"].head(10),
                        hoverinfo="x+text",
                        hovertext=top_10_songs_time_df["Listening Time (Hours)"].head(10), marker_color="cyan"))
        b3.update_layout(xaxis_tickangle=-75)
        return b3
    elif top_track_dd_value == 'listen-count':
        b4 = go.Figure(
            data=go.Bar(x=top_10_songs_count_df.head(10).index, y=top_10_songs_count_df["count"].head(10),
                        hoverinfo="x+text",
                        hovertext=top_10_songs_count_df["count"].head(10), marker_color="cyan"))
        b4.update_layout(xaxis_tickangle=-75)
        return b4


@app.callback(Output(component_id='unique-plot', component_property='figure'),
              [Input(component_id='unique-dd', component_property='value')])
def unique(unique_val):
    if unique_val == 'artist':
        p1 = go.Figure(
            data=go.Pie(values=unique_artists_list, labels=unique_artists_list_labels, textinfo='label+percent',
                        insidetextorientation='radial', pull=0.2, rotation=90))
        return p1
    elif unique_val == 'track':
        p2 = go.Figure(data=go.Pie(values=unique_songs_list, labels=unique_songs_list_labels, textinfo='label+percent',
                                   insidetextorientation='radial', pull=0.2, rotation=90))
        return p2


if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:8888/')
    app.run_server(port=8888)