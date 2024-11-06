# Filename: data_loader.py
import streamlit as st
import os
import pandas as pd
from pathlib import Path

# Directory where files are stored
DATA_DIR = "inputs"
Path(DATA_DIR).mkdir(exist_ok=True)  # Ensure the inputs directory exists

def list_xlsx_files(directory):
    """Lists all .xlsx files in the given directory."""
    return [f for f in os.listdir(directory) if f.endswith('.xlsx')]

def load_excel(file_path):
    """Loads an Excel file as a DataFrame."""
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return None

def main():
    st.title("Data Loading for SNIES Analysis")

    # Step 1: Display available files in inputs directory
    st.subheader("Available Data Files")
    available_files = list_xlsx_files(DATA_DIR)
    if len(available_files) < 4:
        st.warning("At least four years of data are required for analysis.")
    
    # Show files in directory
    for file_name in available_files:
        st.text(file_name)

    # Step 2: File upload functionality
    st.subheader("Upload Additional Data Files")
    uploaded_file = st.file_uploader("Upload an .xlsx file", type="xlsx")
    if uploaded_file:
        save_path = os.path.join(DATA_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File {uploaded_file.name} uploaded successfully!")
        available_files = list_xlsx_files(DATA_DIR)  # Refresh file list

    # Step 3: Load and preview data
    st.subheader("Select Files to Load and Preview")
    selected_files = st.multiselect("Choose files to load", available_files)

    if selected_files:
        for file_name in selected_files:
            file_path = os.path.join(DATA_DIR, file_name)
            data = load_excel(file_path)
            if data is not None:
                st.write(f"Preview of {file_name}")
                st.dataframe(data.head())  # Display first few rows of the file

if __name__ == "__main__":
    main()
