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

    def listar_usuarios(self):
        print("\n--- LISTADO DE USUARIOS ---")
        if not self.__usuarios:
            print("No hay usuarios en el sistema.")
        for usr in self.__usuarios:
            print(f"- {usr.get_dni()} | {usr.get_username()} | {usr.get_nombre_completo()} | Tipo: {usr.get_tipo()}")

    def listar_salas(self):
        print("\n--- LISTADO DE SALAS ---")
        if not self.__salas:
            print("No hay salas en el sistema.")
        for sala in self.__salas:
            print(sala)  # Esto usará el método __str__ definido en Sala

    def buscar_reserva_por_id(self, id_reserva):
        for reserva in self.__reservas:
            if reserva.id == id_reserva:
                return reserva
        return None

    def cancelar_reserva(self, id_reserva):
        reserva = self.buscar_reserva_por_id(id_reserva)
        if reserva:
            self.__reservas.remove(reserva)
            print(f"Reserva '{id_reserva}' cancelada con éxito.")
            return True
        print("Error: No se ha encontrado ninguna reserva con ese ID.")
        return False

    def editar_reserva(self, id_reserva, nueva_fecha, nueva_hora_inicio, nueva_hora_fin):
        reserva = self.buscar_reserva_por_id(id_reserva)
        if not reserva:
            print("Error: No se ha encontrado la reserva.")
            return False

            # Retiramos temporalmente la reserva para que no genere solape consigo misma al comprobar
        self.__reservas.remove(reserva)

        if self.comprobar_disponibilidad(reserva.get_sala(), nueva_fecha, nueva_hora_inicio, nueva_hora_fin):
                # Usamos los setters definidos en Reserva
            reserva.fecha = nueva_fecha
            reserva.hora_inicio = nueva_hora_inicio
            reserva.hora_fin = nueva_hora_fin
            self.__reservas.append(reserva)
            print(f"Reserva '{id_reserva}' actualizada correctamente.")
            return True
        else:
            # Si no hay disponibilidad, volvemos a meter la reserva original y fallamos
            self.__reservas.append(reserva)
            print("Error: La sala no está disponible en ese nuevo horario.")
            return False

    def filtrar_reservas(self, fecha=None, id_sala=None, dni_usuario=None):
        resultados = self.__reservas

        if fecha:
            resultados = [r for r in resultados if r.get_fecha() == fecha]
        if id_sala:
            resultados = [r for r in resultados if r.get_sala().id_sala == id_sala]
        if dni_usuario:
            resultados = [r for r in resultados if r.get_usuario().get_dni() == dni_usuario]

        print("\n--- RESULTADOS DEL FILTRO ---")
        if not resultados:
            print("No se encontraron reservas con esos criterios.")
        for r in resultados:
            print(f"[{r.id}] Sala: {r.get_sala().nombre} | Fecha: {r.get_fecha()} | Horario: {r.hora_inicio}h - {r.hora_fin}h | Usuario: {r.get_usuario().get_username()}")

    def asociar_recurso_a_sala(self, recurso, id_sala):
        sala = self.buscar_sala_por_id(id_sala)
        if sala:
            sala.agregar_recurso(recurso)
            print(f"Recurso '{recurso.nombre}' añadido exitosamente a la sala '{sala.nombre}'.")
            return True
        print("Error: Sala no encontrada.")
        return False