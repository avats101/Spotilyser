# import dash
# from dash import html
# from dash import dcc
# from dash.dependencies import Input, Output
# import plotly.graph_objects as go
# import plotly.express as px
#
# app = dash.Dash()
# df = px.data.stocks()
#
# # def stock_prices():
# #     fig = go.Figure([go.Scatter(x=df['date'], y=df['GOOG'], line=dict(color='firebrick', width=4), name='Google')])
# #     fig.update_layout(title='Prices Over Time', xaxis_title='Dates', yaxis_title='Prices')
# #     return fig
#
#
# app.layout = html.Div(id='parent', style={"width": "50%"}, children=[
#     html.H1(id='H1', children='Styling using html components',
#             style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
#     dcc.Dropdown(id='dropdown',
#                  options=[
#                      {'label': 'Google', 'value': "GOOG"},
#                      {'label': 'Apple', 'value': "AAPL"},
#                      {'label': 'Amazon', 'value': "AMZN"},
#                  ],
#                  value='GOOG'
#                  ),
#     dcc.Graph(id='bar_plot')
#     # dcc.Graph(id='line_plot', figure=stock_prices())
# ]
#                       )
#
#
# @app.callback(Output(component_id='bar_plot', component_property='figure'),
#               [Input(component_id='dropdown', component_property='value')])
# def graph_update(dropdown_value):
#     print(dropdown_value)
#     fig = go.Figure([go.Scatter(x=df['date'], y=df[f'{dropdown_value}'], line=dict(color="firebrick", width=4))])
#     fig.update_layout(title='Stock Prices Over Time',
#                       xaxis_title="Dates",
#                       yaxis_title="Prices"
#                       )
#     return fig
#
#
# if __name__ == "__main__":
#     app.run_server(port=80)


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# app = Dash(__name__)
#
# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }
#
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
#
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
#
# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )
#
# app.layout = html.Div(children=[
#     html.H1(
#         children="Hello Dash",
#         style={
#             'textAlign': 'center',
#             'color': colors['text']
#         }
#     ),
#     html.Div(
#         children="Dash: A Web Application framework for your data.",
#         style={
#             'textAlign': 'center',
#             'color': colors['text']
#         }
#     ),
#     dcc.Graph(
#         id="example-graph",
#         figure=fig
#     )
# ])
#
# if __name__ == "__main__":
#     app.run_server(debug=True)
