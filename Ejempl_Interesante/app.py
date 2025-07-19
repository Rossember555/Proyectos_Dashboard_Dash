import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ==============================================================================
# 1. Paleta de Colores y Estilos
# ==============================================================================
colors = {
    'background': '#1E1E2F',
    'component_bg': '#27293D',
    'text': '#FFFFFF',
    'primary': '#8A2BE2',  # Un tono de morado
    'accent1': '#FBC02D',  # Amarillo/Dorado
    'accent2': '#4FC3F7',  # Azul claro
    'accent3': '#FF5252',  # Rojo/Rosa
    'grid_color': '#444444'
}

card_style = {
    'backgroundColor': colors['component_bg'],
    'borderRadius': '10px',
    'padding': '20px',
    'color': colors['text'],
    'boxShadow': '0 4px 6px 0 rgba(0, 0, 0, 0.2)'
}

# ==============================================================================
# 2. Generación de Datos de Ejemplo
# ==============================================================================
np.random.seed(42)

# Fuentes de ingresos
fuentes = ['Ventas', 'Servicios', 'Inversiones', 'Otros']
df_ingresos = pd.DataFrame({
    'Fuente': fuentes,
    'Monto': np.random.randint(1000, 5000, len(fuentes))
})

# Categorías de gastos
gastos = ['Salarios', 'Marketing', 'Infraestructura', 'Gastos Varios']
df_gastos = pd.DataFrame({
    'Categoria': gastos,
    'Monto': np.random.randint(500, 3000, len(gastos))
})

# Evolución de acciones (precios a lo largo del tiempo)
dates_acciones = pd.date_range(start='2024-01-01', periods=50, freq='W')
df_acciones = pd.DataFrame({
    'Fecha': dates_acciones,
    'Precio': np.round(np.random.uniform(50, 150, len(dates_acciones)), 2)
})

# Flujo de caja acumulado
df_flujo_caja = pd.DataFrame({
    'Fecha': dates_acciones,
    'Flujo_Acumulado': np.cumsum(np.random.uniform(100, 500, len(dates_acciones)))
})

# Distribución de cartera
df_cartera = pd.DataFrame({
    'Activo': ['Acciones', 'Bonos', 'Bienes Raíces', 'Efectivo', 'Commodities'],
    'Porcentaje': [20, 25, 15, 30, 10]
})

# Composición de ingresos por línea de negocio
df_ingresos_linea = pd.DataFrame({
    'Linea_de_Negocio': ['Línea A', 'Línea B', 'Línea C'],
    'Monto': np.random.randint(1000, 4000, 3)
})

# Rendimiento de fondos
df_fondos = pd.DataFrame({
    'Fondo': ['Fondo A', 'Fondo B', 'Fondo C', 'Fondo D'],
    'Rendimiento': np.round(np.random.uniform(2, 12, 4), 2)
})

# Gastos por departamento
df_gastos_depto = pd.DataFrame({
    'Departamento': ['Recursos Humanos', 'TI', 'Ventas', 'Operaciones'],
    'Gasto': np.random.randint(800, 2500, 4)
})

# Objetivo e ingresos anuales
df_ingresos_anual = pd.DataFrame({
    'Concepto': ['Ingresos Actuales', 'Meta de Ingresos'],
    'Valor': [np.random.randint(50000, 80000), 100000]
})

# Endeudamiento total
df_endeudamiento = pd.DataFrame({
    'Concepto': ['Endeudamiento Actual', 'Límite de Endeudamiento'],
    'Valor': [np.random.randint(20000, 40000), 50000]
})

# Distribución de transacciones
df_transacciones = pd.DataFrame({
    'Valor_Transaccion': np.random.uniform(10, 1000, 100)
})

# Antigüedad de cuentas por cobrar
df_antiguedad_cuentas = pd.DataFrame({
    'Antiguedad_Dias': np.random.randint(0, 120, 200)
})

# Evolución histórica de ingresos
dates_hist = pd.date_range(start='2023-01-01', periods=24, freq='ME')
df_hist_ingresos = pd.DataFrame({
    'Fecha': dates_hist,
    'Ingresos': np.round(np.random.uniform(20000, 50000, len(dates_hist)), 2)
})

# KPI e indicadores
df_kpis = pd.DataFrame({
    'KPI': ['Rentabilidad', 'Liquidez', 'Cobertura', 'Solvencia'],
    'Valor': np.round(np.random.uniform(50, 200, 4), 2),
    'Grupo': ['LOREM IPSUM ST', 'ADIPISCING ELIT', 'SED DO EIUSMOD', 'TEMPOR INCIDIDUNT']
})

# ==============================================================================
# 3. Creación de las Figuras de Plotly
# ==============================================================================

# Gráfico de Barras Horizontales: Fuentes de Ingresos
fig_dolor = go.Figure(go.Bar(
    x=df_ingresos['Monto'],
    y=df_ingresos['Fuente'],
    orientation='h',
    marker_color=colors['primary']
))
fig_dolor.update_layout(
    title_text='Principales Fuentes de Ingresos',
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color=colors['text'],
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor=colors['grid_color']),
    yaxis=dict(showgrid=False)
)

# Gráfico de Área: Evolución de Acciones
fig_minim = go.Figure(go.Scatter(
    x=df_acciones['Fecha'],
    y=df_acciones['Precio'],
    mode='lines',
    fill='tozeroy',
    line=dict(color=colors['primary'], width=2)
))
fig_minim.update_layout(
    title_text='Evolución Precio de Acción',
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color=colors['text'],
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor=colors['grid_color'])
)

# Gráfico de Dona: Distribución de Cartera
fig_lorem = go.Figure(go.Pie(
    labels=df_cartera['Activo'],
    values=df_cartera['Porcentaje'],
    hole=.7,
    marker_colors=[colors['accent1'], colors['accent2'], colors['accent3'], colors['primary'], '#6a1b9a']
))
total_cartera = df_cartera['Porcentaje'].sum()
fig_lorem.update_layout(
    title_text='Distribución de Cartera',
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color=colors['text'],
    showlegend=False,
    margin=dict(l=10, r=10, t=40, b=10),
    annotations=[dict(text=f'{total_cartera}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
)

# Gráfico de Barras Verticales: Rendimiento de Fondos
fig_velit1 = go.Figure(go.Bar(
    x=df_fondos['Fondo'],
    y=df_fondos['Rendimiento'],
    marker_color=[colors['accent1'], colors['primary'], colors['accent2'], colors['accent3']]
))
fig_velit1.update_layout(
    title_text='Rendimiento de Fondos',
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color=colors['text'],
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor=colors['grid_color'])
)

# Indicador: Objetivo de Ingresos Anual
valor_actual_ingresos = df_ingresos_anual.loc[df_ingresos_anual['Concepto'] == 'Ingresos Actuales', 'Valor'].iloc[0]
meta_ingresos = df_ingresos_anual.loc[df_ingresos_anual['Concepto'] == 'Meta de Ingresos', 'Valor'].iloc[0]
fig_irure = go.Figure(go.Indicator(
    mode="gauge+number",
    value=valor_actual_ingresos,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Objetivo de Ingresos Anual"},
    gauge={
        'axis': {'range': [None, meta_ingresos], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': colors['accent2']},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, meta_ingresos * 0.5], 'color': colors['component_bg']},
            {'range': [meta_ingresos * 0.5, meta_ingresos * 0.8], 'color': '#333652'},
        ],
    }
))
fig_irure.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    font={'color': colors['text'], 'family': "Arial"}
)

# Histograma: Antigüedad de Cuentas por Cobrar
fig_velit2 = go.Figure(go.Histogram(
    x=df_antiguedad_cuentas['Antiguedad_Dias'],
    marker_color=colors['accent1'],
    xbins=dict(start=0, end=100, size=15)
))
fig_velit2.update_layout(
    title_text='Antigüedad Cuentas por Cobrar',
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color=colors['text'],
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(title_text='Días', showgrid=False),
    yaxis=dict(title_text='Frecuencia', gridcolor=colors['grid_color'])
)

# Gráfico de Línea Grande: Evolución Histórica de Ingresos
fig_magna = go.Figure(go.Scatter(
    x=df_hist_ingresos['Fecha'],
    y=df_hist_ingresos['Ingresos'],
    mode='lines',
    line=dict(color=colors['accent2'], width=2),
    fill='tozeroy',
    fillcolor='rgba(79, 195, 247, 0.2)'
))
fig_magna.update_layout(
    title_text='Evolución Histórica de Ingresos',
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color=colors['text'],
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor=colors['grid_color'])
)

# Indicadores Circulares: KPI Grupo IPSUM

def create_circular_indicator(value, title, color):
    numeric_value = float(str(value).replace('%', ''))
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=numeric_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'shape': "angular",
            'axis': {'range': [None, max(100, numeric_value * 1.5)]},
            'bar': {'color': color, 'thickness': 0.8},
            'bgcolor': colors['grid_color'],
        }
    ))
    fig.update_layout(
        title={'text': title, 'font': {'size': 16}},
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': colors['text']},
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

# Toma los 3 primeros KPIs sin filtrar por grupo
fig_ipsum1 = create_circular_indicator(df_kpis.iloc[0]['Valor'], df_kpis.iloc[0]['KPI'], colors['accent1'])
fig_ipsum2 = create_circular_indicator(df_kpis.iloc[1]['Valor'], df_kpis.iloc[1]['KPI'], colors['accent2'])
fig_ipsum3 = create_circular_indicator(df_kpis.iloc[2]['Valor'], df_kpis.iloc[2]['KPI'], colors['accent3'])

# ==============================================================================
# 4. Inicialización de la App Dash
# ==============================================================================
app = dash.Dash(__name__, external_stylesheets=[
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
])
app.title = 'Dashboard Financiero'

# ==============================================================================
# 5. Layout de la Aplicación
# ==============================================================================

def create_kpi_card(title, value, icon, color):
    return html.Div(
        style={**card_style, 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'},
        children=[
            html.Div([
                html.H3(value, style={'color': color, 'margin': '0'}),
                html.P(title, style={'margin': '0', 'fontSize': '14px'})
            ]),
            html.Div(
                html.I(className=icon, style={'fontSize': '32px', 'color': color})
            )
        ]
    )


def safe_kpi_card(group, icon, color):
    if not group.empty:
        return create_kpi_card(group.iloc[0]['KPI'], group.iloc[0]['Valor'], icon, color)
    else:
        return html.Div("Sin datos", style=card_style)

sidebar = html.Div(
    style={
        'width': '250px',
        'backgroundColor': colors['component_bg'],
        'padding': '20px',
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100vh',
        'color': colors['text']
    },
    children=[
        html.H2('DASHBOARD', style={'textAlign': 'center'}),
        html.Hr(),
        html.Ul(style={'listStyle': 'none', 'padding': '0'}, children=[
            html.Li(html.A([html.I(className='fas fa-home'), ' Dashboard'], href='#', style={'color': colors['text'], 'textDecoration': 'none', 'display': 'block', 'padding': '10px'})),
            html.Li(html.A([html.I(className='fas fa-chart-bar'), ' Finanzas'], href='#', style={'color': colors['text'], 'textDecoration': 'none', 'display': 'block', 'padding': '10px'})),
            html.Li(html.A([html.I(className='fas fa-table'), ' Datos'], href='#', style={'color': colors['text'], 'textDecoration': 'none', 'display': 'block', 'padding': '10px'})),
        ]),
        html.Div(style={'flexGrow': 1}),
        html.Hr(),
        html.A([html.I(className='fas fa-cog'), ' Configuración'], href='#', style={'color': colors['text'], 'textDecoration': 'none', 'display': 'block', 'padding': '10px'}),
        html.A([html.I(className='fas fa-question-circle'), ' Soporte'], href='#', style={'color': colors['text'], 'textDecoration': 'none', 'display': 'block', 'padding': '10px'}),
    ]
)

kpi_group_1 = df_kpis[df_kpis['Grupo'] == 'LOREM IPSUM ST']
kpi_group_2 = df_kpis[df_kpis['Grupo'] == 'ADIPISCING ELIT']
kpi_group_3 = df_kpis[df_kpis['Grupo'] == 'SED DO EIUSMOD']
kpi_group_4 = df_kpis[df_kpis['Grupo'] == 'TEMPOR INCIDIDUNT']

main_content = html.Div(
    style={'flexGrow': 1, 'padding': '20px', 'height': '100vh', 'overflowY': 'auto'},
    children=[
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '20px'},
            children=[
                dcc.Input(placeholder='Buscar...', type='text', style={'width': '300px', 'backgroundColor': colors['component_bg'], 'border': 'none', 'padding': '10px', 'borderRadius': '5px', 'color': colors['text']}),
                html.Div([
                    html.I(className='fas fa-bell', style={'margin': '0 15px', 'cursor': 'pointer'}),
                    html.I(className='fas fa-cog', style={'margin': '0 15px', 'cursor': 'pointer'}),
                    html.Span('Analista Financiero', style={'margin': '0 15px'}),
                    html.I(className='fas fa-user-circle', style={'fontSize': '24px'})
                ])
            ]
        ),
        html.Div(
            style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(4, 1fr)',
                'gridTemplateRows': 'auto',
                'gap': '20px',
            },
            children=[
                html.Div(safe_kpi_card(kpi_group_1, 'fas fa-percent', colors['accent1']), style={'gridColumn': 'span 1'}),
                html.Div(safe_kpi_card(kpi_group_2, 'fas fa-exchange-alt', colors['primary']), style={'gridColumn': 'span 1'}),
                html.Div(safe_kpi_card(kpi_group_3, 'fas fa-wallet', colors['accent2']), style={'gridColumn': 'span 1'}),
                html.Div(safe_kpi_card(kpi_group_4, 'fas fa-dollar-sign', colors['accent3']), style={'gridColumn': 'span 1'}),
                html.Div(dcc.Graph(figure=fig_dolor, config={'displayModeBar': False}), style={**card_style, 'gridColumn': 'span 2'}),
                html.Div(dcc.Graph(figure=fig_minim, config={'displayModeBar': False}), style={**card_style, 'gridColumn': 'span 2'}),
                html.Div(dcc.Graph(figure=fig_lorem, config={'displayModeBar': False}), style={**card_style, 'gridColumn': 'span 1'}),
                html.Div(dcc.Graph(figure=fig_velit1, config={'displayModeBar': False}), style={**card_style, 'gridColumn': 'span 1'}),
                html.Div(dcc.Graph(figure=fig_irure, config={'displayModeBar': False}), style={**card_style, 'gridColumn': 'span 1'}),
                html.Div(dcc.Graph(figure=fig_velit2, config={'displayModeBar': False}), style={**card_style, 'gridColumn': 'span 1'}),
                html.Div(dcc.Graph(figure=fig_magna, config={'displayModeBar': False}), style={**card_style, 'gridColumn': 'span 4'}),
                html.Div(dcc.Graph(figure=fig_ipsum1, config={'displayModeBar': False}), style={**card_style, 'gridColumn': 'span 1'}),
                html.Div(dcc.Graph(figure=fig_ipsum2, config={'displayModeBar': False}), style={**card_style, 'gridColumn': 'span 1'}),
                html.Div(dcc.Graph(figure=fig_ipsum3, config={'displayModeBar': False}), style={**card_style, 'gridColumn': 'span 1'}),
            ]
        )
    ]
)

# Layout final
app.layout = html.Div(
    style={'backgroundColor': colors['background'], 'fontFamily': 'Arial, sans-serif', 'color': colors['text']},
    children=[
        html.Div(style={'display': 'flex'}, children=[
            sidebar,
            main_content
        ])
    ]
)

# ==============================================================================
# 6. Ejecutar la Aplicación
# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True)