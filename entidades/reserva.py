from datetime import datetime, date, time, timedelta

class Reserva:

    def __init__(self, id: str, usuario: 'Usuario', sala: 'Sala', fecha: date, hora_inicio: time, hora_fin: time, num_personas: int) -> None:
        self.__id: str = id
        self.__usuario: 'Usuario' = usuario
        self.__sala: 'Sala' = sala
        self.__fecha: date = fecha
        self.__hora_inicio: time = hora_inicio
        self.__hora_fin: time = hora_fin
        self.__num_personas: int = num_personas

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, nuevo_id: str) -> None:
        self.__id = nuevo_id

    @property
    def usuario(self) -> 'Usuario':
        return self.__usuario

    @usuario.setter
    def usuario(self, nuevo_usuario: 'Usuario') -> None:
        self.__usuario = nuevo_usuario

    @property
    def sala(self) -> 'Sala':
        return self.__sala

    @sala.setter
    def sala(self, nueva_sala: 'Sala') -> None:
        self.__sala = nueva_sala

    @property
    def fecha(self) -> date:
        return self.__fecha

    @fecha.setter
    def fecha(self, nueva_fecha: date) -> None:
        self.__fecha = nueva_fecha

    @property
    def hora_inicio(self) -> time:
        return self.__hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, nueva_hora: time) -> None:
        self.__hora_inicio = nueva_hora

    @property
    def hora_fin(self) -> time:
        return self.__hora_fin

    @hora_fin.setter
    def hora_fin(self, nueva_hora: time) -> None:
        self.__hora_fin = nueva_hora

    @property
    def num_personas(self) -> int:
        return self.__num_personas

    @num_personas.setter
    def num_personas(self, nuevo_num: int) -> None:
        self.__num_personas = nuevo_num

    def get_usuario(self) -> 'Usuario':
        return self.__usuario

    def get_sala(self) -> 'Sala':
        return self.__sala

    def get_fecha(self) -> date:
        return self.__fecha

    def duracion(self) -> timedelta:
        inicio_dt = datetime.combine(self.__fecha, self.__hora_inicio)
        fin_dt = datetime.combine(self.__fecha, self.__hora_fin)
        return fin_dt - inicio_dt

    def capacidad_correcta(self, otra_capacidad: int) -> bool:
        return not otra_capacidad > self.__num_personas

    def es_del_usuario(self, usuario: 'Usuario') -> bool:
        return self.__usuario == usuario

    def es_de_la_sala(self, otra_sala: 'Sala') -> bool:
        return self.__sala == otra_sala

    def misma_fecha(self, fecha: date) -> bool:
        return self.__fecha == fecha

    def hay_solape(self, fecha: date, inicio: time, fin: time) -> bool:
        if self.__fecha != fecha:
            return False
        inicio_dt = datetime.combine(self.__fecha, self.__hora_inicio)
        fin_dt = datetime.combine(self.__fecha, self.__hora_fin)
        inicio_n = datetime.combine(fecha, inicio)
        fin_n = datetime.combine(fecha, fin)
        return inicio_n < fin_dt and fin_n > inicio_dt