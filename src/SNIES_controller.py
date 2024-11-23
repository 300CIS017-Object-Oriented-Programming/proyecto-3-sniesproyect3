from lectura_Archivos import leer_xlsx,escribir_archivo
from filtro import filtrar_programas
import pandas as pd

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
                    ruta = f"{self.ruta_archivos}/{archivo}"
                    df = leer_xlsx(ruta)
                    df["archivo"] = archivo  # Agregar metadata del archivo
                    dfs.append(df)
                    break
        if dfs:
            self.data = pd.concat(dfs, ignore_index=True)
        else:
            self.data = pd.DataFrame()  # Si no hay archivos en el rango, crear DataFrame vacío

    def filtrar_programas(self, palabras_clave):
        """Filtra programas por palabras clave."""
        if self.data is None or self.data.empty:
            raise ValueError("No hay datos cargados para filtrar.")
        return filtrar_programas(self.data, palabras_clave)

