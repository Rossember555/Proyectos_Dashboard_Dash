import dash
from dash import html, dcc, Input, Output, State, dash_table, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- 1. Generación de Datos Simulados ---
# Se genera un conjunto de datos aleatorio para simular ventas.
def generate_data():
    """Genera un DataFrame de pandas con datos de ventas simulados."""
    np.random.seed(int(datetime.now().timestamp()) % 10000)
    start_date = datetime(2023, 1, 1)
    end_date = datetime.now()
    date_range_days = (end_date - start_date).days

    dates = [start_date + timedelta(days=np.random.randint(date_range_days)) for _ in range(1000)]
    categories = ['Electrónica', 'Ropa', 'Hogar', 'Libros', 'Deportes']
    regions = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']

    df = pd.DataFrame({
        'Fecha': pd.to_datetime(dates),
        'Categoría': np.random.choice(categories, 1000, p=[0.3, 0.2, 0.2, 0.15, 0.15]),
        'Región': np.random.choice(regions, 1000),
        'Ventas': np.random.uniform(50, 2000, 1000).round(2),
        'Cantidad': np.random.randint(1, 10, 1000)
    })
    df['Beneficio'] = (df['Ventas'] * np.random.uniform(0.1, 0.4, 1000)).round(2)
    return df

# --- 2. Inicialización de la App ---
# Se crea la instancia de la aplicación Dash con un tema de Bootstrap.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
server = app.server

# --- 3. Definición del Layout ---

# --- Barra de Navegación (Navbar) ---
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Img(src="/assets/logo.png", height="80px")),
            dbc.Col(dbc.NavbarBrand("Dashboard de Ventas IA", className="ms-2")),
        ], align="center", className="g-0"),
        dbc.Button(html.I(className="bi bi-filter-circle-fill"), color="light", id="btn-sidebar", className="ms-auto", n_clicks=0)
    ]),
    color="dark",
    dark=True,
    sticky="top"
)

# --- Panel Lateral de Filtros (Sidebar) ---
sidebar = dbc.Offcanvas(
    [
        html.H5("Filtros", className="text-secondary"),
        html.Hr(),
        dbc.Label("Rango de Fechas", className="fw-bold mb-2"),
        dcc.DatePickerRange(
            id='date-range-picker',
            min_date_allowed=datetime(2023, 1, 1),
            max_date_allowed=datetime.now(),
            start_date=datetime(2023, 1, 1),
            end_date=datetime.now(),
            display_format='YYYY-MM-DD',
            className="w-100"
        ),
        html.Br(), html.Br(),
        dbc.Label("Regiones", className="fw-bold mb-2"),
        dcc.Checklist(
            id='region-checklist',
            options=[{'label': r, 'value': r} for r in ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']],
            value=['Norte', 'Sur', 'Este', 'Oeste', 'Centro'],
            inline=False,
            inputClassName="me-2"
        ),
        html.Br(),
        dbc.Label("Categorías", className="fw-bold mb-2"),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': c, 'value': c} for c in ['Electrónica', 'Ropa', 'Hogar', 'Libros', 'Deportes']],
            value=['Electrónica', 'Ropa', 'Hogar', 'Libros', 'Deportes'],
            multi=True,
            placeholder="Seleccionar categorías"
        ),
        html.Br(),
        dbc.Button("🔄 Refrescar Datos", id='refresh-data-btn', color='info', className='mt-3 w-100'),
    ],
    id='sidebar',
    is_open=False,
    title="Filtros Avanzados",
    placement='start'
)

# --- Contenido Principal de la Página ---
content = html.Div(id='page-content', style={'padding':'2rem 1rem'})

# --- Layout General de la Aplicación ---
app.layout = html.Div([
    dcc.Store(id='raw-data-store'), # Almacena los datos brutos sin filtrar
    navbar,
    sidebar,
    content,
    dcc.Interval(id='interval-refresh', interval=5 * 60 * 1000, n_intervals=0) # Refresco automático cada 5 minutos
])

# --- 4. Callbacks (Lógica de la Aplicación) ---

@app.callback(
    Output('sidebar', 'is_open'),
    Input('btn-sidebar', 'n_clicks'),
    State('sidebar', 'is_open'),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, is_open):
    """Abre y cierra el panel lateral de filtros."""
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output('raw-data-store', 'data'),
    Input('refresh-data-btn', 'n_clicks'),
    Input('interval-refresh', 'n_intervals')
)
def update_raw_data(n_clicks, n_intervals):
    """Genera y almacena nuevos datos cuando se presiona el botón o se cumple el intervalo."""
    df = generate_data()
    return df.to_dict('records')

@app.callback(
    Output('page-content', 'children'),
    Input('raw-data-store', 'data'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date'),
    Input('region-checklist', 'value'),
    Input('category-dropdown', 'value')
)
def update_page_content(raw_data, start_date, end_date, selected_regions, selected_categories):
    """
    Filtra los datos según los controles y renderiza todo el contenido del dashboard.
    Este es el callback principal que reacciona a todos los filtros.
    """
    if not raw_data:
        return dbc.Alert("Generando datos, por favor espere...", color="info")

    # Convertir datos del Store a DataFrame
    df = pd.DataFrame(raw_data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Aplicar filtros
    mask = (
        (df['Fecha'] >= pd.to_datetime(start_date)) &
        (df['Fecha'] <= pd.to_datetime(end_date)) &
        (df['Región'].isin(selected_regions)) &
        (df['Categoría'].isin(selected_categories))
    )
    dff = df[mask] # dff es el DataFrame filtrado

    if dff.empty:
        return dbc.Alert("No hay datos que coincidan con los filtros seleccionados.", color="warning")

    # --- Cálculos de KPIs ---
    total_sales = dff['Ventas'].sum()
    total_profit = dff['Beneficio'].sum()
    total_orders = len(dff)
    avg_ticket = total_sales / total_orders if total_orders else 0

    # --- Creación de Gráficos Sparkline ---
    def create_sparkline(data, color):
        fig = go.Figure(go.Scatter(
            x=data.index, y=data.values, mode='lines',
            line=dict(color=color, width=2), fill='tozeroy'
        ))
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False), yaxis=dict(visible=False)
        )
        return fig

    sales_by_day = dff.set_index('Fecha').resample('D')['Ventas'].sum()
    profit_by_day = dff.set_index('Fecha').resample('D')['Beneficio'].sum()
    orders_by_day = dff.set_index('Fecha').resample('D')['Cantidad'].count()

    spark_sales = create_sparkline(sales_by_day, '#0d6efd')
    spark_profit = create_sparkline(profit_by_day, '#198754')
    spark_orders = create_sparkline(orders_by_day, '#ffc107')

    # --- Creación de Componentes del Layout ---
    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Ventas Totales", className="card-title"), html.H2(f"${total_sales:,.0f}"), dcc.Graph(figure=spark_sales, config={'displayModeBar': False}, style={'height': '60px'})])), lg=3, sm=6, className="mb-4"),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Beneficio Total", className="card-title"), html.H2(f"${total_profit:,.0f}"), dcc.Graph(figure=spark_profit, config={'displayModeBar': False}, style={'height': '60px'})])), lg=3, sm=6, className="mb-4"),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Pedidos Totales", className="card-title"), html.H2(f"{total_orders:,}"), dcc.Graph(figure=spark_orders, config={'displayModeBar': False}, style={'height': '60px'})])), lg=3, sm=6, className="mb-4"),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Ticket Promedio", className="card-title"), html.H2(f"${avg_ticket:,.2f}")])), lg=3, sm=6, className="mb-4"),
    ])

    # Gráfico de Ventas vs. Beneficio
    scatter_fig = go.Figure(data=go.Scatter(
        x=dff['Ventas'],
        y=dff['Beneficio'],
        mode='markers',
        marker=dict(
            size=dff['Cantidad']*2,
            color=dff['Ventas'],
            colorscale='Viridis',
            showscale=True,
            colorbar_title='Ventas'
        ),
        text=dff['Categoría'],
        hovertemplate='<b>Venta:</b> %{x:$,.2f}<br><b>Beneficio:</b> %{y:$,.2f}<br><b>Categoría:</b> %{text}<extra></extra>'
    ))
    scatter_fig.update_layout(
        title='Análisis de Rentabilidad por Venta',
        xaxis_title='Ventas ($)',
        yaxis_title='Beneficio ($)',
        transition_duration=500
    )

    # Gráfico de Series Temporales
    sales_over_time = dff.set_index('Fecha').resample('ME')[['Ventas', 'Beneficio']].sum().reset_index()
    time_series_fig = go.Figure()
    time_series_fig.add_trace(go.Scatter(x=sales_over_time['Fecha'], y=sales_over_time['Ventas'], mode='lines+markers', name='Ventas'))
    time_series_fig.add_trace(go.Scatter(x=sales_over_time['Fecha'], y=sales_over_time['Beneficio'], mode='lines+markers', name='Beneficio'))
    time_series_fig.update_layout(
        title='Evolución Mensual de Ventas y Beneficios',
        xaxis_title='Fecha',
        yaxis_title='Monto ($)',
        legend_title='Métrica'
    )

    # Tabla de Datos
    data_table = dash_table.DataTable(
        data=dff.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in dff.columns],
        page_size=15,
        filter_action='native',
        sort_action='native',
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
    )

    # Ensamblar el layout final de la página
    return html.Div([
        kpi_cards,
        dbc.Row([
            dbc.Col(dcc.Graph(figure=time_series_fig), lg=7),
            dbc.Col(dcc.Graph(figure=scatter_fig), lg=5),
        ], className="mb-4"),
        dbc.Card(dbc.CardBody([
            html.H4("Datos Detallados", className="card-title"),
            data_table
        ]))
    ])

# --- 5. Ejecución de la Aplicación ---
if __name__ == '__main__':
    app.run(debug=True)