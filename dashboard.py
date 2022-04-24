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

df1 = pd.read_json("C:/Users/praji/Downloads/my_spotify_data/MyData/StreamingHistory0.json", encoding='utf-8')
df2 = pd.read_json("C:/Users/praji/Downloads/my_spotify_data/MyData/StreamingHistory1.json", encoding='utf-8')
stream_df = pd.concat([df1, df2], ignore_index=True)
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
ax.set(title="My Top 10 Favourite Artist (based on Hours)", xlabel="Artists", ylabel="No. of Hours Songs Played")
plt.xticks(rotation=75)
# plt.show()

# ***** Plotly Code *****

b1 = go.Figure(
    data=go.Bar(x=top_10_artist_time_df.head(10).index, y=top_10_artist_time_df["Listening Time (Hours)"].head(10),
                hoverinfo="x+text", hovertext=top_10_artist_time_df["Listening Time (Hours)"].head(10),
                marker_color="cyan"))
b1.update_layout(title_text="My Top 10 Favourite Artist (based on Hours)", xaxis_tickangle=-75)
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
b2.update_layout(title_text="My Top 10 Favourite Artist (based on Listen Count)", xaxis_tickangle=-75)
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
b3.update_layout(title_text="My Top 10 Favourite Artist (based on Hours Listened)", xaxis_tickangle=-75)
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
b4.update_layout(title_text="My Top 10 Favourite Artist (based on Listen Count)", xaxis_tickangle=-75)
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
    title_text="Average Spotify Usage Over The Year",
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
    title_text="HeatMap Of Spotify Usage Over the Week",
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

app = Dash(__name__)

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
    polar={'radialaxis': {'visible': False}}
)
# ps.show()

# Bar Chart 1
b1 = go.Figure(
    data=go.Bar(x=top_10_artist_time_df.head(10).index, y=top_10_artist_time_df["Listening Time (Hours)"].head(10),
                hoverinfo="x+text", hovertext=top_10_artist_time_df["Listening Time (Hours)"].head(10),
                marker_color="cyan"))
b1.update_layout(title_text="My Top 10 Favourite Artist (based on Hours)", xaxis_tickangle=-75)

# Bar Chart 2
b2 = go.Figure(
    data=go.Bar(x=top_10_artist_count_df.head(10).index, y=top_10_artist_count_df["count"].head(10), hoverinfo="x+text",
                hovertext=top_10_artist_count_df["count"].head(10), marker_color="cyan"))
b2.update_layout(title_text="My Top 10 Favourite Artist (based on Listen Count)", xaxis_tickangle=-75)

# Bar Chart 3
b3 = go.Figure(
    data=go.Bar(x=top_10_songs_time_df.head(10).index, y=top_10_songs_time_df["Listening Time (Hours)"].head(10),
                hoverinfo="x+text",
                hovertext=top_10_songs_time_df["Listening Time (Hours)"].head(10), marker_color="cyan"))
b3.update_layout(title_text="My Top 10 Favourite Artist (based on Hours Listened)", xaxis_tickangle=-75)

# Bar Chart 4
b4 = go.Figure(
    data=go.Bar(x=top_10_songs_count_df.head(10).index, y=top_10_songs_count_df["count"].head(10), hoverinfo="x+text",
                hovertext=top_10_songs_count_df["count"].head(10), marker_color="cyan"))
b4.update_layout(title_text="My Top 10 Favourite Artist (based on Listen Count)", xaxis_tickangle=-75)

# Bar Chart 5
# print(list(Counter(stream_df['month']).values()))
# print(list(Counter(stream_df['month']).keys()))
b5 = go.Figure(
    data=go.Bar(x=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                y=list(Counter(stream_df['month']).values()), hoverinfo="x+y", marker_color="cyan"))
b5.update_layout(
    title_text="Average Spotify Usage Over The Year",
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
    title_text="HeatMap Of Spotify Usage Over the Week",
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

# HTML Layout

app.layout = html.Div(children=[
    # html.Div(children=[
    #     html.H1("Percentage Of Unique Artists Listened To"),
    #     dcc.Graph(
    #         id='unique_artist',
    #         figure=p1
    #     )
    # ]),
    html.Div(children=[
        dcc.Dropdown(
            id='unique-dd',
            options=[
                {'label': 'Percentage Of Unique Artists Listened To', 'value': 'artist'},
                {'label': 'Percentage Of Unique Tracks Listened To', 'value': 'track'}
            ],
            value='artist'
        ),
        dcc.Graph(id='unique-plot')
    ]),
    html.Div(children=[
        dcc.Dropdown(
            id='top-artist-dd',
            options=[
                {'label': 'Top 10 Artists Based On Listening Time', 'value': 'listen-time'},
                {'label': 'Top 10 Artists Based On Listening Count', 'value': 'listen-count'}
            ],
            value='listen-time'
        ),
        dcc.Graph(id='top-artist-plot')
    ]),
    html.Div(children=[
        dcc.Dropdown(
            id='top-track-dd',
            options=[
                {'label': 'Top 10 Tracks Based On Listening Time', 'value': 'listen-time'},
                {'label': 'Top 10 Tracks Based On Listening Count', 'value': 'listen-count'}
            ],
            value='listen-time'
        ),
        dcc.Graph(id='top-track-plot')
    ]),
    # html.Div(children=[
    #     dcc.Dropdown(
    #         id='wordcloud',
    #         options=[
    #             {'label': 'WordCloud of Top 10 Artists', 'value': 'artist'},
    #             {'label': 'WordCloud of Top 10 Tracks', 'value': 'track'}
    #         ],
    #         value='artist'
    #     ),
    #     dcc.Graph(id='wordcloud-plot')
    # ]),
    # html.Div(children=[
    #     html.H1("Top 10 Artists (Based On Listening Time)"),
    #     dcc.Graph(
    #         id='top-artist-hours',
    #         figure=b1
    #     )
    # ]),
    # html.Div(children=[
    #     html.H1("Top 10 Artists (Based On Listen Counts)"),
    #     dcc.Graph(
    #         id='top-artist-counts',
    #         figure=b2
    #     )
    # ]),
    # html.Div(children=[
    #     html.H1("Percentage Of Unique Tracks Listened To"),
    #     dcc.Graph(
    #         id='unique_track',
    #         figure=p2
    #     )
    # ]),
    # html.Div(children=[
    #     html.H1("Top 10 Tracks (Based On Listening Time)"),
    #     dcc.Graph(
    #         id='top-tracks-hours',
    #         figure=b3
    #     )
    # ]),
    # html.Div(children=[
    #     html.H1("Top 10 Tracks (Based On Listen Count)"),
    #     dcc.Graph(
    #         id='top-track-count',
    #         figure=b4
    #     )
    # ]),
    html.Div(children=[
        html.H1("Daywise Distribution Of Listening Time"),
        dcc.Graph(
            id='daywise-time',
            figure=ps
        )
    ]),
    html.Div(children=[
        html.H1("Daytime Streaming Hours)"),
        dcc.Graph(
            id='hourwise-time',
            figure=h1
        )
    ]),
    html.Div(children=[
        html.H1("Distribution Of Spotify Streaming Over The Year"),
        dcc.Graph(
            id='year-dist',
            figure=b5
        )
    ]),
    html.Div(children=[
        html.H1("HeatMap Of Listening Time"),
        dcc.Graph(
            id='listen-heatmap',
            figure=hm
        )
    ]),
    html.Div(children=[
        html.H1("WordCloud Of Favourite Artists"),
        html.Img(id='img-wc-artist')
    ]),
    html.Div(children=[
        html.H1("WordCloud Of Favourite Tracks"),
        html.Img(id='img-wc-tracks')
    ])
])


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
        b1.update_layout(title_text="My Top 10 Favourite Artist (based on Hours)", xaxis_tickangle=-75)
        return b1
    elif top_artist_dd_value == 'listen-count':
        b2 = go.Figure(
            data=go.Bar(x=top_10_artist_count_df.head(10).index, y=top_10_artist_count_df["count"].head(10),
                        hoverinfo="x+text",
                        hovertext=top_10_artist_count_df["count"].head(10), marker_color="cyan"))
        b2.update_layout(title_text="My Top 10 Favourite Artist (based on Listen Count)", xaxis_tickangle=-75)
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
        b3.update_layout(title_text="My Top 10 Favourite Tracks (based on Hours Listened)", xaxis_tickangle=-75)
        return b3
    elif top_track_dd_value == 'listen-count':
        b4 = go.Figure(
            data=go.Bar(x=top_10_songs_count_df.head(10).index, y=top_10_songs_count_df["count"].head(10),
                        hoverinfo="x+text",
                        hovertext=top_10_songs_count_df["count"].head(10), marker_color="cyan"))
        b4.update_layout(title_text="My Top 10 Favourite Tracks (based on Listen Count)", xaxis_tickangle=-75)
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
    app.run_server(debug=True)
