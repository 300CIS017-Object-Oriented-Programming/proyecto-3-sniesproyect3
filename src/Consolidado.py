class Consolidado:
    def __init__(self, id_sexo=0, sexo="", ano=0, semestre=0, inscritos=0, admitidos=0, matriculados=0, matriculados_primer_semestre=0, graduados=0):
        self.id_sexo = id_sexo
        self.sexo = sexo
        self.ano = ano
        self.semestre = semestre
        self.inscritos = inscritos
        self.admitidos = admitidos
        self.matriculados = matriculados
        self.matriculados_primer_semestre = matriculados_primer_semestre
        self.graduados = graduados

    def get_id_sexo(self):
        return self.id_sexo

    def set_id_sexo(self, id_sexo):
        self.id_sexo = id_sexo

    def get_sexo(self):
        return self.sexo

    def set_sexo(self, sex):
        self.sexo = sex

    def get_ano(self):
        return self.ano

    def set_ano(self, ano):
        self.ano = ano

    def get_semestre(self):
        return self.semestre

    def set_semestre(self, semestre):
        self.semestre = semestre

    def get_inscritos(self):
        return self.inscritos

    def set_inscritos(self, inscritos):
        self.inscritos = inscritos

    def get_admitidos(self):
        return self.admitidos

    def set_admitidos(self, admitidos):
        self.admitidos = admitidos

    def get_matriculados(self):
        return self.matriculados

    def set_matriculados(self, matriculados):
        self.matriculados = matriculados

    def get_matriculados_primer_semestre(self):
        return self.matriculados_primer_semestre

    def set_matriculados_primer_semestre(self, matriculados_primer_semestre):
        self.matriculados_primer_semestre = matriculados_primer_semestre

    def get_graduados(self):
        return self.graduados

    def set_graduados(self, graduados):
        self.graduados = graduados
