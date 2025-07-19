import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# --- 1. Carga y Preparación de Datos ---

# Cargar los datos de ventas
try:
    df = pd.read_csv('ventas_agricolas_sinteticas.csv')
except FileNotFoundError:
    print("Error: Asegúrate de que 'ventas_agricolas_sinteticas.csv' esté en la misma carpeta que el script.")
    exit()

# --- 2. Definición de Estilos ---
colors = {
    'background': '#F9F9F9',
    'text': '#333333',
    'header_bg': '#2E8B57', # Verde Marino
    'card_bg': '#FFFFFF',
    'accent': '#3CB371'  # Verde Medio
}

# --- 3. Inicialización de la App Dash ---
app = dash.Dash(__name__)
server = app.server

# --- 4. Layout del Dashboard ---
app.layout = html.Div(style={'backgroundColor': colors['background'], 'fontFamily': 'Arial, sans-serif', 'color': colors['text']}, children=[
    
    # Encabezado
    html.Div(
        style={'backgroundColor': colors['header_bg'], 'padding': '20px', 'color': 'white'},
        children=[html.H1('Dashboard de Ventas Agrícolas', style={'textAlign': 'center', 'margin': '0'})]
    ),

    # Contenedor principal
    html.Div(style={'padding': '20px'}, children=[

        # Fila de KPIs y Filtros
        html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}, children=[
            # Columna de KPIs
            html.Div(style={'flex': 2, 'display': 'flex', 'gap': '15px'}, children=[
                html.Div(id='kpi-ventas', style={'flex': 1, 'backgroundColor': colors['card_bg'], 'padding': '20px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.05)', 'textAlign': 'center'}),
                html.Div(id='kpi-cantidad', style={'flex': 1, 'backgroundColor': colors['card_bg'], 'padding': '20px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.05)', 'textAlign': 'center'}),
                html.Div(id='kpi-precio-promedio', style={'flex': 1, 'backgroundColor': colors['card_bg'], 'padding': '20px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.05)', 'textAlign': 'center'}),
            ]),
            # Columna de Filtros
            html.Div(style={'flex': 1, 'backgroundColor': colors['card_bg'], 'padding': '20px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'}, children=[
                html.H4("Filtros", style={'marginTop': '0', 'textAlign': 'center'}),
                dcc.Dropdown(
                    id='filtro-departamento',
                    options=[{'label': 'Todos los Departamentos', 'value': 'all'}] + [{'label': i, 'value': i} for i in sorted(df['Departamento'].unique())],
                    value='all',
                    clearable=False
                ),
                html.Br(),
                dcc.Dropdown(
                    id='filtro-producto',
                    options=[{'label': 'Todos los Productos', 'value': 'all'}] + [{'label': i, 'value': i} for i in sorted(df['Producto'].unique())],
                    value='all',
                    clearable=False
                ),
            ]),
        ]),
        
        # Fila de Gráficos (ambos de barras)
        html.Div(style={'display': 'flex', 'gap': '20px'}, children=[
            # NUEVO: Gráfico de barras por departamento
            dcc.Graph(id='bar-ventas-departamento', style={'flex': 1}),
            dcc.Graph(id='bar-ventas-producto', style={'flex': 1}),
        ]),
    ]),
])

# --- 5. Callbacks para la Interactividad ---
@app.callback(
    [Output('kpi-ventas', 'children'),
     Output('kpi-cantidad', 'children'),
     Output('kpi-precio-promedio', 'children'),
     # Se actualiza el output para el nuevo gráfico
     Output('bar-ventas-departamento', 'figure'),
     Output('bar-ventas-producto', 'figure')],
    [Input('filtro-departamento', 'value'),
     Input('filtro-producto', 'value')]
)
def actualizar_dashboard(depto_seleccionado, producto_seleccionado):
    dff = df.copy()
    if depto_seleccionado != 'all':
        dff = dff[dff['Departamento'] == depto_seleccionado]
    if producto_seleccionado != 'all':
        dff = dff[dff['Producto'] == producto_seleccionado]

    # --- Calcular KPIs ---
    total_ventas = dff['Ventas_Totales'].sum()
    total_cantidad = dff['Cantidad_KG'].sum()
    precio_promedio = total_ventas / total_cantidad if total_cantidad > 0 else 0
    
    kpi_ventas_layout = [html.H4("Ventas Totales"), html.H3(f"${total_ventas:,.0f}")]
    kpi_cantidad_layout = [html.H4("Cantidad Total (KG)"), html.H3(f"{total_cantidad:,.0f}")]
    kpi_precio_promedio_layout = [html.H4("Precio Promedio/KG"), html.H3(f"${precio_promedio:,.2f}")]

    # --- Generar Gráficos ---

    # Gráfico de Barras: Ventas por Departamento
    ventas_por_depto = dff.groupby('Departamento')['Ventas_Totales'].sum().reset_index().sort_values('Ventas_Totales', ascending=False)
    fig_bar_depto = px.bar(
        ventas_por_depto,
        x='Departamento',
        y='Ventas_Totales',
        title='Ventas por Departamento',
        labels={'Ventas_Totales': 'Ventas Totales (COP)', 'Departamento': 'Departamento'},
        text='Ventas_Totales'
    )
    fig_bar_depto.update_traces(
        marker_color=colors['accent'],
        texttemplate='$%{text:,.0s}',
        textposition='outside'
    )
    fig_bar_depto.update_layout(
        title_x=0.5,
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['card_bg']
    )
    
    # Gráfico de Barras: Ventas por Producto
    ventas_por_prod = dff.groupby('Producto')['Ventas_Totales'].sum().reset_index().sort_values('Ventas_Totales', ascending=False)
    fig_bar_prod = px.bar(
        ventas_por_prod,
        x='Producto',
        y='Ventas_Totales',
        title='Ventas por Producto',
        labels={'Ventas_Totales': 'Ventas Totales (COP)', 'Producto': 'Producto'},
        text='Ventas_Totales'
    )
    fig_bar_prod.update_traces(
        marker_color='#5DADE2', # Un color azul para diferenciar
        texttemplate='$%{text:,.0s}',
        textposition='outside'
    )
    fig_bar_prod.update_layout(
        title_x=0.5,
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['card_bg']
    )

    return kpi_ventas_layout, kpi_cantidad_layout, kpi_precio_promedio_layout, fig_bar_depto, fig_bar_prod

# --- 6. Ejecutar la App ---
if __name__ == '__main__':
    app.run(debug=True)