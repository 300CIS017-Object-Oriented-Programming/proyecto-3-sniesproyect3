# gestor_archivo.py
import os
import pandas as pd
from pathlib import Path
import re
import streamlit as st

class GestorArchivo:
    def __init__(self, data_directory):
        self.data_directory = Path(data_directory)
        # Create all missing parent directories
        self.data_directory.mkdir(exist_ok=True, parents=True)

    def list_csv_files(self):
        """Lists all .csv files in the directory."""
        return [f for f in os.listdir(self.data_directory) if f.endswith('.csv')]

    def filter_files_by_year(self, files, start_year, end_year):
        """Filters files based on the specified year range in the filename."""
        filtered_files = []
        for file_name in files:
            match = re.search(r'(\d{4})', file_name)
            if match:
                year = int(match.group(1))
                if start_year <= year <= end_year:
                    filtered_files.append(file_name)
        return filtered_files

    def load_csv(self, file_path):
        """Loads a CSV file as a DataFrame."""
        try:
            return pd.read_csv(self.data_directory / file_path, delimiter=";")
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")
            return None

    def save_uploaded_file(self, uploaded_file):
        """Saves an uploaded file to the data directory."""
        try:
            file_path = self.data_directory / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} uploaded and saved successfully!")
            return file_path
        except Exception as e:
            st.error(f"Error saving file {uploaded_file.name}: {e}")
            return None
