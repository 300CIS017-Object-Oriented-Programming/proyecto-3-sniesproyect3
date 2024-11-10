#ProgramaAcademico
class ProgramaAcademico:
    def __init__(self):
        self._codigo_de_la_institucion = 0
        self._ies_padre = 0
        self._institucion_de_educacion_superior_ies = ""
        self._principal_o_seccional = ""
        self._id_sector_ies = 0
        self._sector_ies = ""
        self._id_caracter = 0
        self._caracter_ies = ""
        self._codigo_del_departamento_ies = 0
        self._departamento_de_domicilio_de_la_ies = ""
        self._codigo_del_municipio_ies = 0
        self._municipio_de_domicilio_de_la_ies = ""
        self._codigo_snies_del_programa = 0
        self._programa_academico = ""
        self._id_nivel_academico = 0
        self._nivel_academico = ""
        self._id_nivel_de_formacion = 0
        self._nivel_de_formacion = ""
        self._id_metodologia = 0
        self._metodologia = ""
        self._id_area = 0
        self._area_de_conocimiento = ""
        self._id_nucleo = 0
        self._nucleo_basico_del_conocimiento_nbc = ""
        self._id_cine_campo_amplio = 0
        self._desc_cine_campo_amplio = ""
        self._id_cine_campo_especifico = 0
        self._desc_cine_campo_especifico = ""
        self._id_cine_codigo_detallado = 0
        self._desc_cine_codigo_detallado = ""
        self._codigo_del_departamento_programa = 0
        self._departamento_de_oferta_del_programa = ""
        self._codigo_del_municipio_programa = 0
        self._municipio_de_oferta_del_programa = ""
        self._consolidados = [None] * Settings.COLUMNAS_INFO_CONSOLIDADOS

    @property
    def codigo_de_la_institucion(self):
        return self._codigo_de_la_institucion

    @codigo_de_la_institucion.setter
    def codigo_de_la_institucion(self, value):
        self._codigo_de_la_institucion = value

    @property
    def ies_padre(self):
        return self._ies_padre

    @ies_padre.setter
    def ies_padre(self, value):
        self._ies_padre = value

    @property
    def institucion_de_educacion_superior_ies(self):
        return self._institucion_de_educacion_superior_ies

    @institucion_de_educacion_superior_ies.setter
    def institucion_de_educacion_superior_ies(self, value):
        self._institucion_de_educacion_superior_ies = value

    @property
    def principal_o_seccional(self):
        return self._principal_o_seccional

    @principal_o_seccional.setter
    def principal_o_seccional(self, value):
        self._principal_o_seccional = value

    @property
    def id_sector_ies(self):
        return self._id_sector_ies

    @id_sector_ies.setter
    def id_sector_ies(self, value):
        self._id_sector_ies = value

    @property
    def sector_ies(self):
        return self._sector_ies

    @sector_ies.setter
    def sector_ies(self, value):
        self._sector_ies = value

    @property
    def id_caracter(self):
        return self._id_caracter

    @id_caracter.setter
    def id_caracter(self, value):
        self._id_caracter = value

    @property
    def caracter_ies(self):
        return self._caracter_ies

    @caracter_ies.setter
    def caracter_ies(self, value):
        self._caracter_ies = value

    @property
    def codigo_del_departamento_ies(self):
        return self._codigo_del_departamento_ies

    @codigo_del_departamento_ies.setter
    def codigo_del_departamento_ies(self, value):
        self._codigo_del_departamento_ies = value

    @property
    def departamento_de_domicilio_de_la_ies(self):
        return self._departamento_de_domicilio_de_la_ies

    @departamento_de_domicilio_de_la_ies.setter
    def departamento_de_domicilio_de_la_ies(self, value):
        self._departamento_de_domicilio_de_la_ies = value

    @property
    def codigo_del_municipio_ies(self):
        return self._codigo_del_municipio_ies

    @codigo_del_municipio_ies.setter
    def codigo_del_municipio_ies(self, value):
        self._codigo_del_municipio_ies = value

    @property
    def municipio_de_domicilio_de_la_ies(self):
        return self._municipio_de_domicilio_de_la_ies

    @municipio_de_domicilio_de_la_ies.setter
    def municipio_de_domicilio_de_la_ies(self, value):
        self._municipio_de_domicilio_de_la_ies = value

    @property
    def codigo_snies_del_programa(self):
        return self._codigo_snies_del_programa

    @codigo_snies_del_programa.setter
    def codigo_snies_del_programa(self, value):
        self._codigo_snies_del_programa = value

    @property
    def programa_academico(self):
        return self._programa_academico

    @programa_academico.setter
    def programa_academico(self, value):
        self._programa_academico = value

    @property
    def id_nivel_academico(self):
        return self._id_nivel_academico

    @id_nivel_academico.setter
    def id_nivel_academico(self, value):
        self._id_nivel_academico = value

    @property
    def nivel_academico(self):
        return self._nivel_academico

    @nivel_academico.setter
    def nivel_academico(self, value):
        self._nivel_academico = value

    @property
    def id_nivel_de_formacion(self):
        return self._id_nivel_de_formacion

    @id_nivel_de_formacion.setter
    def id_nivel_de_formacion(self, value):
        self._id_nivel_de_formacion = value

    @property
    def nivel_de_formacion(self):
        return self._nivel_de_formacion

    @nivel_de_formacion.setter
    def nivel_de_formacion(self, value):
        self._nivel_de_formacion = value

    @property
    def id_metodologia(self):
        return self._id_metodologia

    @id_metodologia.setter
    def id_metodologia(self, value):
        self._id_metodologia = value

    @property
    def metodologia(self):
        return self._metodologia

    @metodologia.setter
    def metodologia(self, value):
        self._metodologia = value

    @property
    def id_area(self):
        return self._id_area

    @id_area.setter
    def id_area(self, value):
        self._id_area = value

    @property
    def area_de_conocimiento(self):
        return self._area_de_conocimiento

    @area_de_conocimiento.setter
    def area_de_conocimiento(self, value):
        self._area_de_conocimiento = value

    @property
    def id_nucleo(self):
        return self._id_nucleo

    @id_nucleo.setter
    def id_nucleo(self, value):
        self._id_nucleo = value

    @property
    def nucleo_basico_del_conocimiento_nbc(self):
        return self._nucleo_basico_del_conocimiento_nbc

    @nucleo_basico_del_conocimiento_nbc.setter
    def nucleo_basico_del_conocimiento_nbc(self, value):
        self._nucleo_basico_del_conocimiento_nbc = value

    @property
    def id_cine_campo_amplio(self):
        return self._id_cine_campo_amplio

    @id_cine_campo_amplio.setter
    def id_cine_campo_amplio(self, value):
        self._id_cine_campo_amplio = value

    @property
    def desc_cine_campo_amplio(self):
        return self._desc_cine_campo_amplio

    @desc_cine_campo_amplio.setter
    def desc_cine_campo_amplio(self, value):
        self._desc_cine_campo_amplio = value

    @property
    def id_cine_campo_especifico(self):
        return self._id_cine_campo_especifico

    @id_cine_campo_especifico.setter
    def id_cine_campo_especifico(self, value):
        self._id_cine_campo_especifico = value

    @property
    def desc_cine_campo_especifico(self):
        return self._desc_cine_campo_especifico

    @desc_cine_campo_especifico.setter
    def desc_cine_campo_especifico(self, value):
        self._desc_cine_campo_especifico = value

    @property
    def id_cine_codigo_detallado(self):
        return self._id_cine_codigo_detallado

    @id_cine_codigo_detallado.setter
    def id_cine_codigo_detallado(self, value):
        self._id_cine_codigo_detallado = value

    @property
    def desc_cine_codigo_detallado(self):
        return self._desc_cine_codigo_detallado

    @desc_cine_codigo_detallado.setter
    def desc_cine_codigo_detallado(self, value):
        self._desc_cine_codigo_detallado = value

    @property
    def codigo_del_departamento_programa(self):
        return self._codigo_del_departamento_programa

    @codigo_del_departamento_programa.setter
    def codigo_del_departamento_programa(self, value):
        self._codigo_del_departamento_programa = value

    @property
    def departamento_de_oferta_del_programa(self):
        return self._departamento_de_oferta_del_programa

    @departamento_de_oferta_del_programa.setter
    def departamento_de_oferta_del_programa(self, value):
        self._departamento_de_oferta_del_programa = value

    @property
    def codigo_del_municipio_programa(self):
        return self._codigo_del_municipio_programa

    @codigo_del_municipio_programa.setter
    def codigo_del_municipio_programa(self, value):
        self._codigo_del_municipio_programa = value

    @property
    def municipio_de_oferta_del_programa(self):
        return self._municipio_de_oferta_del_programa

    @municipio_de_oferta_del_programa.setter
    def municipio_de_oferta_del_programa(self, value):
        self._municipio_de_oferta_del_programa = value