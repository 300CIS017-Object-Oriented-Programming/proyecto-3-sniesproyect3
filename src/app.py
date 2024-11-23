import streamlit as st
import os
from SNIES_controller import SNIESController
from streamlit_free_text_select import st_free_text_select

# Set the title
st.title("SNIES Extractor APP 📊")

# Create tabs
tabs = st.tabs(["Inicio", "Filtrado de Información", "Análisis Final"])

# Base directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

with tabs[0]:
    st.subheader("Análisis de datos de educación superior")
    st.write(
        "Bienvenido a la aplicación de análisis de datos de educación superior. "
        "Seleccione un rango de años y los archivos que desea analizar para comenzar."
    )


    image_path = os.path.join(base_dir, "images", "imagen1.jpg")


    if os.path.exists(image_path):
        st.image(image_path, caption=".", use_container_width=True)
    else:
        st.error("La imagen no se encuentra en la ruta especificada.")


    ruta_archivos = os.path.join(base_dir, "inputs")
    ruta_temporal = os.path.join(base_dir, "temporal")


    # Crear la carpeta temporal si no existe
    if not os.path.exists(ruta_temporal):
        os.makedirs(ruta_temporal)



    # Sidebar
    st.subheader("1. Selección de Rango de Años 📅")
    anio_inicio = st.number_input("Año de inicio", min_value=2020, max_value=2024, value=2021)
    anio_fin = st.number_input("Año de fin", min_value=2021, max_value=2024, value=2023)
    if anio_inicio > anio_fin:
         st.warning("El año de inicio no puede ser mayor que el año de fin.")

    st.subheader("2. Archivos Disponibles 📂")
    archivos_disponibles = []

    # Filtrar archivos por rango de años
    if os.path.exists(ruta_archivos):
        for archivo in os.listdir(ruta_archivos):
            for anio in range(anio_inicio, anio_fin + 1):
                if archivo.endswith(".xlsx") and str(anio) in archivo:
                    archivos_disponibles.append(archivo)
    else:
        st.error("La ruta especificada no existe.")

    # Mostrar los archivos disponibles
    with st.expander("Mostrar Archivos Disponibles"):
        if archivos_disponibles:
            for archivo in archivos_disponibles:
                st.write(archivo)
        else:
            st.write("No se encontraron archivos para el rango de años seleccionado.")

    # Botón para seleccionar archivos
    if archivos_disponibles:
        seleccionados = []
        st.subheader("3. Selección de Archivos")
        if st.button("Seleccionar Archivos"):
            seleccionados = archivos_disponibles
            st.success(f"Archivos seleccionados: {len(seleccionados)} archivo(s).")
            for archivo in seleccionados:
                st.write(f"- {archivo}")

    # Cargar nuevos archivos
    st.subheader("4. Cargar Nuevos Archivos 📤")
    uploaded_files = st.file_uploader(
        "Sube tus archivos aquí (solo .xlsx):", accept_multiple_files=True, type=["xlsx"]
    )

    if uploaded_files:
        st.write(f"{len(uploaded_files)} archivo(s) subido(s):")
        for uploaded_file in uploaded_files:
            st.write(f"- {uploaded_file.name}")

            # Guardar el archivo en la carpeta temporal
            temp_file_path = os.path.join(ruta_temporal, uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Archivo {uploaded_file.name} guardado en la carpeta temporal.")

        # Mostrar los archivos en la carpeta temporal
    #with st.expander("Mostrar Archivos en la Carpeta Temporal"):
     #   temp_files = os.listdir(ruta_temporal)
      #  if temp_files:
       #     st.write("Archivos en la carpeta temporal:")
        #    for temp_file in temp_files:
         #       st.write(f"- {temp_file}")
       # else:
          #  st.write("No hay archivos en la carpeta temporal.")

#with tabs[1]:
 #   st.subheader("Filtrado de información:")
  #  texto_buqueda = st.text_input("Ingrese palabras clave (nombre programa Académico o nivel de formación):")

    #if texto_buqueda:
    #selected_option = st_free_text_select(
      #  label="Selecciona una opción",
     #   options=["opción1", "opción2", "opción3","casaa","perro"],
        #default="opción1"
    #)

with tabs[1]:
    st.subheader("Filtrado de información:")

    # Inicializar el controlador
    controller = SNIESController(ruta_archivos)

    # Validar si hay archivos disponibles
    if archivos_disponibles:
        # Cargar solo los archivos dentro del rango seleccionado
        controller.cargar_datos_por_rango(archivos_disponibles, anio_inicio, anio_fin)
        st.success("Archivos cargados correctamente.")

        # Mostrar los datos iniciales consolidados
        st.write("Datos consolidados:")
        st.dataframe(controller.data)

        # Filtro de palabras clave
        palabras_clave = st_free_text_select(
            "Ingrese palabras clave para buscar programas académicos:",
            controller.data["programa"].unique().tolist()
        )

        # Aplicar filtro
        if palabras_clave:
            df_filtrado = controller.filtrar_programas(palabras_clave)

            # Mostrar resultados filtrados
            if not df_filtrado.empty:
                st.write(f"Programas encontrados: {len(df_filtrado)}")
                st.dataframe(df_filtrado)

                # Preselección de programas
                programas_seleccionados = st.multiselect(
                    "Seleccione programas para el análisis:",
                    df_filtrado["programa"].unique()
                )
                st.write("Programas seleccionados:")
                st.write(programas_seleccionados)
            else:
                st.warning("No se encontraron programas con las palabras clave especificadas.")
    else:
        st.warning("Por favor, seleccione un rango de años y cargue archivos en la pestaña 'Inicio'.")

with tabs[2]:
    st.subheader("Analisis Final")
    st.subheader("Exportación de Datos")
    if controller.data != None & controller.data != controller.data.empty():
        st.write("Datos disponibles para exportación")
        st.dataframe(controller.data)

        st.subheader("Exportar Datos")
        export_format = st.radio("Seleccione el formato de exportación:", ["CSV","JSON","XLSX"])

        if st._bottom("Exportar"):
            output_path = os.path.join(ruta_temporal, f"exported_data.{export_format.lower()}")

            try:
                if export_format == "CSV":
                    controller.data.to_csv(output_path, index = False)
                elif export_format == "JSON":
                    controller.data.to_json(output_path, orient = "records", lines = True)
                elif export_format == "XLSX":
                    controller.data.to_excel(output_path, index= False, engine= "openpyxl")

                with open(output_path, "rb") as file:
                    btn = st.download_button(
                        label=f"Descargar{export_format}", 
                        data= file, 
                        file_name= f"Data exportado{export_format.lower()}", 
                        mime=f"texto{export_format.lower()}"
                        if export_format != "XLSX" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" #lo de applicaciton.etc es el MIME para archivos Excel en formato xlsx
                        )
                    st.success(f"Datos exportados exitosamente como {export_format}.")

            except Exception as e:
                st.error(f"Error al exportar datos {e}")

        else:
            st.warning("No hay datos disponibles para exportar.")

            



                
                