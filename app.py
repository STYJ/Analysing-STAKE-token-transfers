import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd


# Setup app details

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Stake Dashboard 🥩'
time_now = pd.to_datetime("today").strftime("%d/%m/%Y, %H:%M:%S")

app.layout = html.Div([
    html.Div([
        html.H1(
            'Stake Dashboard 🥩',
            style={'marginTop': '2rem', 'marginBottom': '0'},
        ),
        html.P(
            children=f'Last updated on: {time_now}',
            id='update-time',
            style={'display': 'inline-block'}),
        html.Button(
            '🔄',
            id='update-button',
            style={'border': '0', 'padding': '4px', 'fontSize': '16px'}),
    ], className='row'),
    html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
            value='LA',
            className='twelve columns'
        ),
    ], className='row'),

    html.Div(id='display-value'),
], className='container')


@app.callback(Output('display-value', 'children'),
              [Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


@app.callback(Output('update-time', 'children'),
              Input('update-button', 'n_clicks'),
              State('update-time', 'children'))
def refresh_data(n_clicks, old_time):
    i = old_time.find(':')
    offset = 2
    old = pd.to_datetime(old_time[i + offset:], format="%d/%m/%Y, %H:%M:%S")
    now = pd.to_datetime('today')
    if (now - old) > pd.Timedelta(value=10, unit='seconds'):
        return f'Last updated on: {now.strftime("%d/%m/%Y, %H:%M:%S")}'
    else:
        return old_time


if __name__ == '__main__':
    app.run_server(debug=True)
