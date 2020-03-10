
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
#from django_plotly_dash import DjangoDash
import pandas as pd
from sqltags import get_sql_data
import dash
from datetime import datetime as dt


hotags = ['Recovery_total','PPD_total','TDC_total']
ngtags = ['Furnaces_total']
 

hodata = get_sql_data(hotags, 'hopower')
ngdata = get_sql_data(ngtags, 'ngpower')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = DjangoDash('hotoil_dashapp', external_stylesheets=external_stylesheets)


app = dash.Dash()


app.layout = html.Div([
    html.H1('Oil consumption overview'),
    dcc.Graph(id='hot-oil-power', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
#    dcc.DatePickerRange(
#        id='date-picker-range',
#        min_date_allowed=dt(2019, 1, 1),
#        max_date_allowed=dt(2020, 1, 1),
#        initial_visible_month = dt(2019,1,1),
#        start_date = dt(2019,1,1),
#        end_date = dt(2019,2,1),
#        start_date_placeholder_text="Start Period",
#        end_date_placeholder_text="End Period",
#    ),
    dcc.Dropdown(
        id='interval-selection-dropdown',
        options=[
            {'label': 'month', 'value': 'M'},
            {'label': 'week', 'value': 'w'},
            {'label': 'day', 'value': 'd'}
        ],
        value='M'
    ),
    
    html.H1('Oil production overview'),
    dcc.Graph(id='hot-oil-production', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),

    dcc.Dropdown(
        id='interval-selection-dropdown2',
        options=[
            {'label': 'month', 'value': 'M'},
            {'label': 'week', 'value': 'w'},
            {'label': 'day', 'value': 'd'}
        ],
        value='M'
    ),
])


@app.callback(
               Output('hot-oil-power', 'figure'),
              [Input('interval-selection-dropdown', 'value')])
def hot_oil_consumption(value):
       
    y = hodata['Recovery_total'].resample(value).sum()
    y2 = hodata ['PPD_total'].resample(value).sum()
    y3 = hodata['TDC_total'].resample(value).sum()
    
    
    trace1 = go.Bar(
        x=y.index,
        y = y,
        name='Recovery hot oil consumption',
        marker_color='rgb(93,127,255)'
    )
    trace2 = go.Bar(
        x=y.index,
        y = y2,
        name='PPD hot oil consumption',
        marker_color='rgb(252,193,0)'
    )
    trace3 = go.Bar(
        x=y.index,
        y = y3,
        name='TDC hot oil consumption',
        marker_color='rgb(71,186,193)'
    )
    
    data = [trace1, trace2, trace3]


    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        #xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(title = 'kWh', range=[0, (max(y+y2+y3))*1.2]),
        font=dict(size=24, color='white'),
        margin = go.layout.Margin(
                    l=100,
                    r=50,
                    b=50,
                    t=50,
                    pad=4
                ),
    )

    figure = go.Figure(data=data, layout=layout)
    figure.update_layout(barmode='stack')
    return figure


@app.callback(
               Output('hot-oil-production', 'figure'),
              [Input('interval-selection-dropdown2', 'value')])
def hot_oil_production(value):
      
       
    y = (hodata['Recovery_total'] + hodata ['PPD_total'] + hodata['TDC_total']).resample(value).sum()
    y2 = ngdata['Furnaces_total'].resample(value).sum()
    
    
    trace1 = go.Bar(
        x = y.index,
        y = y,
        name='Hot oil consumption'
    )
    
    trace2 = go.Bar(
        x = y2.index,
        y = y2,
        name='NG to furnaces'
    )

    
    data = [trace1, trace2]


    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        #xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(title = 'kWh', range=[0, (max(y+y2))*1.2]),
        font=dict(size=24, color='white'),
        margin = go.layout.Margin(
                    l=100,
                    r=50,
                    b=50,
                    t=50,
                    pad=4
                ),
    )

    figure = go.Figure(data=data, layout=layout)
#    figure.update_layout(barmode='stack')
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
