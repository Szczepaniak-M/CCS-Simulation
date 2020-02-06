import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

input_layout = html.Div([
    html.Div(
        html.Center(
            [html.H1('TEMPOMAT'),
             html.H2('Stwórz swoje auto')]),

    ),
    html.Br(),
    html.Div([
        html.Center(html.Div([

            html.H4('Typ samochodu:'),
            dcc.RadioItems(
                id='type',
                options=[
                    {'label': 'Sportowy', 'value': 'sport'},
                    {'label': 'Miejski', 'value': 'city'},
                    {'label': 'SUV', 'value': 'suv'},
                    {'label': 'Terenowy   ', 'value': 'offroad'}
                ],
                value='sport',
                labelStyle=dict(
                    display='inline-block',
                    fontSize=20,
                    padding=7,
                )
            ),
            html.H4('Masa [kg]'),
            dcc.Input(
                id='mass',
                type='number',
                debounce=True,
                value=0,
                min=0,
            ),
            html.Br(),
            html.H4('Moc samochodu [KM]'),
            dcc.Input(
                id='power',
                type='number',
                debounce=True,
                value=0,
                min=0,
            ),
            html.H4('Powierzchnia czołowa samochodu[m\u00b2]'),
            dcc.Input(
                id='area',
                type='number',
                debounce=True,
                value=0,
                min=0,
                max=4,
                step=0.05,
            ),
            html.Br(),
            html.Br(),
            dcc.Link(html.Button(
                id='next_btn',
                n_clicks=0,
                children='Dalej',
                style=dict(backgroundColor='#ffffff')
            ), href='/graph'),
            html.Br(),
            html.Br(), ],
            style=dict(
                backgroundColor='#7272f2',
                color='#ffffff',
                width='70%',
                height='110%',

            )
        )),
        html.Div([
            html.Img(id='car-image', src='/assets/sport.jpg'),
            html.Br()
        ], style=dict(padding=25, marginLeft=-40))],
        style=dict(
            columnCount=2,
        ),
    ),

],
    style=dict(
        backgroundColor='#5252f2',
        color='#ffffff',
        position='fixed',
        width='100%',
        height='100%',
        top='0px',
        left='0px',
        verticalAlign='middle',
    ))


@app.callback(Output('car-image', 'src'),
              [Input('type', 'value')])
def display_page(option):
    if option == 'sport':
        return app.get_asset_url('sport.jpg')
    elif option == 'city':
        return app.get_asset_url('miejski.png')
    elif option == 'suv':
        return app.get_asset_url('suv.jpg')
    else:
        return app.get_asset_url('terenowy.jpg')


@app.callback(Output('data-input', 'data'),
              [Input('type', 'value'),
               Input('area', 'value'),
               Input('mass', 'value'),
               Input('power', 'value')])
def store_value(kind, area, mass, power):
    if kind == 'sport':
        coefficient = 0.30
    elif kind == 'city':
        coefficient = 0.25
    elif kind == 'suv':
        coefficient = 0.35
    else:
        coefficient = 0.43

    if area == '':
        area = 0

    if mass == '':
        mass = 0

    if power == '':
        power = 0
    return {'coefficient': coefficient,
            'area': area,
            'mass': mass,
            'power': power}
