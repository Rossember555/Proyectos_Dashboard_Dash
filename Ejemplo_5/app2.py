import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
from sklearn.cluster import KMeans

# === 1) Cargar y limpiar datos ===
df = pd.read_excel("datos.xlsx", engine="openpyxl")
df.rename(columns={"U._DE_MEDIDA": "UNIDAD_MEDIDA"}, inplace=True)

# Convertir campos numéricos (posible coma decimal) a float
for col in ["CANTIDAD", "PRECIO_UNITARIO", "VALOR_TOTAL"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )
df = df.drop_duplicates().dropna(subset=["CANTIDAD", "PRECIO_UNITARIO", "VALOR_TOTAL"])

# === 2) Estadísticos descriptivos ===
stats = df[["CANTIDAD", "PRECIO_UNITARIO", "VALOR_TOTAL"]].describe().reset_index()

# === 3) Clustering ===
X = df[["CANTIDAD", "PRECIO_UNITARIO"]]
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
df["cluster"] = kmeans.labels_.astype(str)

# === 4) Inicializar la app Dash con un tema Bootstrap moderno ===
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX],
    title="Dashboard de Ventas"
)

# === 5) Layout ===
app.layout = dbc.Container(fluid=True, children=[

    # Navbar fija superior
    dbc.NavbarSimple(
        brand="Dashboard de Ventas",
        color="dark",
        dark=True,
        className="mb-4"
    ),

    dbc.Row([
        # Sidebar de filtros globales
        dbc.Col(width=2, children=[
            dbc.Card(body=True, className="h-100", children=[
                html.H5("Filtros", className="card-title"),
                html.Label("Canal:"),
                dcc.Dropdown(
                    id="filter-canal",
                    options=[{"label": c, "value": c} for c in df["CANAL_COMERCIALIZACIÓN"].unique()],
                    value=df["CANAL_COMERCIALIZACIÓN"].unique().tolist(),
                    multi=True
                ),
                html.Br(),
                html.Label("Proveedor:"),
                dcc.Dropdown(
                    id="filter-proveedor",
                    options=[{"label": p, "value": p} for p in df["PROVEEDOR"].unique()],
                    value=df["PROVEEDOR"].unique().tolist(),
                    multi=True
                ),
                html.Br(),
                html.Label("Producto:"),
                dcc.Dropdown(
                    id="filter-producto",
                    options=[{"label": p, "value": p} for p in df["PRODUCTO"].unique()],
                    value=df["PRODUCTO"].unique().tolist(),
                    multi=True
                ),
                html.Br(),
                html.Label("Precio unitario:"),
                dcc.RangeSlider(
                    id="filter-precio",
                    min=df["PRECIO_UNITARIO"].min(),
                    max=df["PRECIO_UNITARIO"].max(),
                    value=[df["PRECIO_UNITARIO"].min(), df["PRECIO_UNITARIO"].max()],
                    tooltip={"placement": "bottom", "always_visible": False},
                    marks={
                        int(df["PRECIO_UNITARIO"].min()): str(int(df["PRECIO_UNITARIO"].min())),
                        int(df["PRECIO_UNITARIO"].max()): str(int(df["PRECIO_UNITARIO"].max()))
                    }
                )
            ])
        ]),

        # Área principal
        dbc.Col(width=10, children=[
            # KPI cards
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H6("Ventas Totales", className="card-subtitle"),
                        html.H2(id="kpi-valor-total")
                    ])
                ], color="info", inverse=True), width=3),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H6("Cantidad Total", className="card-subtitle"),
                        html.H2(id="kpi-cantidad-total")
                    ])
                ], color="success", inverse=True), width=3),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H6("Precio Promedio", className="card-subtitle"),
                        html.H2(id="kpi-precio-avg")
                    ])
                ], color="warning", inverse=True), width=3),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H6("Proveedores Únicos", className="card-subtitle"),
                        html.H2(id="kpi-proveedores")
                    ])
                ], color="primary", inverse=True), width=3),
            ], className="mb-4"),

            # Tabs con gráficos
            dcc.Tabs([
                # Distribuciones
                dcc.Tab(label="Distribuciones", children=[
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="hist-price"), width=6),
                        dbc.Col(dcc.Graph(id="box-cantidad"), width=6),
                    ])
                ]),

                # Geografía
                dcc.Tab(label="Geografía", children=[
                    dcc.Graph(id="graph-geografia")
                ]),

                # Unidades por Municipio
                dcc.Tab(label="Unidades por Municipio", children=[
                    html.Br(),
                    html.Label("Selecciona Municipio:"),
                    dcc.Dropdown(
                        id="filter-municipio-unidades",
                        options=[{"label": m, "value": m} for m in sorted(df["MUNICIPIO_VENTA"].unique())],
                        value=sorted(df["MUNICIPIO_VENTA"].unique())[0],
                        clearable=False
                    ),
                    dcc.Graph(id="graph-unidades")
                ]),

                # Ranking Proveedores
                dcc.Tab(label="Ranking Proveedores", children=[
                    dcc.Graph(id="graph-ranking-proveedores")
                ])
            ])
        ])
    ])
])


# === 6) Callbacks ===

# Callback KPIs
@app.callback(
    [
        Output("kpi-valor-total", "children"),
        Output("kpi-cantidad-total", "children"),
        Output("kpi-precio-avg", "children"),
        Output("kpi-proveedores", "children"),
    ],
    [
        Input("filter-canal", "value"),
        Input("filter-proveedor", "value"),
        Input("filter-producto", "value"),
        Input("filter-precio", "value"),
    ]
)
def update_kpis(canales, proveedores, productos, precio_range):
    dff = df[
        df["CANAL_COMERCIALIZACIÓN"].isin(canales) &
        df["PROVEEDOR"].isin(proveedores) &
        df["PRODUCTO"].isin(productos) &
        df["PRECIO_UNITARIO"].between(precio_range[0], precio_range[1])
    ]
    total_ventas = f"${dff['VALOR_TOTAL'].sum():,.0f}"
    total_cant  = f"{dff['CANTIDAD'].sum():,.0f}"
    avg_precio   = f"${dff['PRECIO_UNITARIO'].mean():,.2f}"
    n_provs      = dff["PROVEEDOR"].nunique()
    return total_ventas, total_cant, avg_precio, n_provs

# Callback Distribuciones
@app.callback(
    [
        Output("hist-price", "figure"),
        Output("box-cantidad", "figure")
    ],
    [
        Input("filter-canal", "value"),
        Input("filter-proveedor", "value"),
        Input("filter-producto", "value"),
        Input("filter-precio", "value"),
    ]
)
def update_distributions(canales, proveedores, productos, precio_range):
    dff = df[
        df["CANAL_COMERCIALIZACIÓN"].isin(canales) &
        df["PROVEEDOR"].isin(proveedores) &
        df["PRODUCTO"].isin(productos) &
        df["PRECIO_UNITARIO"].between(precio_range[0], precio_range[1])
    ]
    hist = px.histogram(
        dff, x="PRECIO_UNITARIO", nbins=30,
        title="Histograma de Precio Unitario",
        labels={"PRECIO_UNITARIO": "Precio Unitario"}
    )
    box = px.box(
        dff, y="CANTIDAD",
        title="Boxplot de Cantidad Vendida",
        labels={"CANTIDAD": "Cantidad"}
    )
    return hist, box

# Callback Geografía
@app.callback(
    Output("graph-geografia", "figure"),
    [
        Input("filter-canal", "value"),
        Input("filter-proveedor", "value"),
        Input("filter-producto", "value"),
        Input("filter-precio", "value"),
    ]
)
def update_geography(canales, proveedores, productos, precio_range):
    dff = df[
        df["CANAL_COMERCIALIZACIÓN"].isin(canales) &
        df["PROVEEDOR"].isin(proveedores) &
        df["PRODUCTO"].isin(productos) &
        df["PRECIO_UNITARIO"].between(precio_range[0], precio_range[1])
    ]
    agg = (
        dff.groupby("MUNICIPIO_VENTA")["VALOR_TOTAL"]
           .sum()
           .reset_index()
           .sort_values("VALOR_TOTAL", ascending=False)
    )
    fig = px.bar(
        agg, x="MUNICIPIO_VENTA", y="VALOR_TOTAL",
        title="Valor Total por Municipio de Venta",
        labels={"MUNICIPIO_VENTA": "Municipio", "VALOR_TOTAL": "Valor Total"}
    )
    return fig

# Callback Ranking Proveedores
@app.callback(
    Output("graph-ranking-proveedores", "figure"),
    [
        Input("filter-canal", "value"),
        Input("filter-proveedor", "value"),
        Input("filter-producto", "value"),
        Input("filter-precio", "value"),
    ]
)
def update_ranking(canales, proveedores, productos, precio_range):
    dff = df[
        df["CANAL_COMERCIALIZACIÓN"].isin(canales) &
        df["PROVEEDOR"].isin(proveedores) &
        df["PRODUCTO"].isin(productos) &
        df["PRECIO_UNITARIO"].between(precio_range[0], precio_range[1])
    ]
    top = (
        dff.groupby("PROVEEDOR")["VALOR_TOTAL"]
           .sum()
           .nlargest(5)
           .reset_index()
    )
    fig = px.bar(
        top, x="PROVEEDOR", y="VALOR_TOTAL",
        title="Top 5 Proveedores por Valor de Ventas",
        labels={"PROVEEDOR": "Proveedor", "VALOR_TOTAL": "Valor Total"}
    )
    return fig

# Callback Unidades por Municipio
@app.callback(
    Output("graph-unidades", "figure"),
    Input("filter-municipio-unidades", "value")
)
def update_units_by_municipio(municipio):
    dff = df[df["MUNICIPIO_VENTA"] == municipio]
    agg = (
        dff.groupby("UNIDAD_MEDIDA")["CANTIDAD"]
           .sum()
           .reset_index()
           .sort_values("CANTIDAD", ascending=False)
    )
    fig = px.bar(
        agg, x="UNIDAD_MEDIDA", y="CANTIDAD",
        title=f"Cantidad por Unidad de Medida en {municipio}",
        labels={"UNIDAD_MEDIDA": "Unidad de Medida", "CANTIDAD": "Cantidad"}
    )
    return fig

# === 7) Ejecutar servidor ===
if __name__ == "__main__":
    app.run(debug=True)

# === 8) Comentarios finales ===