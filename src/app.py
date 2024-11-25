import streamlit as st
import os
import pandas as pd
import unicodedata
import io
from filtrado import filtrar_por_programas, obtener_programas_unicos
from lectura import leer_y_consolidar_archivos_cached, limpiar_columna
from grafico import graficar_tendencias, graficar_comparativo

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
    STR_GENERO,
)

from settings import COLUMNAS_RELEVANTES, COLORES_TENDENCIA, COLOR_MAP_MODALIDAD, COLOR_MAP_SEXO, COLOR_MAP_NIVEL_FORMACION, MAPEO_GENERO


# Lista de columnas relevantes
COLUMNAS_RELEVANTES = [limpiar_columna(col) for col in COLUMNAS_RELEVANTES]

#app
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

    # Inicializar variables globales en st.session_state para q se guarden
    if "anio_inicio" not in st.session_state:
        st.session_state.anio_inicio = 2021
    if "anio_fin" not in st.session_state:
        st.session_state.anio_fin = 2023
    if "archivos_disponibles" not in st.session_state:
        st.session_state.archivos_disponibles = []  # Archivos disponibles (inputs)
    if "archivos_seleccionados" not in st.session_state:
        st.session_state.archivos_seleccionados = []  # Archivos seleccionados para analisis

    ruta_archivos = os.path.join(base_dir, "inputs")
    ruta_temporal = os.path.join(base_dir, "temporal")

    if not os.path.exists(ruta_temporal):
        os.makedirs(ruta_temporal)

    # Seleccion de rango de años
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
        st.write("Archivos seleccionados... Vaya a la pestaña filtrado de información para continuar.")

with tabs[1]:  # Pestaña: Filtrado de Información
    st.subheader("Filtrado de Información por Programa Académico")

    # Verificar que haya archivos seleccionados
    if st.session_state.archivos_seleccionados:
        st.write("Archivos seleccionados:")
        for archivo in st.session_state.archivos_seleccionados:
            st.write(f"- {archivo}")

        st.write("Cargando y consolidando datos... Espere un momento")

        # Lee y consolida los datos de los archivos seleccionados
        df_consolidado = leer_y_consolidar_archivos_cached(st.session_state.archivos_seleccionados, ruta_archivos)

        # Guardar df_consolidado en session_state (global)
        st.session_state.df_consolidado = df_consolidado

        if not df_consolidado.empty:
            # Validar si la columna 'programa_academico' está presente
            columna_programa = limpiar_columna(STR_PROGRAMA_ACADEMICO)
            columna_anio = limpiar_columna(STR_SEMESTRE)  # Columna del semestre

            if columna_programa not in df_consolidado.columns:
                st.error(f"La columna '{STR_PROGRAMA_ACADEMICO}' no está presente en los datos consolidados. Revisa los archivos seleccionados.")
            else:
                # Crear la columna anio_periodo combinando año y periodo academico
                if columna_anio in df_consolidado.columns:
                    df_consolidado["anio_periodo"] = df_consolidado[columna_anio].astype(str)
                    st.session_state.df_consolidado = df_consolidado
                else:
                    st.error(f"La columna del semestre ('{columna_anio}') no está presente en los datos.")

                # Obtener los programas unicos
                programas_unicos = obtener_programas_unicos(df_consolidado, columna_programa)

                # Boton de calculo arriba
                if st.button("Calcular datos para los programas seleccionados (Filtrado)"):
                    if not st.session_state.programas_seleccionados:
                        st.warning("Por favor, selecciona al menos un programa académico antes de continuar.")
                    else:
                        # Filtrar los datos por los programas seleccionados
                        programas_seleccionados = list(st.session_state.programas_seleccionados)
                        df_filtrado = filtrar_por_programas(df_consolidado, programas_seleccionados, columna_programa)

                        # Guardar el resultado filtrado y seleccionados para analisis final
                        st.session_state.df_filtrado = df_filtrado
                        st.session_state.programas_seleccionados_final = programas_seleccionados

                        # Mostrar los datos filtrados (o realizar cálculos)
                        st.write("Calculando resultados... Espere un momento")
                        st.subheader("Resultados para los programas seleccionados:")
                        columnas_presentes = [col for col in COLUMNAS_RELEVANTES if col in df_filtrado.columns]
                        df_resultado = df_filtrado[columnas_presentes]
                        st.write("Continue a la siguiente pestaña para el analisis final.😄")

                        st.dataframe(df_resultado)

                # entrada de texto para filtrar programas
                filtro = st.text_input("Filtra programas académicos escribiendo aquí:")

                # Filtrar los programas unicos según el texto ingresado
                programas_filtrados = [p for p in programas_unicos if filtro.lower() in p.lower()] if filtro else programas_unicos

                # Inicializar seleccionados en session_state si no existe
                if "programas_seleccionados" not in st.session_state:
                    st.session_state.programas_seleccionados = set()  # Usamos un set para evitar duplicados

                # Mostrar los checkboxes segun el filtro
                st.subheader("Selecciona los programas académicos de interés:")
                for programa in programas_filtrados:
                    if st.checkbox(programa, key=f"checkbox_{programa}"):
                        st.session_state.programas_seleccionados.add(programa)  # Agregar al set global si se marca
                    else:
                        st.session_state.programas_seleccionados.discard(programa)  # Quitar del set global si no se marca
        else:
            st.warning("El DataFrame consolidado está vacío. Revisa los archivos seleccionados.")
    else:
        st.warning("No hay archivos seleccionados😵. Por favor, selecciona archivos en la pestaña 'Inicio'")


with tabs[2]:
    st.subheader("Análisis Final de los Programas Seleccionados")

    if "df_consolidado" not in st.session_state or st.session_state.df_consolidado.empty:
        st.warning("No hay datos consolidados disponibles. Vuelve a la pestaña de Filtrado de Información.")
    else:
        df_consolidado = st.session_state.df_consolidado

        # Normalizar la columna de género (si existe)
        columna_genero = limpiar_columna(STR_GENERO)

        if columna_genero in df_consolidado.columns:
            # Aplicar el mapeo
            df_consolidado[columna_genero] = df_consolidado[columna_genero].map(MAPEO_GENERO).fillna("No especificado")

        df_consolidado = df_consolidado[df_consolidado[columna_genero].isin(["Masculino", "Femenino"])]

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

        # Verificar y filtrar las columnas que existen en el DataFrame
        columnas_presentes = [col for col in columnas_metrica if col in df_consolidado.columns]
        columnas_necesarias = [columna_modalidad, columna_institucion, columna_programa, columna_anio_periodo]

        # Continuar con las columnas disponibles
        if columnas_presentes:
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
                    st.success(
                        f"Programas seleccionados para el análisis final: {len(programas_finales_seleccionados)}")

                    df_analisis_final = st.session_state.df_filtrado[
                        st.session_state.df_filtrado[columna_programa].isin(programas_finales_seleccionados)
                    ]

                    # Agrupar por las columnas disponibles
                    agrupacion_columnas = [col for col in [columna_modalidad, columna_programa, columna_institucion,
                                                           columna_anio_periodo] if col in df_analisis_final.columns]
                    df_resultado_agrupado = (
                        df_analisis_final.groupby(agrupacion_columnas)[columnas_presentes]
                        .sum()
                        .reset_index()
                    )

                    # Pivotear si la columna 'anio_periodo' está disponible
                    if columna_anio_periodo in agrupacion_columnas:
                        df_pivot = df_resultado_agrupado.pivot_table(
                            index=[col for col in agrupacion_columnas if col != columna_anio_periodo],
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
                    else:
                        df_pivot = df_resultado_agrupado  # Sin pivotear

                    # Mostrar tabla final
                    st.subheader("Resultados Finales Agrupados:")
                    st.dataframe(df_pivot, use_container_width=True)

                    # Exportar resultados
                    st.subheader("Exportar resultados:")
                    col1, col2, col3 = st.columns(3)  # Crear tres columnas

                    # Boton para descargar como CSV
                    with col1:
                        csv = df_pivot.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            label="Descargar CSV",
                            data=csv,
                            file_name="resultados_analisis_final.csv",
                            mime="text/csv",
                        )

                    # Boton para descargar como JSON
                    with col2:
                        json = df_pivot.to_json(orient="records", force_ascii=False)
                        st.download_button(
                            label="Descargar JSON",
                            data=json,
                            file_name="resultados_analisis_final.json",
                            mime="application/json",
                        )

                    # Boton para descargar como xlsx
                    with col3:
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            df_pivot.to_excel(writer, index=False, sheet_name='Resultados')

                        buffer.seek(0)

                        st.download_button(
                            label="Descargar Excel",
                            data=buffer,
                            file_name="resultados_analisis_final.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                    # Crear columna anio_periodo si no existe
                    if "anio_periodo" not in df_analisis_final.columns:
                        df_analisis_final["anio_periodo"] = pd.to_datetime(df_analisis_final["semestre"],
                                                                           errors="coerce").dt.year

                    # Graficar tendencias
                    st.subheader("Gráficos de Tendencias 📈")

                    # Generar graficos para las métricas seleccionadas
                    graficas_tendencias = graficar_tendencias(
                        df_analisis_final,
                        programas_finales_seleccionados,
                        columnas_presentes,  # Metricas disponibles
                        columna_anio_periodo,
                        color_discrete_sequence=COLORES_TENDENCIA,
                    )

                    # Mostrar las graficas
                    for metrica, fig in graficas_tendencias.items():
                        st.plotly_chart(fig, use_container_width=True)

                    st.subheader("Gráficos Comparativos 📊")

                    # Opciones de comparación
                    opciones_comparacion = {
                        "Modalidad": (columna_modalidad if columna_modalidad in df_analisis_final.columns else None,
                                      COLOR_MAP_MODALIDAD),
                        "Género": ("sexo" if "sexo" in df_analisis_final.columns else None, COLOR_MAP_SEXO),
                        "Nivel de Formación": (limpiar_columna(STR_NIVEL_FORMACION) if limpiar_columna(
                            STR_NIVEL_FORMACION) in df_analisis_final.columns else None, COLOR_MAP_NIVEL_FORMACION),
                    }

                    # Filtrar opciones validas
                    opciones_comparacion = {k: v for k, v in opciones_comparacion.items() if v[0]}


                    categoria_comparativa = st.selectbox("Seleccione la categoría para la comparación",
                                                         list(opciones_comparacion.keys()))
                    columna_categoria, color_map = opciones_comparacion[categoria_comparativa]

                    if columna_categoria in df_analisis_final.columns:
                        graficas_comparativas = graficar_comparativo(
                            df_analisis_final,
                            columna_categoria,
                            columnas_presentes,
                            columna_programa=columna_programa,
                            color_discrete_map=color_map
                        )

                        for metrica, fig in graficas_comparativas.items():
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No hay datos disponibles para la categoría seleccionada.")
                else:
                    st.info("No se seleccionó ningún programa para el análisis final.")
            else:
                st.warning("No hay datos filtrados disponibles. Vuelve a la pestaña de Filtrado de Información.")
