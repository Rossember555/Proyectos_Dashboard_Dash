import subprocess
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output, State
from data_cleaner import DataCleaner

# --- 1. Carga y limpieza de datos ---
df = pd.read_csv('datos.csv')
cleaner = DataCleaner(df, 'email', 'fecha', '%Y-%m-%d')
df_clean = cleaner.clean_email().clean_date().get_clean_data()
df_clean['dominio'] = df_clean['email'].dropna().apply(lambda e: e.split('@')[-1])

# --- 2. Función auxiliar para invocar a Gemini CLI ---
def query_gemini(prompt: str) -> str:
    """
    Envía el prompt a Gemini vía CLI y devuelve la respuesta.
    Asegúrate de tener autenticado tu CLI con `gemini auth login`.
    """
    proc = subprocess.run(
        ['gemini', 'chat', '--model=chat-bison-001', '--prompt-through-stdin'],
        input=prompt,
        text=True,
        capture_output=True,
        timeout=15
    )
    return proc.stdout.strip()

# --- 3. Inicializar la app Dash ---
app = Dash(__name__)

# --- 4. Layout ---
app.layout = html.Div([
    html.H1('📊 Dashboard + 🤖 Chatbot con Gemini'),
    # ------ Tabla y filtros existentes ------
    dash_table.DataTable(
        id='tabla',
        columns=[{'name': i, 'id': i} for i in df_clean.columns],
        data=df_clean.to_dict('records'),
        page_size=10,
        filter_action='native',
        sort_action='native',
    ),
    html.Label('Dominio de correo:'),
    dcc.Dropdown(
        id='filtro-dominio',
        options=[{'label': d, 'value': d} for d in sorted(df_clean['dominio'].dropna().unique())],
        placeholder='Selecciona un dominio'
    ),

    # ------ Gráficos existentes ------
    html.Div([
        dcc.Graph(id='grafico-fechas'),
        dcc.Graph(id='grafico-notas'),
        dcc.Graph(id='grafico-dominios'),
        dcc.Graph(id='grafico-acumulado'),
    ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'marginTop': '40px'}),

    html.H2('💬 Chatbot de datos'),
    # ------ Chatbot UI ------
    dcc.Textarea(
        id='chat-input',
        placeholder='Escribe tu pregunta sobre los datos...',
        style={'width': '100%', 'height': 80}
    ),
    html.Button('Enviar', id='btn-send', n_clicks=0),
    html.Div(id='chat-history', style={
        'whiteSpace': 'pre-wrap', 'backgroundColor': '#f9f9f9',
        'padding': '10px', 'borderRadius': '5px', 'marginTop': '10px'
    })
])

# --- 5. Callbacks ------
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

    # Gráfico de barras por fecha
    conteo_fecha = dff['fecha'].value_counts().sort_index()
    fig_fechas = {
        'data': [{'x': conteo_fecha.index, 'y': conteo_fecha.values, 'type': 'bar'}],
        'layout': {'title': 'Registros por fecha'}
    }
    # Histograma de notas
    fig_notas = {
        'data': [{'x': dff['nota'], 'type': 'histogram'}],
        'layout': {'title': 'Distribución de notas'}
    }
    # Pie de dominios
    conteo_dom = dff['dominio'].value_counts()
    fig_dom = {
        'data': [{'labels': conteo_dom.index, 'values': conteo_dom.values, 'type': 'pie', 'hole': .3}],
        'layout': {'title': 'Porcentaje de dominios'}
    }
    # Línea acumulada
    acumulado = conteo_fecha.cumsum()
    fig_acum = {
        'data': [{'x': acumulado.index, 'y': acumulado.values, 'type': 'line'}],
        'layout': {'title': 'Registros acumulados'}
    }

    return dff.to_dict('records'), fig_fechas, fig_notas, fig_dom, fig_acum

@app.callback(
    Output('chat-history', 'children'),
    Input('btn-send', 'n_clicks'),
    State('chat-input', 'value'),
    State('chat-history', 'children')
)
def interactuar_chat(n_clicks, pregunta, historia):
    if n_clicks and pregunta:
        prompt = (
            "Eres un asistente que conoce un DataFrame con columnas "
            "'id', 'nombre', 'email', 'fecha', 'nota', 'dominio'.\n"
            f"Pregunta del usuario: {pregunta}\n"
            "Responde de forma concisa y clara."
        )
        respuesta = query_gemini(prompt)
        nueva_historia = (historia or '') + f"\n\n🤔 Tú: {pregunta}\n💡 Gemini: {respuesta}"
        return nueva_historia
    return historia

if __name__ == '__main__':
    app.run(debug=True)
