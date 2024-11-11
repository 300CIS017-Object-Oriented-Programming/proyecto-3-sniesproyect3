# main.py
import streamlit as st
from data_loader import DataLoaderApp
from SNIESController import SNIESController
from GestorArchivo import GestorArchivo

def main():
    data_directory = r"proyecto-3-sniesproyect3\docs"
    gestor_archivo = GestorArchivo(data_directory)
    data_loader = DataLoaderApp(gestor_archivo)
    snies_controller = SNIESController(data_directory)

    # Run DataLoaderApp to manage file selection and filtering
    data_loader.run()

    # Load and analyze selected files in SNIESController
    if data_loader.selected_files:
        start_year = data_loader.start_year
        end_year = data_loader.end_year
        keywords = data_loader.keywords  # New: retrieve keywords from DataLoaderApp
        snies_controller.cargar_programas(start_year, end_year, keywords)  # Pass keywords

        # Display Analysis Section
        st.subheader("Data Analysis Results")
        for file, df in snies_controller.programas_academicos.items():
            st.write(f"Data from {file}")
            st.dataframe(df)

        # Download options
        st.subheader("Download Data")
        snies_controller.download_button()

if __name__ == "__main__":
    main()