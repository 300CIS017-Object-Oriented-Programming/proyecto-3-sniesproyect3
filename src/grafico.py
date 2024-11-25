import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def graficar_tendencias(df, programas, columnas_metrica, columna_anio_periodo, color_discrete_sequence=None):
    """
    Genera gráficos de lieneas para mostrar tendencias por año y programa academico

     Parametros:
     df: DataFrame consolidado con datos de múltiples archivos
     programas: Lista de programas academicos seleccionados por el usuario
     columnas_metrica: Lista de metricas a graficar (inscritos, admitidos)
     columna_anio_periodo: columna para el eje x - años
     color_discrete_sequence: colores personalizasdos
     devuelve: Diccionario de figuras plotly
    """
    graficas = {}

    # Filtrar DataFrame por los programas seleccionados
    df_filtrado = df[df["programa_academico"].isin(programas)]

    for metrica in columnas_metrica:
        if metrica in df_filtrado.columns:
            # Transformar a formato largo para manejar múltiples columnas de metricas
            df_long = pd.melt(
                df_filtrado,
                id_vars=["programa_academico", columna_anio_periodo],
                value_vars=[metrica],
                var_name="Métrica",
                value_name="Valor"
            )

            # Crear el gráfico de tendencia
            fig = px.line(
                df_long,
                x=columna_anio_periodo,  # x: Años
                y="Valor",               # y: Valor de la métrica
                color="programa_academico",  # linea por cada programa
                markers=True,
                color_discrete_sequence=color_discrete_sequence,
                labels={
                    columna_anio_periodo: "Año",
                    "Valor": f"Número de {metrica}",
                    "programa_academico": "Programa Académico"
                },
            )

            fig.update_layout(
                annotations=[
                    dict(
                        text=f"Tendencia de {metrica.capitalize()}",
                        x=0.5,
                        xref="paper",
                        y=1.1,
                        yref="paper",
                        showarrow=False,
                        font=dict(size=20)
                    )
                ],
                xaxis_title="Año",
                yaxis_title=metrica.capitalize(),
                legend_title="Programas Académicos",
                margin=dict(t=100, b=40, l=40, r=40),
                template="plotly_dark"
            )
            fig.update_traces(mode="lines+markers", line_shape="linear")

            graficas[metrica] = fig

    return graficas



def graficar_comparativo(df, columna_categoria, columnas_metrica, columna_programa=None, color_discrete_map=None):
    """
    Genera graficos de barras agrupadas para comparar metricas por categorias y años

    Parametros:
    df: DataFrame filtrado
    columna_categoria: Columna de la categoría a comparar (e.g., modalidad, nivel de formación)
    columnas_metrica: Lista de métricas a graficar (e.g., inscritos, admitidos)
    columna_programa: columna para diferenciar programas académicos
    color_discrete_map: colores personalizados
    devuelve: Diccionario de figuras (Plotly)
    """
    graficas = {}

    for metrica in columnas_metrica:
        if metrica in df.columns and columna_categoria in df.columns:
            # Transformar el DataFrame en formato largo para facilitar las comparaciones
            df_long = pd.melt(
                df,
                id_vars=["anio_periodo", columna_categoria, columna_programa] if columna_programa else ["anio_periodo", columna_categoria],
                value_vars=[metrica],
                var_name="Métrica",
                value_name="Valor"
            )

            fig = px.bar(
                df_long,
                x="anio_periodo",
                y="Valor",
                color=columna_categoria,
                barmode="group",
                facet_col=columna_programa if columna_programa else None,  # Dividir por programa academico
                color_discrete_map=color_discrete_map,
                labels={
                    "anio_periodo": "Año",
                    "Valor": f"Número de {metrica}",
                    columna_categoria: columna_categoria.capitalize(),
                    columna_programa: "Programa Académico" if columna_programa else None
                },
            )

            fig.update_layout(
                annotations=[
                    dict(
                        text=f"Comparación de {metrica.capitalize()} por {columna_categoria.capitalize()} y Año",
                        x=0.5,
                        xref="paper",
                        y=1.1,
                        yref="paper",
                        showarrow=False,
                        font=dict(size=20)
                    )
                ],
                xaxis_title="Año",
                yaxis_title=metrica.capitalize(),
                legend_title=columna_categoria.capitalize(),
                template="plotly_dark"
            )
            graficas[metrica] = fig
    return graficas