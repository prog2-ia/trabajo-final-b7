"""Gestor central de reservas.

Se encarga de almacenar usuarios, salas y reservas en memoria y ofrece
operaciones para crear reservas comprobando permisos, capacidad y solapes.
"""

from entidades.reserva import Reserva
from datetime import datetime, date, time


def _comprobar_formato_fecha(fecha):
    # Acepta datetime.date o string 'YYYY-MM-DD'
    if isinstance(fecha, date):
        return fecha
    if isinstance(fecha, str):
        try:
            return date.fromisoformat(fecha)
        except Exception:
            raise ValueError("Formato de fecha inválido. Use 'YYYY-MM-DD'.")
    raise ValueError("Fecha debe ser datetime.date o string 'YYYY-MM-DD'.")


def _comprobar_formato_hora(h):
    # Acepta datetime.time, string 'HH:MM' o float (como 10.5 -> 10:30)
    if isinstance(h, time):
        return h
    if isinstance(h, str):
        try:
            return datetime.strptime(h, "%H:%M").time()
        except Exception:
            raise ValueError("Formato de hora inválido. Use 'HH:MM'.")
    if isinstance(h, (int, float)):
        # Convertir decimal a horas/minutos (10.5 -> 10:30)
        horas = int(h)
        minutos = int(round((float(h) - horas) * 60))
        if minutos == 60:
            horas += 1
            minutos = 0
        return time(hour=horas, minute=minutos)
    raise ValueError("Hora debe ser datetime.time, string 'HH:MM' o número (horas).")


class GestorReservas:

    def __init__(self):
        # Listas en memoria
        self.__usuarios = []
        self.__salas = []
        self.__reservas = []
        self.__contador_reservas = 1

    def agregar_usuario(self, usuario):
        """Añade un usuario al gestor."""
        self.__usuarios.append(usuario)

    def agregar_sala(self, sala):
        """Añade una sala al gestor."""
        self.__salas.append(sala)

    def buscar_usuario_por_dni(self, dni):
        """Busca y devuelve un usuario por su DNI, o None si no existe."""
        for usuario in self.__usuarios:
            if usuario.get_dni() == dni:
                return usuario
        return None

    def buscar_sala_por_id(self, id_sala):
        """Busca y devuelve una sala por su identificador."""
        for sala in self.__salas:
            if sala.id_sala == id_sala:
                return sala
        return None

    def comprobar_disponibilidad(self, sala, fecha, hora_inicio, hora_fin):
        """Comprueba que la sala no tenga reservas que se solapen con el intervalo dado.

        La condición usada comprueba si existe alguna reserva en la misma fecha
        cuya ventana horaria intersecta con el intervalo [hora_inicio, hora_fin).
        """
        # Normalizar tipos
        fecha_n = _comprobar_formato_fecha(fecha)
        inicio_n = _comprobar_formato_hora(hora_inicio)
        fin_n = _comprobar_formato_hora(hora_fin)

        for reserva in self.__reservas:
            if reserva.get_sala() == sala and reserva.get_fecha() == fecha_n:
                if inicio_n < reserva.hora_fin and fin_n > reserva.hora_inicio:
                    return False
        return True

    def crear_reserva(self, dni_usuario, id_sala, fecha, hora_inicio, hora_fin, num_personas):
        """Crea una reserva realizando todas las comprobaciones necesarias.

        Flujo:
        - Buscar usuario y sala
        - Comprobar capacidad y permisos
        - Verificar disponibilidad (sin solapes)
        - Crear y almacenar la reserva si todo es correcto
        """
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

        # Parsear fecha y horas a tipos correctos
        try:
            fecha_n = _comprobar_formato_fecha(fecha)
            inicio_n = _comprobar_formato_hora(hora_inicio)
            fin_n = _comprobar_formato_hora(hora_fin)
        except ValueError as e:
            print(f"Error: {e}")
            return False

        if not self.comprobar_disponibilidad(sala, fecha_n, inicio_n, fin_n):
            print("Error: La sala ya está reservada en ese horario.")
            return False

        id_reserva = f"RES-{self.__contador_reservas}"
        nueva_reserva = Reserva(id_reserva, usuario, sala, fecha_n, inicio_n, fin_n, num_personas)

        self.__reservas.append(nueva_reserva)
        self.__contador_reservas += 1

        print(f"Reserva {id_reserva} creada correctamente para {usuario.get_nombre_completo()}.")
        return True

    def listar_reservas(self):
        """Imprime por consola el listado de reservas existentes."""
        print("\n--- LISTADO DE RESERVAS ---")
        if not self.__reservas:
            print("No hay reservas en el sistema.")
        for reservas in self.__reservas:
            fecha_str = reservas.get_fecha().isoformat() if hasattr(reservas.get_fecha(), 'isoformat') else str(reservas.get_fecha())
            inicio_str = reservas.hora_inicio.strftime("%H:%M") if hasattr(reservas.hora_inicio, 'strftime') else str(reservas.hora_inicio)
            fin_str = reservas.hora_fin.strftime("%H:%M") if hasattr(reservas.hora_fin, 'strftime') else str(reservas.hora_fin)
            print(
                f"[{reservas.id}] Sala: {reservas.get_sala().nombre} | Fecha: {fecha_str} | Horario: {inicio_str} - {fin_str} | Usuario: {reservas.get_usuario().get_username()}")