


# Import necessary libraries 
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from dash import dash_table as dt
#import dash_table as dt
from plotly import __version__
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from pandas_datareader import data as pdr
#import yfinance as yf
import yahoo_fin.stock_info as yf
import pycountry

# Define the path to the Excel file
file_path = 'Yahoo Ticker Symbols.xlsx'

# Read the Excel file into a DataFrame
df_tickers = pd.read_excel(file_path)

ticker_list = np.sort(df_tickers['Ticker'].unique())

def country_to_alpha3(name):
    try:
        country = pycountry.countries.get(name=name)
        return country.alpha_3
    except AttributeError:
        # If the country is not found or does not have an alpha_3 code, return None
        return name

def figure_performance(portfolio):
    
    interval = int(round((len(portfolio))/10, 0))-1
    result = [r*interval for r in range(1, 11)]
    selected_rows = portfolio.iloc[result]
    selected_rows = selected_rows['total']
    
    # Create the Scatter trace
    trace = go.Scatter(
        x=selected_rows.index,
        y=selected_rows,
        mode='lines',
        line=dict(
            color='#02BC77',
            shape='spline'
        ),
        #fill='tozeroy',
    )
    
    # Define the layout
    layout = dict(
        height=80,
        #width=338,
        margin=dict(l=12, r=12, t=0, b=0),
        #padding=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='white',
    )
    
    fig1 = go.Figure(data=trace, layout=layout)
    
    #fig1.show()
    
    return fig1


def figure_sharp_ratio(portfolio, bond_data):
    
    # Calculate daily returns for the bond and the portfolio
    bond_returns = (bond_data.pct_change() + 1).cumprod().to_frame() - 1
    stocks_returns = portfolio['return_perc'].to_frame()
    
    merged_df = bond_returns.merge(stocks_returns, left_index=True, right_index=True, how='inner')
    
    interval = int(round((len(merged_df))/10, 0))-1
    result = [r*interval for r in range(1, 11)]
    selected_rows_merged_df = merged_df.iloc[result]

    
    # Create the Scatter trace
    trace1 = go.Scatter(
        x=selected_rows_merged_df.index,
        y=selected_rows_merged_df['close'],
        mode='lines',
        line=dict(
            color='#02BC77',
            shape='spline'
        ),
        showlegend=False,
        #fill='tozeroy',
    )
    
    # Create the Scatter trace
    trace2 = go.Scatter(
        x=selected_rows_merged_df.index,
        y=selected_rows_merged_df['return_perc'],
        mode='lines',
        line=dict(
            color='#4791FF',
            shape='spline'
        ),
        showlegend=False,
        #fill='tozeroy',
    )
    
    # Define the layout
    layout = dict(
        height=80,
        #width=338,
        margin=dict(l=12, r=12, t=0, b=0),
        #padding=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='white',
    )
    
    fig1 = go.Figure(data=[trace1, trace2], layout=layout)
    
    #fig1.show()
    
    return fig1


def volatility(annual_volatility):
    
    # Create the Scatter trace
    trace = go.Scatter(
        x=annual_volatility.index,
        y=annual_volatility,
        mode='lines',
        line=dict(
            color='#FF2366',
            shape='spline'
        ),
        #fill='tozeroy',
    )
    
    # Define the layout
    layout = dict(
        height=80,
        #width=338,
        margin=dict(l=12, r=12, t=0, b=0),
        #padding=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='white',
    )
    
    fig1 = go.Figure(data=trace, layout=layout)
    
    #fig1.show()
    
    return fig1

def InformationRatio(portfolio, bench_data):
    
    portfolio_returns = portfolio['return_perc'].to_frame()
    bench_data_returns = ((bench_data.pct_change() + 1).cumprod() -1).to_frame()
    
    merged_df = portfolio_returns.merge(bench_data_returns, left_index=True, right_index=True, how='inner')
    merged_df.columns = ['Portfolio', 'Benchmark']
    
    interval = int(round((len(merged_df))/10, 0))-1
    result = [r*interval for r in range(1, 11)]
    selected_rows_merged_df = merged_df.iloc[result]
    
    # Create the Scatter trace
    trace_performance = go.Scatter(
        x=selected_rows_merged_df.index,
        y=selected_rows_merged_df['Portfolio'],
        mode='lines',
        line=dict(
            color='#4791FF',
            shape='spline'
        ),
        showlegend=False,
        #name="Portfolio",
    )
    
    # Create the Scatter trace
    trace_performance_bench = go.Scatter(
        x=selected_rows_merged_df.index,
        y=selected_rows_merged_df['Benchmark'],
        mode='lines',
        line=dict(
            color='#02BC77',
            shape='spline'
        ),
        showlegend=False,
        #name="Benchmark",
    )
    
    # Define the layout
    layout = dict(
        height=80,
        #width=338,
        margin=dict(l=12, r=12, t=0, b=0),
        #padding=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='white',
    )
    
    fig1 = go.Figure(data=[trace_performance, trace_performance_bench], layout=layout)
    
    #fig1.show()
    
    return fig1


def figure_performance_line(portfolio, bench_data):
    
    portfolio_returns = portfolio['return_perc'].to_frame()
    bench_data_returns = ((bench_data.pct_change() + 1).cumprod() -1).to_frame()
    
    merged_df = portfolio_returns.merge(bench_data_returns, left_index=True, right_index=True, how='inner')
    merged_df.columns = ['Portfolio', 'Benchmark']
    # Create the Scatter trace
    trace_performance = go.Scatter(
        x=merged_df.index,
        y=merged_df['Portfolio'],
        mode='lines',
        line=dict(
            color='#4791FF',
            shape='spline'
        ),
        name="Portfolio",
    )
    
    # Create the Scatter trace
    trace_performance_bench = go.Scatter(
        x=merged_df.index,
        y=merged_df['Benchmark'],
        mode='lines',
        line=dict(
            color='#02BC77',
            shape='spline'
        ),
        name="Benchmark",
    )
    
    # Define the layout
    layout_performance = dict(
        height=350,
        #width=100,
        margin=dict(l=20, r=20, t=10, b=20),
        #padding=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            visible=True,
            linecolor='#5E5E5E',
            linewidth=0.5,
            showgrid=False,
            tickfont=dict(
                family='Montserrat',
                color='#5E5E5E',
                size=12,
                #weight='bold'
            )
        ), 
        yaxis=dict(
            visible=True,
            linecolor='#5E5E5E',
            linewidth=0.5,
            showgrid=True,
            gridcolor='#5E5E5E',
            gridwidth=0.5,
            tickfont=dict(
                family='Montserrat',
                color='#5E5E5E',
                size=12,
                #weight='bold'
            )
        ),
        legend=dict(
            orientation='h',
            y=-0.1,
            x=0.8,
            xanchor='center',
            font=dict(
                family='Montserrat',
                size=12,
                color='#5E5E5E',
                #weight= "lighter",
            ),
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return go.Figure(data=[trace_performance, trace_performance_bench], layout=layout_performance)


def figure_bar_sector(portfolio, sectors):
    
    returns = portfolio.drop(portfolio.columns[[-1,-2, -3]], axis=1).resample('Y').last().pct_change()[1:]
    # invert the DataFrame
    inverted_returns = returns.T

    inverted_returns['Sector'] = [sectors.loc[index, 'Sector'] for index, row in inverted_returns.iterrows()]
    sector_returns = inverted_returns.set_index('Sector')
    sector_returns = sector_returns.T
    
    # Define the data list
    data = []

    # Create the Bar traces
    for col in sector_returns.columns[0:]:
        trace = go.Bar(
            x=sector_returns.index,
            y=sector_returns[col],
            name=col,
            marker=dict(
                line=dict(
                    color='rgba(0,0,0,0)',
                    width=0
                )
            ),
        )
        data.append(trace)

    # Define the layout
    layout_performance_sector = dict(
        height=350,
        #width=100,
        barmode='group',
        margin=dict(l=20, r=20, t=10, b=20),
        #padding=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            visible=True,
            linecolor='#5E5E5E',
            linewidth=0.5,
            showgrid=False,
            tickfont=dict(
                family='Montserrat',
                color='#5E5E5E',
                size=12,
                #weight='bold'
            )
        ),
        yaxis=dict(
            visible=True,
            linecolor='#5E5E5E',
            linewidth=0.5,
            showgrid=True,
            gridcolor='#5E5E5E',
            gridwidth=0.5,
            tickfont=dict(
                family='Montserrat',
                color='#5E5E5E',
                size=12,
                #weight='bold'
            ),
            #gridwidth=0.5,
            zerolinecolor = '#5E5E5E',
        ),
        legend=dict(
            orientation='h',
            y=-0.1,
            x=0.5,
            xanchor='center',
            font=dict(
                family='Montserrat',
                size=12,
                color='#5E5E5E',
            ),
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return go.Figure(data=data, layout=layout_performance_sector)

def figure_performance_country(portfolio, tickers_country):
    
    
    portfolio_country = portfolio[tickers_country].sum(axis=1) #.cumprod().to_frame()
    
    interval = int(round((len(portfolio_country))/10, 0))-1
    result = [r*interval for r in range(1, 11)]
    selected_rows_df = portfolio_country.iloc[result]
    
    color = '#02BC77' if selected_rows_df[-1] > selected_rows_df[0] else '#FF2366'

    trace = go.Scatter(
        x=selected_rows_df.index,
        y=selected_rows_df,
        mode='lines',
        line=dict(
            color=color,
            shape='spline'
        )
    )
    
    # Define the layout
    layout = dict(
        height=30,
        width=60,
        margin=dict(l=0, r=0, t=0, b=0),
        #padding=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return go.Figure(data=trace, layout=layout)

def create_child_div(portfolio_df, portfolio, countries):
    
    fig7 = go.Figure(figure_performance_country(portfolio, countries))
    
    countries_list = countries['Country'].unique()
    country_perc = [sum(portfolio_df.loc[portfolio_df['COUNTRY'] == c, 'MARKET VALUE']) / sum(portfolio_df['MARKET VALUE']) for c in countries_list]
    countries_sort = pd.DataFrame(country_perc, countries_list).sort_values(by=[0], ascending=False).index.unique()


    #tickers_country = portfolio_df.loc[portfolio_df['COUNTRY'] == 'USA', 'TICKER']

    #country_name
    #perc_total_country
    #total_country
    #total_return_country
        
    return [dbc.Col(
            [
            html.Div(
                [ 
                dbc.Row(
                    [
                        #html.Img(src=app.get_asset_url('abw.png'))
                        dbc.Col(
                            html.Div(
                                html.Img(src=r'/assets/images/svg/' + c + '.svg', style={'height': '100%', 'width': '100%',  'object-fit': 'cover','border-radius': '15%'}),
                                style={'height': '15px', "margin-left": "10px", 'width': '25px', 'border-radius': '15%', },
                            ),
                            #style={"background-color": "blue"},
                            width=3,
                        ),
                        dbc.Col(
                            html.Label(
                                c,
                                style={
                                    #"textAlign": "left",
                                    "color": 'white',
                                    "padding-left": "0px",
                                    "font-size": "12px",
                                },
                            ),
                            #style={"background-color": "yellow"},
                            width=5,
                        ),
                        dbc.Col(
                            html.Label(
                                str(round(sum(portfolio_df.loc[portfolio_df['COUNTRY'] == c, 'MARKET VALUE']) / sum(portfolio_df['MARKET VALUE']) * 100, 2)) + '%',
                                style={
                                    "textAlign": "left",
                                    "color": 'white',
                                    "font-size": "11px",
                                },
                            ),
                            #style={"background-color": "green"},
                            width=3,
                        ),
                    ],
                    style={'display': 'flex', 'padding-left': '10px' }
                    #width: 1,
                ),
                html.Hr(style={"background-color": "white", 'height': '1px', 'border': 'none', 'opacity': '0.2',}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        html.Label(
                                            '$' + str(round(sum(portfolio_df.loc[portfolio_df['COUNTRY'] == c, 'MARKET VALUE']), 2)),
                                            style={
                                                "font-size": "18px",
                                                #"font-weight": "bold",
                                            },
                                        ),
                                        html.Label(
                                            str(round((sum(portfolio_df.loc[portfolio_df['COUNTRY'] == c, 'MARKET VALUE']) / sum(portfolio_df.loc[portfolio_df['COUNTRY'] == c, 'COST BASIS'])) - 1, 2)) + '%',
                                            style={
                                                "font-size": "10px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "textAlign": "left",
                                        "color": 'white',
                                        "margin": "0px 0 10px 10px",
                                    },
                                ),
                            ],
                            width=4,
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id='country-line-chart',
                                figure=go.Figure(figure_performance_country(portfolio, portfolio_df.loc[portfolio_df['COUNTRY'] == c, 'TICKER'])),
                            ),
                            style={"padding": "0px 0px 0px 60px",},
                            width=8,
                        ),
                    ],
                    #style={"border-top": '0.2px solid white', }
                ),
                ],
                style={
                    "background-color": "#151519",
                    'padding': '10px 0 10px 0',
                    "border-radius": "15px",
                    #'margin': '10px 10px 10px 20px',
                    #'width': 1,
                    #'height': '150px',
                },
            ),
                
            ],
            style={
                #"background-color": "#151519",
                "color": 'white',
                #"color": "white",
                "border-style": "none",
                "border-radius": "15px",
                'font-family':'montserrat',
                'font-weight': "lighter",
                'padding-right': '10px',
                #'margin': '10px 10px 10px 20px',
                #'width': 1,
                #'height': '150px',
            },
            width=2
        ) for c in countries_sort]


#/Users/yannkrautz/Documents/Project/assets/images/svg
#Image.open(r'assets/images/svg/abw.png')

#from PIL import Image                                                                                
#img = Image.open('abw.png')
#img.show() 

external_stylesheets = [dbc.themes.SLATE]

# adding css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# Define the app layout
app.layout = html.Div(children=[
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Row(
                                        [
                                            html.Label(
                                                "Performance",
                                                style={
                                                    "font-size": "12px",
                                                    #"font-weight": "bold",
                                                },
                                            ),
                                            html.Label(
                                                "$138.761,06",
                                                id = 'total-balance-label',
                                                style={
                                                    "font-size": "20px",
                                                    #"font-weight": "bold",
                                                },
                                            ),
                                            
                                        ],
                                        style={
                                            "textAlign": "left",
                                            "color": 'white',
                                            "margin": "15px 0 0px 10px",
                                        },
                                    ),
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                html.Label(
                                    "+7%",
                                    id = 'balance-performace-label',
                                    style={
                                        "textAlign": "left",
                                        "color": 'white',
                                        "font-size": "12px",
                                    },
                                ),
                                style={"padding": "25px 0px 0px 100px"},
                                width=6,
                            ),
                        ],
                    ),
                    dbc.Row(
                        [
                            #html.Img(src=app.get_asset_url('abw.png'))
                            html.Div(
                                dcc.Loading(
                                    id='my-loading-1',
                                    type='circle',
                                    children=dcc.Graph(
                                        id='performance-line-chart',
                                        #figure=go.Figure(data=[trace], layout=layout)
                                    ),
                                ),
                                style={"padding": "0 0 20px 0", 'margin': '0',},
                               # width=12,
                            ),  
                        ],
                        #style={'border-bottom': '0.2 solid white', 'display': 'flex', 'padding-left': '10px'} ,
                        #width: 1,
                    ),
                    ],
                    style={
                        "background-color": "#151519",
                        "color": 'white',
                        #"color": "white",
                        "border-style": "none",
                        "border-radius": "15px",
                        'font-family':'montserrat',
                        'font-weight': "lighter",
                        #'padding': '10px',
                        'margin': '0px 0px 0px 40px',
                        #'width': 1,
                        #'height': '150px',
                    },
                ),
                style={'margin': '20px 0px 20px 0px', 'padding': '0px',},
                width=3
            ),
            dbc.Col(
                html.Div(
                    [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Row(
                                        [
                                            html.Label(
                                                "Sharp Ratio",
                                                style={
                                                    "font-size": "12px",
                                                    #"font-weight": "bold",
                                                },
                                            ),
                                            html.Label(
                                                #"$138.761,06",
                                                id = 'sharp-ratio-label',
                                                style={
                                                    "font-size": "20px",
                                                    #"font-weight": "bold",
                                                },
                                            ),
                                            
                                        ],
                                        style={
                                            "textAlign": "left",
                                            "color": 'white',
                                            "margin": "15px 0 0px 10px",
                                        },
                                    ),
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                html.Label(
                                    #"+7%",
                                    id = 'sharp-ratio-data-label',
                                    style={
                                        "textAlign": "left",
                                        "color": 'white',
                                        "font-size": "12px",
                                    },
                                ),
                                style={"padding": "25px 0px 0px 100px"},
                                width=6,
                            ),
                        ],
                    ),
                    dbc.Row(
                        [
                            #html.Img(src=app.get_asset_url('abw.png'))
                            html.Div(
                                dcc.Loading(
                                    id='my-loading-2',
                                    type='circle',
                                    children= dcc.Graph(
                                        id='sharp-ratio-line-chart',
                                        #figure=go.Figure(data=[trace], layout=layout)
                                    ),
                                ),
                                style={"padding": "0 0 20px 0", 'margin': '0',},
                               # width=12,
                            ),  
                        ],
                        #style={'border-bottom': '0.2 solid white', 'display': 'flex', 'padding-left': '10px'} ,
                        #width: 1,
                    ),
                    ],
                    style={
                        "background-color": "#151519",
                        "color": 'white',
                        #"color": "white",
                        "border-style": "none",
                        "border-radius": "15px",
                        'font-family':'montserrat',
                        'font-weight': "lighter",
                        #'padding': '10px',
                        'margin': '0px 15px 0px 25px',
                        #'width': 1,
                        #'height': '150px',
                    },
                ),
                style={'margin': '20px 0px 20px 0px', 'padding': '0px',},
                width=3
            ),            
            dbc.Col(
                html.Div(
                    [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Row(
                                        [
                                            html.Label(
                                                "Volatility",
                                                style={
                                                    "font-size": "12px",
                                                    #"font-weight": "bold",
                                                },
                                            ),
                                            html.Label(
                                                #"$138.761,06",
                                                id = 'volatility-label',
                                                style={
                                                    "font-size": "20px",
                                                    #"font-weight": "bold",
                                                },
                                            ),
                                            
                                        ],
                                        style={
                                            "textAlign": "left",
                                            "color": 'white',
                                            "margin": "15px 0 0px 10px",
                                        },
                                    ),
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                html.Label(
                                    #"+7%",
                                    id = 'volatility-data-label',
                                    style={
                                        "textAlign": "left",
                                        "color": 'white',
                                        "font-size": "12px",
                                    },
                                ),
                                style={"padding": "25px 0px 0px 100px"},
                                width=6,
                            ),
                        ],
                    ),
                    dbc.Row(
                        [
                            #html.Img(src=app.get_asset_url('abw.png'))
                            html.Div(
                                dcc.Loading(
                                    id='my-loading-3',
                                    type='circle',
                                    children=dcc.Graph(
                                        id='volatility-line-chart',
                                        #figure=go.Figure(data=[trace], layout=layout)
                                    ),
                                ),
                                style={"padding": "0 0 20px 0", 'margin': '0',},
                               # width=12,
                            ),  
                        ],
                        #style={'border-bottom': '0.2 solid white', 'display': 'flex', 'padding-left': '10px'} ,
                        #width: 1,
                    ),
                    ],
                    style={
                        "background-color": "#151519",
                        "color": 'white',
                        #"color": "white",
                        "border-style": "none",
                        "border-radius": "15px",
                        'font-family':'montserrat',
                        'font-weight': "lighter",
                        #'padding': '10px',
                        'margin': '0px 25px 0px 15px',
                        #'width': 1,
                        #'height': '150px',
                    },
                ),
                style={'margin': '20px 0px 20px 0px', 'padding': '0px',},
                width=3
            ),    
            dbc.Col(
                html.Div(
                    [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Row(
                                        [
                                            html.Label(
                                                "Information Ratio",
                                                style={
                                                    "font-size": "12px",
                                                    #"font-weight": "bold",
                                                },
                                            ),
                                            html.Label(
                                                #"$138.761,06",
                                                id = 'ir-label',
                                                style={
                                                    "font-size": "20px",
                                                    #"font-weight": "bold",
                                                },
                                            ),
                                            
                                        ],
                                        style={
                                            "textAlign": "left",
                                            "color": 'white',
                                            "margin": "15px 0 0px 10px",
                                        },
                                    ),
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                html.Label(
                                    #"+7%",
                                    id = 'ir-data-label',
                                    style={
                                        "textAlign": "left",
                                        "color": 'white',
                                        "font-size": "12px",
                                    },
                                ),
                                style={"padding": "25px 0px 0px 100px"},
                                width=6,
                            ),
                        ],
                    ),
                    dbc.Row(
                        [
                            #html.Img(src=app.get_asset_url('abw.png'))
                            html.Div(
                                dcc.Loading(
                                    id='my-loading-4',
                                    type='circle',
                                    children=dcc.Graph(
                                        id='ir-line-chart',
                                        #figure=go.Figure(data=[trace], layout=layout)
                                    ),
                                ),
                                style={"padding": "0 0 20px 0", 'margin': '0',},
                               # width=12,
                            ),  
                        ],
                        #style={'border-bottom': '0.2 solid white', 'display': 'flex', 'padding-left': '10px'} ,
                        #width: 1,
                    ),
                    ],
                    style={
                        "background-color": "#151519",
                        "color": 'white',
                        #"color": "white",
                        "border-style": "none",
                        "border-radius": "15px",
                        'font-family':'montserrat',
                        'font-weight': "lighter",
                        #'padding': '10px',
                        'margin': '0px 40px 0px 0px',
                        #'width': 1,
                        #'height': '150px',
                    },
                ),
                style={'margin': '20px 0px 20px 0px', 'padding': '0px', },
                width=3
            ),   
        ],
    ),
    
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                        html.Label(
                                            "RETURN BY YEAR",
                                            style={
                                                #"textAlign": "left",
                                                "color": 'white',
                                                "margin": "20px 0 0 20px",
                                                "font-size": "14px",
                                                'font-family':'montserrat',
                                                'font-weight': "lighter",
                                            },
                                        ),
                                        ],
                                        width=4,
                                    ),
                                    dbc.Col(
                                        [
                                        html.Label(
                                            "S&P 500",
                                            style={
                                                #"textAlign": "left",
                                                "color": 'white',
                                                "margin": "20px 20px 0 0px",
                                                "font-size": "14px",
                                                'font-family':'montserrat',
                                                'font-weight': "lighter",
                                            },
                                        ),
                                        ],
                                        width=8,
                                        style={
                                            'display': 'inline-block',
                                            'text-align': 'right',
                                            'padding': '',
                                        },
                                    ),
                                ]
                            ),
                            html.Hr(),
                            dcc.Loading(
                                id='my-loading-5',
                                type='circle',
                                children=dcc.Graph(
                                    id='line-chart',
                                    #figure=go.Figure(data=[trace_performance], layout=layout_performance),
                                ),
                            ),
                        ],
                        style={"background-color": "#151519", "border-radius": "15px", "margin": '0 0px 0 30px'},
                    ),
                ],
                width=6,
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.Label(
                                "RETURN BY SECTOR BY YEAR",
                                style={
                                    #"textAlign": "left",
                                    "color": 'white',
                                    "margin": "20px 0 0 20px",
                                    "font-size": "14px",
                                    'font-family':'montserrat',
                                    'font-weight': "lighter",
                                },
                            ),
                            html.Hr(),
                            dcc.Loading(
                                id='my-loading-6',
                                type='circle',
                                children=dcc.Graph(
                                    id='multi-bar-chart',
                                    #figure=go.Figure(data=data, layout=layout_performance_sector),
                                ),
                            ),
                        ],
                        style={"background-color": "#151519", "border-radius": "15px", "margin": '0 30px 0 0'},
                    ),
                ],
                width=6,
            ),
        ]
    ), 
    dcc.Loading(
        id='my-loading-7',
        type='circle',
        children=dbc.Row(
            id="parent-div",
            style={
                'padding': '20px 30px 20px 30px',
            },
        ),
    ),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [ 
                                        html.Label(
                                            "PORTFOLIO",
                                            style={
                                                #"textAlign": "left",
                                                "color": 'white',
                                                "margin": "20px 0 0 20px",
                                                "font-size": "14px",
                                                'font-family':'montserrat',
                                                'font-weight': "lighter",
                                            },
                                        ),
                                        ],
                                        width=2,
                                    ),
                                    dbc.Col(
                                        [
                                        #dbc.Button("Primary", color="primary", className="me-1"),
                                        html.Label('Add row', id='add-row-button', n_clicks=0, style={'background-color': '#4791FF', 'font-size': '14px', 'padding': '8px', 'border-radius': '5px', "color": "black", 'cursor': 'pointer'}),
                                        html.Label('Update', id='btn-update', n_clicks=0, style={'background-color': '#5DFF89', 'font-size': '14px', 'padding': '8px', 'margin-left': '10px', 'border-radius': '5px', "color": "black", 'cursor': 'pointer'}),
                                        #'btn-update'
                                        ],
                                        style={
                                            'display': 'inline-block',
                                            'text-align': 'right',
                                            'padding': '15px 15px 0 0',
                                        },
                                        width=10,
                                    ),
                                ],
                            ),
                            html.Hr(),
                            dcc.Loading(
                                id='my-loading-30',
                                type='circle',
                                children= dt.DataTable(
                                    id="table_list",
                                    style_table={'width': '100%',
                                                 "border-radius": "10px",},
                                    style_cell={
                                        'textAlign': 'center',
                                        "white_space": "normal",
                                        #"height": "auto",
                                        #"width": "25%",
                                        "backgroundColor": '#151519',
                                        "color": "white",
                                        "font_size": "14px",
                                        'font-family':'montserrat',
                                        'font-weight': "lighter",
                                    },
                                    style_data={"border": "#4d4d4d"},
                                    #style_header={'display': 'none'},
                                    style_header={
                                        "backgroundColor": '#151519',
                                        #'font-weight': "lighter",
                                        "border": "#4d4d4d",
                                        'border-bottom': '0.2px solid #5E5E5E'
                                    },
                                    editable=True,
                                    row_deletable=True,
                                    merge_duplicate_headers=True,
                                    sort_action='native',
                                    #editable_columns=['ACQUISITION DATE', 'TICKER', 'AMOUNT', 'UNIT COST', 'COST BASIS'],
                                    #dropdown={
                                    #    'TICKER': {
                                    #        'options': [
                                    #            {
                                    #                "label": str(ticker_list[i]),
                                    #                "value": str(ticker_list[i]),
                                    #            }
                                    #            for i in range(len(ticker_list))
                                    #        ]
                                    #    },
                                    #},
                                    #row_selectable='single',
                                    style_cell_conditional=[
                                        {"if": {"column_id": c}, "textAlign": "center"}
                                        for c in ["attribute", "value"]
                                    ],
                                    #["Ticker 1", "Ticker 2", "Start Date", "End Date", "Standard deviation", "Critical Value", "Executable", "Backtest"]
                                    columns=[
                                        {'name': ["",'ACQUISITION DATE'], 'id': 'ACQUISITION DATE', 'editable': True},
                                        {'name': ["",'TICKER'], 'id': 'TICKER', 'editable': True},
                                        {'name': ["",'AMOUNT'], 'id': 'AMOUNT', 'editable': True},
                                        {'name': ["",'UNIT COST'], 'id': 'UNIT COST', 'editable': True},
                                        {'name': ["",'COST BASIS'], 'id': 'COST BASIS', 'editable': False},
                                        {'name': ["ACQUISITION DATE",'LOW'], 'id': 'LOW', 'editable': False},
                                        {'name': ["ACQUISITION DATE", 'HIGH'], 'id': 'HIGH', 'editable': False},
                                        {'name': ["",'SECTOR'], 'id': 'SECTOR', 'editable': False},
                                        {'name': ["",'COUNTRY'], 'id': 'COUNTRY', 'editable': False},
                                        {'name': ["",'LIVE PRICE'], 'id': 'LIVE PRICE', 'editable': False},
                                        #portfolio_df_data['LAST PRICE']
                                        {'name': ["",'MARKET VALUE'], 'id': 'MARKET VALUE', 'editable': False},
                                        {'name': ["",'GAIN'], 'id': 'GAIN', 'editable': False},
                                        {'name': ["",'RETURN'], 'id': 'RETURN', 'editable': False}, #html.Button('Executable', id='btn-executable')
                                        {'name': ["",'YEAR'], 'id': 'YEAR', 'editable': False},
                                        {'name': ["",'MONTH'], 'id': 'MONTH', 'editable': False},
                                        {'name': ["",'DAY'], 'id': 'DAY', 'editable': False},
                                        #{'name': 'YEAR', 'id': 'YEAR'},
                                        #{'name': 'Backtest', 'id': 'Backtest'},
                                        # Add a button to the 'Country' header cell
                                        #{'name': html.Button('Executable', id='btn-executable'), 'id': 'Executable'}
                                    ],
                                    style_data_conditional=[
                                            {'if': {'filter_query': '{GAIN} > 0','column_id': 'GAIN'},'color': '#02BC77', 'fontWeight': 'bold'},
                                            {'if': {'filter_query': '{GAIN} < 0','column_id': 'GAIN'},'color': '#FF2366', 'fontWeight': 'bold'},
                                            {'if': {'filter_query': '{RETURN} > 0','column_id': 'RETURN'},'color': '#02BC77', 'fontWeight': 'bold'},
                                            {'if': {'filter_query': '{RETURN} < 0','column_id': 'RETURN'},'color': '#FF2366', 'fontWeight': 'bold'},
                                            {'if': {'filter_query': '{YEAR} > 0','column_id': 'YEAR'},'color': '#02BC77', 'fontWeight': 'bold'},
                                            {'if': {'filter_query': '{YEAR} < 0','column_id': 'YEAR'},'color': '#FF2366', 'fontWeight': 'bold'},
                                            {'if': {'filter_query': '{MONTH} > 0','column_id': 'MONTH'},'color': '#02BC77', 'fontWeight': 'bold'},
                                            {'if': {'filter_query': '{MONTH} < 0','column_id': 'MONTH'},'color': '#FF2366', 'fontWeight': 'bold'},
                                            {'if': {'filter_query': '{DAY} > 0','column_id': 'DAY'},'color': '#02BC77', 'fontWeight': 'bold'},
                                            {'if': {'filter_query': '{DAY} < 0','column_id': 'DAY'},'color': '#FF2366', 'fontWeight': 'bold'},
                                            {
                                                'if': {
                                                    'filter_query': '{UNIT COST} < {LOW} || {UNIT COST} > {HIGH}',
                                                    'column_id': 'UNIT COST'
                                                },
                                                #'backgroundColor': '#FF2366',
                                                'color': '#FF2366'
                                            },
                                            {
                                                'if': {'column_id': ['ACQUISITION DATE', 'TICKER', 'AMOUNT', 'UNIT COST']},
                                                'backgroundColor': '#1E2024',
                                            }, #for col in ['ACQUISITION DATE', 'TICKER', 'AMOUNT', 'UNIT COST'],
                                            
                                    ]
                                ),
                            ),
                        ],
                        width={"size": 12,},
                        style={
                            #"padding": "0px 0px 0px 0px",
                            "border-radius": "15px",
                            'font-family':'montserrat',
                            'font-size': "10px",
                            "backgroundColor": '#151519',
                        },
                ),
                dbc.Col(
                    [
                    ],
                ),
            
                ],
                style={
                    "padding": "0 40px 0 40px",
                    "margin-bottom": "50px",
                    'font-family':'montserrat',
                    #'font-weight': "lighter",
                    'font-size': "10px",
                    #"backgroundColor": '#151519',
                    #'width': 500,
                }, 
            ), 
        ]
    ),
    
])

portfolio_df = pd.read_excel('Stocks_v3.xls')
portfolio_df.columns = ['ACQUISITION DATE', 'TICKER', 'AMOUNT', 'UNIT COST', 'COST BASIS', 'SECTOR', 'COUNTRY']
start_stocks = min(portfolio_df['ACQUISITION DATE'])
#end_stocks = datetime.datetime(2020, 12, 29)

bond_ticker = '^TNX'  # Ticker symbol for the 10-year Treasury bond
bond_data = yf.get_data(bond_ticker, start_stocks)['close']

bench_ticker = '^GSPC'
bench_data = yf.get_data(bench_ticker, start_stocks)['close']
# Get the yield data for the bond
#bond_yield = bond_data.history(period="1d")['Close'][0]

#print(f"10-Year Treasury Bond Yield: {bond_yield:.2f}%")

# create a sample datatable with daily prices of three stocks
tickers = portfolio_df['TICKER'].unique()

start_stocks = min(portfolio_df['ACQUISITION DATE'])

# Function for pulling the ticker data
def get(tickers):
    def data(ticker):
        yf_data = yf.get_data(ticker) #type(yf_data.index)
        #print(ticker)
        portfolio_df.loc[portfolio_df['TICKER'] == ticker, 'HIGH'] = round(yf_data.loc[portfolio_df.loc[portfolio_df['TICKER'] == ticker, 'ACQUISITION DATE'].iloc[0].to_pydatetime()]['high'], 2)
        portfolio_df.loc[portfolio_df['TICKER'] == ticker, 'LOW'] = round(yf_data.loc[portfolio_df.loc[portfolio_df['TICKER'] == ticker, 'ACQUISITION DATE'].iloc[0].to_pydatetime()]['low'], 2)
        #print(yf_data[(portfolio_df.loc[portfolio_df['TICKER'] == 'BABA', 'ACQUISITION DATE'].dt.strftime('%Y-%m-%d').iloc[0]):])
        return yf_data[(portfolio_df.loc[portfolio_df['TICKER'] == ticker, 'ACQUISITION DATE'].dt.strftime('%Y-%m-%d').iloc[0]):]['close'] * float(portfolio_df.loc[portfolio_df['TICKER'] == ticker, 'AMOUNT'].iloc[0])
        #close_price = pdr.get_data_yahoo('VZ', start=datetime.datetime(2019, 12, 29), end=datetime.datetime(2021, 12, 29)).Close
    datas = map(data, tickers)
    print(datas)
    return pd.concat(datas, axis=1, keys=tickers)

portfolio = get(tickers)
portfolio = portfolio.fillna(method='ffill')
portfolio = portfolio.fillna(value=0)

portfolio_df['ACQUISITION DATE'] = portfolio_df['ACQUISITION DATE'].dt.strftime('%m/%d/%Y')
portfolio_df['COST BASIS'] = round(portfolio_df['COST BASIS'], 2)
#portfolio_df['LOW-HIGH'] = portfolio_df['LOW'].astype(str) + "-" +  portfolio_df['HIGH'].astype(str)
portfolio_df['LIVE PRICE'] = [ round( yf.get_live_price(portfolio_df['TICKER'].iloc[r]), 2) for r in range(0, len(portfolio_df))]
portfolio_df['MARKET VALUE'] = round(portfolio_df['AMOUNT'] * portfolio_df['LIVE PRICE'], 2)
portfolio_df['GAIN'] = round(portfolio_df['MARKET VALUE'] - portfolio_df['COST BASIS'], 2)
portfolio_df['RETURN'] = round(((portfolio_df['MARKET VALUE'] / portfolio_df['COST BASIS']) - 1) * 100, 2)
portfolio_df['YEAR'] = [round(portfolio[portfolio_df['TICKER'].iloc[r]].resample('Y').last().pct_change()[-1] * 100, 2) for r in range(0, len(portfolio_df))]
portfolio_df['MONTH'] = [round(portfolio[portfolio_df['TICKER'].iloc[r]].resample('M').last().pct_change()[-1] * 100, 2) for r in range(0, len(portfolio_df))]
portfolio_df['DAY'] = [round(portfolio[portfolio_df['TICKER'].iloc[r]].resample('D').last().pct_change()[-1] * 100, 2) for r in range(0, len(portfolio_df))]


# create a dictionary representing the amount of each stock in wallet
#unit_costs = portfolio_df.set_index('Ticker')['Unit Cost'].to_frame()
    
@app.callback(
    # output
    [Output("performance-line-chart", "figure"), 
     Output("total-balance-label", "children"), 
     Output("balance-performace-label", "children"), 
     Output("sharp-ratio-line-chart", "figure"), 
     Output("sharp-ratio-label", "children"), 
     Output("volatility-line-chart", "figure"),
     Output("volatility-label", "children"),
     Output("ir-line-chart", "figure"),
     Output("ir-label", "children"),     
     Output("line-chart", "figure"),
     Output("multi-bar-chart", "figure"),
     #Output("country-line-chart", "figure"),
     Output("parent-div", "children"),
     #Output('table_list', 'data'),
     ], #Output("live price 2", "figure"), Output("graph", "figure"), Output("graph2", "figure"), Output("coint1", "children"), Output("z_score1", "children")],
    # input
    [Input('btn-update', 'n_clicks')],
     [State('table_list', 'data'),], 
    #Input('btn-price', 'n_clicks'),
    #Input('btn-lr', 'n_clicks'),
    #Input('btn-cointegration', 'n_clicks'),
    #Input('btn-chart', 'n_clicks')],
)
def graph_genrator(n_clicks_update, data):#, ticker2, sd, pvalue): #btn_price, btn_lr, btn_cointegration, btn_chart):
 
    #ticker1 = "TSLA" 
    #ticker2 = "MSFT"
    global portfolio
    global portfolio_df
    
    if n_clicks_update is not None and n_clicks_update > 0:
        
        portfolio_df = pd.DataFrame(data).copy()
        
        tickers = portfolio_df['TICKER'].unique()

        # Function for pulling the ticker data
        def get(tickers):
            def data(ticker):
                yf_data = yf.get_data(ticker) #type(yf_data.index)
                return yf_data[(portfolio_df.loc[portfolio_df['TICKER'] == ticker, 'ACQUISITION DATE'].iloc[0]):]['close'] *  float(portfolio_df.loc[portfolio_df['TICKER'] == ticker, 'AMOUNT'].iloc[0])
                #close_price = pdr.get_data_yahoo('VZ', start=datetime.datetime(2019, 12, 29), end=datetime.datetime(2021, 12, 29)).Close
            datas = map(data, tickers)
            #print(datas)
            return pd.concat(datas, axis=1, keys=tickers)
        
        portfolio = get(tickers)
        portfolio = portfolio.fillna(method='ffill')
        portfolio = portfolio.fillna(value=0)
    

    
    invest = portfolio.copy()#.drop(portfolio.columns[[-1,-2]], axis=1)
    invest[invest != 0] = [list(portfolio_df.loc[portfolio_df['TICKER'] == c]['COST BASIS'])[0] if c in portfolio_df['TICKER'].tolist() else 0 for c in invest.columns]
    invest = invest.sum(axis=1)
    
    portfolio['total'] = portfolio.sum(axis=1)
    portfolio['return'] = portfolio['total'] - invest
    portfolio['return_perc'] = portfolio['return'] / portfolio['total']
    
    print(portfolio)
    
    totalbalance = round(portfolio['total'].iloc[len(portfolio)-1], 2)
    totalreturn = round((portfolio['return'][-1] / invest[-1]) * 100, 2)
    fig1 = go.Figure(figure_performance(portfolio))
    
    # Calculate daily returns for the bond and the portfolio
    bond_returns = bond_data.pct_change()
    stocks_returns = portfolio['return'].pct_change()

    # Calculate the daily excess return of the portfolio over the bond
    excess_returns = stocks_returns - bond_returns

    # Calculate the average daily excess return
    avg_excess_return = excess_returns.mean()

    # Calculate the standard deviation of daily excess returns
    std_excess_return = excess_returns.std()

    # Calculate the Sharpe ratio
    sharpe_ratio = round((avg_excess_return / std_excess_return) * 100, 2)
    
    fig2 = go.Figure(figure_sharp_ratio(portfolio, bond_data))
    
    #import plotly.offline as pyo
    #pyo.iplot(fig1)
    
    # Calculate the daily returns
    #portfolio['return'] = portfolio['total'].pct_change()
    # Group the returns by year
    annual_returns = portfolio['return_perc'].groupby(portfolio.index.year)
    # Calculate the annualized volatility for each year
    annual_volatility = portfolio['return_perc'].groupby(portfolio.index.year).apply(lambda x: np.std(x) * np.sqrt(252))
    # Calculate the total volatility for the entire period
    total_volatility = round(annual_volatility.iloc[-1] * 100, 2)#round((np.std(portfolio['return_perc']) * np.sqrt(len())) * 100, 2)
    
    fig3 = go.Figure(volatility(annual_volatility))
    
    #np.prod(portfolio['total'].pct_change() + 1)
    
    tracking_error = (portfolio['return_perc'] - bench_data.pct_change()).std()*np.sqrt(252)
    
    informatio_ratio = round((portfolio['return_perc'][-1] - (np.prod(bench_data.pct_change() + 1) - 1)) / tracking_error, 2)
    
    #bench_perc = round(( ( portfolio['total'].pct_change() + 1).cumprod().iloc[[-1]][0] - 1 / (bench_data.pct_change() + 1).cumprod().iloc[[-1]][0] - 1 ), 2)
    
    fig4 = go.Figure(InformationRatio(portfolio, bench_data))
    
    fig5 = go.Figure(figure_performance_line(portfolio, bench_data))
    
    sectors = pd.DataFrame({
        'Stock': portfolio_df['TICKER'],
        'Sector': portfolio_df['SECTOR']
    })#.set_index('Stock', inplace=True, verify_integrity=True)
    sectors = sectors.set_index('Stock')
    
    print(sectors)
    
    fig6 = go.Figure(figure_bar_sector(portfolio, sectors))
    
    countries = pd.DataFrame({
        'Stock': portfolio_df['TICKER'],
        'Country': portfolio_df['COUNTRY']
    })#.set_index('Stock', inplace=True, verify_integrity=True)
    countries = countries.set_index('Stock')

    child_div = create_child_div(portfolio_df, portfolio, countries)
    
    return fig1,'$' + str(totalbalance), str(totalreturn) + '%', fig2, str(sharpe_ratio), fig3,  str(total_volatility) + '%', fig4, str(informatio_ratio), fig5, fig6, child_div #, fig7, parent_div
    
@app.callback(
    [Output('table_list', 'data'),
    Output('add-row-button', 'n_clicks')],
    [Input('table_list', 'data'),
     Input('add-row-button', 'n_clicks')],
    [State('table_list', 'data_previous'),
     State('table_list', 'columns')]
)
def update_table(data, n_clicks, data_previous, columns):


    if n_clicks is not None and n_clicks > 0:
        data.append({c['id']: '' for c in columns})
        return data, 0
    
    if data_previous is None:
        dash.exceptions.PreventUpdate()
    else:
        if len(data_previous) > len(data):
            return [f'Just removed {row}' for row in data_previous if row not in data]

    #print(dash.callback_context.triggered)
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'table_list.data' in changed_id:
        for i, row in enumerate(data):
            if row != data_previous[i]:
                
                row['COST BASIS'] = round(float(row['AMOUNT']) * float(row['UNIT COST']), 2) if row['AMOUNT'] != "" and row['UNIT COST'] != "" else ""
                row['COUNTRY'] = country_to_alpha3(df_tickers[df_tickers['Ticker'] == row['TICKER']]['Country'].item()) if row['TICKER'] != "" else ""
                row['SECTOR'] =  df_tickers[df_tickers['Ticker'] == row['TICKER']]['Category Name'].item() if row['TICKER'] != "" else ""
                row['LIVE PRICE'] = round(yf.get_live_price(row['TICKER']), 2) if row['TICKER'] != "" else ""
                row['MARKET VALUE'] = round(float(row['AMOUNT']) * float(row['LIVE PRICE']), 2) if row['AMOUNT'] and row['LIVE PRICE'] != "" else ""
                row['GAIN'] = round(float(row['MARKET VALUE']) - float(row['COST BASIS']), 2) if row['MARKET VALUE'] != "" and row['COST BASIS'] != "" else ""
                row['RETURN'] = round(((float(row['MARKET VALUE']) / float(row['COST BASIS'])) - 1) * 100, 2) if row['MARKET VALUE'] != "" and row['COST BASIS'] != "" else ""
                try:
                    df_ticker = yf.get_data(row['TICKER']) if row['TICKER'] != "" else None
                except:
                    df_ticker = None
                row['YEAR'] = round(df_ticker['close'].resample('Y').last().pct_change()[-1] * 100, 2) if df_ticker is not None else ""
                row['MONTH'] = round(df_ticker['close'].resample('M').last().pct_change()[-1] * 100, 2) if df_ticker is not None else ""
                row['DAY'] = round(df_ticker['close'].resample('D').last().pct_change()[-1] * 100, 2) if df_ticker is not None else ""
                row['HIGH'] = round(df_ticker.loc[row['ACQUISITION DATE']]['high'], 2) if df_ticker is not None and row['ACQUISITION DATE'] != "" else "" 
                row['LOW'] = round(df_ticker.loc[row['ACQUISITION DATE']]['low'], 2) if df_ticker is not None and row['ACQUISITION DATE'] != "" else "" 
                return data, 0
            
    
    t_data = portfolio_df.to_dict("records")
    
    return t_data, 0

if __name__ == '__main__':
    app.run_server()
