#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 12:37:11 2019

@author: zshengqi
"""

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output#, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
#import math
#import base64

external_stylesheets =['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_csv("NBA_data.csv")
df = pd.read_excel("https://s3.amazonaws.com/programmingforanalytics/NBA_data.xlsx")


#Stacked Graph Variables
def type_col():
    newcolumn = []

    for names in range(20):
        newcolumn.append('field')

    for names in range(21,41):
        newcolumn.append('3P')
    
    newcolumn = pd.DataFrame(newcolumn)

    return newcolumn

x = df['Name']
y1 = df['Field_goals_made_per_game']
y2 = df['3P_made_per_game']
y = y1.append(y2)
x = x.append(x)
newcolumn = type_col()

frame = [x,y]
df1 = pd.concat(frame,axis = 1)
df1 = df1.reset_index(drop=True)
result = pd.concat([df1,newcolumn],axis = 1)
result.columns = ['Name','Goal','Type']


app_template = go.layout.Template(
    layout = go.Layout(title_font = dict(color = 'Black'),
                plot_bgcolor = '#DFF0EF',
                paper_bgcolor = '#DFF0EF',
                legend = {'bgcolor':'LightSteelBlue',
                            'bordercolor':'Black',
                            'borderwidth':0.5,
                            'font':dict(color = 'Black')},
                xaxis = dict(color = 'Black'),
                yaxis = dict(color = 'Black'),
        )
    )
				
#App
app.layout = html.Div(
    style={'backgroundColor': '#DFF0EF', 'color':'black'},
    children = [
        html.H1(children = 'NBA Dashboard',
           style = {
                    'fontSize':45,
                    '-webkit-text-stroke': '3px black',
                    'textAlign':'left',
                    'background-image':'url(https://i.ibb.co/37TzT2x/nba-logo.jpg)',
                    'color':'#DFF0EF',
                    'padding-left':'50px'},
               ),
        html.Div(children = [ html.H1("Introduction"),
            dcc.Markdown('''In this dashboard there are two interactive graphs and two graphs.  
                            The first graph is a scatter plot. Next to the graph is a dropdown menu that allows the user to select the x-axis for the graph. The graph then takes in this value and plots the Player Salary against the value selecte by the user.
                            The Second graph is a stacked graph that shows the number of Field Goals and 3-Pointers made by each player.
                            The 3rd graph is a bubble graph that plots Salary vs Points Per Game and uses the players Salary to dictate the size of the bubble graph.
                            The final graph is a bar chart that compares two players that are selected by the user in the two dropdown menus next to the graph. The dropdown menus are also interactive as the list of players changes to prevent the same player being selected in both drop downs. 
                            Finally, there is a table that shows all the data.''')],
            style = {'fontSize': 18}),

        #Row 1
        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'col1',
                    children = [
                        html.H3(children = "Select X-Axis Variable",
                                style = {'textAlign':'center'}
                        ),
                        dcc.Dropdown(
                            id = "x-axis",
                            options = [{'label':i, 'value':i} for i in df.columns[2:16]],
                            value = df.columns[2],
                            clearable=False,
                            style = {
                                'width':'350px',
                                'fontSize':'20px',
                                'padding-left':'50px',
                                'textAlign':'center',
                                'color':'black'}
                        ),
                    ], style = {'width': '30%',
                                'display':'inline-block',
                                'padding-right':'30px',
                                }
                ),

                html.Div(
                    className = "col2",
                    children = [
                        html.H2(children = 'Salary Plot',
                        style = {'textAlign':'center'}),

                        dcc.Graph(
                            id = "salary-graph",
                        )
                    ], style = {'width':'70%',
                                'display':'inline-block',
                                'padding-right':'20px'}
                ),
            ], style = {'padding-top':'20px',
                        'width': '100%',
                        'display': 'flex',
                        'align-items': 'center',
                        'justify-content': 'center',}
        ),

        #Row 2
        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'col1',
                    children = [
                        dcc.Graph(id = 'stacked-plot',
                                  figure = px.bar(result, x = "Name",y="Goal",color = 'Type',
                                                  template = app_template,
                                    title = 'Player Shots Made Per Game',
                                    ),
                                style = {'width': '45%', 'padding-right':'30px','textAlign':'center'},
                                ),
                        dcc.Graph(id = 'bubble-chart',
                                  figure = px.scatter(df, template = app_template,
                                            title = 'Player\'s Salary Comparison',
                                            x = df['Points_per_game'],
                                            y = df['Salary'],
                                            color = 'Name',
                                            size = df['Salary']),
                                    style = {'width':'45%','padding-left':'30px'},
                                 ),

                    ], style = {'padding-top':'50px',
                                'width': '100%',
                                'display': 'flex',
                                'align-items': 'center',
                                'justify-content': 'center',}
                ),
            ]
        ),

        #Row 3
        html.Div(
            className = 'row',
            children = [
                html.Div(
                    className = 'col1',
                    children = [
                        html.H3(children = 'Select Player One',
                        style = {'padding-top':'50px',}),
                        dcc.Dropdown(
                            id='player_1',
                            clearable=False,
                            options = [{'label':i, 'value':i} for i in df.Name],
                            value = df.Name[0],
                            style = {
                                'width':'350px',
                                'fontSize':'20px',
                                'padding-left':'80px',
                                'textAlign':'center',
                                'color':'black'}
                        ),

                        html.H3(children = 'Select Player Two',
                        style = {'display':'inline-block',
                                 'padding-top':'50px'}),
                        dcc.Dropdown(
                            id = 'player_2',
                            clearable=False,
                            options = [{'label':i, 'value':i} for i in df.Name],
                            value = df.Name[1],
                            style = {
                                'width':'350px',
                                'fontSize':'20px',
                                'padding-left':'80px',
                                'textAlign':'center',
                                'color':'black'}
                        )
                    ], style = {'width':'30%',
                                'textAlign':'center',}
                ),
                html.Div(
                    className = 'col2',
                    children = [
                        dcc.Graph(id = 'comparison-graph')
                    ], style = {'padding-top':'50px',
                                'width':'70%',
                                'textAlign':'center'}
                ),
            ],
            style = {'padding-top':'50px',
                        'width': '100%',
                        'display': 'flex',
                        'align-items': 'center',
                        'justify-content': 'center',}
        ),

        #Show Table
        html.Div(
            className = 'NBA-Data-Table',
            children = [
                html.H2(children = 'NBA Player Stats',
                        style = {'textAlign':'center',
                                 'padding-top':'50px'}),
                dash_table.DataTable(
                    id = 'data_table',
                    columns = [{'name':i,'id':i, 'editable':(i=='Name' or i == 'Salary')} for i in df.columns[0:18]],
                    data = df.to_dict('records'),
                    style_cell = {
                        'textAlign':'center',
                        'color':'black'
                    },
                    style_data_conditional = [{
                        'if': {'row_index':'odd'},
                        'backgroundColor':'rgb(248,248,248)',
                        'if':{'column_editable':True},
                        'backgroundColor':'rgb(230,230,230)',
                        'fontWeight':'bold'
                    }],
                    style_header={
                        'backgroundColor':'rgb(230,230,230)',
                        'fontWeight':'bold',
                        'color':'black'
                    },
                    style_table={
                        'maxHeight':'300px',
                        'overflowY':'scroll',
                    },
                )
            ]
        ),
    ],
)

#Callbarck for scatter plot
@app.callback(
    Output(component_id='salary-graph', component_property='figure'),
    [Input(component_id='x-axis',component_property='value')],
)

#Updates Scatter Plot
def update_scatter(x_value):
    figure = {
        'data': [
            go.Scatter(
                x = df[df['Name'] == i][x_value],
                y = df[df['Name'] == i]['Salary'],
                text = df[df['Name'] == i]['Name'],
                mode = 'markers',
                opacity = 0.8,
                marker = {
                    'size':15,
                    'line': {'width':0.5, 'color':'orange'}
                },
                name = i
            ) for i in df.Name.unique()
        ],
        'layout': go.Layout(
            xaxis = {'type':'log', 'title':x_value, 'color':'black'},
            yaxis = {'title':'Salary', 'color':'black'},
            margin = {'l': 50, 'b': 40, 't': 10, 'r': 10},
            hovermode = 'closest',
            plot_bgcolor = '#DFF0EF',
            paper_bgcolor = '#DFF0EF',
            legend = {'bgcolor':'LightSteelBlue',
            'bordercolor':'Black','borderwidth':1,}
        )
    }

    return figure

@app.callback(
    Output(component_id='comparison-graph', component_property = 'figure'),
    [Input(component_id='player_1', component_property = 'value'),
    Input(component_id='player_2',component_property = 'value')]
)

def update_comparison(player_1,player_2):
    dff = pd.DataFrame()
    dff = dff.append(df[df['Name'] == player_1])
    dff = dff.append(df[df['Name'] == player_2])
    dff.set_index("Name", inplace = True)

    stats = ['MPG', 'PPG','Assists', 'Rebounds', 'Plus/Minus']

    stats1 = []
    stats1.append(dff.loc[player_1,'Minutes_played_per_game'])
    stats1.append(dff.loc[player_1, 'Points_per_game'])
    stats1.append(dff.loc[player_1,'Assists_per_game'])
    stats1.append(dff.loc[player_1, 'Rebounds_per_game'])
    stats1.append(dff.loc[player_1, 'Plus_minus'])

    stats2 = []
    stats2.append(dff.loc[player_2,'Minutes_played_per_game'])
    stats2.append(dff.loc[player_2, 'Points_per_game'])
    stats2.append(dff.loc[player_2,'Assists_per_game'])
    stats2.append(dff.loc[player_2, 'Rebounds_per_game'])
    stats2.append(dff.loc[player_2, 'Plus_minus'])

    data1 = go.Bar(name = player_1.title(), x = stats1, y = stats, orientation = 'h')
    data2 = go.Bar(name = player_2.title(), x = stats2, y = stats, orientation = 'h')

    return {
        'data': [data1,data2],
        'layout': go.Layout(title = 'Comparing {player1} and {player2}'.format(player1 = player_1, player2 = player_2),
                          		plot_bgcolor = '#DFF0EF',
                          		paper_bgcolor = '#DFF0EF',
                          		legend = {'bgcolor':'LightSteelBlue',
                          		'bordercolor':'Black',
                          		'borderwidth':1,
                          		'font':dict(color = 'Black')},
                          		font = dict(color = 'black') 
                          	)
        }

#Remove the name selected as player 2 from dropdown for player 1
@app.callback(
    Output('player_1','options'),
    [Input('player_2', 'value')]
)

def update_player_1(player2):
    names  = []
    for name in df.Name:
        if name != player2:
            names.append(name)

    options = [{'label':i, 'value':i} for i in names]

    return options

#Remove the name selected as player 1 from dropdown for player 2
@app.callback(
    Output('player_2','options'),
    [Input('player_1', 'value')]
)

def update_player_2(player1):
    names  = []
    for name in df.Name:
        if name != player1:
            names.append(name)

    options = [{'label':i, 'value':i} for i in names]

    return options

if __name__ == '__main__':
    app.run_server(debug=True)
