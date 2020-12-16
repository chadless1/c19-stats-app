#!/usr/bin/nv python3

import pandas as pd
import numpy as np
import datetime 

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Read csv file from github
#df_states = pd.read_html('https://github.com/nytimes/covid-19-data/blob/master/us-states.csv')[0]

# Read data from csv file
df_states = pd.read_csv('data/us-states_12.15.csv')

# Create Date objects

df_states['date'] = pd.to_datetime(df_states['date'])

date = df_states['date'].iloc[-1]
date = date.strftime('%m-%d-%Y')

# Dash App

app = dash.Dash(__name__)

app.layout = html.Div(children=[

        # Header image and title
        html.Header(
            html.Div([ 
            
                html.Img(src=app.get_asset_url('c19.jpeg')),

                html.H1('Covid-19 Data'),

                ],className='head')

            ),

        html.Br(),
        
        # Data Date
        html.P('Data on Covid-19 Case Numbers and Deaths for the United States. Search by State and find out more about your area.'),
       
        html.P('Data is currently valid from *{}*'.format(date)),

        html.A('data source', href='https://github.com/nytimes/covid-19-data/'),

        html.Br(),

        html.A('code source', href='https://github.com/chadless1/c19-stats-app/'),

        # Line break
        html.Br(),
        html.Hr(),
        html.Br(),
        
        # Tabs
        dcc.Tabs(id="tabs", value='tab-1', children=[
            
            dcc.Tab(label='USA', value='tab-1'),
            dcc.Tab(label='Data By State', value='tab-2'),

            ], style={'width': '90%', 'margin': 'auto'}),
        # Tab contnent
        html.Div(id='tabs-content'),

        

        ]) # main div tag
           # End of app layout

###########################################################
#                     CallBacks                           #
###########################################################


# Tab Callbacks
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):

    today = df_states['date'].iloc[-1]

    df_usa = df_states[df_states['date'] == today]
    
    usa_total_cases = df_usa['cases'].sum()
    usa_total_deaths = df_usa['deaths'].sum()

    usa_total_df = df_states[['cases','deaths']].groupby(df_states['date'])
    usa_total_df = usa_total_df.sum()

    usa_last = usa_total_df.tail()

    usa_case_percent = (usa_total_df['cases'].iloc[-1] - usa_total_df['cases'].iloc[-5]) / usa_total_df['cases'].iloc[-5] * 100
    usa_case_percent = round(usa_case_percent, 2)

    usa_death_percent = (usa_total_df['deaths'].iloc[-1] - usa_total_df['deaths'].iloc[-5]) / usa_total_df['deaths'].iloc[-5] * 100
    usa_death_percent = round(usa_death_percent, 2)



    if tab == 'tab-1':
        return html.Div([

            html.Div([

                html.Br(),
                html.H3('USA Data'),
                html.Br(),

                ] ,className='row'),

            # Main Div
            html.Div([

                # USA Cases
                html.Div([

                    html.Div([

                        html.H4('Total Cases'),

                        ],className='div_head'),

                    html.H3('{:,}'.format(usa_total_cases)),


                    ],className='four columns'),
                
                # USA Deaths
                html.Div([

                    html.Div([

                        html.H4('Total Deaths'),

                        ],className='div_head'),

                    html.H3('{:,}'.format(usa_total_deaths)),


                    ],className='four columns'),


                # USA Case Change
                html.Div([

                    html.Div([

                        html.H4('Case Change %'),

                        ],className='div_head'),

                    html.H3('{:,}%'.format(usa_case_percent)),
                    html.P('over last 5 Days'),


                    ],className='four columns'),
                
                # USA Death Change
                html.Div([

                    html.Div([

                        html.H4('Death Change %'),

                        ],className='div_head'),

                    html.H3('{:,}%'.format(usa_death_percent)),
                    html.P('over last 5 Days'),


                    ],className='four columns'),


               
                ]),

                html.Br(),

                html.Div([

                    dcc.Graph(

                        figure={

                            'data': [
                                
                                {'x': usa_total_df.index, 'y': usa_total_df['cases'].values, 'type': 'line', 'name': 'cases'},
                                {'x': usa_total_df.index, 'y': usa_total_df['deaths'].values, 'type': 'line', 'name': 'deaths'},

                                ],

                            'layout': {
                                'title': 'Cases & Deaths',
                                #'height': 310,

                                }}

                        ),

                    ],className='five columns'),

                html.Div([

                    dcc.Graph(

                        figure={

                            'data': [
                                
                                {'x': usa_last.index, 'y': usa_last['cases'].values, 'type': 'line', 'name': 'cases'},

                                ],

                            'layout': {
                                'title': 'Cases Last 5 Days',
                                #'height': 310,

                                }}

                        ),

                    ],className='five columns'),

                html.Div([

                    dcc.Graph(

                        figure={

                            'data': [
                                
                                {'x': usa_last.index, 'y': usa_last['deaths'].values, 'type': 'line', 'name': 'cases', 'marker': {'color': 'orange'}},

                                ],

                            'layout': {
                                'title': 'Deaths Last 5 Days',
                                #'height': 310,

                                }}

                        ),

                    ],className='five columns'),


            
                    ],className='container')

        #########################################################
        # End Tab1
    
    elif tab == 'tab-2':
        return html.Div([
                               
           # Tab 2 Content #
           #################

           # States
            html.H3('Select State'),
            
            html.Div([
            dcc.Dropdown(id='my-dropdown2',
                
                options=[{'label': i, 'value': i} for i in sorted(df_states['state'].unique())],
                #multi=True,
                value='Massachusetts',
                searchable=False,
            
                ),
            ], style={'margin': 'auto', 'width': '50%', 'text-align': 'center'}),

            html.Br(),

            # Radio Button Graph
            html.Div([

                    dcc.RadioItems(id='r_button',
                        options=[
                            {'label': 'Cases', 'value': 'CASES'},
                            {'label': 'Deaths', 'value': 'DEATH'},
                            {'label': 'Both', 'value': 'BOTH'}
                         ],
                        value='BOTH',
                        labelStyle={'display': 'inline-block', 'margin-bottom': '10px', 'padding': '5px 5px'}
                                )  

                    ],className='row', style={'text-align': 'left', 'margin-left': '90px'}),
            
            # Main Content Div    

            html.Div([
                
                # graph div
                html.Div([

                    dcc.Graph(id='graph_1')

                    ],className='six columns'),
                
                # Data div
                html.Div([

                    html.Div(id='total_cases'),

                    ],className='six columns'),

                # second graph div
                html.Div([

                    dcc.Graph(id='graph_2')

                    ],className='twelve columns'),
                
                ],className='container'),
    ##########################################################




        ])# end of Tab 2



# State Graphs Callback and Functions
# Case Graph

@app.callback(Output('graph_1', 'figure'),
        [Input('my-dropdown2', 'value'), Input('r_button', 'value')])


def update_figure(value, button):


    if button == 'BOTH':

        df3 = df_states[df_states['state'] == value]
        
        df3 = df3.set_index('date')
        
        df4 = df3['cases'].diff()
        df5 = df3['deaths'].diff()

        df4 = df4.mask(df4 < 0)
        df5 = df5.mask(df5 < 0)

        figure={
                
                
                'data': [
                    
                    {'x': df4.index, 'y': df4, 'type': 'line', 'name': 'cases'},
                    {'x': df5.index, 'y': df5, 'type': 'line', 'name': 'deaths'},

                    ],
                 'layout': {
                    'title': 'Cases & Deaths',
                    'height': 310,
                   # 'paper_bgcolor': '#e6e6ff',
                   # 'plot_bgcolor': '#e6e6ff'
                 
                }}


        return(figure)

    elif button == 'CASES':

        df3 = df_states[df_states['state'] == value]
        
        df3 = df3.set_index('date')
        
        df4 = df3['cases'].diff()
        df5 = df3['deaths'].diff()

        df4 = df4.mask(df4 < 0)
        df5 = df5.mask(df5 < 0)

        figure={
                
                
                'data': [
                    
                    {'x': df4.index, 'y': df4, 'type': 'line', 'name': 'cases'},

                    ],
                 'layout': {
                    'title': 'Cases'
                
                }}


        return(figure)
    
    elif button == 'DEATH':

        df3 = df_states[df_states['state'] == value]
        
        df3 = df3.set_index('date')
        
        df4 = df3['cases'].diff()
        df5 = df3['deaths'].diff()

        df4 = df4.mask(df4 < 0)
        df5 = df5.mask(df5 < 0)

        figure={
                
                
                'data': [
                    
                    {'x': df5.index, 'y': df5, 'type': 'line', 'name': 'deaths', 'marker': {'color': 'orange'}},

                    ],
                 'layout': {
                    'title': 'Deaths'
                
                }}


        return(figure)



@app.callback(Output('total_cases', 'children'),
        [Input('my-dropdown2', 'value')])

def update_contetnt(value):

    # New DataFrame
    dff = df_states[df_states['state'] == value]

    # Case and Death Totals
    t_cases = dff['cases'].iloc[-1]
    t_deaths = dff['deaths'].iloc[-1]

    # Case Calculations
    dff2 = dff.set_index('date')
    dff2 = dff2['cases'].diff()
    dff2 = dff2.dropna()

    average_cases = dff2.mean()
    average_cases = round(average_cases)

    case_percent = (dff['cases'].iloc[-1] - dff['cases'].iloc[-5]) / dff['cases'].iloc[-5] * 100
    case_percent = round(case_percent, 2)
  
    month_cases = (dff['cases'].iloc[-1] - dff['cases'].iloc[-30]) / dff['cases'].iloc[-30] * 100
    month_cases = round(month_cases, 2)

    average_5_cases = dff2.tail()
    average_5_cases = round(average_5_cases.mean())

    average_30_cases = dff2.tail(30)
    average_30_cases = round(average_30_cases.mean())


    # Death Calculations
    dff3 = dff.set_index('date')
    dff3 = dff3['deaths'].diff()
    dff3 = dff3.dropna()

    average_deaths = dff3.mean()
    average_deaths = round(average_deaths)

    death_percent = (dff['deaths'].iloc[-1] - dff['deaths'].iloc[-5]) / dff['deaths'].iloc[-5] * 100
    death_percent = round(death_percent, 2)
    
    month_deaths = (dff['deaths'].iloc[-1] - dff['deaths'].iloc[-30]) / dff['deaths'].iloc[-30] * 100
    month_deaths = round(month_deaths, 2)

    average_5_deaths = dff3.tail()
    average_5_deaths = round(average_5_deaths.mean())

    average_30_deaths = dff3.tail(30)
    average_30_deaths = round(average_30_deaths.mean())


    return(
            # HTML TABLE
            html.Table([
                html.Tr([
                    # Headers
                    html.Th('     '),
                    html.Th('Cases'),
                    html.Th('Deaths'),

                ] ),

                html.Tr([
                    #Total
                    html.Td('Total:'),
                    html.Td('{:,}'.format(t_cases)),
                    html.Td('{:,}'.format(t_deaths)),

                ] ),
                
                html.Tr([
                    #Average per day
                    html.Td('Daily Average:'),
                    html.Td('{:,}'.format(average_cases)),
                    html.Td('{:,}'.format(average_deaths)),

                ] ),

                html.Tr([
                    # Average 5 Days
                    html.Td('Average Last 5 Days:'),
                    html.Td('{:,}'.format(average_5_cases)),
                    html.Td('{:,}'.format(average_5_deaths)),

                ] ),
                
                html.Tr([
                    # Average 30 Days
                    html.Td('Average Last 30 Days:'),
                    html.Td('{:,}'.format(average_30_cases)),
                    html.Td('{:,}'.format(average_30_deaths)),

                ] ),


                html.Tr([
                    # Change 5 Days
                    html.Td('% Change 5 Days:'),
                    html.Td('{:,}%'.format(case_percent)),
                    html.Td('{:,}%'.format(death_percent)),

                ] ),
                
                html.Tr([
                    #Change 30 Days
                    html.Td('% Change 30 Days:'),
                    html.Td('{:,}%'.format(month_cases)),
                    html.Td('{:,}%'.format(month_deaths)),

                ] ),



                ] ),



            )

# Graph 2

@app.callback(Output('graph_2', 'figure'),
        [Input('my-dropdown2', 'value'), Input('r_button', 'value')])


def update_figure(value, button):


    if button == 'BOTH':

        df3 = df_states[df_states['state'] == value]
        
        df3 = df3.set_index('date')
        
        df4 = df3['cases'].diff()
        df5 = df3['deaths'].diff()

        df4 = df4.mask(df4 < 0)
        df5 = df5.mask(df5 < 0)

        df4 = df4.tail()
        df5 = df5.tail()

        figure={
                
                
                'data': [
                    
                    {'x': df4.index, 'y': df4, 'type': 'bar', 'name': 'cases'},
                    {'x': df5.index, 'y': df5, 'type': 'bar', 'name': 'deaths'},

                    ],
                 'layout': {
                    'title': 'Last 5 Days',
                    'height': '300',
                    'xaxis': {'tickformat': '%b %d, %Y'},
                    'xaxis': {'maxnumberoflabels': '5'},
                   # 'paper_bgcolor': '#e6e6ff',
                   # 'plot_bgcolor': '#e6e6ff'
                 
                }}


        return(figure)

    elif button == 'CASES':

        df3 = df_states[df_states['state'] == value]
        
        df3 = df3.set_index('date')
        
        df4 = df3['cases'].diff()
        df5 = df3['deaths'].diff()

        df4 = df4.mask(df4 < 0)
        df5 = df5.mask(df5 < 0)

        df4 = df4.tail()
    
        figure={
                
                
                'data': [
                    
                    {'x': df4.index, 'y': df4, 'type': 'bar', 'name': 'cases'},
                    {'x': df4.index, 'y': df4, 'type': 'line', 'marker': {'color': 'black'}},

                    ],
                 'layout': {
                    'title': 'Cases Last 5 Days', 
                    'xaxis': {'tickformat': '%b %d, %Y'},
                    'xaxis': {'maxnumberoflabels': '5'},
                }}


        return(figure)
    
    elif button == 'DEATH':

        df3 = df_states[df_states['state'] == value]
        
        df3 = df3.set_index('date')
        
        df4 = df3['cases'].diff()
        df5 = df3['deaths'].diff()

        df4 = df4.mask(df4 < 0)
        df5 = df5.mask(df5 < 0)

        df5 = df5.tail()

        figure={
                
                
                'data': [
                    
                    {'x': df5.index, 'y': df5, 'type': 'bar', 'name': 'deaths', 'marker': {'color': 'orange'}},
                    {'x': df5.index, 'y': df5, 'type': 'line', 'marker': {'color': 'black'}},

                    ],
                 'layout': {
                    'title': 'Deaths Last 5 Days', 
                    'xaxis': {'tickformat': '%b %d, %Y'},
                    'xaxis': {'maxnumberoflabels': '5'},
                }}


        return(figure)



########################################################


app.config.suppress_callback_exceptions=True

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)



