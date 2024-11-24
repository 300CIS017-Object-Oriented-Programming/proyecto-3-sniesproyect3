import streamlit as st
import os
import pandas as pd
import unicodedata
from settings import COLUMNAS_RELEVANTES, STR_PROGRAMA_ACADEMICO

# Función para limpiar y estandarizar nombres de columnas
def limpiar_columna(nombre):
    """
    Elimina acentos y normaliza un nombre de columna.
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', nombre)
        if unicodedata.category(c) != 'Mn'
    ).lower().replace(" ", "_")

@st.cache_data
def leer_y_consolidar_archivos_cached(archivos_seleccionados, ruta_base):
    dfs = []

    for archivo in archivos_seleccionados:
        ruta_completa = os.path.join(ruta_base, archivo)
        try:
            df = pd.read_excel(ruta_completa, engine="openpyxl")
            df.columns = [limpiar_columna(col) for col in df.columns]

            columna_estandar = limpiar_columna(STR_PROGRAMA_ACADEMICO)
            if columna_estandar not in df.columns:
                st.error(
                    f"El archivo {archivo} no contiene la columna '{STR_PROGRAMA_ACADEMICO}'. Revisa el nombre de la columna.")
                continue

            df["archivo_origen"] = archivo  # Añadir columna de origen
            dfs.append(df)

        except Exception as e:
            st.error(f"Error al leer el archivo {archivo}: {e}")

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()