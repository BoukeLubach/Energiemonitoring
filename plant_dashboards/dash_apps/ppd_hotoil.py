
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from plant_dashboards.dash_apps.sqltags import get_sql_data
import dash
from datetime import datetime as dt


hot_oil = {
    'cp'                    : {'value': 2.7, 'uom': 'kj/kgK'},
    'density'               : {'value': 750, 'uom': 'kg/m3'},
    'furnace_temperature'   : {'value': 277, 'uom': 'degC'}
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


tags = ['16F02', '16T07', '16F01', '16F07', '16F06', ]
table = 'ppd'
AC1601 = get_sql_data(tags, table)


AC1601['ho consumption'] = AC1601['16F02']*hot_oil['cp']['value']*(hot_oil['furnace_temperature']['value']-AC1601['16T07'])/3600



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
    
    y = AC1601.resample(value).sum()
    
    
    
    graph = go.Bar(
        x=y.index,
        y=y,
        name='Manipulate Graph'
    )

    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        #xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(title = 'ton', range=[0, 2000000]),#max(y)*1.2]),
        font=dict(color='white'),
        margin = go.layout.Margin(
                    l=100,
                    r=40,
                    b=150,
                    t=0,
                    pad=4
                )
    )

    return {'data': [graph], 'layout': layout}


if __name__ == '__main__':
    app_local.run_server(debug=True)
