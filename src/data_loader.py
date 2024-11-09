# Filename: data_loader.py
import streamlit as st
import os
import pandas as pd
from pathlib import Path
import re

DATA_DIR = r"C:\Users\isabe\OneDrive\Escritorio\POO\proyecto-3-sniesproyect3\docs"
Path(DATA_DIR).mkdir(exist_ok=True)  # Ensure the directory exists


def list_csv_files(directory):
    """Lists all .csv files in the given directory."""
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    return files

def filter_files_by_year(files, start_year, end_year):
    """Filters files based on the specified year range in the filename."""
    filtered_files = []
    for file_name in files:
        match = re.search(r'(\d{4})', file_name)
        if match:
            year = int(match.group(1))
            if start_year <= year <= end_year:
                filtered_files.append(file_name)
    return filtered_files

def load_csv(file_path):
    """Loads a CSV file as a DataFrame."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return None

def save_uploaded_file(uploaded_file, save_directory):
    """Saves the uploaded file to the specified directory."""
    try:
        # Ensure save_directory is a Path object
        save_directory = Path(DATA_DIR) if isinstance(save_directory, str) else save_directory
        file_path = save_directory / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File {uploaded_file.name} uploaded and saved successfully!")
        return file_path
    except Exception as e:
        st.error(f"Error saving file {uploaded_file.name}: {e}")
        return None


def main():
    st.title("SNIES Data Loader and Analyzer")
    
    # Step 1: Select year range
    st.subheader("Files Year Range for Analysis")
    start_year = st.number_input("Start Year", min_value=2020, max_value=2024, value=2020)
    end_year = st.number_input("End Year", min_value=2020, max_value=2024, value=2020)
    
    if start_year > end_year:
        st.warning("Start year cannot be greater than end year.")
        return

    # Step 2: Display available files within the selected year range
    st.subheader("Available Data Files")
    available_files = list_csv_files(DATA_DIR)
    filtered_files = filter_files_by_year(available_files, start_year, end_year)
    
    if not filtered_files:
        st.warning(f"No files available in the year range {start_year} to {end_year}.")
    else:
        st.write(f"Files available for analysis ({start_year} - {end_year}):")
        for file_name in filtered_files:
            st.text(file_name)


    # Step 3: File upload functionality
    st.subheader("Additional Data Files for Analysis")
    uploaded_file = st.file_uploader("Upload a .csv file", type="csv")
    temp_files = []

    if uploaded_file:
        save_uploaded_file(uploaded_file, DATA_DIR)

    elif uploaded_file:
        temp_file_path = Path(DATA_DIR) / f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        temp_files.append(temp_file_path)
        st.success(f"File {uploaded_file.name} uploaded temporarily!")
    
    # Step 4: Select files to include in analysis (including temp files if uploaded)
    st.subheader("Select Files for Analysis")
    all_files = filtered_files + [f.name for f in temp_files]
    selected_files = st.multiselect("Choose files to load", all_files)

    # Step 5: Load and preview data for selected files
    if selected_files:
        st.subheader("Data Preview")
        for file_name in selected_files:
            file_path = Path(DATA_DIR) / (file_name if "temp_" not in file_name else f"temp_{file_name}")
            data = load_csv(file_path)
            if data is not None:
                st.write(f"Preview of {file_name}")
                st.dataframe(data.head())

if __name__ == "__main__":
    main()
