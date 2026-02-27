class Recurso:
    def __init__(self, id, nombre, tipo, disponible):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.disponible = disponible

    def esta_disponible(self):
        return self.disponible

    def reservar(self):
        if self.disponible:
            return True
        else:
            return False

    def liberar(self):
        if not self.disponible:
            return True

    def es_tipo(self):
        return self.tipo

    def coincide_id(self, otro_id):
        if otro_id == self.id:
            return True

    def es_valido(self):
        return (self.id != "") and (self.nombre != "") and (self.tipo is not None)
