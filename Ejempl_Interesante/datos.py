import os
import pandas as pd
import numpy as np
import zipfile

# Directorio base para los archivos
base_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'Finanzas_y_Contabilidad')
os.makedirs(base_dir, exist_ok=True)

# Semilla para reproducibilidad
np.random.seed(42)



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


# Lista de tuplas para nombres de archivos
file_list = [
    (df_ingresos, 'DOLOR_fuentes_ingresos.csv'),
    (df_gastos, 'DOLOR_categorias_gastos.csv'),
    (df_acciones, 'MINIM_evolucion_acciones.csv'),
    (df_flujo_caja, 'MINIM_flujo_caja_acumulado.csv'),
    (df_cartera, 'LOREM_distribucion_cartera.csv'),
    (df_ingresos_linea, 'LOREM_composicion_ingresos.csv'),
    (df_fondos, 'VELIT1_rendimiento_fondos.csv'),
    (df_gastos_depto, 'VELIT1_gastos_departamento.csv'),
    (df_ingresos_anual, 'IRURE_objetivo_ingresos.csv'),
    (df_endeudamiento, 'IRURE_endeudamiento_total.csv'),
    (df_transacciones, 'VELIT2_distribucion_transacciones.csv'),
    (df_antiguedad_cuentas, 'VELIT2_antiguedad_cuentas.csv'),
    (df_hist_ingresos, 'MAGNA_evolucion_ingresos.csv'),
    (df_kpis, 'KPIs_indicadores.csv')
]

# Escritura de archivos CSV
for df, filename in file_list:
    path = os.path.join(base_dir, filename)
    df.to_csv(path, index=False)

# Creación de un ZIP con todos los CSV
zip_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Finanzas_y_Contabilidad.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, start=base_dir)
            zipf.write(full_path, arcname)

zip_path