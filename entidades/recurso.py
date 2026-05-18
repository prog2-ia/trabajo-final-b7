class Recurso:

    def __init__(self, id: str, nombre: str, tipo: str, disponible: bool = True) -> None:
        self.__id: str = id
        self.__nombre: str = nombre
        self.__tipo: str = tipo
        self.__disponible: bool = disponible

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, nuevo_id: str) -> None:
        self.__id = nuevo_id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        self.__nombre = nuevo_nombre

    @property
    def tipo(self) -> str:
        return self.__tipo

    @tipo.setter
    def tipo(self, nuevo_tipo: str) -> None:
        self.__tipo = nuevo_tipo

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self.__disponible = estado

    def esta_disponible(self) -> bool:
        return self.__disponible

    def reservar(self) -> bool:
        if self.__disponible:
            self.__disponible = False
            return True
        else:
            return False

    def liberar(self) -> bool:
        if not self.__disponible:
            self.__disponible = True
            return True
        return False

    def get_tipo(self) -> str:
        return self.__tipo

    def coincide_id(self, otro_id: str) -> bool:
        if otro_id == self.__id:
            return True
        return False

    def es_valido(self) -> bool:
        return (self.__id != "") and (self.__nombre != "") and (self.__tipo is not None)