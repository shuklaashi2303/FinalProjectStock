# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go

external_scripts = ['/assets/style.css']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def getFig(symble='MMM'):
    # 1. get data from database based on symble
    # 2. make it as a datafrome
    # 3. modify the column name as the go Figure
    df = pd.read_csv(symble+'.csv')
    fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    return fig

# READ List
df = pd.read_csv('constituents.csv')
droptown_items = []
for index, row in df.iterrows():
   droptown_items.append({'label': row['Name'], 'value': row['Symbol']})

# GENERATE HTML
app.layout = html.Div(children=[
        html.H1(children='This interactive dashboad helps with Stock Price Prediction. This dashboard has been created using SP500 historical data obtained from Yahoo Finance (https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC'),
        dcc.Dropdown(
            id='symbol-input',
            options=droptown_items,
            value='MTL'
        ),
        dcc.Graph(id='cs-graphic'),

        html.Div(id='my-output')
    ])

# Output(component_id='my-output', component_property='children'),
@app.callback(
    Output('cs-graphic', 'figure'),
    [Input(component_id='symbol-input', component_property='value')]
)
def update_output_div(input_value):
    # logic to change the chart
    # GENERATE HTML
    return getFig(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
