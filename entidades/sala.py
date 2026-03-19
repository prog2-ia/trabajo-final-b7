from abc import ABC, abstractmethod

class Sala(ABC):

    def __init__(self, id_sala, nombre, capacidad, disponible=True):

        self.__id_sala = id_sala
        self.__nombre = nombre
        self.__capacidad = capacidad
        self.__disponible  = disponible
        self.__recursos = []

    @property
    def id_sala(self):
        return self.__id_sala

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, nueva_capacidad):
        self.__capacidad = nueva_capacidad

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self.__disponible = estado

    @property
    def recursos(self):
        return self.__recursos

    def get_capacidad(self):
        return self.__capacidad

    @abstractmethod
    def get_tipo(self):
        pass

    def esta_disponible(self):
        return self.__disponible

    def tiene_capacidad(self, personas):
        return self.__capacidad >= personas

    def ocupar(self):
        if self.__disponible:
            self.__disponible = False
            return True
        return False

    def liberar(self):
        if not self.__disponible:
            self.__disponible = True
            return True
        return False

    def puede_reservar(self, usuario):
        return True

    def es_valida(self):
        return self.__capacidad > 0

    def agregar_recurso(self, recurso):
        self.__recursos.append(recurso)

    def quitar_recurso(self, id_recurso):
        for recurso in self.__recursos:
            if recurso.coincide_id(id_recurso):
                self.__recursos.remove(recurso)
                return recurso
        return None

    def listar_nombres_recursos(self):
        if not self.__recursos:
            return "Ninguno"
        nombres = []
        for r in self.__recursos:
            nombres.append(r.nombre)
        return ", ".join(nombres)

    def __str__(self):
        estado = "Libre" if self.__disponible else "Ocupada"
        recursos_str = self.listar_nombres_recursos()
        return f"[{self.get_tipo()}] {self.__nombre} (Capacidad: {self.__capacidad}) - {estado} | Recursos: {recursos_str}"


class SalaReuniones(Sala):

    def __init__(self, id_sala, nombre, capacidad, disponible=True):
        super().__init__(id_sala, nombre, capacidad, disponible)

    def get_tipo(self):
        return "Sala de Reuniones"

    def puede_reservar(self, usuario):
        return super().puede_reservar(usuario)


class Despacho(Sala):

    def __init__(self, id_sala, nombre, capacidad, disponible=True):
        super().__init__(id_sala, nombre, capacidad, disponible)

    def get_tipo(self):
        return "Despacho"

    def puede_reservar(self, usuario):
        return usuario.es_premium() or usuario.es_admin()


class EspacioAbierto(Sala):

    def __init__(self, id_sala, nombre, capacidad, disponible=True):
        super().__init__(id_sala, nombre, capacidad, disponible)

    def get_tipo(self):
        return "Espacio Abierto"

    def puede_reservar(self, usuario):
        return super().puede_reservar(usuario)