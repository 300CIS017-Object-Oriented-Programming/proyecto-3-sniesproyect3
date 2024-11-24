import streamlit as st
import os
import pandas as pd
import unicodedata
from filtrado import filtrar_por_programas, obtener_programas_unicos
from lectura import leer_y_consolidar_archivos_cached, limpiar_columna

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



COLUMNAS_RELEVANTES = [limpiar_columna(col) for col in COLUMNAS_RELEVANTES]



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
        st.image(image_path, caption="SNIES Extractor", use_container_width = True)
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

with tabs[1]:  # Pestaña: Filtrado de Información
    st.subheader("Filtrado de Información por Programa Académico")

    # Verificar que haya archivos seleccionados
    if st.session_state.archivos_seleccionados:
        st.write("Archivos seleccionados:")
        for archivo in st.session_state.archivos_seleccionados:
            st.write(f"- {archivo}")

        st.write("Cargando y consolidando datos... Espere un momento")

        # Leer y consolidar los datos de los archivos seleccionados
        df_consolidado = leer_y_consolidar_archivos_cached(st.session_state.archivos_seleccionados, ruta_archivos)

        # Guardar df_consolidado en session_state
        st.session_state.df_consolidado = df_consolidado

        if not df_consolidado.empty:
            # Validar si la columna 'programa_academico' está presente
            columna_programa = limpiar_columna(STR_PROGRAMA_ACADEMICO)
            columna_anio = limpiar_columna(STR_SEMESTRE)  # Columna del semestre

            if columna_programa not in df_consolidado.columns:
                st.error(f"La columna '{STR_PROGRAMA_ACADEMICO}' no está presente en los datos consolidados. Revisa los archivos seleccionados.")
            else:
                # Crear la columna 'anio_periodo' combinando año y periodo académico
                if columna_anio in df_consolidado.columns:
                    df_consolidado["anio_periodo"] = df_consolidado[columna_anio].astype(str)
                    st.session_state.df_consolidado = df_consolidado
                else:
                    st.error(f"La columna del semestre ('{columna_anio}') no está presente en los datos.")

                # Obtener los programas únicos
                programas_unicos = obtener_programas_unicos(df_consolidado, columna_programa)

                # Botón de cálculo arriba
                if st.button("Calcular datos para los programas seleccionados (Filtrado)"):
                    if not st.session_state.programas_seleccionados:
                        st.warning("Por favor, selecciona al menos un programa académico antes de continuar.")
                    else:
                        # Filtrar los datos por los programas seleccionados
                        programas_seleccionados = list(st.session_state.programas_seleccionados)
                        df_filtrado = filtrar_por_programas(df_consolidado, programas_seleccionados, columna_programa)

                        # Guardar el resultado filtrado y seleccionados para análisis posterior
                        st.session_state.df_filtrado = df_filtrado
                        st.session_state.programas_seleccionados_final = programas_seleccionados

                        # Mostrar los datos filtrados (o realizar cálculos)
                        st.subheader("Resultados para los programas seleccionados:")
                        columnas_presentes = [col for col in COLUMNAS_RELEVANTES if col in df_filtrado.columns]
                        df_resultado = df_filtrado[columnas_presentes]

                        st.dataframe(df_resultado)

                # Crear una entrada de texto para filtrar programas
                filtro = st.text_input("Filtra programas académicos escribiendo aquí:")

                # Filtrar los programas únicos según el texto ingresado
                programas_filtrados = [p for p in programas_unicos if filtro.lower() in p.lower()] if filtro else programas_unicos

                # Inicializar seleccionados en session_state si no existe
                if "programas_seleccionados" not in st.session_state:
                    st.session_state.programas_seleccionados = set()  # Usamos un set para evitar duplicados

                # Mostrar los checkboxes dinámicamente según el filtro
                st.subheader("Selecciona los programas académicos de interés:")
                for programa in programas_filtrados:
                    if st.checkbox(programa, key=f"checkbox_{programa}"):
                        st.session_state.programas_seleccionados.add(programa)  # Agregar al set global
                    else:
                        st.session_state.programas_seleccionados.discard(programa)  # Quitar del set global
        else:
            st.warning("El DataFrame consolidado está vacío. Revisa los archivos seleccionados.")
    else:
        st.warning("No hay archivos seleccionados. Por favor, selecciona archivos en la pestaña 'Inicio'.")

with tabs[2]:  # Pestaña: Análisis Final
    st.subheader("Análisis Final de los Programas Seleccionados")

    if "df_consolidado" not in st.session_state or st.session_state.df_consolidado.empty:
        st.warning("No hay datos consolidados disponibles. Vuelve a la pestaña de Filtrado de Información.")
    else:
        df_consolidado = st.session_state.df_consolidado

        # Verificar si las columnas necesarias existen en los datos
        columna_modalidad = limpiar_columna(STR_METODOLOGIA)
        columna_institucion = limpiar_columna(STR_NOMBRE_IES)
        columna_programa = limpiar_columna(STR_PROGRAMA_ACADEMICO)
        columna_anio_periodo = "anio_periodo"

        # Crear lista de columnas métricas
        columnas_metrica = [
            limpiar_columna(STR_INSCRITOS),
            limpiar_columna(STR_ADMITIDOS),
            limpiar_columna(STR_PRIMER_CURSO),
            limpiar_columna(STR_MATRICULADOS),
            limpiar_columna(STR_GRADUADOS),
        ]

        # Filtrar las columnas que existen en el DataFrame
        columnas_presentes = [col for col in columnas_metrica if col in df_consolidado.columns]

        if not columnas_presentes:
            st.error("Ninguna de las columnas métricas está presente en los datos. Verifica los archivos cargados.")
        else:
            if columna_modalidad not in df_consolidado.columns:
                st.error(f"La columna de modalidad ('{columna_modalidad}') no está presente en los datos.")
            elif columna_anio_periodo not in df_consolidado.columns:
                st.error(f"La columna 'anio_periodo' no está presente en los datos. Asegúrate de generarla en el filtrado.")
            else:
                # Mostrar programas seleccionados para análisis final
                if "df_filtrado" in st.session_state and not st.session_state.df_filtrado.empty:
                    st.subheader("Selecciona programas específicos para el análisis final:")

                    filtro_final = st.text_input("Filtra programas específicos escribiendo aquí (Análisis Final):")

                    programas_filtrados_final = [
                        p for p in st.session_state.programas_seleccionados_final
                        if filtro_final.lower() in p.lower()
                    ] if filtro_final else st.session_state.programas_seleccionados_final

                    programas_finales_seleccionados = []
                    for programa in programas_filtrados_final:
                        if st.checkbox(programa, key=f"checkbox_final_{programa}"):
                            programas_finales_seleccionados.append(programa)

                    if programas_finales_seleccionados:
                        st.success(f"Programas seleccionados para el análisis final: {len(programas_finales_seleccionados)}")

                        df_analisis_final = st.session_state.df_filtrado[
                            st.session_state.df_filtrado[columna_programa].isin(programas_finales_seleccionados)
                        ]

                        # Agrupar por Modalidad, Programa, Institución y Año/Periodo
                        df_resultado_agrupado = (
                            df_analisis_final.groupby(
                                [columna_modalidad, columna_programa, columna_institucion, columna_anio_periodo]
                            )[columnas_presentes]
                            .sum()
                            .reset_index()
                        )

                        # Pivotear para estructurar como en la imagen
                        df_pivot = df_resultado_agrupado.pivot_table(
                            index=[columna_modalidad, columna_programa, columna_institucion],
                            columns=columna_anio_periodo,
                            values=columnas_presentes,
                            aggfunc="sum",
                            fill_value=0,
                        )

                        # Renombrar columnas
                        df_pivot.columns = [
                            f"{metric} ({period})" for period, metric in df_pivot.columns
                        ]
                        df_pivot.reset_index(inplace=True)

                        # Mostrar tabla final
                        st.subheader("Resultados Finales Agrupados:")
                        st.dataframe(df_pivot, use_container_width=True)

                        # Exportar resultados
                        # Opciones para exportar resultados
                        st.subheader("Exportar resultados:")
                        col1, col2, col3 = st.columns(3)  # Crear tres columnas

                        # Botón para descargar como CSV
                        with col1:
                            csv = df_pivot.to_csv(index=False).encode("utf-8")
                            st.download_button(
                                label="Descargar CSV",
                                data=csv,
                                file_name="resultados_analisis_final.csv",
                                mime="text/csv",
                            )

                        # Botón para descargar como JSON
                        with col2:
                            json = df_pivot.to_json(orient="records", force_ascii=False)
                            st.download_button(
                                label="Descargar JSON",
                                data=json,
                                file_name="resultados_analisis_final.json",
                                mime="application/json",
                            )

                        # Botón para descargar como TXT
                        with col3:
                            txt = df_pivot.to_string(index=False)
                            st.download_button(
                                label="Descargar TXT",
                                data=txt,
                                file_name="resultados_analisis_final.txt",
                                mime="text/plain",
                            )

                    else:
                        st.info("No se seleccionó ningún programa para el análisis final.")
                else:
                    st.warning("No hay datos filtrados disponibles. Vuelve a la pestaña de Filtrado de Información.")