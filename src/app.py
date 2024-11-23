import streamlit as st
import os
import pandas as pd
from settings import STR_PROGRAMA_ACADEMICO

import unicodedata


# Función para limpiar y estandarizar nombres de columnas
def limpiar_columna(nombre):
    """
    Elimina acentos y normaliza un nombre de columna.
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', nombre)
        if unicodedata.category(c) != 'Mn'
    ).lower().replace(" ", "_")


# Función para leer y consolidar archivos
def leer_y_consolidar_archivos(archivos_seleccionados, ruta_base):
    dfs = []

    for archivo in archivos_seleccionados:
        ruta_completa = os.path.join(ruta_base, archivo)
        st.write(f"Intentando leer archivo: {ruta_completa}")
        try:
            df = pd.read_excel(ruta_completa, engine="openpyxl")
            st.write(f"Archivo leído correctamente: {archivo} - Filas: {len(df)}")

            # Estandarizar nombres de columnas
            df.columns = [limpiar_columna(col) for col in df.columns]
            st.write(f"Columnas después de la estandarización: {df.columns.tolist()}")

            # Validar columna 'programa_academico' usando STR_PROGRAMA_ACADEMICO
            columna_estandar = limpiar_columna(STR_PROGRAMA_ACADEMICO)
            if columna_estandar not in df.columns:
                st.error(
                    f"El archivo {archivo} no contiene la columna '{STR_PROGRAMA_ACADEMICO}'. Revisa el nombre de la columna.")
                continue

            df["archivo_origen"] = archivo  # Añadir columna de origen
            dfs.append(df)

        except Exception as e:
            st.error(f"Error al leer el archivo {archivo}: {e}")

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()


# Función para filtrar por palabras clave
def filtrar_por_palabras_clave(df, palabras_clave):
    """
    Filtra un DataFrame por palabras clave en la columna 'programa_academico'.
    """
    if not palabras_clave:
        return df  # Si no hay palabras clave, devuelve el DataFrame completo

    # Crear una expresión regular con las palabras clave
    regex = "|".join(palabras_clave)

    # Filtrar programas académicos
    return df[df["programa_academico"].str.contains(regex, case=False, na=False)]


# Aplicación de Streamlit
st.title("SNIES Extractor APP 📊")

tabs = st.tabs(["Inicio", "Filtrado de Información", "Análisis Final"])

base_dir = os.path.dirname(os.path.abspath(__file__))

with tabs[0]:
    st.subheader("Análisis de datos de educación superior")
    st.write(
        "Bienvenido a la aplicación de análisis de datos de educación superior. "
        "Seleccione un rango de años y los archivos que desea analizar para comenzar."
    )

    image_path = os.path.join(base_dir, "images", "imagen1.jpg")
    if os.path.exists(image_path):
        st.image(image_path, caption="SNIES Extractor", use_container_width=True)
    else:
        st.error("La imagen no se encuentra en la ruta especificada.")

    # Inicializar variables globales en st.session_state
    if "anio_inicio" not in st.session_state:
        st.session_state.anio_inicio = 2021  # Valor predeterminado
    if "anio_fin" not in st.session_state:
        st.session_state.anio_fin = 2023  # Valor predeterminado
    if "archivos_disponibles" not in st.session_state:
        st.session_state.archivos_disponibles = []  # Archivos disponibles (inputs)
    if "archivos_seleccionados" not in st.session_state:
        st.session_state.archivos_seleccionados = []  # Archivos seleccionados para análisis

    # Configuración de rutas
    ruta_archivos = os.path.join(base_dir, "inputs")
    ruta_temporal = os.path.join(base_dir, "temporal")

    # Crear carpeta temporal si no existe
    if not os.path.exists(ruta_temporal):
        os.makedirs(ruta_temporal)

    # Selección de rango de años
    st.subheader("1. Selección de Rango de Años 📅")
    st.session_state.anio_inicio = st.number_input(
        "Año de inicio",
        min_value=2020,
        max_value=2024,
        value=st.session_state.anio_inicio,
        key="anio_inicio_input",
    )
    st.session_state.anio_fin = st.number_input(
        "Año de fin",
        min_value=2021,
        max_value=2024,
        value=st.session_state.anio_fin,
        key="anio_fin_input",
    )

    if st.session_state.anio_inicio > st.session_state.anio_fin:
        st.warning("El año de inicio no puede ser mayor que el año de fin.")
    else:
        st.success(f"Rango de años seleccionado: {st.session_state.anio_inicio} - {st.session_state.anio_fin}")

    # Cargar archivos desde la carpeta inputs y filtrar por rango de años
    st.subheader("2. Archivos Disponibles 📂")
    archivos_disponibles = []
    if os.path.exists(ruta_archivos):
        for archivo in os.listdir(ruta_archivos):
            # Incluir el límite superior (anio_fin)
            for anio in range(st.session_state.anio_inicio, st.session_state.anio_fin + 1):
                if archivo.endswith(".xlsx") and str(anio) in archivo:
                    archivos_disponibles.append(archivo)

    # Mostrar archivos disponibles
    if archivos_disponibles:
        st.session_state.archivos_disponibles = archivos_disponibles
        with st.expander("Mostrar Archivos Disponibles"):
            for archivo in st.session_state.archivos_disponibles:
                st.write(f"- {archivo}")
    else:
        st.warning("No hay archivos disponibles en el rango de años seleccionado.")

    # Selección de archivos disponibles
    seleccionados_disponibles = st.multiselect(
        "Selecciona archivos disponibles para incluir:",
        st.session_state.archivos_disponibles
    )

    # Subir nuevos archivos
    st.subheader("3. Cargar Nuevos Archivos 📤")
    uploaded_files = st.file_uploader(
        "Sube tus archivos aquí (solo .xlsx):", accept_multiple_files=True, type=["xlsx"]
    )

    uploaded_files_names = []
    if uploaded_files:
        st.write(f"{len(uploaded_files)} archivo(s) subido(s):")
        for uploaded_file in uploaded_files:
            st.write(f"- {uploaded_file.name}")
            temp_file_path = os.path.join(ruta_temporal, uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            uploaded_files_names.append(uploaded_file.name)

    # Botón para combinar selección
    if st.button("Confirmar Selección de Archivos"):
        # Combinar los seleccionados disponibles con los nombres de los subidos
        archivos_seleccionados = list(set(seleccionados_disponibles + uploaded_files_names))

        if archivos_seleccionados:
            st.session_state.archivos_seleccionados = archivos_seleccionados
            st.success(f"Archivos seleccionados: {len(st.session_state.archivos_seleccionados)} archivo(s).")
        else:
            st.warning("No has seleccionado ni subido ningún archivo.")

    # Mostrar archivos seleccionados
    st.subheader("4. Archivos Seleccionados para Análisis")
    if st.session_state.archivos_seleccionados:
        with st.expander("Mostrar Archivos Seleccionados"):
            for archivo in st.session_state.archivos_seleccionados:
                st.write(f"- {archivo}")
    else:
        st.info("No se han seleccionado archivos para análisis.")


with tabs[1]:
    st.subheader("Filtrado de Información por Programa Académico")

    # Verificar que haya archivos seleccionados
    if st.session_state.archivos_seleccionados:
        st.write("Archivos seleccionados:")
        for archivo in st.session_state.archivos_seleccionados:
            st.write(f"- {archivo}")

            # Leer y consolidar los datos de los archivos seleccionados
        df_consolidado = leer_y_consolidar_archivos(st.session_state.archivos_seleccionados, ruta_archivos)

        if not df_consolidado.empty:
            st.success(
                f"Datos consolidados: {len(df_consolidado)} filas de {len(st.session_state.archivos_seleccionados)} archivos.")

            # Mostrar columnas disponibles en el DataFrame consolidado
            st.write("Columnas disponibles después de la estandarización:")
            st.write(df_consolidado.columns.tolist())

            # Validar si la columna 'programa_academico' está presente
            columna_programa = limpiar_columna(STR_PROGRAMA_ACADEMICO)
            if columna_programa not in df_consolidado.columns:
                st.error(
                    f"La columna '{STR_PROGRAMA_ACADEMICO}' no está presente en los datos consolidados. Revisa los archivos seleccionados.")
            else:
                # Entrada de texto para palabras clave
                palabras_clave = st.text_input("Escribe palabras clave para filtrar programas académicos:")

                if palabras_clave:
                    st.write("Procesando palabras clave...")
                    lista_palabras = [p.strip() for p in palabras_clave.split()]
                    st.write("Lista de palabras clave:", lista_palabras)

                    # Filtrar programas académicos
                    df_filtrado = filtrar_por_palabras_clave(df_consolidado, lista_palabras)

                    if not df_filtrado.empty:
                        st.success(f"Se encontraron {len(df_filtrado)} programas que coinciden con las palabras clave.")
                        st.dataframe(df_filtrado)

                        # Seleccionar programas específicos
                        seleccionados_programas = st.multiselect(
                            "Selecciona programas para análisis:",
                            options=df_filtrado[columna_programa].unique()
                        )

                        # Guardar programas seleccionados en st.session_state
                        if seleccionados_programas:
                            st.session_state.programas_seleccionados = seleccionados_programas
                            st.success(f"Programas seleccionados: {len(seleccionados_programas)}")
                    else:
                        st.warning("No se encontraron programas académicos que coincidan con las palabras clave.")
        else:
            st.warning("El DataFrame consolidado está vacío. Revisa los archivos seleccionados.")
    else:
        st.warning("No hay archivos seleccionados. Por favor, selecciona archivos en la pestaña 'Inicio'.")
