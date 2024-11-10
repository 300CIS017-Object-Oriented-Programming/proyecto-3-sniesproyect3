import streamlit as st
from data_loader import DataLoaderApp
from SNIESController import SNIESController
from GestorArchivo import GestorArchivo

def main():
    data_directory = r"C:\SNIES_EXTRACTOR\inputs"
    gestor_archivo = GestorArchivo(data_directory)
    data_loader = DataLoaderApp(gestor_archivo)
    snies_controller = SNIESController(data_directory)

    # Run DataLoaderApp to manage file selection
    data_loader.run()
    
    # Load and analyze selected files in SNIESController
    if data_loader.selected_files:
        start_year = data_loader.start_year
        end_year = data_loader.end_year
        snies_controller.cargar_programas(start_year, end_year)

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
