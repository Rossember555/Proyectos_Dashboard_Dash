import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output
from data_cleaner import DataCleaner

# 1. Carga y limpieza de datos
df = pd.read_csv('datos.csv')
cleaner = DataCleaner(df, 'email', 'fecha', '%Y-%m-%d')
df_clean = cleaner.clean_email().clean_date().get_clean_data()

# Extraer dominio de email en una columna para facilitar el análisis
df_clean['dominio'] = df_clean['email'].dropna().apply(lambda e: e.split('@')[-1])

# 2. Inicializar la app
app = Dash(__name__)

# 3. Layout con más gráficos
app.layout = html.Div([
    html.H1('Dashboard de Datos Limpios'),
    html.Div([
        # Tabla interactiva
        dash_table.DataTable(
            id='tabla',
            columns=[{'name': i, 'id': i} for i in df_clean.columns],
            data=df_clean.to_dict('records'),
            page_size=10,
            filter_action='native',
            sort_action='native',
        ),
        # Filtro por dominio de email
        html.Div([
            html.Label('Dominio de correo:'),
            dcc.Dropdown(
                id='filtro-dominio',
                options=[{'label': d, 'value': d} for d in sorted(df_clean['dominio'].dropna().unique())],
                placeholder='Selecciona un dominio'
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ]),
    # Contenedor de gráficos
    html.Div([
        dcc.Graph(id='grafico-fechas'),
        dcc.Graph(id='grafico-notas'),
        dcc.Graph(id='grafico-dominios'),
        dcc.Graph(id='grafico-acumulado'),
    ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'marginTop': '40px'})
])

# 4. Callbacks
@app.callback(
    Output('tabla', 'data'),
    Output('grafico-fechas', 'figure'),
    Output('grafico-notas', 'figure'),
    Output('grafico-dominios', 'figure'),
    Output('grafico-acumulado', 'figure'),
    Input('filtro-dominio', 'value')
)
def actualizar_dashboard(dominio):
    dff = df_clean.copy()
    if dominio:
        dff = dff[dff['dominio'] == dominio]

    # 4.1. Conteo por fecha (bar)
    conteo_fecha = dff['fecha'].value_counts().sort_index()
    fig_fechas = {
        'data': [{'x': conteo_fecha.index, 'y': conteo_fecha.values, 'type': 'bar'}],
        'layout': {'title': 'Registros por fecha', 'xaxis': {'title': 'Fecha'}, 'yaxis': {'title': 'Cantidad'}}
    }

    # 4.2. Histograma de notas
    fig_notas = {
        'data': [{'x': dff['nota'], 'type': 'histogram'}],
        'layout': {'title': 'Distribución de notas', 'xaxis': {'title': 'Nota'}, 'yaxis': {'title': 'Frecuencia'}}
    }

    # 4.3. Pie chart de dominios
    conteo_dominios = dff['dominio'].value_counts()
    fig_dominios = {
        'data': [{'labels': conteo_dominios.index, 'values': conteo_dominios.values, 'type': 'pie', 'hole': .3}],
        'layout': {'title': 'Porcentaje de dominios de email'}
    }

    # 4.4. Línea de registros acumulados por fecha
    acumulado = conteo_fecha.cumsum()
    fig_acumulado = {
        'data': [{'x': acumulado.index, 'y': acumulado.values, 'type': 'line'}],
        'layout': {'title': 'Registros acumulados', 'xaxis': {'title': 'Fecha'}, 'yaxis': {'title': 'Acumulado'}}
    }

    return dff.to_dict('records'), fig_fechas, fig_notas, fig_dominios, fig_acumulado

if __name__ == '__main__':
    app.run(debug=True)
