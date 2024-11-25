import plotly.express as px

def generar_tendencia(df, x, y, color, titulo):
    """Genera un gráfico de líneas para tendencias históricas."""
    fig = px.line(df, x=x, y=y, color=color, title=titulo)
    fig.update_layout(legend_title_text=color)
    return fig

def generar_comparacion_barras(df, x, y, color, titulo):
    """Genera un gráfico de barras para comparaciones entre categorías."""
    fig = px.bar(df, x=x, y=y, color=color, title=titulo)
    fig.update_layout(legend_title_text=color)
    return fig
