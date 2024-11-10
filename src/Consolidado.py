class Consolidado:
    def __init__(self, id_sexo=0, sexo="", ano=0, semestre=0, inscritos=0, admitidos=0, matriculados=0, matriculados_primer_semestre=0, graduados=0):
        self._id_sexo = id_sexo
        self._sexo = sexo
        self._ano = ano
        self._semestre = semestre
        self._inscritos = inscritos
        self._admitidos = admitidos
        self._matriculados = matriculados
        self._matriculados_primer_semestre = matriculados_primer_semestre
        self._graduados = graduados

    @property
    def id_sexo(self):
        return self._id_sexo

    @id_sexo.setter
    def id_sexo(self, id_sexo):
        self._id_sexo = id_sexo

    @property
    def sexo(self):
        return self._sexo

    @sexo.setter
    def sexo(self, sexo):
        self._sexo = sexo

    @property
    def ano(self):
        return self._ano

    @ano.setter
    def ano(self, ano):
        self._ano = ano

    @property
    def semestre(self):
        return self._semestre

    @semestre.setter
    def semestre(self, semestre):
        self._semestre = semestre

    @property
    def inscritos(self):
        return self._inscritos

    @inscritos.setter
    def inscritos(self, inscritos):
        self._inscritos = inscritos

    @property
    def admitidos(self):
        return self._admitidos

    @admitidos.setter
    def admitidos(self, admitidos):
        self._admitidos = admitidos

    @property
    def matriculados(self):
        return self._matriculados

    @matriculados.setter
    def matriculados(self, matriculados):
        self._matriculados = matriculados

    @property
    def matriculados_primer_semestre(self):
        return self._matriculados_primer_semestre

    @matriculados_primer_semestre.setter
    def matriculados_primer_semestre(self, matriculados_primer_semestre):
        self._matriculados_primer_semestre = matriculados_primer_semestre

    @property
    def graduados(self):
        return self._graduados

    @graduados.setter
    def graduados(self, graduados):
        self._graduados = graduados