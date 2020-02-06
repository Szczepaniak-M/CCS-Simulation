import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps.functions import make_data

graph_layout = html.Div([
    html.Center(html.H1('TEMPOMAT')),
    html.Br(),
    html.Div([
        html.Div(html.Center([
            html.H4('Rodzaj symulacji'),
            dcc.RadioItems(
                id='simulation',
                options=[
                    {'label': 'Statyczna', 'value': 1},
                    {'label': 'Czasu rzeczywistego', 'value': 0},
                ],
                value=1,
                labelStyle=dict(
                    display='inline-block',
                    fontSize=20,
                    padding=7,
                )
            ),
            html.H4('Prędkość początkową [km/h]'),
            dcc.Input(
                id='velocity-start',
                placeholder='Prędkość początkowa',
                type='number',
                value=40,
                debounce=True,
                min=40,
                max=350,
            ),
            html.H4('Prędkość docelowa [km/h]'),
            dcc.Input(
                id='velocity',
                placeholder='Prędkość',
                type='number',
                value=40,
                debounce=True,
                min=40,
                max=350,
            ),
            html.Br(),
            html.Div([html.H4('Czas symulacji statycznej'),
                      dcc.Input(
                          id='time',
                          placeholder='Czas symulacji',
                          type='number',
                          value=0,
                          debounce=True,
                          min=0,
                      ),
                      html.Br()],
                     id='static-div'),
            html.Br(),
            html.Div([html.Button(id='start-btn', children='Start', n_clicks=0,
                                  style=dict(backgroundColor='#ffffff', display='inline-block')),
                      " ",
                      html.Button(id='reset-btn', children='Reset', n_clicks=0),
                      html.Br(),
                      html.Br()],
                     style=dict(
                         display='inline-block',
                     ), ),
            html.Br(),
        ],
            id='input',
            style=dict(
                backgroundColor='#7272f2',
                color='#ffffff',
                width='20%',
                marginLeft='2%',
                float='left',
                marginTop='0%'
            )
        )),
        html.Div([
            dcc.Interval(
                id='interval-component',
                interval=1000,  # in milliseconds
                n_intervals=0),
            dcc.Graph(
                id='graph',
                style=dict(
                    height='100%',
                )
            ),
            html.Br(),
            html.Br(),
            html.Br()
        ], style=dict(
            float='left',
            clear='right',
            padding=25,
            width='74%',
        )), ], ),

    dcc.Link(html.Button('Powrót do wyboru samochodu', id='back-btn', style=dict(backgroundColor='#ffffff')),
             href='/',
             style=dict(marginLeft='2%')
             ),
    dcc.Store(id='data-graph', storage_type='session'),
    dcc.Store(id='counters', storage_type='session'), ],

    style=dict(
        backgroundColor='#5252f2',
        color='#ffffff',
        position='fixed',
        width='100%',
        height='100%',
        top='0px',
        left='0px',
        verticalAlign='middle',
    )
)


@app.callback(Output('counters', 'data'),
              [Input('start-btn', 'n_clicks'),
               Input('reset-btn', 'n_clicks'),
               Input('simulation', 'value'),
               Input('interval-component', 'n_intervals')],
              [State('counters', 'data')])
def store_value(start_click, reset_click, static, n_time, prev_data):
    if prev_data is not None:
        if prev_data['real_start'] != start_click:
            prev_data['real_start'] += 1
            update_start = True
        else:
            update_start = False

        if prev_data['real_reset'] != reset_click:
            prev_data['real_reset'] += 1
            update_reset = True
        else:
            update_reset = False

        if prev_data['real_time'] != n_time:
            prev_data['real_time'] += 1
            update_time = True
        else:
            update_time = False

        if prev_data['prev_state'] != static:
            prev_data['prev_state'] += 1
            prev_data['prev_state'] = prev_data['prev_state'] % 2
            update_state = True
        else:
            update_state = False

        if static:
            prev_data['current_start'] = 0
            prev_data['current_time'] = 0
        else:
            if update_start:
                prev_data['current_start'] += 1
            if update_reset:
                prev_data['current_start'] = 0
                prev_data['current_time'] = 0
            if update_time:
                prev_data['current_time'] += 1
            if update_state:
                prev_data['current_start'] = 0
                prev_data['current_time'] = 0
        return prev_data
    else:
        data = {'real_start': 0,
                'current_start': 0,
                'real_reset': 0,
                'current_reset': 0,
                'real_time': 0,
                'current_time': 0,
                'prev_state': 0,
                }
    return data


@app.callback(Output('counters', 'clear_data'),
              [Input('back-btn', 'n_clicks')])
def reset_store(n):
    return True


@app.callback(Output('reset-btn', 'style'),
              [Input('simulation', 'value')])
def show(static):
    if static:
        return {'display': 'none'}
    else:
        return {'display': 'inline-block',
                'backgroundColor': '#ffffff'}


@app.callback(Output('static-div', 'style'),
              [Input('simulation', 'value')])
def show(static):
    if not static:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback(Output('input', 'style'),
              [Input('simulation', 'value')])
def show(static):
    if static:
        return dict(
            backgroundColor='#7272f2',
            color='#ffffff',
            width='20%',
            marginLeft='2%',
            float='left',
            marginTop='0%'
        )
    else:
        return dict(
            backgroundColor='#7272f2',
            color='#ffffff',
            width='20%',
            marginLeft='2%',
            float='left',
            marginTop='2%'
        )


@app.callback(Output('interval-component', 'interval'),
              [Input('counters', 'data')])
def start(data):
    if data['current_start'] % 2 == 0:
        return 10000000
    else:
        return 1000


@app.callback(Output('start-btn', 'children'),
              [Input('counters', 'data')])
def start(data):
    if data['current_start'] % 2 == 0:
        return 'Start'
    else:
        return 'Stop'


@app.callback(Output('data-graph', 'data'),
              [Input('counters', 'data')],
              [State('velocity-start', 'value'),
               State('time', 'value'),
               State('velocity', 'value'),
               State('data-input', 'data'),
               State('data-graph', 'data'),
               State('simulation', 'value')])
def new_data(counters, velocity_start, time, velocity, input_data, graph_data, static):
    if static:
        if time > 0:
            for i in range(time * 100):
                graph_data = make_data(i, time, velocity_start, velocity, input_data, graph_data)
        else:
            graph_data = make_data(0, 20, velocity_start, velocity, input_data, graph_data)
    else:
        if counters['current_time'] > 0:
            for i in range(100):
                graph_data = make_data(counters['current_time'] * 100 + i, 20, velocity_start, velocity, input_data,
                                       graph_data)
        else:
            graph_data = make_data(counters['current_time'], 20, velocity_start, velocity, input_data, graph_data)
    return graph_data


@app.callback(Output('graph', 'figure'),
              [Input('data-graph', 'data')])
def make_plot(data):
    figure = dict(
        data=[
            dict(
                x=data['x'],
                y=data['power'],
                name='% użycia mocy silnika',
                mode='lines',
                marker=dict(
                    color='#37536d'
                ),
                yaxis='y2',
            ),
            dict(
                x=data['x'],
                y=data['velocity'],
                name='Prędkość',
                mode='lines',
                marker=dict(
                    color='#1a76ff'
                ),

            )
        ],
        layout=dict(
            title='',
            showlegend=True,
            xaxis=dict(
                title='Czas',
                range=data['x_range'],
                titlefont=dict(
                    colorfont='#000000'
                ),
                tickfont=dict(
                    colorfont='#000000'
                ),
            ),
            yaxis=dict(
                title='Prędkość',
                range=data['y_range'],
                titlefont=dict(
                    colorfont='#000000'
                ),
                tickfont=dict(
                    colorfont='#000000'
                ),
                tickformat='.0f'
            ),
            yaxis2=dict(
                title='% użycia mocy silnika',
                anchor='x',
                overlaying='y',
                side='right',
                range=[0, 1],
                tickformat=',.0%',
                tickfont=dict(
                    colorfont='#000000'
                ),
            ),
            legend=dict(
                x=0,
                y=1.1,
                orientation='h',
            ),
            margin=dict(l=60, r=60, t=60, b=60)
        )
    )
    return figure
