class SNIESController:
    def __init__(self):
        self.programas_academicos: Dict[int, ProgramaAcademico] = {}
        self.gestor_csv_obj = GestorCsv()
        self.etiquetas_columnas: List[str] = []
        self.ruta_programas_csv = Settings.PROGRAMAS_FILTRAR_FILE_PATH
        self.ruta_admitidos = Settings.ADMITIDOS_FILE_PATH
        self.ruta_graduados = Settings.GRADUADOS_FILE_PATH
        self.ruta_inscritos = Settings.INSCRITOS_FILE_PATH
        self.ruta_matriculados = Settings.MATRICULADOS_FILE_PATH
        self.ruta_matriculados_primer_semestre = Settings.MATRICULADOS_PRIMER_SEMESTRE_FILE_PATH
        self.ruta_output = Settings.OUTPUT_FILE_PATH

    def procesar_datos_csv(self):
        try:
            with open(self.ruta_programas_csv, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                self.etiquetas_columnas = next(csvreader)  # Assuming the first row has headers
                for row in csvreader:
                    id_programa = int(row[0])  # Example assuming first column is ID
                    programa = ProgramaAcademico(id_programa, *row[1:])
                    self.programas_academicos[id_programa] = programa
        except Exception as e:
            print(f"Error processing CSV file: {e}")

    def exportar_datos(self, formato: str):
        if formato.lower() == "json":
            with open(self.ruta_output, 'w') as jsonfile:
                json.dump({id_: p.to_dict() for id_, p in self.programas_academicos.items()}, jsonfile)
        elif formato.lower() == "csv":
            with open(self.ruta_output, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(self.etiquetas_columnas)
                for programa in self.programas_academicos.values():
                    csvwriter.writerow(programa.to_list())
        elif formato.lower() == "txt":
            with open(self.ruta_output, 'w') as txtfile:
                for programa in self.programas_academicos.values():
                    txtfile.write(str(programa) + "\\n")
        else:
            print("Unsupported format")

    def agregar_programa_academico(self, id_programa: int, datos: List[str]):
        programa = ProgramaAcademico(id_programa, *datos)
        self.programas_academicos[id_programa] = programa

    def obtener_programa_por_id(self, id_programa: int) -> ProgramaAcademico:
        return self.programas_academicos.get(id_programa, None)

    def listar_programas(self):
        for id_, programa in self.programas_academicos.items():
            print(f"{id_}: {programa}")
