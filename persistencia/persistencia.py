import pickle
import os
from typing import Any
from entidades.usuario import UsuarioNormal, UsuarioPremium, Admin, Usuario
from entidades.sala import SalaReuniones, Despacho, EspacioAbierto, Sala
from entidades.recurso import Recurso
from entidades.reserva import Reserva
from servicios.gestorreserva import GestorReservas

# Clase encargada de leer y escribir la información en el disco.
class Persistencia:

    # Guarda las listas de objetos del gestor en diferentes ficheros de texto.
    def guardar_todos(self, gestor: GestorReservas, carpeta: str = "./archivos") -> None:
        estado: dict[str, Any] = gestor.obtener_estado()
        try:
            os.makedirs(carpeta, exist_ok=True)
        except Exception:
            pass
        self._escribir_usuarios(f"{carpeta}/usuarios.txt", estado["usuarios"])
        self._escribir_salas(f"{carpeta}/salas.txt", estado["salas"])
        self._escribir_reservas(f"{carpeta}/reservas.txt", estado["reservas"])

    def _escribir_usuarios(self, ruta: str, usuarios: list[Usuario]) -> None:
        with open(ruta, "w", encoding="utf-8") as f:
            for u in usuarios:
                linea: str = f"{u.get_dni()},{u.get_username()},{u.get_nombre()},{u.get_apellidos()},{u.get_email()},{u.get_tlf()},{u.get_tipo()}\n"
                f.write(linea)

    def _escribir_salas(self, ruta: str, salas: list[Sala]) -> None:
        with open(ruta, "w", encoding="utf-8") as f:
            for s in salas:
                recursos: list[str] = []
                for r in s.recursos:
                    recursos.append(f"{r.id}:{r.nombre}:{r.tipo}:{r.disponible}")
                recursos_str: str = "|".join(recursos)
                linea: str = f"{s.id_sala},{s.nombre},{s.capacidad},{s.disponible},{s.get_tipo()},{recursos_str}\n"
                f.write(linea)

    def _escribir_reservas(self, ruta: str, reservas: list[Reserva]) -> None:
        with open(ruta, "w", encoding="utf-8") as f:
            for r in reservas:
                fecha: str = r.get_fecha().isoformat() if hasattr(r.get_fecha(), 'isoformat') else str(r.get_fecha())
                inicio: str = r.hora_inicio.strftime("%H:%M") if hasattr(r.hora_inicio, 'strftime') else str(r.hora_inicio)
                fin: str = r.hora_fin.strftime("%H:%M") if hasattr(r.hora_fin, 'strftime') else str(r.hora_fin)
                linea: str = f"{r.id},{r.get_usuario().get_dni()},{r.get_sala().id_sala},{fecha},{inicio},{fin},{r.num_personas}\n"
                f.write(linea)

    # Inicializa la recarga de datos guardados y sustituye los de inicio.
    def cargar_todos(self, gestor: GestorReservas, carpeta: str = "./archivos") -> None:
        usuarios: list[Usuario] = self._leer_usuarios(f"{carpeta}/usuarios.txt")
        salas: list[Sala] = self._leer_salas(f"{carpeta}/salas.txt")
        reservas: list[Reserva] = self._leer_reservas(f"{carpeta}/reservas.txt", usuarios, salas)
        estado: dict[str, Any] = {
            "usuarios": usuarios,
            "salas": salas,
            "reservas": reservas,
            "contador_reservas": 1,
        }
        if estado["reservas"]:
            try:
                max_id: int = max(int(r.id.split("-")[-1]) for r in estado["reservas"])
                estado["contador_reservas"] = max_id + 1
            except Exception:
                estado["contador_reservas"] = len(estado["reservas"]) + 1
        gestor.cargar_estado(estado)

    # Restaura mediante instanciación de objetos la lista de usuarios.
    def _leer_usuarios(self, ruta: str) -> list[Usuario]:
        usuarios: list[Usuario] = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    parts: list[str] = linea.split(",")
                    dni, username, nombre, apellidos, email, tlf, tipo_str = parts
                    tipo: int = int(tipo_str)
                    usr: Usuario
                    if tipo == 2:
                        usr = Admin(dni, username, nombre, apellidos, email, tlf)
                    elif tipo == 1:
                        usr = UsuarioPremium(dni, username, nombre, apellidos, email, tlf)
                    else:
                        usr = UsuarioNormal(dni, username, nombre, apellidos, email, tlf)
                    usuarios.append(usr)
        except FileNotFoundError:
            pass
        return usuarios

    # Restaura la lista de salas instanciando sus clases concretas.
    def _leer_salas(self, ruta: str) -> list[Sala]:
        salas: list[Sala] = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    parts: list[str] = linea.split(",")
                    id_sala, nombre, capacidad_str, disponible_str, tipo_sala, recursos_str = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5] if len(parts) > 5 else ""
                    capacidad: int = int(capacidad_str)
                    disponible: bool = (disponible_str == 'True')
                    s: Sala
                    if tipo_sala == "Despacho":
                        s = Despacho(id_sala, nombre, capacidad, disponible)
                    elif tipo_sala == "Espacio Abierto":
                        s = EspacioAbierto(id_sala, nombre, capacidad, disponible)
                    else:
                        s = SalaReuniones(id_sala, nombre, capacidad, disponible)
                    if recursos_str:
                        for rec in recursos_str.split("|"):
                            if not rec:
                                continue
                            rid, rnombre, rtipo, rdisp = rec.split(":")
                            r = Recurso(rid, rnombre, rtipo, rdisp == 'True')
                            s.agregar_recurso(r)
                    salas.append(s)
        except FileNotFoundError:
            pass
        return salas

    # Restaura reservas validando relaciones entre las clases instanciadas.
    def _leer_reservas(self, ruta: str, usuarios: list[Usuario], salas: list[Sala]) -> list[Reserva]:
        from datetime import datetime
        reservas: list[Reserva] = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    parts: list[str] = linea.split(",")
                    idr, dni_usr, id_sala, fecha_s, inicio_s, fin_s, num_personas = parts
                    fecha = datetime.fromisoformat(fecha_s).date()
                    h_ini = datetime.strptime(inicio_s, "%H:%M").time()
                    h_fin = datetime.strptime(fin_s, "%H:%M").time()
                    usuario = next((u for u in usuarios if u.get_dni() == dni_usr), None)
                    sala = next((s for s in salas if s.id_sala == id_sala), None)
                    if usuario and sala:
                        r = Reserva(idr, usuario, sala, fecha, h_ini, h_fin, int(num_personas))
                        reservas.append(r)
        except FileNotFoundError:
            pass
        return reservas

    def guardar_backup(self, ruta: str, gestor: GestorReservas) -> None:
        estado = gestor.obtener_estado()
        with open(ruta, "wb") as f:
            pickle.dump(estado, f)

    def restaurar_backup(self, ruta: str, gestor: GestorReservas) -> bool:
        with open(ruta, "rb") as f:
            estado = pickle.load(f)
        gestor.cargar_estado(estado)
        return True