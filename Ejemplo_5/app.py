import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output  # Añadido Output
import plotly.express as px
from sklearn.cluster import KMeans

# === 1) Cargar datos y renombrar columna de unidad de medida ===
df = pd.read_excel("datos.xlsx", engine="openpyxl")
df.rename(columns={"U._DE_MEDIDA": "UNIDAD_MEDIDA"}, inplace=True)

# === 2) Limpiar y convertir columnas numéricas ===
for col in ["CANTIDAD", "PRECIO_UNITARIO", "VALOR_TOTAL"]:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(",", ".", regex=False),
        errors="coerce"
    )
df = df.drop_duplicates().dropna(subset=["CANTIDAD", "PRECIO_UNITARIO", "VALOR_TOTAL"])

# === 3) Estadísticos descriptivos ===
stats = df[["CANTIDAD", "PRECIO_UNITARIO", "VALOR_TOTAL"]].describe().reset_index()

# === 4) Clustering (3 grupos sobre cantidad y precio) ===
X = df[["CANTIDAD", "PRECIO_UNITARIO"]]
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
df["cluster"] = kmeans.labels_.astype(str)

# === 5) Crear la app Dash ===
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Análisis Riguroso de Ventas", style={"textAlign": "center"}),
    dcc.Tabs([

        # Pestaña 1: Resumen Estadístico
        dcc.Tab(label="Resumen Estadístico", children=[
            dash_table.DataTable(
                data=stats.to_dict("records"),
                columns=[{"name": c, "id": c} for c in stats.columns],
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "center"}
            )
        ]),

        # Pestaña 2: Distribuciones univariadas
        dcc.Tab(label="Distribuciones", children=[
            dcc.Graph(
                figure=px.histogram(
                    df, x="PRECIO_UNITARIO", nbins=30,
                    title="Histograma de Precio Unitario",
                    labels={"PRECIO_UNITARIO": "Precio Unitario"}
                )
            ),
            dcc.Graph(
                figure=px.box(
                    df, y="CANTIDAD",
                    title="Boxplot de Cantidad Vendida",
                    labels={"CANTIDAD": "Cantidad"}
                )
            )
        ]),

        # Pestaña 3: Correlaciones y Clusters
        dcc.Tab(label="Correlaciones", children=[
            dcc.Graph(
                figure=px.imshow(
                    df[["CANTIDAD","PRECIO_UNITARIO","VALOR_TOTAL"]].corr(),
                    text_auto=True,
                    title="Matriz de Correlación"
                )
            ),
            dcc.Graph(
                figure=px.scatter(
                    df, x="PRECIO_UNITARIO", y="CANTIDAD", color="cluster",
                    title="Scatter Precio vs. Cantidad (Clusters)",
                    labels={"PRECIO_UNITARIO": "Precio Unitario", "CANTIDAD": "Cantidad"}
                )
            )
        ]),

        # Pestaña 4: Geografía y Concentración
        dcc.Tab(label="Geografía y Concentración", children=[
            dcc.Graph(
                figure=px.bar(
                    df.groupby("MUNICIPIO_VENTA")["VALOR_TOTAL"]
                      .sum()
                      .sort_values(ascending=False)
                      .reset_index(),
                    x="MUNICIPIO_VENTA", y="VALOR_TOTAL",
                    title="Valor Total por Municipio de Venta",
                    labels={"MUNICIPIO_VENTA": "Municipio", "VALOR_TOTAL": "Valor Total"}
                )
            ),
            dcc.Graph(
                figure=px.bar(
                    df.groupby("PROVEEDOR")["VALOR_TOTAL"]
                      .sum()
                      .nlargest(5)
                      .reset_index(),
                    x="PROVEEDOR", y="VALOR_TOTAL",
                    title="Top 5 Proveedores por Valor de Ventas",
                    labels={"PROVEEDOR": "Proveedor", "VALOR_TOTAL": "Valor Total"}
                )
            )
        ]),

        # Pestaña 5: Cantidad por Unidad de Medida y Municipio
        dcc.Tab(label="Cantidad por Unidad de Medida", children=[

            # Filtro de municipio
            html.Div([
                html.Label("Selecciona Municipio:"),
                dcc.Dropdown(
                    id="filtro-municipio",
                    options=[{"label": m, "value": m} for m in sorted(df["MUNICIPIO_VENTA"].unique())],
                    value=sorted(df["MUNICIPIO_VENTA"].unique())[0],
                    clearable=False
                )
            ], style={"width": "40%", "margin": "20px auto"}),

            # Gráfico que se actualiza según municipio
            dcc.Graph(id="graf-cant-um-municipio")
        ])

    ])
])

# === 6) Callback para la pestaña 5 ===
@app.callback(
    Output("graf-cant-um-municipio", "figure"),
    Input("filtro-municipio", "value")
)
def mostrar_cantidad_por_um(municipio):
    dff = df[df["MUNICIPIO_VENTA"] == municipio]
    agg = (
        dff.groupby("UNIDAD_MEDIDA")["CANTIDAD"]
           .sum()
           .reset_index()
           .sort_values("CANTIDAD", ascending=False)
    )
    fig = px.bar(
        agg,
        x="UNIDAD_MEDIDA",
        y="CANTIDAD",
        title=f"Cantidad Total por Unidad de Medida en {municipio}",
        labels={"UNIDAD_MEDIDA": "Unidad de Medida", "CANTIDAD": "Cantidad"}
    )
    return fig

# === 7) Ejecutar servidor ===
if __name__ == "__main__":
    app.run(debug=True)
# === 8) Comentarios finales ===