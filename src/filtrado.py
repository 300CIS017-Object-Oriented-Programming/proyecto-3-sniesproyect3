import streamlit as st
import os
import pandas as pd
import unicodedata


@st.cache_data
def obtener_programas_unicos(df, columna_programa):
    """
    Devuelve una lista ordenada de programas académicos únicos.
    """
    return sorted(df[columna_programa].dropna().unique())

# Función para filtrar DataFrame por programas seleccionados
def filtrar_por_programas(df, programas_seleccionados, columna_programa):
    """
    Filtra el DataFrame por los programas seleccionados.
    """
    return df[df[columna_programa].isin(programas_seleccionados)]