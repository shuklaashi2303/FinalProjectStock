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
app.layout = html.Div([
    html.H1("Predict Stock App"),
    dcc.Graph(id='graph'),
    html.Label(["Stock Symbols"]),
    dcc.Dropdown(
        id='Stock Symbols-dropdown', clearable=False,
        value='ticker', 
        options=[{'label': i, 'value': i} for i in ticker]
        )
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
    fig = px.line(Stock_Data, x="Date", y="MMM")


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
              

    
    
    return fig

# Run app and display result external in the notebook
app.run_server(mode='external')