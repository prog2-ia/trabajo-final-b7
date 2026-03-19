from entidades.reserva import Reserva

class GestorReservas:

    def __init__(self):
        self.__usuarios = []
        self.__salas = []
        self.__reservas = []
        self.__contador_reservas = 1

    def agregar_usuario(self, usuario):
        self.__usuarios.append(usuario)

    def agregar_sala(self, sala):
        self.__salas.append(sala)

    def buscar_usuario_por_dni(self, dni):
        for usuario in self.__usuarios:
            if usuario.get_dni() == dni:
                return usuario
        return None

    def buscar_sala_por_id(self, id_sala):
        for sala in self.__salas:
            if sala.id_sala == id_sala:
                return sala
        return None

    def comprobar_disponibilidad(self, sala, fecha, hora_inicio, hora_fin):
        for reserva in self.__reservas:
            if reserva.get_sala() == sala and reserva.get_fecha() == fecha:
                if hora_inicio < reserva.hora_fin and hora_fin > reserva.hora_inicio:
                    return False
        return True

    def crear_reserva(self, dni_usuario, id_sala, fecha, hora_inicio, hora_fin, num_personas):
        usuario = self.buscar_usuario_por_dni(dni_usuario)
        sala = self.buscar_sala_por_id(id_sala)

        if not usuario:
            print("Error: Usuario no encontrado.")
            return False

        if not sala:
            print("Error: Sala no encontrada.")
            return False

        if not sala.tiene_capacidad(num_personas):
            print(f"Error: La sala {sala.nombre} no tiene capacidad para {num_personas} personas. (Máximo: {sala.capacidad})")
            return False

        if not usuario.puede_reservar_sala(sala):
            print("Error: El usuario no tiene permisos para reservar este tipo de sala.")
            return False

        if not self.comprobar_disponibilidad(sala, fecha, hora_inicio, hora_fin):
            print("Error: La sala ya está reservada en ese horario.")
            return False

        id_reserva = f"RES-{self.__contador_reservas}"
        nueva_reserva = Reserva(id_reserva, usuario, sala, fecha, hora_inicio, hora_fin, num_personas)

        self.__reservas.append(nueva_reserva)
        self.__contador_reservas += 1

        print(f"Reserva {id_reserva} creada correctamente para {usuario.get_nombre_completo()}.")
        return True

    def listar_reservas(self):
        print("\n--- LISTADO DE RESERVAS ---")
        if not self.__reservas:
            print("No hay reservas en el sistema.")
        for reservas in self.__reservas:
            print(
                f"[{reservas.id}] Sala: {reservas.get_sala().nombre} | Fecha: {reservas.get_fecha()} | Horario: {reservas.hora_inicio}h - {reservas.hora_fin}h | Usuario: {reservas.get_usuario().get_username()}")