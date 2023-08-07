# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import mysql_utils as mysql
import mongodb_utils as mongodb
import neo4j_utils as neo4j
import traceback

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)

university_dropdown_data = mysql.university_dropdown()

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('University Faculty Directory', className="text-primary text-center fs-3 mb-3 mt-3")
    ]),

    dbc.Row([
        dcc.Dropdown(options=university_dropdown_data, value=12, id="university-dropdown")
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.Div('Faculty Count', className="text-primary text-center fs-3"),
            html.Div(className="text-primary text-center fs-1", id="faculty-count")
        ], style={
            "margin-left": "10px",
            "border": "2px solid #007BFF",
            "border-radius": "10px",
            "padding": "10px",
            "height": "100px",
        }, width=2),
        
        dbc.Col([
            dash_table.DataTable(data=[], columns=[
                {'name': 'Name', 'id': 'Name'},
                {'name': 'Position', 'id': 'Position'},
                {'name': 'Email', 'id': 'Email'},
                {'name': 'Phone', 'id': 'Phone'},
            ], 
            page_size=10, 
            style_cell={
                'maxWidth': '200px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'whiteSpace': 'normal'
            },
            style_table={'overflowX': 'auto'},
            id="faculty-table",
            editable=True)
        ], style={
            "margin-left": "10px",
            "border": "2px solid #007BFF",
            "border-radius": "10px",
            "padding": "10px"
        }, width=9)
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.Div('Insert Faculty', className="text-primary text-center fs-3"),
            
            dbc.Form([
               dbc.Label("Name:"),
               dbc.Input(id='name-input', type='text', placeholder='Enter name...', required=True, className="mb-3"),
               dbc.Label("Position:"),
               dbc.Input(id='position-input', type='text', placeholder='Enter position...', required=True, className="mb-3"),
               dbc.Label("Email:"),
               dbc.Input(id='email-input', type='text', placeholder='Enter Email...', required=True, className="mb-3"),
               dbc.Label("Phone #:"),
               dbc.Input(id='phone-input', type='text', placeholder='Enter phone #...', required=True, className="mb-3"),
               dbc.Label("University Affiliation"),
               dcc.Dropdown(id='university-input', options=university_dropdown_data, className="mb-3"),
               dbc.Button('Submit', id='submit-button', color='primary', className="mb-3"),
            ]),
            html.Div(id='form-submitted', className="text-primary text-center fs-5")

        ], style={
            "margin-left": "10px",
            "border": "2px solid #007BFF",
            "border-radius": "10px",
            "padding": "10px"
        }, width=3),

        dbc.Col([

            dbc.Row([
                html.Div('Select Faculty', className="text-primary text-center fs-3 mb-3 mt-3")
            ]),

            dbc.Row([
                dcc.Dropdown(options=[], id="faculty-dropdown")
            ], className="mb-3"),

            dbc.Row([
                html.Div('Faculty Keywords', className="text-primary text-center fs-3 mb-3 mt-3", style={'textDecoration': 'underline'})
            ], className="mb-3"),

            dbc.Row([
                html.Div(className="text-primary text-center fs-3", id='keyword-list')
            ], className="mb-3"),

            dbc.Row([
                html.Div('Faculty Publication Count', className="text-primary text-center fs-3 mb-3 mt-3", style={'textDecoration': 'underline'})
            ], className="mb-3"),

            dbc.Row([
                html.Div(className="text-primary text-center fs-3", id='publication-count')
            ], className="mb-3"),
            
        ], style={
            "margin-left": "10px",
            "border": "2px solid #007BFF",
            "border-radius": "10px",
            "padding": "10px"
        }, width=7)

    ], className="mb-3")


], fluid=True)

# Add controls to build the interaction
@callback(
    Output(component_id='faculty-count', component_property='children'),
    Input(component_id='university-dropdown', component_property='value')
)
def update_faculty_count(univ_id):
    print(mysql.faculty_count(univ_id))
    return mysql.faculty_count(univ_id)

@callback(
    Output(component_id='faculty-table', component_property='data'),
    Input(component_id='university-dropdown', component_property='value'),
)
def update_faculty_table(univ_id):
    data = mysql.faculty_table(univ_id)
    return data

@callback(
    Output(component_id='faculty-dropdown', component_property='options'),
    Input(component_id='university-dropdown', component_property='value'),
)
def update_faculty_dropdown(univ_id):
    data = mysql.faculty_dropdown(univ_id)
    return data

@callback(
        Output(component_id='keyword-list', component_property='children'),
        Output(component_id='publication-count', component_property='children'),
        Input(component_id='university-dropdown', component_property='value'),
        Input(component_id='faculty-dropdown', component_property='value')
)
def update_keyword_and_publication(univ_id, name):
    keyword_data = mongodb.get_keywords(univ_id, name)
    publication_data = neo4j.get_publication_count(name)
    return keyword_data, publication_data

@callback(
    Output(component_id='form-submitted', component_property='children'),
    Output(component_id='name-input', component_property='value'),
    Output(component_id='position-input', component_property='value'),
    Output(component_id='email-input', component_property='value'),
    Output(component_id='phone-input', component_property='value'),
    Output(component_id='university-input', component_property='value'),
    Input(component_id='submit-button', component_property='n_clicks'),
    [State('name-input', 'value'),
     State('position-input', 'value'),
     State('email-input', 'value'),
     State('phone-input', 'value'),
     State('university-input', 'value')]
)
def insert_into_faculty(n_clicks, name, position, email, phone, univ_affiliation):
    if n_clicks is None:
        raise PreventUpdate
    
    if not all([name, position, email, phone, univ_affiliation]):
        return html.Div("Please fill out all required fields."), name, position, email, phone, univ_affiliation
    
    try:
        mysql.insert_faculty(name, position, email, phone, univ_affiliation)
    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        return html.Div("Error inserting data: " + str(Exception)), name, position, email, phone, univ_affiliation

    return html.Div("Faculty Inserted!"), '', '', '', '', ''


# Run the app
if __name__ == '__main__':
    app.run(debug=True)

