import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State


df = pd.read_csv('https://bit.ly/elements-periodic-table')
def identity(x): return x
options = []
for col in df.columns:
    options.append({'label':'{}'.format(col, col), 'value':col})


app = dash.Dash(__name__)

app.layout = app.layout = html.Div([
        html.Label("Select a feature from drop-down for row index"),
        dcc.Dropdown(
            id = 'my_dropdown1',
            options= options,
            value='Period'
        ),
        html.Label(id='my_label1'),

        html.Label("Select a feature from drop-down for column index"),
        dcc.Dropdown(
            id = 'my_dropdown2',
            options= options,
            value='Group'
        ),
        html.Label(id='my_label2'),

        html.Label("Select a feature from drop-down for table values"),
        dcc.Dropdown(
            id = 'my_dropdown3',
            options= options,
            value='AtomicMass'
        ),
        html.Label(id='my_label3'),

        html.Label("Select a feature from drop-down for aggregate function options"),
        dcc.Dropdown(
            id = 'my_dropdown4',
            options= [
    {"label": "mean", "value": 'mean'},
    {"label": "sum", "value": 'sum'},
    {"label": "count", "value": "count"},
],
            value= 'mean'
        ),
        html.Label(id='my_label4'),

        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':16}
        ),
        
    dash_table.DataTable(
    id='table',
    columns=[{"name": str(i), "id": str(i)} for i in df.columns],
    data=df.to_dict('records'),
    )
])

@app.callback(
    [Output(component_id='table', component_property='columns'),
    Output(component_id='table', component_property='data')],
    Input(component_id='submit-button', component_property='n_clicks'),
    State(component_id='my_dropdown1', component_property='value'),
    State(component_id='my_dropdown2', component_property='value'),
    State(component_id='my_dropdown3', component_property='value'),
    State(component_id='my_dropdown4', component_property='value'),
)

def updateTable(n_clicks, input_my_dropdown1,input_my_dropdown2,input_my_dropdown3,input_my_dropdown4 ):
    if (n_clicks == 0):
        return ([{"name": str(i), "id": str(i)} for i in df.columns],df.to_dict('records'))
    else: 
        df2 = df.pivot_table(
        index=input_my_dropdown1,
        columns=input_my_dropdown2, 
        values=input_my_dropdown3,
        aggfunc=input_my_dropdown4,)
        df2.reset_index(level=0, inplace=True)
        return (
            [{"name": str(i), "id": str(i)} for i in df2.columns],
            df2.to_dict('records'))

    
        


app.run_server(debug=True, host="0.0.0.0")