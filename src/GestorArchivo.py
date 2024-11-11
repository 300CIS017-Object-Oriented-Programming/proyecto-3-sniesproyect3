# gestor_archivo.py
import os
import pandas as pd
from pathlib import Path
import re
import streamlit as st

class GestorArchivo:
    def __init__(self, data_directory):
        self.data_directory = Path(data_directory)
        # Crear directorio si no existe
        self.data_directory.mkdir(exist_ok=True, parents=True)

    def list_csv_files(self):
        """Lista todos los archivos .csv en el directorio."""
        return [f for f in os.listdir(self.data_directory) if f.endswith('.csv')]

    def filter_files_by_year(self, files, start_year, end_year):
        """Filtra archivos según el rango de años en el nombre del archivo."""
        filtered_files = []
        for file_name in files:
            match = re.search(r'(\d{4})', file_name)
            if match:
                year = int(match.group(1))
                if start_year <= year <= end_year:
                    filtered_files.append(file_name)
        return filtered_files

    def load_csv(self, file_path):
        """Carga un archivo CSV como DataFrame."""
        try:
            return pd.read_csv(self.data_directory / file_path, delimiter=";")
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")
            return None

