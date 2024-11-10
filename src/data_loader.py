# Filename: data_loader.py
import streamlit as st
import os
import pandas as pd
from pathlib import Path
import re


class FileHandler:
    """Handles file listing, filtering, loading, and saving operations."""

    def __init__(self, data_directory):
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(exist_ok=True)  # Ensure the directory exists

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
            return pd.read_csv(self.data_directory / file_path)
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


class DataLoaderApp:
    """Streamlit application for loading and previewing CSV data files."""

    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.temp_files = []

    def run(self):
        st.title("SNIES Data Loader and Analyzer")

        # Step 1: Select year range
        self.select_year_range()

        # Step 2: Display available files within the selected year range
        available_files = self.file_handler.list_csv_files()
        self.display_available_files(available_files)

        # Step 3: File upload functionality
        self.handle_file_upload()

        # Step 4: Select files to include in analysis
        self.select_files_for_analysis(available_files)

    def select_year_range(self):
        """Allows user to select the year range."""
        st.subheader("Files Year Range for Analysis")
        self.start_year = st.number_input("Start Year", min_value=2020, max_value=2024, value=2020)
        self.end_year = st.number_input("End Year", min_value=2020, max_value=2024, value=2020)
        
        if self.start_year > self.end_year:
            st.warning("Start year cannot be greater than end year.")
            return False
        return True

    def display_available_files(self, available_files):
        """Displays the list of available files filtered by the selected year range."""
        st.subheader("Available Data Files")
        filtered_files = self.file_handler.filter_files_by_year(available_files, self.start_year, self.end_year)
        
        if not filtered_files:
            st.warning(f"No files available in the year range {self.start_year} to {self.end_year}.")
        else:
            st.write(f"Files available for analysis ({self.start_year} - {self.end_year}):")
            for file_name in filtered_files:
                st.text(file_name)
        
        self.filtered_files = filtered_files

    def handle_file_upload(self):
        """Handles file upload and saves the uploaded files."""
        st.subheader("Additional Data Files for Analysis")
        uploaded_file = st.file_uploader("Upload a .csv file", type="csv")
        
        if uploaded_file:
            file_path = self.file_handler.save_uploaded_file(uploaded_file)
            if file_path:
                self.temp_files.append(file_path.name)

    def select_files_for_analysis(self, available_files):
        """Allows user to select files for analysis and previews the data."""
        st.subheader("Select Files for Analysis")
        all_files = self.filtered_files + self.temp_files
        selected_files = st.multiselect("Choose files to load", all_files)
        
        # Load and preview data for selected files
        if selected_files:
            st.subheader("Data Preview")
            for file_name in selected_files:
                data = self.file_handler.load_csv(file_name)
                if data is not None:
                    st.write(f"Preview of {file_name}")
                    st.dataframe(data.head())


if __name__ == "__main__":
    data_directory = r"C:\Users\isabe\OneDrive\Escritorio\POO\proyecto-3-sniesproyect3\docs"
    file_handler = FileHandler(data_directory)
    app = DataLoaderApp(file_handler)
    app.run()
