import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

# --- 1. Crear un archivo CSV de ejemplo (si no existe) ---
# En un escenario real, ya tendrías tu archivo "datos_ventas.csv".
# Este paso es para que el ejemplo sea autoejecutable.
csv_file_path = 'datos_ventas.csv'

if not os.path.exists(csv_file_path):
    print(f"Creando el archivo de ejemplo '{csv_file_path}'...")
    data_para_csv = {
        'Fecha': pd.to_datetime(['2024-06-25', '2024-06-24', '2024-06-25', '2024-06-26', '2024-06-27', '2024-06-26', '2024-06-28', '2024-06-29']),
        'Categoría': ['Ropa', 'Libros', 'Electrónica', 'Ropa', 'Hogar', 'Libros', 'Electrónica', 'Ropa'],
        'Región': ['Sur', 'Norte', 'Sur', 'Oeste', 'Norte', 'Este', 'Sur', 'Norte'],
        'Ventas': [1214.45, 1740.2, 2500.0, 850.75, 1999.99, 950.5, 3100.0, 1500.0],
        'Cantidad': [4, 2, 1, 3, 2, 1, 2, 5],
        'Beneficio': [276.96, 670.71, 850.0, 210.2, 550.0, 320.1, 1050.5, 450.0]
    }
    df_ejemplo = pd.DataFrame(data_para_csv)
    df_ejemplo.to_csv(csv_file_path, index=False, encoding='utf-8')

# --- 2. Cargar y procesar los datos ---
# Se especifica la codificación utf-8 para leer correctamente caracteres como 'í' o 'ó'.
try:
    df = pd.read_csv(csv_file_path, encoding='utf-8')
except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")
    # Si falla, intenta con otra codificación común en Windows
    df = pd.read_csv(csv_file_path, encoding='latin1')

# Convertir la columna 'Fecha' a tipo datetime para un manejo adecuado de las fechas
df['Fecha'] = pd.to_datetime(df['Fecha'])


# --- 3. Crear figuras de Plotly ---
# Gráfico de barras: Ventas totales por Categoría
fig_bar_ventas_categoria = px.bar(
    df.groupby('Categoría')['Ventas'].sum().reset_index(),
    x='Categoría',
    y='Ventas',
    title='Ventas Totales por Categoría 📊',
    labels={'Ventas': 'Total de Ventas ($)', 'Categoría': 'Categoría de Producto'},
    template='plotly_white'
)

# Gráfico de pastel: Distribución de ventas por Región
fig_pie_ventas_region = px.pie(
    df,
    names='Región',
    values='Ventas',
    title='Distribución de Ventas por Región 🌎',
    hole=0.3, # Crea un gráfico de dona
    template='plotly_white'
)


# --- 4. Inicializar la aplicación Dash ---
app = dash.Dash(__name__)
server = app.server

# --- 5. Definir el Layout de la aplicación ---
app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f4f4f4', 'padding': '20px'},
    children=[
        html.H1(
            'Tablero de Análisis de Ventas 📈',
            style={'textAlign': 'center', 'color': '#333'}
        ),
        html.Hr(),

        # Contenedor para los gráficos estáticos (lado a lado)
        html.Div(className='row', children=[
            html.Div(
                dcc.Graph(figure=fig_bar_ventas_categoria),
                className='six columns',
                style={'display': 'inline-block', 'width': '49%'}
            ),
            html.Div(
                dcc.Graph(figure=fig_pie_ventas_region),
                className='six columns',
                style={'display': 'inline-block', 'width': '49%'}
            )
        ]),

        html.Hr(),

        # Contenedor para el gráfico interactivo
        html.Div(className='row', children=[
            html.H3('Análisis de Ventas por Región a lo largo del Tiempo 🕰️', style={'textAlign': 'center', 'color': '#333'}),

            # Menú desplegable para seleccionar la región
            dcc.Dropdown(
                id='selector-region',
                options=[{'label': region, 'value': region} for region in df['Región'].unique()],
                value=df['Región'].unique()[0], # Valor inicial
                clearable=False,
                style={'width': '50%', 'margin': '0 auto'}
            ),

            # Gráfico de líneas que se actualizará con el callback
            dcc.Graph(id='grafico-ventas-tiempo')
        ])
    ]
)


# --- 6. Definir el Callback para la interactividad ---
@app.callback(
    Output('grafico-ventas-tiempo', 'figure'),
    Input('selector-region', 'value')
)
def actualizar_grafico_lineas(region_seleccionada):
    """
    Esta función se activa cada vez que el valor del dropdown 'selector-region' cambia.
    Filtra el DataFrame por la región seleccionada y devuelve un nuevo gráfico de líneas.
    """
    # Filtrar el dataframe basado en la región seleccionada
    df_filtrado = df[df['Región'] == region_seleccionada]

    # Crear el gráfico de líneas con los datos filtrados
    fig = px.line(
        df_filtrado,
        x='Fecha',
        y='Ventas',
        title=f'Evolución de Ventas en la Región: {region_seleccionada}',
        markers=True, # Muestra puntos en los datos
        labels={'Ventas': 'Ventas ($)', 'Fecha': 'Fecha'},
        template='plotly_white'
    )
    
    fig.update_layout(
        title_x=0.5 # Centrar el título
    )
    
    return fig


# --- 7. Ejecutar el servidor de la aplicación ---
if __name__ == '__main__':
    app.run(debug=True)