
def filtrar_programas(df, palabra_clave=None, nivel_formacion=None):
    """Filtra programas académicos por palabra clave y nivel de formación."""
    if palabra_clave:
        df = df[df["programa"].str.contains(palabra_clave, case=False, na=False)]
    if nivel_formacion:
        df = df[df["niveldeformacion"] == nivel_formacion]
    return df
