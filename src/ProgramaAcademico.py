class ProgramaAcademico:
    def __init__(self):
        self.codigo_de_la_institucion = 0
        self.ies_padre = 0
        self.institucion_de_educacion_superior_ies = ""
        self.principal_o_seccional = ""
        self.id_sector_ies = 0
        self.sector_ies = ""
        self.id_caracter = 0
        self.caracter_ies = ""
        self.codigo_del_departamento_ies = 0
        self.departamento_de_domicilio_de_la_ies = ""
        self.codigo_del_municipio_ies = 0
        self.municipio_de_domicilio_de_la_ies = ""
        self.codigo_snies_del_programa = 0
        self.programa_academico = ""
        self.id_nivel_academico = 0
        self.nivel_academico = ""
        self.id_nivel_de_formacion = 0
        self.nivel_de_formacion = ""
        self.id_metodologia = 0
        self.metodologia = ""
        self.id_area = 0
        self.area_de_conocimiento = ""
        self.id_nucleo = 0
        self.nucleo_basico_del_conocimiento_nbc = ""
        self.id_cine_campo_amplio = 0
        self.desc_cine_campo_amplio = ""
        self.id_cine_campo_especifico = 0
        self.desc_cine_campo_especifico = ""
        self.id_cine_codigo_detallado = 0
        self.desc_cine_codigo_detallado = ""
        self.codigo_del_departamento_programa = 0
        self.departamento_de_oferta_del_programa = ""
        self.codigo_del_municipio_programa = 0
        self.municipio_de_oferta_del_programa = ""
        self.consolidados = [None] * Settings.COLUMNAS_INFO_CONSOLIDADOS

    def set_codigo_de_la_institucion(self, nuevo_codigo_de_la_institucion):
        self.codigo_de_la_institucion = nuevo_codigo_de_la_institucion

    def get_codigo_de_la_institucion(self):
        return self.codigo_de_la_institucion

    def set_ies_padre(self, nuevo_ies_padre):
        self.ies_padre = nuevo_ies_padre

    def get_ies_padre(self):
        return self.ies_padre

    def set_institucion_de_educacion_superior_ies(self, nuevo_institucion_de_educacion_superior_ies):
        self.institucion_de_educacion_superior_ies = nuevo_institucion_de_educacion_superior_ies

    def get_institucion_de_educacion_superior_ies(self):
        return self.institucion_de_educacion_superior_ies

    def set_principal_o_seccional(self, nuevo_principal_o_seccional):
        self.principal_o_seccional = nuevo_principal_o_seccional

    def get_principal_o_seccional(self):
        return self.principal_o_seccional

    def set_id_sector_ies(self, nuevo_id_sector_ies):
        self.id_sector_ies = nuevo_id_sector_ies

    def get_id_sector_ies(self):
        return self.id_sector_ies

    def set_sector_ies(self, nuevo_sector_ies):
        self.sector_ies = nuevo_sector_ies

    def get_sector_ies(self):
        return self.sector_ies

    def set_id_caracter(self, nuevo_id_caracter):
        self.id_caracter = nuevo_id_caracter

    def get_id_caracter(self):
        return self.id_caracter

    def set_caracter_ies(self, nuevo_caracter_ies):
        self.caracter_ies = nuevo_caracter_ies

    def get_caracter_ies(self):
        return self.caracter_ies

    def set_codigo_del_departamento_ies(self, nuevo_codigo_del_departamento_ies):
        self.codigo_del_departamento_ies = nuevo_codigo_del_departamento_ies

    def get_codigo_del_departamento_ies(self):
        return self.codigo_del_departamento_ies

    def set_departamento_de_domicilio_de_la_ies(self, nuevo_departamento_de_domicilio_de_la_ies):
        self.departamento_de_domicilio_de_la_ies = nuevo_departamento_de_domicilio_de_la_ies

    def get_departamento_de_domicilio_de_la_ies(self):
        return self.departamento_de_domicilio_de_la_ies

    def set_codigo_del_municipio_ies(self, nuevo_codigo_del_municipio_ies):
        self.codigo_del_municipio_ies = nuevo_codigo_del_municipio_ies

    def get_codigo_del_municipio_ies(self):
        return self.codigo_del_municipio_ies

    def set_municipio_de_domicilio_de_la_ies(self, nuevo_municipio_de_domicilio_de_la_ies):
        self.municipio_de_domicilio_de_la_ies = nuevo_municipio_de_domicilio_de_la_ies

    def get_municipio_de_domicilio_de_la_ies(self):
        return self.municipio_de_domicilio_de_la_ies

    def set_codigo_snies_del_programa(self, nuevo_codigo_snies_del_programa):
        self.codigo_snies_del_programa = nuevo_codigo_snies_del_programa

    def get_codigo_snies_del_programa(self):
        return self.codigo_snies_del_programa

    def set_programa_academico(self, nuevo_programa_academico):
        self.programa_academico = nuevo_programa_academico

    def get_programa_academico(self):
        return self.programa_academico

    def set_id_nivel_academico(self, nuevo_id_nivel_academico):
        self.id_nivel_academico = nuevo_id_nivel_academico

    def get_id_nivel_academico(self):
        return self.id_nivel_academico

    def set_nivel_academico(self, nuevo_nivel_academico):
        self.nivel_academico = nuevo_nivel_academico

    def get_nivel_academico(self):
        return self.nivel_academico

    def set_id_nivel_de_formacion(self, nuevo_id_nivel_de_formacion):
        self.id_nivel_de_formacion = nuevo_id_nivel_de_formacion

    def get_id_nivel_de_formacion(self):
        return self.id_nivel_de_formacion

    def set_nivel_de_formacion(self, nuevo_nivel_de_formacion):
        self.nivel_de_formacion = nuevo_nivel_de_formacion

    def get_nivel_de_formacion(self):
        return self.nivel_de_formacion

    def set_id_metodologia(self, nuevo_id_metodologia):
        self.id_metodologia = nuevo_id_metodologia

    def get_id_metodologia(self):
        return self.id_metodologia

    def set_metodologia(self, nueva_metodologia):
        self.metodologia = nueva_metodologia

    def get_metodologia(self):
        return self.metodologia

    def set_id_area(self, nuevo_id_area):
        self.id_area = nuevo_id_area

    def get_id_area(self):
        return self.id_area

    def set_area_de_conocimiento(self, area_conocimiento):
        self.area_de_conocimiento = area_conocimiento

    def get_area_de_conocimiento(self):
        return self.area_de_conocimiento

    def set_id_nucleo(self, nuevo_id_nucleo):
        self.id_nucleo = nuevo_id_nucleo

    def get_id_nucleo(self):
        return self.id_nucleo

    def set_nucleo_basico_del_conocimiento_nbc(self, nuevo_nucleo_basico_del_conocimiento_nbc):
        self.nucleo_basico_del_conocimiento_nbc = nuevo_nucleo_basico_del_conocimiento_nbc

    def get_nucleo_basico_del_conocimiento_nbc(self):
        return self.nucleo_basico_del_conocimiento_nbc

    def set_id_cine_campo_amplio(self, nuevo_id_cine_campo_amplio):
        self.id_cine_campo_amplio = nuevo_id_cine_campo_amplio

    def get_id_cine_campo_amplio(self):
        return self.id_cine_campo_amplio

    def set_desc_cine_campo_amplio(self, nuevo_desc_cine_campo_amplio):
        self.desc_cine_campo_amplio = nuevo_desc_cine_campo_amplio

    def get_desc_cine_campo_amplio(self):
        return self.desc_cine_campo_amplio

    def set_id_cine_campo_especifico(self, nuevo_id_cine_campo_especifico):
        self.id_cine_campo_especifico = nuevo_id_cine_campo_especifico

    def get_id_cine_campo_especifico(self):
        return self.id_cine_campo_especifico

    def set_desc_cine_campo_especifico(self, nuevo_desc_cine_campo_especifico):
        self.desc_cine_campo_especifico = nuevo_desc_cine_campo_especifico

    def get_desc_cine_campo_especifico(self):
        return self.desc_cine_campo_especifico

    def set_id_cine_codigo_detallado(self, nuevo_id_cine_codigo_detallado):
        self.id_cine_codigo_detallado = nuevo_id_cine_codigo_detallado

    def get_id_cine_codigo_detallado(self):
        return self.id_cine_codigo_detallado

    def set_desc_cine_codigo_detallado(self, nuevo_desc_cine_codigo_detallado):
        self.desc_cine_codigo_detallado = nuevo_desc_cine_codigo_detallado

    def get_desc_cine_codigo_detallado(self):
        return self.desc_cine_codigo_detallado

    def set_codigo_del_departamento_programa(self, nuevo_codigo_del_departamento_programa):
        self.codigo_del_departamento_programa = nuevo_codigo_del_departamento_programa

    def get_codigo_del_departamento_programa(self):
        return self.codigo_del_departamento_programa

    def set_departamento_de_oferta_del_programa(self, nuevo_departamento_de_oferta_del_programa):
        self.departamento_de_oferta_del_programa = nuevo_departamento_de_oferta_del_programa

    def get_departamento_de_oferta_del_programa(self):
        return self.departamento_de_oferta_del_programa

    def set_codigo_del_municipio_programa(self, nuevo_codigo_del_municipio_programa):
        self.codigo_del_municipio_programa = nuevo_codigo_del_municipio_programa

    def get_codigo_del_municipio_programa(self):
        return self.codigo_del_municipio_programa

    def set_municipio_de_oferta_del_programa(self, nuevo_municipio_de_oferta_del_programa):
        self.municipio_de_oferta_del_programa = nuevo_municipio_de_oferta_del_programa

    def get_municipio_de_oferta_del_programa(self):
        return self.municipio_de_oferta_del_programa

    def set_consolidado(self, nuevo_consolidado, pos):
        self.consolidados[pos] = nuevo_consolidado

    def get_consolidado(self, posicion_consolidado):
        return self.consolidados[posicion_consolidado]

    def __del__(self):
        for consolidado in self.consolidados:
            if consolidado is not None:
                del consolidado
