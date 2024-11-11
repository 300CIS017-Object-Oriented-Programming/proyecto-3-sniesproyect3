# gestor_archivo.py
import os
import pandas as pd
from pathlib import Path
import re
import streamlit as st

class GestorArchivo:
    def __init__(self, data_directory):
        self.data_directory = Path(data_directory)
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
        """Carga un archivo CSV como DataFrame, especificando el tipo de datos para evitar advertencias."""
        try:
            # Define column dtypes explicitly for known columns
            dtype_dict = {'AÑO': str}  # Convert 'AÑO' column to string to avoid Arrow conversion issues
            return pd.read_csv(
                self.data_directory / file_path,
                delimiter=";",
                low_memory=False,  # Disable low_memory to handle mixed types better
                dtype=dtype_dict  # Specify dtypes to control mixed-type warnings
            )
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")
            return None

    def save_uploaded_file(self, uploaded_file):
        """Guarda el archivo subido en el directorio de datos."""
        try:
            file_path = self.data_directory / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} saved successfully!")
            return file_path
        except Exception as e:
            st.error(f"Failed to save file {uploaded_file.name}: {e}")
            return None
