"""Gestor central de reservas.

Se encarga de almacenar usuarios, salas y reservas en memoria y ofrece
operaciones para crear reservas comprobando permisos, capacidad y solapes.
"""

from entidades.reserva import Reserva
from persistencia.persistencia import Persistencia
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
        self.__persistencia = Persistencia()
        try:
            self.__persistencia.cargar_todos(self, carpeta='./archivos')
        except Exception:
            print("Aviso: no se pudo cargar persistencia al iniciar.")

    def obtener_estado(self):
        return {
            "usuarios": list(self.__usuarios),
            "salas": list(self.__salas),
            "reservas": list(self.__reservas),
            "contador_reservas": self.__contador_reservas,
        }

    def cargar_estado(self, estado):
        self.__usuarios = estado.get("usuarios", [])
        self.__salas = estado.get("salas", [])
        self.__reservas = estado.get("reservas", [])
        self.__contador_reservas = estado.get("contador_reservas", 1)

    def agregar_usuario(self, usuario):
        """Añade un usuario al gestor."""
        self.__usuarios.append(usuario)
        try:
            self.__persistencia.guardar_todos(self)
        except Exception:
            pass

    def agregar_sala(self, sala):
        """Añade una sala al gestor."""
        self.__salas.append(sala)
        try:
            self.__persistencia.guardar_todos(self)
        except Exception:
            pass

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

        try:
            self.__persistencia.guardar_todos(self)
        except Exception:
            pass

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
            try:
                self.__persistencia.guardar_todos(self)
            except Exception:
                pass
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
            try:
                self.__persistencia.guardar_todos(self)
            except Exception:
                pass
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
            try:
                self.__persistencia.guardar_todos(self)
            except Exception:
                pass
            print(f"Recurso '{recurso.nombre}' añadido exitosamente a la sala '{sala.nombre}'.")
            return True
        print("Error: Sala no encontrada.")
        return False

    def guardar_txt(self, ruta):
        try:
            self.__persistencia.guardar_todos(self, carpeta=ruta)
            print("Guardado en txt correcto.")
            return True
        except Exception as e:
            print("Error guardando txt.")
            return False

    def guardar_backup(self, ruta):
        try:
            self.__persistencia.guardar_backup(ruta, self)
            print("Backup creado.")
            return True
        except Exception:
            print("Error creando backup.")
            return False

    def restaurar_backup(self, ruta):
        try:
            self.__persistencia.restaurar_backup(ruta, self)
            print("Backup restaurado.")
            return True
        except Exception:
            print("Error restaurando backup.")
            return False