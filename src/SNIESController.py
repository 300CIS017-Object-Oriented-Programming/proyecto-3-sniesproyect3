# snies_controller.py
import csv
import json
import pandas as pd
from Settings import Settings
from GestorArchivo import GestorArchivo
import streamlit as st

class SNIESController:
    def __init__(self, data_directory):
        self.gestor_archivo = GestorArchivo(data_directory)
        self.programas_academicos = {}

    def cargar_programas(self, start_year, end_year):
        files = self.gestor_archivo.list_csv_files()
        filtered_files = self.gestor_archivo.filter_files_by_year(files, start_year, end_year)

        for file_name in filtered_files:
            data = self.gestor_archivo.load_csv(file_name)
            if data is not None:
                self.programas_academicos[file_name] = data

    def export_data(self, format_type="csv"):
        if not self.programas_academicos:
            st.warning("No data available to export.")
            return

        output_file = Settings.OUTPUTS_PATH + "program_data." + format_type

        if format_type == "json":
            with open(output_file, 'w') as json_file:
                json.dump({file: df.to_dict(orient="records") for file, df in self.programas_academicos.items()}, json_file)
        elif format_type == "csv":
            with open(output_file, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=";")
                for file, df in self.programas_academicos.items():
                    csv_writer.writerow([f"Data from {file}"])
                    df.to_csv(csv_file, index=False, header=True, sep=";", mode="a")
        elif format_type == "xlsx":
            with pd.ExcelWriter(output_file) as writer:
                for file, df in self.programas_academicos.items():
                    df.to_excel(writer, sheet_name=file[:30], index=False)

        st.success(f"Data exported successfully as {format_type.upper()}!")

    def download_button(self):
        if st.button("Download CSV"):
            self.export_data("csv")
        if st.button("Download JSON"):
            self.export_data("json")
        if st.button("Download XLSX"):
            self.export_data("xlsx")
