class Reserva:
    def __init__(self, id, usuario, sala, fecha, hora_inicio, hora_fin, num_personas):
        self.id = id
        self.usuario = usuario
        self.sala = sala
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.num_personas = num_personas

    def get_usuario(self):
        return self.usuario

    def get_sala(self):
        return self.sala

    def get_fecha(self):
        return self.fecha

    def duracion(self):
        return (self.hora_fin - self.hora_inicio)

    def capacidad_correcta(self, otra_capacidad):
        return not otra_capacidad > self.num_personas

    def es_del_usuario(self, usuario):
        return self.usuario == usuario

    def es_de_la_sala(self):
        return self.sala == self.sala

    def misma_fecha(self, fecha):
        return self.fecha == fecha

    def hay_solape(self, fecha, inicio, fin):
        return self.fecha == fecha and self.hora_inicio == inicio and self.hora_fin == fin
