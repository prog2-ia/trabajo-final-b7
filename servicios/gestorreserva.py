"""Gestor central de reservas.

Se encarga de almacenar usuarios, salas y reservas en memoria y ofrece
operaciones para crear reservas comprobando permisos, capacidad y solapes.
"""
from typing import Any
from entidades.reserva import Reserva
from entidades.usuario import Usuario
from entidades.sala import Sala
from entidades.recurso import Recurso
from persistencia.persistencia import Persistencia
from datetime import datetime, date, time

# Validamos que el formato de fecha sea correcto.
def _comprobar_formato_fecha(fecha: date | str) -> date:
    if isinstance(fecha, date):
        return fecha
    if isinstance(fecha, str):
        try:
            return date.fromisoformat(fecha)
        except Exception:
            raise ValueError("Formato de fecha inválido. Use 'YYYY-MM-DD'.")
    raise ValueError("Fecha debe ser datetime.date o string 'YYYY-MM-DD'.")

# Validamos que el formato de hora sea la clase requerida.
def _comprobar_formato_hora(h: time | str | float | int) -> time:
    if isinstance(h, time):
        return h
    if isinstance(h, str):
        try:
            return datetime.strptime(h, "%H:%M").time()
        except Exception:
            raise ValueError("Formato de hora inválido. Use 'HH:MM'.")
    if isinstance(h, (int, float)):
        horas = int(h)
        minutos = int(round((float(h) - horas) * 60))
        if minutos == 60:
            horas += 1
            minutos = 0
        return time(hour=horas, minute=minutos)
    raise ValueError("Hora debe ser datetime.time, string 'HH:MM' o número (horas).")


# Clase centrada en gestionar todo el sistema de la aplicación.
class GestorReservas:

    # Inicializa las listas de datos y trata de cargar copias si existían.
    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []
        self.__salas: list[Sala] = []
        self.__reservas: list[Reserva] = []
        self.__contador_reservas: int = 1
        self.__persistencia: Persistencia = Persistencia()
        try:
            self.__persistencia.cargar_todos(self, carpeta='./archivos')
        except Exception:
            print("Aviso: no se pudo cargar persistencia al iniciar.")

    # Retorna un diccionario con todas las listas.
    def obtener_estado(self) -> dict[str, Any]:
        return {
            "usuarios": list(self.__usuarios),
            "salas": list(self.__salas),
            "reservas": list(self.__reservas),
            "contador_reservas": self.__contador_reservas,
        }

    # Restaura dicts de estado hacia sus listas correspondientes.
    def cargar_estado(self, estado: dict[str, Any]) -> None:
        self.__usuarios = estado.get("usuarios", [])
        self.__salas = estado.get("salas", [])
        self.__reservas = estado.get("reservas", [])
        self.__contador_reservas = estado.get("contador_reservas", 1)

    # Añade de forma persistente un usuario en su lista.
    def agregar_usuario(self, usuario: Usuario) -> None:
        self.__usuarios.append(usuario)
        try:
            self.__persistencia.guardar_todos(self)
        except Exception:
            pass

    # Añade de forma persistente una sala en su lista.
    def agregar_sala(self, sala: Sala) -> None:
        self.__salas.append(sala)
        try:
            self.__persistencia.guardar_todos(self)
        except Exception:
            pass

    # Módulo de busqueda simple hacia usuarios mediante DNI.
    def buscar_usuario_por_dni(self, dni: str) -> Usuario | None:
        for usuario in self.__usuarios:
            if usuario.get_dni() == dni:
                return usuario
        return None

    # Módulo de busqueda simple hacia salas mediante ID.
    def buscar_sala_por_id(self, id_sala: str) -> Sala | None:
        for sala in self.__salas:
            if sala.id_sala == id_sala:
                return sala
        return None

    # Comprueba logica de tiempo.
    def comprobar_disponibilidad(self, sala: Sala, fecha: date | str, hora_inicio: time | str | float | int,
                                 hora_fin: time | str | float | int) -> bool:
        fecha_n = _comprobar_formato_fecha(fecha)
        inicio_n = _comprobar_formato_hora(hora_inicio)
        fin_n = _comprobar_formato_hora(hora_fin)

        for reserva in self.__reservas:
            if reserva.get_sala() == sala and reserva.get_fecha() == fecha_n:
                if inicio_n < reserva.hora_fin and fin_n > reserva.hora_inicio:
                    return False
        return True

    def crear_reserva(self, dni_usuario: str, id_sala: str, fecha: date | str, hora_inicio: time | str | float | int,
                      hora_fin: time | str | float | int, num_personas: int) -> bool:
        usuario = self.buscar_usuario_por_dni(dni_usuario)
        sala = self.buscar_sala_por_id(id_sala)

        if not usuario:
            print("Error: Usuario no encontrado.")
            return False

        if not sala:
            print("Error: Sala no encontrada.")
            return False

        if not sala.tiene_capacidad(num_personas):
            print(
                f"Error: La sala {sala.nombre} no tiene capacidad para {num_personas} personas. (Máximo: {sala.capacidad})")
            return False

        if not usuario.puede_reservar_sala(sala):
            print("Error: El usuario no tiene permisos para reservar este tipo de sala.")
            return False

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

    def listar_reservas(self) -> None:
        print("\n--- LISTADO DE RESERVAS ---")
        if not self.__reservas:
            print("No hay reservas en el sistema.")
        for reservas in self.__reservas:
            fecha_str = reservas.get_fecha().isoformat() if hasattr(reservas.get_fecha(), 'isoformat') else str(
                reservas.get_fecha())
            inicio_str = reservas.hora_inicio.strftime("%H:%M") if hasattr(reservas.hora_inicio, 'strftime') else str(
                reservas.hora_inicio)
            fin_str = reservas.hora_fin.strftime("%H:%M") if hasattr(reservas.hora_fin, 'strftime') else str(
                reservas.hora_fin)
            print(
                f"[{reservas.id}] Sala: {reservas.get_sala().nombre} | Fecha: {fecha_str} | Horario: {inicio_str} - {fin_str} | Usuario: {reservas.get_usuario().get_username()}")

    def listar_usuarios(self) -> None:
        print("\n--- LISTADO DE USUARIOS ---")
        if not self.__usuarios:
            print("No hay usuarios en el sistema.")
        for usr in self.__usuarios:
            print(f"- {usr.get_dni()} | {usr.get_username()} | {usr.get_nombre_completo()} | Tipo: {usr.get_tipo()}")

    def listar_salas(self) -> None:
        print("\n--- LISTADO DE SALAS ---")
        if not self.__salas:
            print("No hay salas en el sistema.")
        for sala in self.__salas:
            print(sala)

    def buscar_reserva_por_id(self, id_reserva: str) -> Reserva | None:
        for reserva in self.__reservas:
            if reserva.id == id_reserva:
                return reserva
        return None

    def cancelar_reserva(self, id_reserva: str) -> bool:
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

    def editar_reserva(self, id_reserva: str, nueva_fecha: date | str, nueva_hora_inicio: time | str | float | int,
                       nueva_hora_fin: time | str | float | int) -> bool:
        reserva = self.buscar_reserva_por_id(id_reserva)
        if not reserva:
            print("Error: No se ha encontrado la reserva.")
            return False

        try:
            nueva_fecha_n = _comprobar_formato_fecha(nueva_fecha)
            nueva_hora_inicio_n = _comprobar_formato_hora(nueva_hora_inicio)
            nueva_hora_fin_n = _comprobar_formato_hora(nueva_hora_fin)
        except ValueError as e:
            print(f"Error: {e}")
            return False

        self.__reservas.remove(reserva)

        if self.comprobar_disponibilidad(reserva.get_sala(), nueva_fecha_n, nueva_hora_inicio_n, nueva_hora_fin_n):
            reserva.fecha = nueva_fecha_n
            reserva.hora_inicio = nueva_hora_inicio_n
            reserva.hora_fin = nueva_hora_fin_n
            self.__reservas.append(reserva)
            try:
                self.__persistencia.guardar_todos(self)
            except Exception:
                pass
            print(f"Reserva '{id_reserva}' actualizada correctamente.")
            return True
        else:
            self.__reservas.append(reserva)
            print("Error: La sala no está disponible en ese nuevo horario.")
            return False

    def filtrar_reservas(self, fecha: date | str | None = None, id_sala: str | None = None,
                         dni_usuario: str | None = None) -> None:
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
            print(
                f"[{r.id}] Sala: {r.get_sala().nombre} | Fecha: {r.get_fecha()} | Horario: {r.hora_inicio}h - {r.hora_fin}h | Usuario: {r.get_usuario().get_username()}")

    def asociar_recurso_a_sala(self, recurso: Recurso, id_sala: str) -> bool:
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

    def guardar_txt(self, ruta: str) -> bool:
        try:
            self.__persistencia.guardar_todos(self, carpeta=ruta)
            print("Guardado en txt correcto.")
            return True
        except Exception:
            print("Error guardando txt.")
            return False

    def guardar_backup(self, ruta: str) -> bool:
        try:
            self.__persistencia.guardar_backup(ruta, self)
            print("Backup creado.")
            return True
        except Exception:
            print("Error creando backup.")
            return False

    def restaurar_backup(self, ruta: str) -> bool:
        try:
            self.__persistencia.restaurar_backup(ruta, self)
            print("Backup restaurado.")
            return True
        except Exception:
            print("Error restaurando backup.")
            return False