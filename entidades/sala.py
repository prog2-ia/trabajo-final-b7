from abc import ABC, abstractmethod

class Sala(ABC):

    def __init__(self, id_sala: str, nombre: str, capacidad: int, disponible: bool = True) -> None:
        self.__id_sala: str = id_sala
        self.__nombre: str = nombre
        self.__capacidad: int = capacidad
        self.__disponible: bool = disponible
        self.__recursos: list['Recurso'] = []

    @property
    def id_sala(self) -> str:
        return self.__id_sala

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        self.__nombre = nuevo_nombre

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, nueva_capacidad: int) -> None:
        self.__capacidad = nueva_capacidad

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self.__disponible = estado

    @property
    def recursos(self) -> list['Recurso']:
        return self.__recursos

    def get_capacidad(self) -> int:
        return self.__capacidad

    @abstractmethod
    def get_tipo(self) -> str:
        pass

    def esta_disponible(self) -> bool:
        return self.__disponible

    def tiene_capacidad(self, personas: int) -> bool:
        return self.__capacidad >= personas

    def ocupar(self) -> bool:
        if self.__disponible:
            self.__disponible = False
            return True
        return False

    def liberar(self) -> bool:
        if not self.__disponible:
            self.__disponible = True
            return True
        return False

    def puede_reservar(self, usuario: 'Usuario') -> bool:
        return True

    def es_valida(self) -> bool:
        return self.__capacidad > 0

    def agregar_recurso(self, recurso: 'Recurso') -> None:
        self.__recursos.append(recurso)

    def quitar_recurso(self, id_recurso: str) -> 'Recurso' | None:
        for recurso in self.__recursos:
            if recurso.coincide_id(id_recurso):
                self.__recursos.remove(recurso)
                return recurso
        return None

    def listar_nombres_recursos(self) -> str:
        if not self.__recursos:
            return "Ninguno"
        nombres: list[str] = []
        for r in self.__recursos:
            nombres.append(r.nombre)
        return ", ".join(nombres)

    def __str__(self) -> str:
        estado = "Libre" if self.__disponible else "Ocupada"
        recursos_str = self.listar_nombres_recursos()
        return f"[{self.get_tipo()}] {self.__nombre} (Capacidad: {self.__capacidad}) - {estado} | Recursos: {recursos_str}"


class SalaReuniones(Sala):

    def __init__(self, id_sala: str, nombre: str, capacidad: int, disponible: bool = True) -> None:
        super().__init__(id_sala, nombre, capacidad, disponible)

    def get_tipo(self) -> str:
        return "Sala de Reuniones"

    def puede_reservar(self, usuario: 'Usuario') -> bool:
        return super().puede_reservar(usuario)


class Despacho(Sala):

    def __init__(self, id_sala: str, nombre: str, capacidad: int, disponible: bool = True) -> None:
        super().__init__(id_sala, nombre, capacidad, disponible)

    def get_tipo(self) -> str:
        return "Despacho"

    def puede_reservar(self, usuario: 'Usuario') -> bool:
        return usuario.es_premium() or usuario.es_admin()