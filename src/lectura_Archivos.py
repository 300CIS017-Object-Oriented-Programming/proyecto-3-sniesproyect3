import pandas as pd


def estandarizar_columnas(df):
    """Estandariza los nombres de las columnas a minúsculas y sin espacios."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def leer_xlsx(ruta):
    """Lee un archivo Excel (.xlsx) y devuelve un DataFrame."""
    try:
        df = pd.read_excel(ruta, engine="openpyxl")
        df = estandarizar_columnas(df)
        return df
    except Exception as e:
        raise ValueError(f"Error al leer el archivo: {e}")

def escribir_archivo(df, ruta_salida, formato="csv"):
    """
    Guarda un DataFrame en el formato especificado (csv, xlsx, json).
    """
    try:
        if formato == "csv":
            df.to_csv(ruta_salida, index=False)
        elif formato == "xlsx":
            df.to_excel(ruta_salida, index=False, engine="openpyxl")
        elif formato == "json":
            df.to_json(ruta_salida, orient="records", lines=True)
        else:
            raise ValueError("Formato no soportado. Use 'csv', 'xlsx' o 'json'.")
        print(f"Archivo guardado en {ruta_salida}")
    except Exception as e:
        raise ValueError(f"Error al guardar el archivo: {e}")
