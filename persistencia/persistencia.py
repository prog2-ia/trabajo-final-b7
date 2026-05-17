import pickle
import os
from entidades.usuario import UsuarioNormal, UsuarioPremium, Admin
from entidades.sala import SalaReuniones, Despacho, EspacioAbierto
from entidades.recurso import Recurso


class Persistencia:

    def guardar_todos(self, gestor, carpeta="./archivos"):
        estado = gestor.obtener_estado()
        try:
            os.makedirs(carpeta, exist_ok=True)
        except Exception:
            pass
        self._escribir_usuarios(f"{carpeta}/usuarios.txt", estado["usuarios"])
        self._escribir_salas(f"{carpeta}/salas.txt", estado["salas"])
        self._escribir_reservas(f"{carpeta}/reservas.txt", estado["reservas"])

    def _escribir_usuarios(self, ruta, usuarios):
        with open(ruta, "w", encoding="utf-8") as f:
            for u in usuarios:
                linea = f"{u.get_dni()},{u.get_username()},{u.get_nombre()},{u.get_apellidos()},{u.get_email()},{u.get_tlf()},{u.get_tipo()}\n"
                f.write(linea)

    def _escribir_salas(self, ruta, salas):
        with open(ruta, "w", encoding="utf-8") as f:
            for s in salas:
                recursos = []
                for r in s.recursos:
                    recursos.append(f"{r.id}:{r.nombre}:{r.tipo}:{r.disponible}")
                recursos_str = "|".join(recursos)
                linea = f"{s.id_sala},{s.nombre},{s.capacidad},{s.disponible},{s.get_tipo()},{recursos_str}\n"
                f.write(linea)

    def _escribir_reservas(self, ruta, reservas):
        with open(ruta, "w", encoding="utf-8") as f:
            for r in reservas:
                fecha = r.get_fecha().isoformat() if hasattr(r.get_fecha(), 'isoformat') else str(r.get_fecha())
                inicio = r.hora_inicio.strftime("%H:%M") if hasattr(r.hora_inicio, 'strftime') else str(r.hora_inicio)
                fin = r.hora_fin.strftime("%H:%M") if hasattr(r.hora_fin, 'strftime') else str(r.hora_fin)
                linea = f"{r.id},{r.get_usuario().get_dni()},{r.get_sala().id_sala},{fecha},{inicio},{fin},{r.num_personas}\n"
                f.write(linea)

    def cargar_todos(self, gestor, carpeta="./archivos"):
        usuarios = self._leer_usuarios(f"{carpeta}/usuarios.txt")
        salas = self._leer_salas(f"{carpeta}/salas.txt")
        reservas = self._leer_reservas(f"{carpeta}/reservas.txt", usuarios, salas)
        estado = {
            "usuarios": usuarios,
            "salas": salas,
            "reservas": reservas,
            "contador_reservas": 1,
        }
        # ajustar contador de reservas si hay reservas
        if estado["reservas"]:
            try:
                max_id = max(int(r.id.split("-")[-1]) for r in estado["reservas"])
                estado["contador_reservas"] = max_id + 1
            except Exception:
                estado["contador_reservas"] = len(estado["reservas"]) + 1
        gestor.cargar_estado(estado)

    def _leer_usuarios(self, ruta):
        usuarios = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    parts = linea.split(",")
                    dni, username, nombre, apellidos, email, tlf, tipo = parts
                    tipo = int(tipo)
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

    def _leer_salas(self, ruta):
        salas = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    parts = linea.split(",")
                    # id,nombre,capacidad,disponible,tipo,recursos
                    id_sala, nombre, capacidad, disponible, tipo_sala, recursos_str = parts[0], parts[1], int(parts[2]), parts[3] == 'True', parts[4], parts[5] if len(parts) > 5 else ""
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

    def _leer_reservas(self, ruta, usuarios, salas):
        from datetime import datetime
        from entidades.reserva import Reserva
        reservas = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    parts = linea.split(",")
                    # id,dni_usuario,id_sala,fecha,inicio,fin,num_personas
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

    def guardar_backup(self, ruta, gestor):
        estado = gestor.obtener_estado()
        with open(ruta, "wb") as f:
            pickle.dump(estado, f)

    def restaurar_backup(self, ruta, gestor):
        with open(ruta, "rb") as f:
            estado = pickle.load(f)
        gestor.cargar_estado(estado)
        return True
