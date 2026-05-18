from datetime import datetime
from typing import Any
from entidades.recurso import Recurso
from entidades.usuario import UsuarioNormal, UsuarioPremium, Admin, Usuario
from entidades.sala import SalaReuniones, Despacho, EspacioAbierto, Sala


from datetime import datetime
from typing import Any
from entidades.recurso import Recurso
from entidades.usuario import UsuarioNormal, UsuarioPremium, Admin, Usuario
from entidades.sala import SalaReuniones, Despacho, EspacioAbierto, Sala


# Imprime las opciones del menú principal.
def mostrar_opciones() -> None:
    print("\n" + "=" * 40)
    print("  GESTOR DE RESERVAS COWORKING")
    print("=" * 40)
    print("1. Crear nuevo usuario")
    print("2. Crear nueva sala")
    print("3. Crear y asignar recurso a sala")
    print("4. Crear nueva reserva")
    print("5. Listar todas las reservas")
    print("6. Listar todos los usuarios")
    print("7. Listar todas las salas")
    print("8. Editar reserva")
    print("9. Cancelar reserva")
    print("10. Filtrar reservas")
    print("11. Guardar backup (pickle)")
    print("12. Restaurar backup (pickle)")
    print("s. Salir del programa")
    print("=" * 40)


# Controla el formato de entrada para números enteros mediante un bucle de gestión de excepciones.
def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Debes introducir un número entero válido (ej. 10).")



# Controla el formato de entrada para números decimales mediante un bucle de gestión de excepciones.
def leer_flotante(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Debes introducir un número decimal válido (ej. 10.5).")

# Valida y retorna una opción de las permitidas.
def leer_opcion(mensaje: str, opciones_validas: list[str]) -> str:
    while True:
        opcion: str = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        print(f"Error: Opción no válida. Selecciona una de estas: {', '.join(opciones_validas)}")

# Verifica el formato de datos temporales (fecha).
def leer_fecha(mensaje: str, opcional: bool = False) -> str | None:
    while True:
        fecha_str: str = input(mensaje).strip()
        if opcional and not fecha_str:
            return None
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha_str
        except ValueError:
            print("Error: El formato debe ser YYYY-MM-DD y ser una fecha real (ej. 2024-12-31).")

# Comprueba la congruencia temporal entre dos horas y asegura que la hora de inicio no sea mayor.
def leer_rango_horas(mensaje_inicio: str, mensaje_fin: str) -> tuple[float, float]:
    while True:
        h_ini: float = leer_flotante(mensaje_inicio)
        h_fin: float = leer_flotante(mensaje_fin)
        if h_ini < h_fin:
            return h_ini, h_fin
        print("Error: La hora de inicio no puede ser igual o posterior a la hora de fin. Inténtalo de nuevo.")

# Ejecuta el bucle del programa.
def iniciar_interfaz(gestor: Any) -> None:
    while True:
        mostrar_opciones()
        opcion: str = input("Selecciona una opción: ").strip().lower()

        if opcion == 's':
            print("\nSaliendo del sistema...")
            break

        elif opcion == '1':
            print("\n--- CREAR NUEVO USUARIO ---")
            dni: str = input("DNI: ").strip()
            username: str = input("Nombre de usuario (Username): ").strip()
            nombre: str = input("Nombre: ").strip()
            apellidos: str = input("Apellidos: ").strip()
            email: str = input("Email: ").strip()
            tlf: str = input("Teléfono: ").strip()

            print("Tipos de usuario: [0] Normal | [1] Premium | [2] Admin")
            tipo: str = input("Selecciona el tipo (0/1/2): ").strip()

            nuevo_usr: Usuario
            if tipo == '1':
                nuevo_usr = UsuarioPremium(dni, username, nombre, apellidos, email, tlf)
            elif tipo == '2':
                nuevo_usr = Admin(dni, username, nombre, apellidos, email, tlf)
            else:
                nuevo_usr = UsuarioNormal(dni, username, nombre, apellidos, email, tlf)

            gestor.agregar_usuario(nuevo_usr)
            try:
                gestor.agregar_usuario(nuevo_usr)
                print(f"Usuario '{username}' creado y añadido con éxito.")
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '2':
            print("\n--- CREAR NUEVA SALA ---")
            id_sala: str = input("ID de la Sala (ej. SR-02): ").strip()
            nombre = input("Nombre descriptivo: ").strip()

            capacidad: int = leer_entero("Capacidad máxima (nº de personas): ")

            print("Tipos de sala: [1] Sala de Reuniones | [2] Despacho | [3] Espacio Abierto")
            tipo = input("Seleccione el tipo (1/2/3): ").strip()

            nueva_sala: Sala
            if tipo == '2':
                nueva_sala = Despacho(id_sala, nombre, capacidad)
            elif tipo == '3':
                nueva_sala = EspacioAbierto(id_sala, nombre, capacidad)
            else:
                nueva_sala = SalaReuniones(id_sala, nombre, capacidad)

            gestor.agregar_sala(nueva_sala)
            try:
                gestor.agregar_sala(nueva_sala)
                print(f"Sala '{nombre}' (ID: {id_sala}) creada con éxito.")
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '3':
            print("\n--- CREAR Y ASIGNAR RECURSO ---")
            id_recurso: str = input("ID del recurso (ej. PZ-02): ").strip()
            nombre = input("Nombre descriptivo: ").strip()
            tipo_rec: str = input("Tipo de recurso: ").strip()
            id_sala = input("ID de la sala a la que se va a asignar: ").strip()

            nuevo_recurso: Recurso = Recurso(id_recurso, nombre, tipo_rec)
            try:
                gestor.asociar_recurso_a_sala(nuevo_recurso, id_sala)
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '4':
            print("\n--- CREAR NUEVA RESERVA ---")
            dni_usr: str = input("DNI del Usuario: ").strip()
            id_sala = input("ID de la Sala: ").strip()
            fecha: str | None = input("Fecha (YYYY-MM-DD): ").strip()

            hora_inicio: float = leer_flotante("Hora de inicio (ej. 10.5): ")
            hora_fin: float = leer_flotante("Hora de fin (ej. 12.0): ")
            num_personas: int = leer_entero("Número de personas: ")

            try:
                gestor.crear_reserva(dni_usr, id_sala, fecha, hora_inicio, hora_fin, num_personas)
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '5':
            try:
                gestor.listar_reservas()
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '6':
            try:
                gestor.listar_usuarios()
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '7':
            try:
                gestor.listar_salas()
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '8':
            print("\n--- EDITAR RESERVA ---")
            id_res: str = input("ID de la reserva a modificar (ej. RES-1): ").strip()
            f_nueva: str = input("Nueva fecha (YYYY-MM-DD): ").strip()

            h_ini: float = leer_flotante("Nueva hora inicio: ")
            h_fin: float = leer_flotante("Nueva hora fin: ")

            try:
                gestor.editar_reserva(id_res, f_nueva, h_ini, h_fin)
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '9':
            print("\n--- CANCELAR RESERVA ---")
            id_res = input("ID de la reserva a cancelar: ").strip()
            try:
                gestor.cancelar_reserva(id_res)
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '10':
            print("\n--- FILTRAR RESERVAS ---")
            print("(Dejar vacío para omitir filtro)")
            f: str | None = input("Fecha (YYYY-MM-DD): ").strip() or None
            s: str | None = input("ID Sala: ").strip() or None
            u: str | None = input("DNI Usuario: ").strip() or None
            try:
                gestor.filtrar_reservas(fecha=f, id_sala=s, dni_usuario=u)
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '11':
            ruta: str = './archivos/' + input("Nombre fichero backup (por defecto backup.pkl): ").strip() or "./archivos/backup.pkl"
            try:
                gestor.guardar_backup(ruta)
            except Exception as e:
                print(f"ERROR: {e}")

        elif opcion == '12':
            ruta = './archivos/' + input("Nombre fichero backup a restaurar (por defecto backup.pkl): ").strip() or "./archivos/backup.pkl"
            try:
                gestor.restaurar_backup(ruta)
            except Exception as e:
                print(f"ERROR: {e}")

        else:
            print("Opción no válida. Inténtalo de nuevo.")