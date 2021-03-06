import dash
import dash_core_components as dcc   
import dash_html_components as html 
from dash_table import DataTable, FormatTemplate
from dash_table.Format import Format, Group
from dash.dependencies import Input, Output, State
import numpy as np
from numpy.core import numeric
import yfinance as yf
import plotly.graph_objects as go 
import pandas as pd
from dash.exceptions import PreventUpdate
import dash_table
import plotly.express as px

name_export = pd.read_csv('https://raw.githubusercontent.com/shuklaashi2303/FinalProjectStock/main/Resources/constituents.csv')
data = name_export.dropna()
symbol_df = data['Symbol']
ticker = [ ]

for i in data['Symbol']:
    ticker.append(i)

def get_stock_price_fig(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(mode="lines", x=df["Date"], y=df["Close"]))
    return fig

def get_dounts(df, label):

    non_main = 1 - df.values[0]
    labels = ["main", label]
    values = [non_main, df.values[0]]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.499)])
    return fig



app = dash.Dash(external_stylesheets=['link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;700&display=swap" rel="stylesheet"'])
money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)
app.title = 'Stock Prediction Dashboard'
app.layout = html.Div([
    
    html.Div([
        html.P("Stock Prediction Dashboard", className="stockp"),
        html.P("Select Stock Symbol", className="start"),
        dcc.Dropdown("dropdown_tickers", options=[
        {"label": i, "value": i} for i in ticker
    ]),
        html.Div([
            html.Button("Company profile", className="companyprofile-btn", id="indicators"),
            html.Button("Stock Price", className="stock-btn", id="stock"),
            
        ], className="Buttons")

    ], className="Navigation"),

    html.Div([
        html.Div([
                html.P(id="ticker"),
                html.Img(id="logo"),
        ], className="header"), 
        html.Div(id="description", className="decription_ticker"),
        html.Div([
            html.Div([], id="graphs-content"),
        ], id="main-content")
    ],className="content"),

], className="container")


@app.callback(
            [Output("description", "children"), Output("logo", "src"), Output("ticker", "children"), Output("indicators", "n_clicks")],
            [Input("dropdown_tickers", "value")]
            )

def update_data(v):
    if v == None:
        raise PreventUpdate
    
    ticker = yf.Ticker(v)
    inf = ticker.info

    df = pd.DataFrame.from_dict(inf, orient="index").T
    df = df[["sector", "lastDividendValue", "fullTimeEmployees", "sharesOutstanding", "priceToBook", "logo_url", "longBusinessSummary", "shortName", "ebitda", "lastDividendDate"]]

    return  df["longBusinessSummary"].values[0], df["logo_url"].values[0], df["shortName"].values[0], 1


@app.callback(
            [Output("graphs-content", "children")],
            [Input("stock", "n_clicks")],
            [State("dropdown_tickers", "value")]
)

def stock_prices(v, v2):
    if v == None:
        raise PreventUpdate
    if v2 == None:
        raise PreventUpdate

    df = yf.download(v2)
    df.reset_index(inplace=True)

    fig = get_stock_price_fig(df)

    return [dcc.Graph(figure=fig)]


@app.callback(
            [Output("main-content", "children"), Output("stock", "n_clicks")],
            [Input("indicators", "n_clicks")],
            [State("dropdown_tickers", "value")]
)

def indicators(v, v2):
    if v == None:
        raise PreventUpdate
    if v2 == None:
        raise PreventUpdate
    ticker = yf.Ticker(v2)


    df_calendar = ticker.calendar.T
    df_info = pd.DataFrame.from_dict(ticker.info, orient="index").T
    df_info.to_csv("test.csv")
    df_info = df_info[["priceToBook", "profitMargins", "bookValue", "shortRatio", "sector", "lastDividendValue", "lastDividendDate", "ebitda", "earningsGrowth"]]
    
    

    df_calendar["Earnings Date"] = pd.to_datetime(df_calendar["Earnings Date"])
    df_calendar["Earnings Date"] = df_calendar["Earnings Date"].dt.date

    tbl = html.Div([
             html.Div([
        html.Div([
            html.H4("Sector"),
            html.P(df_info["sector"]),
        ]),
        html.Div([
            html.H4("Earnings Growth (%)"),
            html.P(df_info["earningsGrowth"])
        ]),
        html.Div([
            html.H4("Profit Margins (%)"),
            html.P(df_info["profitMargins"])
        ]),       
        html.Div([
            html.H4("Last Dividend Value ($)"),
            html.P(df_info["lastDividendValue"])
        ])
        
    ], className="kpi"), 
        html.Div([
            # dcc.Graph(figure=get_dounts(df_info["profitMargins"], "Margin")),
            # dcc.Graph(figure=get_dounts(df_info["shortRatio"], "Ratio"))
        ], className="dounuts")
        ])
       
    
    return [
        html.Div([tbl], id="graphs-content")], None



app.run_server(debug=True, port=8055)