import pandas as pd

def consolidar_métricas(df):
    """
    Calcula métricas consolidadas como inscritos, admitidos, matriculados, etc.,
    agrupadas por programa y año.
    """
    metrics = df.groupby(["Programa", "Año"]).agg(
        Inscritos=("Inscritos", "sum"),
        Admitidos=("Admitidos", "sum"),
        Matriculados=("Matriculados", "sum"),
        Graduados=("Graduados", "sum"),
    ).reset_index()

    
    return metrics