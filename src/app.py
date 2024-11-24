import streamlit as st
import os
import pandas as pd
import unicodedata

from settings import (
    STR_CODIGO_SNIES,
    STR_PROGRAMA_ACADEMICO,
    STR_METODOLOGIA,
    STR_NOMBRE_IES,
    STR_TIPO_IES,
    STR_DEPARTAMENTO,
    STR_MUNICIPIO,
    STR_NIVEL_FORMACION,
    STR_SEMESTRE,
    STR_ADMITIDOS,
    STR_GRADUADOS,
    STR_INSCRITOS,
    STR_MATRICULADOS,
    STR_PRIMER_CURSO,
)

# Lista de columnas relevantes
COLUMNAS_RELEVANTES = [
    STR_CODIGO_SNIES,
    STR_PROGRAMA_ACADEMICO,
    STR_METODOLOGIA,
    STR_NOMBRE_IES,
    STR_TIPO_IES,
    STR_DEPARTAMENTO,
    STR_MUNICIPIO,
    STR_NIVEL_FORMACION,
    STR_SEMESTRE,
    STR_ADMITIDOS,
    STR_GRADUADOS,
    STR_INSCRITOS,
    STR_MATRICULADOS,
    STR_PRIMER_CURSO,
]

# Función para limpiar y estandarizar nombres de columnas
def limpiar_columna(nombre):
    """
    Elimina acentos y normaliza un nombre de columna.
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', nombre)
        if unicodedata.category(c) != 'Mn'
    ).lower().replace(" ", "_")

COLUMNAS_RELEVANTES = [limpiar_columna(col) for col in COLUMNAS_RELEVANTES]

@st.cache_data
def leer_y_consolidar_archivos_cached(archivos_seleccionados, ruta_base):
    dfs = []

    for archivo in archivos_seleccionados:
        ruta_completa = os.path.join(ruta_base, archivo)
        try:
            df = pd.read_excel(ruta_completa, engine="openpyxl")
            df.columns = [limpiar_columna(col) for col in df.columns]

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

@st.cache_data
def obtener_programas_unicos(df, columna_programa):
    """
    Devuelve una lista ordenada de programas académicos únicos.
    """
    return sorted(df[columna_programa].dropna().unique())

# Función para filtrar DataFrame por programas seleccionados
def filtrar_por_programas(df, programas_seleccionados, columna_programa):
    """
    Filtra el DataFrame por los programas seleccionados.
    """
    return df[df[columna_programa].isin(programas_seleccionados)]

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

    ruta_archivos = os.path.join(base_dir, "inputs")
    ruta_temporal = os.path.join(base_dir, "temporal")

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
            for anio in range(st.session_state.anio_inicio, st.session_state.anio_fin + 1):
                if archivo.endswith(".xlsx") and str(anio) in archivo:
                    archivos_disponibles.append(archivo)

    if archivos_disponibles:
        st.session_state.archivos_disponibles = archivos_disponibles
        with st.expander("Mostrar Archivos Disponibles"):
            for archivo in st.session_state.archivos_disponibles:
                st.write(f"- {archivo}")
    else:
        st.warning("No hay archivos disponibles en el rango de años seleccionado.")

    seleccionados_disponibles = st.multiselect(
        "Selecciona archivos disponibles para incluir:",
        st.session_state.archivos_disponibles
    )

    uploaded_files = st.file_uploader(
        "Sube tus archivos aquí (solo .xlsx):", accept_multiple_files=True, type=["xlsx"]
    )

    uploaded_files_names = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            temp_file_path = os.path.join(ruta_temporal, uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            uploaded_files_names.append(uploaded_file.name)

    if st.button("Confirmar Selección de Archivos"):
        archivos_seleccionados = list(set(seleccionados_disponibles + uploaded_files_names))
        st.session_state.archivos_seleccionados = archivos_seleccionados

with tabs[1]:
    st.subheader("Filtrado de Información por Programa Académico")

    # Verificar que haya archivos seleccionados
    if st.session_state.archivos_seleccionados:
        st.write("Archivos seleccionados:")
        for archivo in st.session_state.archivos_seleccionados:
            st.write(f"- {archivo}")

        st.write("Cargando y consolidando datos... Espere un momento")

        # Leer y consolidar los datos de los archivos seleccionados
        df_consolidado = leer_y_consolidar_archivos_cached(st.session_state.archivos_seleccionados, ruta_archivos)

        if not df_consolidado.empty:
            # Validar si la columna 'programa_academico' está presente
            columna_programa = limpiar_columna(STR_PROGRAMA_ACADEMICO)
            if columna_programa not in df_consolidado.columns:
                st.error(f"La columna '{STR_PROGRAMA_ACADEMICO}' no está presente en los datos consolidados. Revisa los archivos seleccionados.")
            else:
                # Obtener los programas únicos
                programas_unicos = obtener_programas_unicos(df_consolidado, columna_programa)

                # Crear una entrada de texto para filtrar programas
                filtro = st.text_input("Filtra programas académicos escribiendo aquí:")

                # Filtrar los programas únicos según el texto ingresado
                programas_filtrados = [p for p in programas_unicos if filtro.lower() in p.lower()] if filtro else programas_unicos

                # Inicializar seleccionados en session_state si no existe
                if "programas_seleccionados" not in st.session_state:
                    st.session_state.programas_seleccionados = set()  # Usamos un set para evitar duplicados

                # **Mover el botón de cálculo aquí**
                if st.button("Calcular datos para los programas seleccionados"):
                    if not st.session_state.programas_seleccionados:
                        st.warning("Por favor, selecciona al menos un programa académico antes de continuar.")
                    else:
                        # Filtrar los datos por los programas seleccionados
                        programas_seleccionados = list(st.session_state.programas_seleccionados)
                        df_filtrado = filtrar_por_programas(df_consolidado, programas_seleccionados, columna_programa)

                        # Mostrar los datos filtrados (o realizar cálculos)
                        st.subheader("Resultados para los programas seleccionados:")
                        columnas_presentes = [col for col in COLUMNAS_RELEVANTES if col in df_filtrado.columns]
                        df_resultado = df_filtrado[columnas_presentes]

                        st.dataframe(df_resultado)

                # Mostrar los checkboxes dinámicamente según el filtro
                st.subheader("Selecciona los programas académicos de interés:")
                for programa in programas_filtrados:
                    if st.checkbox(programa, key=f"checkbox_{programa}"):
                        st.session_state.programas_seleccionados.add(programa)  # Agregar al set global
                    else:
                        st.session_state.programas_seleccionados.discard(programa)  # Quitar del set global

                # Convertir el set a lista para mantener consistencia
                programas_seleccionados = list(st.session_state.programas_seleccionados)

                # Mostrar los programas seleccionados
                #st.success(f"Programas seleccionados: {len(programas_seleccionados)}")
                #st.write(programas_seleccionados)
        else:
            st.warning("El DataFrame consolidado está vacío. Revisa los archivos seleccionados.")
    else:
        st.warning("No hay archivos seleccionados. Por favor, selecciona archivos en la pestaña 'Inicio'.")
