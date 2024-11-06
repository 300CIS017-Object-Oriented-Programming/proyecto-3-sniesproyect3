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
    st.title("SNIES Data Loader and Analyzer")

    # Step 1: Display available files in inputs directory
    st.subheader("Available Data Files")
    available_files = list_xlsx_files(DATA_DIR)
    
    if not available_files:
        st.warning("No files available in the inputs directory.")
    else:
        st.write("Available files for analysis:")
        for file_name in available_files:
            st.text(file_name)

    # Step 2: Upload additional files temporarily
    st.subheader("Upload Additional Data Files for Analysis")
    uploaded_file = st.file_uploader("Upload an .xlsx file", type="xlsx")
    temp_files = []

    if uploaded_file:
        temp_file_path = os.path.join(DATA_DIR, f"temp_{uploaded_file.name}")
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        temp_files.append(temp_file_path)
        st.success(f"File {uploaded_file.name} uploaded temporarily!")
    
    # Step 3: Select files to include in analysis (including temp files if uploaded)
    st.subheader("Select Files for Analysis")
    all_files = available_files + [Path(f).name for f in temp_files]
    selected_files = st.multiselect("Choose files to load", all_files)

    # Step 4: Load and preview data for selected files
    if selected_files:
        st.subheader("Data Preview")
        for file_name in selected_files:
            file_path = os.path.join(DATA_DIR, file_name if "temp_" not in file_name else f"temp_{file_name}")
            data = load_excel(file_path)
            if data is not None:
                st.write(f"Preview of {file_name}")
                st.dataframe(data.head())  # Display first few rows of the file

if __name__ == "__main__":
    main()
