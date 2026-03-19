class Recurso:

    def __init__(self, id, nombre, tipo, disponible=True):
        self.__id = id
        self.__nombre = nombre
        self.__tipo = tipo
        self.__disponible = disponible

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, nuevo_id):
        self.__id = nuevo_id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    @property
    def tipo(self) :
        return self.__tipo

    @tipo.setter
    def tipo(self, nuevo_tipo):
        self.__tipo = nuevo_tipo

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, estado):
        self.__disponible = estado

    def esta_disponible(self):
        return self.__disponible

    def reservar(self):
        if self.__disponible:
            self.__disponible = False
            return True
        else:
            return False

    def liberar(self):
        if not self.__disponible:
            self.__disponible = True
            return True
        return False

    def get_tipo(self):
        return self.__tipo

    def coincide_id(self, otro_id):
        if otro_id == self.__id:
            return True
        return False

    def es_valido(self):
        return (self.__id != "") and (self.__nombre != "") and (self.__tipo is not None)
