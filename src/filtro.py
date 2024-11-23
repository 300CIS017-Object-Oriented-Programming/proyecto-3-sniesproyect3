def filtrar_programas(df, palabras_clave):
    """Filtra programas académicos por palabras clave."""
    if palabras_clave:
        # Crear una expresión regular para buscar todas las palabras clave
        regex = '|'.join(palabras_clave)
        df = df[df["programa"].str.contains(regex, case=False, na=False)]
    return df