# 1. IMPORTAR LIBRERÍAS NECESARIAS
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# 2. CARGAR LOS DATOS DESDE EL ARCHIVO CSV
# Asegúrate de que el archivo 'ventas_agricolas_sinteticas.csv' esté en la misma carpeta.
try:
    df = pd.read_csv("ventas_agricolas_sinteticas.csv")
except FileNotFoundError:
    print("Error: El archivo 'ventas_agricolas_sinteticas.csv' no fue encontrado.")
    # Creamos un DataFrame vacío para que la aplicación no falle al iniciar.
    df = pd.DataFrame({
        'Producto': [], 'Departamento': [], 'Precio_KG': [], 
        'Cantidad_KG': [], 'Ventas_Totales': []
    })

# 3. INICIALIZAR LA APLICACIÓN DE DASH
app = dash.Dash(__name__)

# --- DEFINICIÓN DE LA INTERFAZ DEL DASHBOARD (LAYOUT) ---
app.layout = html.Div(children=[
    # Título principal del dashboard
    html.H1(
        children='📊 Dashboard de Ventas Agrícolas',
        style={'textAlign': 'center', 'color': '#2c3e50'}
    ),

    # Descripción o subtítulo
    html.Div(
        children='Análisis interactivo de ventas de productos por departamento.',
        style={'textAlign': 'center', 'marginBottom': '30px'}
    ),

    # Contenedor para el filtro de departamento
    html.Div([
        html.Label('Selecciona Departamento(s):', style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='filtro-departamento',
            options=[{'label': dep, 'value': dep} for dep in df['Departamento'].unique()],
            value=df['Departamento'].unique().tolist(),  # Selecciona todos por defecto
            multi=True,  # Permite selección múltiple
            placeholder="Selecciona uno o varios departamentos"
        )
    ], style={'padding': '10px 20px'}),

    # Contenedor para los gráficos (organizados en una fila)
    html.Div([
        # Gráfico de barras
        dcc.Graph(
            id='grafico-ventas-producto'
        ),
        # Gráfico de dispersión
        dcc.Graph(
            id='grafico-precio-cantidad'
        )
    ], style={'display': 'flex', 'flexDirection': 'row'}),
    
    # Nuevo gráfico: Distribución de ventas por departamento
    dcc.Graph(
        id='grafico-ventas-departamento'
    )
])

# --- DEFINICIÓN DE LA INTERACTIVIDAD (CALLBACK) ---
@app.callback(
    [Output('grafico-ventas-producto', 'figure'),
     Output('grafico-precio-cantidad', 'figure'),
     Output('grafico-ventas-departamento', 'figure')],
    [Input('filtro-departamento', 'value')]
)
def actualizar_graficos(departamentos_seleccionados):
    # Si no se selecciona ningún departamento, usar el DataFrame completo
    if not departamentos_seleccionados:
        filtered_df = df
    else:
        # Filtrar el DataFrame según los departamentos seleccionados en el dropdown
        filtered_df = df[df['Departamento'].isin(departamentos_seleccionados)]

    # 1. GRÁFICO DE BARRAS: VENTAS TOTALES POR PRODUCTO
    # Agrupamos por producto y sumamos las ventas para tener un total consolidado
    ventas_por_producto = filtered_df.groupby('Producto')['Ventas_Totales'].sum().reset_index()
    fig_barras = px.bar(
        ventas_por_producto,
        x='Producto',
        y='Ventas_Totales',
        title='Ventas Totales por Producto',
        labels={'Ventas_Totales': 'Ventas Totales (COP)', 'Producto': 'Producto'},
        color='Producto',
        template='plotly_white'
    )
    fig_barras.update_layout(title_x=0.5) # Centrar título

    # 2. GRÁFICO DE DISPERSIÓN: PRECIO VS. CANTIDAD
    fig_dispersion = px.scatter(
        filtered_df,
        x='Cantidad_KG',
        y='Precio_KG',
        size='Ventas_Totales',  # El tamaño de la burbuja representa las ventas
        color='Departamento',    # El color representa el producto
        hover_name='Producto', # Muestra el nombre del producto al pasar el mouse
        title='Relación Precio vs. Cantidad Vendida',
        labels={'Cantidad_KG': 'Cantidad Vendida (KG)', 'Precio_KG': 'Precio por KG (COP)'},
        template='plotly_white'
    )
    fig_dispersion.update_layout(title_x=0.5) # Centrar título
    
    # 3. GRÁFICO DE PIE: DISTRIBUCIÓN DE VENTAS POR DEPARTAMENTO
    ventas_por_departamento = filtered_df.groupby('Departamento')['Ventas_Totales'].sum().reset_index()
    fig_pie = px.pie(
        ventas_por_departamento,
        names='Departamento',
        values='Ventas_Totales',
        title='Distribución de Ventas por Departamento',
        hole=0.3 # Estilo dona
    )
    fig_pie.update_layout(title_x=0.5)

    return fig_barras, fig_dispersion, fig_pie


# 4. EJECUTAR EL SERVIDOR DE LA APLICACIÓN
if __name__ == '__main__':
    app.run(debug=True)



