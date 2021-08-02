#from jupyter_dash import JupyterDash
import pandas as pd
import datetime as dt
import yfinance as yf
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate
# Load Data
name_export = pd.read_csv('https://raw.githubusercontent.com/shuklaashi2303/FinalProjectStock/main/Resources/constituents.csv', error_bad_lines= False)
data = name_export.dropna()
symbol_df = data['Symbol']
ticker = [i for i in data['Symbol']]

# Build App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    html.H1("Predict Stock App"),
# Dividing the dashboard in tabs
    dcc.Tabs(id="tabs", children=[
        html.H1("Stocks Prices", 
                style={'textAlign': 'center'}),
        # Adding the first dropdown menu and the subsequent time-series graph
        html.Div([
                  html.Div([dcc.Dropdown(id='Stock Symbols-dropdown', clearable=False,
                  value='ticker', 
                  options=[{'label': i, 'value': i} for i in ticker],
                  multi=True,
                  style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "60%"}),
    dcc.Graph(id='graph')],
    className="container"),
        ])
    ])
])

# Defining the layout of the second tab
dcc.Tab(label='Performance Metrics', children=[
    html.H1("Analysis of Stocks", 
            style={"textAlign": "center"}),
    # Adding a dropdown menu and the subsequent histogram graph
    html.Div([
            html.Div([dcc.Dropdown(id='feature-selected1',
            options=[{'label': i, 'value': i} for i in ticker],
                        value="Type")],
                        className="twelve columns", 
                        style={"display": "block", "margin-left": "auto",
                                        "margin-right": "auto", "width": "60%"}),
                    ], className="row",
                    style={"padding": 50, "width": "60%", 
                           "margin-left": "auto", "margin-right": "auto"}),
                    dcc.Graph(id='graph'),
        ])


@app.callback(Output('graph', 'figure'),
              #Output('Analysis', 'figure'),
              Input('Stock Symbols-dropdown', 'value'))
def update_figure(value):
    start = dt.datetime.today()-dt.timedelta(1825)
    end = dt.datetime.today()
    stock_data = yf.download(value, start, end)[['Date', 'Adj Close']]
    
        
    def update_options(search_value):
        if not search_value:
           raise PreventUpdate
           return [o for o in ticker if search_value in o["label"]]
    fig = px.line(stock_data, x="Date", y="Adj Close")


    fig.update_layout(
      xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
              

    
    
    return {
        'data': [trace],
        'layout': go.Layout(title=f'Metrics considered: {selected_feature1.title()}',
                            colorway=["#EF963B", "#EF533B"], hovermode="closest",
                            xaxis={'title': "Distribution", 
                                   'titlefont': {'color': 'black', 'size': 14},
                                   'tickfont': {'size': 14, 'color': 'black'}},
                            yaxis={'title': "Frequency", 
                                   'titlefont': {'color': 'black', 'size': 14, },
                                   'tickfont': {'color': 'black'}})}

# Run app and display result external in the notebook
if __name__ == '__main__':
    app.run_server(debug=True)