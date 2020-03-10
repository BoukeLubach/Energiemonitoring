
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from plant_dashboards.dash_apps.sqltags import get_sql_data
import dash
from datetime import datetime as dt


steam_30barG = {
        'pressure' : {'value': 30, 'uom' : 'barg'},
        'temperature' : {'value' : 240, 'uom':'degC'},
        'enthalpy': {'value': 3100 , 'uom':'kJ/kgK'},
        'energy': {'value': 2700 , 'uom':'kJ/kgK'}
        }

steam_3barG = {
        'pressure' : {'value': 3, 'uom' : 'barg'},
        'temperature' : {'value' : 160, 'uom':'degC'},
        'enthalpy': {'value': 3000 , 'uom':'kJ/kgK'},
        'energy': {'value': 2600 , 'uom':'kJ/kgK'}
        }


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('poly_dashapp', external_stylesheets=external_stylesheets)


app_local = dash.Dash()

##1601 column, tags in order:
##16F02 hot oil flow
##16T07 hot oil temp
##16F01 reflux
##16F07 bottom flow
##16F06 column feed

tags = ['81F21', '81F61']
table = 'steam'
dryers = get_sql_data(tags, table)


dryers['total steamenergy'] = (dryers['81F21']+dryers['81F61'])/1000



app.layout = html.Div([
    html.H1('Steam energy poly dryers'),
    dcc.Graph(id='steam-poly-bargraph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Dropdown(
        id='selection-dropdown',
        options=[
            {'label': 'month', 'value': 'M'},
            {'label': 'week', 'value': 'w'},
            {'label': 'day', 'value': 'd'}
        ],
        value='M'
    ),

])


@app.callback(
               Output('steam-poly-bargraph', 'figure'),
              [Input('selection-dropdown', 'value')])
def display_value(value):
    
    y = dryers['total steamenergy'].resample(value).sum()
    
    
    
    graph = go.Bar(
        x=y.index,
        y=y,
        name='Manipulate Graph'
    )

    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        #xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(title = 'ton', range=[0, max(y)]),
        font=dict(color='white')
    )

    return {'data': [graph], 'layout': layout}


if __name__ == '__main__':
    app_local.run_server(debug=True)
