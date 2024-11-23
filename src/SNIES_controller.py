from lectura_Archivos import leer_xlsx,escribir_archivo
from filtro import filtrar_programas
import pandas as pd
import os

class SNIESController:
    def __init__(self, ruta_archivos):
        self.ruta_archivos = ruta_archivos
        self.datos = None

    def cargar_datos_por_rango(self, archivos, anio_inicio, anio_fin):
        dfs = []
        for archivo in archivos:

            # Extraer el año del nombre del archivo
            for anio in range(anio_inicio, anio_fin + 1):
                if str(anio) in archivo:
                    ruta = os.path.join(self.ruta_archivos, archivo)
                    try:
                        df = leer_xlsx(ruta)
                        df["archivo"] = archivo  # Metadata del archivo
                        dfs.append(df)
                        break
                    except Exception as e:
                        print(f"Error al cargar el archivo {archivo}: {e}")
        if dfs:
            self.datos = pd.concat(dfs, ignore_index=True)
        else:
            self.datos = pd.DataFrame()  # Si no hay archivos en el rango, crear DataFrame vacío

    def filtrar_programas(self, palabras_clave):
        """Filtra programas por palabras clave."""
        if self.data is None or self.data.empty:
            raise ValueError("No hay datos cargados para filtrar.")
        return filtrar_programas(self.data, palabras_clave)

