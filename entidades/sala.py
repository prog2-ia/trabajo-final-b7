class Sala:
    def __init__(self, id, nombre, tipo, capacidad, disponible):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.capacidad = capacidad
        self.disponible = disponible

    def get_capacidad(self):
        return self.capacidad

    def get_tipo(self):
        return self.tipo

    def esta_disponible(self):
        return self.disponible

    def tiene_capacidad(self, personas):
        return self.capacidad >= personas

    def ocupar(self):
        if self.disponible:
            self.disponible = False
            return True
        else:
            return False

    def liberar(self):
        if not self.disponible:
            self.disponible = True
            return True
        else:
            return False

    def es_valida(self):
        return self.capacidad > 0