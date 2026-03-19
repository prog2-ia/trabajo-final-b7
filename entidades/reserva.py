class Reserva:

    def __init__(self, id, usuario, sala, fecha, hora_inicio, hora_fin, num_personas):
        self.__id = id
        self.__usuario = usuario
        self.__sala = sala
        self.__fecha = fecha
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
        self.__num_personas = num_personas

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, nuevo_id: str):
        self.__id = nuevo_id

    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, nuevo_usuario):
        self.__usuario = nuevo_usuario

    @property
    def sala(self):
        return self.__sala

    @sala.setter
    def sala(self, nueva_sala):
        self.__sala = nueva_sala

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, nueva_fecha):
        self.__fecha = nueva_fecha

    @property
    def hora_inicio(self):
        return self.__hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, nueva_hora):
        self.__hora_inicio = nueva_hora

    @property
    def hora_fin(self):
        return self.__hora_fin

    @hora_fin.setter
    def hora_fin(self, nueva_hora):
        self.__hora_fin = nueva_hora

    @property
    def num_personas(self):
        return self.__num_personas

    @num_personas.setter
    def num_personas(self, nuevo_num):
        self.__num_personas = nuevo_num

    def get_usuario(self):
        return self.__usuario

    def get_sala(self):
        return self.__sala

    def get_fecha(self):
        return self.__fecha

    def duracion(self):
        return self.__hora_fin - self.__hora_inicio

    def capacidad_correcta(self, otra_capacidad):
        return not otra_capacidad > self.__num_personas

    def es_del_usuario(self, usuario):
        return self.__usuario == usuario

    def es_de_la_sala(self, otra_sala):
        return self.__sala == otra_sala

    def misma_fecha(self, fecha):
        return self.__fecha == fecha

    def hay_solape(self, fecha, inicio, fin):
        return self.__fecha == fecha and self.__hora_inicio == inicio and self.__hora_fin == fin
