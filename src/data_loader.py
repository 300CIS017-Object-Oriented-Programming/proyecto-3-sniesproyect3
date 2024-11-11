# data_loader_app.py
import streamlit as st
from GestorArchivo import GestorArchivo

class DataLoaderApp:
    def __init__(self, gestor_archivo):
        self.gestor_archivo = gestor_archivo
        self.temp_files = []
        self.selected_files = []  # Initialize selected_files to avoid AttributeError
        self.keywords = ""

    def run(self):
        st.title("SNIES Data Loader and Analyzer")
        if self.select_year_range():
            available_files = self.gestor_archivo.list_csv_files()
            self.display_available_files(available_files)
            self.handle_file_upload()
            self.select_files_for_analysis()
            self.input_keywords()

    def select_year_range(self):
        st.subheader("Files Year Range for Analysis")
        self.start_year = st.number_input("Start Year", min_value=2020, max_value=2024, value=2020)
        self.end_year = st.number_input("End Year", min_value=2020, max_value=2024, value=2020)
        if self.start_year > self.end_year:
            st.warning("Start year cannot be greater than end year.")
            return False
        return True

    def display_available_files(self, available_files):
        st.subheader("Available Data Files")
        self.filtered_files = self.gestor_archivo.filter_files_by_year(available_files, self.start_year, self.end_year)
        if not self.filtered_files:
            st.warning(f"No files available in the year range {self.start_year} to {self.end_year}.")
        else:
            st.write(f"Files available for analysis ({self.start_year} - {self.end_year}):")
            for file_name in self.filtered_files:
                st.text(file_name)

    def handle_file_upload(self):
        st.subheader("Upload Additional Data Files")
        uploaded_file = st.file_uploader("Upload a .csv file", type="csv")
        if uploaded_file:
            file_path = self.gestor_archivo.save_uploaded_file(uploaded_file)
            if file_path:
                self.temp_files.append(file_path.name)

    def input_keywords(self):
        st.subheader("Search Programs by Keywords")
        self.keywords = st.text_input("Enter keywords to search programs")

    def select_files_for_analysis(self):
        st.subheader("Select Files for Analysis")
        all_files = self.filtered_files + self.temp_files
        self.selected_files = st.multiselect("Choose files to load", all_files)
