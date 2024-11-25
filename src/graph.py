import plotly.express as px

# Función para generar gráficos de líneas
def generar_grafico_linea(df, metrica, programas, titulo):
    fig = px.line(
        df[df["Programa Académico"].isin(programas)], 
        x="Año", 
        y=metrica, 
        color="Programa Académico", 
        markers=True,
        title=titulo
    )
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title=metrica,
        legend_title="Programa Académico"
    )
    return fig

# Función para generar gráficos de barras
def generar_grafico_barra(df, metrica, programas, titulo):
    fig = px.bar(
        df[df["Programa Académico"].isin(programas)], 
        x="Año", 
        y=metrica, 
        color="Programa Académico",
        barmode="group",
        title=titulo
    )
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title=metrica,
        legend_title="Programa Académico"
    )
    return fig
