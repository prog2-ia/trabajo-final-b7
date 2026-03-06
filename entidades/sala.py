class Sala:
    def __init__(self, id_sala, nombre, capacidad, disponible=True):
        self.id_sala = id_sala
        self.nombre = nombre
        self.capacidad = capacidad
        self.disponible = disponible
        self.recursos = []

    def get_capacidad(self):
        return self.capacidad

    def get_tipo(self):
        return "Sala Genérica"

    def esta_disponible(self):
        return self.disponible

    def tiene_capacidad(self, personas):
        return self.capacidad >= personas

    def ocupar(self):
        if self.disponible:
            self.disponible = False
            return True
        return False

    def liberar(self):
        if not self.disponible:
            self.disponible = True
            return True
        return False

    def es_valida(self):
        return self.capacidad > 0

    def agregar_recurso(self, recurso):
        self.recursos.append(recurso)

    def quitar_recurso(self, id_recurso):
        for recurso in self.recursos:
            if recurso.coincide_id(id_recurso):
                self.recursos.remove(recurso)
                return recurso
        return None

    def listar_nombres_recursos(self):
        if not self.recursos:
            return "Ninguno"
        nombres = []
        for r in self.recursos:
            nombres.append(r.nombre)
        return ", ".join(nombres)

    def __str__(self):
        estado = "Libre" if self.disponible else "Ocupada"
        recursos_str = self.listar_nombres_recursos()
        return f"[{self.get_tipo()}] {self.nombre} (Capacidad: {self.capacidad}) - {estado} | Recursos: {recursos_str}"