from entidades.recurso import Recurso
from entidades.usuario import UsuarioNormal, UsuarioPremium, Admin
from entidades.sala import SalaReuniones, Despacho, EspacioAbierto


def mostrar_opciones():
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
    print("s. Salir del programa")
    print("=" * 40)


def iniciar_interfaz(gestor):
    """Bucle principal de la interfaz de usuario por consola."""
    while True:
        mostrar_opciones()
        opcion = input("Selecciona una opción: ").strip().lower()

        if opcion == 's':
            print("\nSaliendo del sistema...")
            break

        elif opcion == '1':
            print("\n--- CREAR NUEVO USUARIO ---")
            dni = input("DNI: ")
            username = input("Nombre de usuario (Username): ")
            nombre = input("Nombre: ")
            apellidos = input("Apellidos: ")
            email = input("Email: ")
            tlf = input("Teléfono: ")

            print("Tipos de usuario: [0] Normal | [1] Premium | [2] Admin")
            tipo = input("Selecciona el tipo (0/1/2): ")

            if tipo == '1':
                nuevo_usr = UsuarioPremium(dni, username, nombre, apellidos, email, tlf)
            elif tipo == '2':
                nuevo_usr = Admin(dni, username, nombre, apellidos, email, tlf)
            else:
                nuevo_usr = UsuarioNormal(dni, username, nombre, apellidos, email, tlf)

            gestor.agregar_usuario(nuevo_usr)
            print(f"Usuario '{username}' creado y añadido con éxito.")

        elif opcion == '2':
            print("\n--- CREAR NUEVA SALA ---")
            id_sala = input("ID de la Sala (ej. SR-02): ")
            nombre = input("Nombre descriptivo: ")
            capacidad = int(input("Capacidad máxima (nº de personas): "))

            print("Tipos de sala: [1] Sala de Reuniones | [2] Despacho | [3] Espacio Abierto")
            tipo = input("Seleccione el tipo (1/2/3): ")

            if tipo == '2':
                nueva_sala = Despacho(id_sala, nombre, capacidad)
            elif tipo == '3':
                nueva_sala = EspacioAbierto(id_sala, nombre, capacidad)
            else:
                nueva_sala = SalaReuniones(id_sala, nombre, capacidad)

            gestor.agregar_sala(nueva_sala)
            print(f"Sala '{nombre}' (ID: {id_sala}) creada con éxito.")

        elif opcion == '3':
            print("\n--- CREAR Y ASIGNAR RECURSO ---")
            id_recurso = input("ID del recurso (ej. PZ-02): ")
            nombre = input("Nombre descriptivo: ")
            tipo_rec = input("Tipo de recurso: ")
            id_sala = input("ID de la sala a la que se va a asignar: ")

            nuevo_recurso = Recurso(id_recurso, nombre, tipo_rec)
            gestor.asociar_recurso_a_sala(nuevo_recurso, id_sala)

        elif opcion == '4':
            print("\n--- CREAR NUEVA RESERVA ---")
            dni_usr = input("DNI del Usuario: ")
            id_sala = input("ID de la Sala: ")
            fecha = input("Fecha (YYYY-MM-DD): ")
            hora_inicio = float(input("Hora de inicio (ej. 10.5): "))
            hora_fin = float(input("Hora de fin (ej. 12.0): "))
            num_personas = int(input("Número de personas: "))

            gestor.crear_reserva(dni_usr, id_sala, fecha, hora_inicio, hora_fin, num_personas)

        elif opcion == '5':
            gestor.listar_reservas()

        elif opcion == '6':
            gestor.listar_usuarios()

        elif opcion == '7':
            gestor.listar_salas()

        elif opcion == '8':
            print("\n--- EDITAR RESERVA ---")
            id_res = input("ID de la reserva a modificar (ej. RES-1): ")
            f_nueva = input("Nueva fecha (YYYY-MM-DD): ")
            h_ini = float(input("Nueva hora inicio: "))
            h_fin = float(input("Nueva hora fin: "))
            gestor.editar_reserva(id_res, f_nueva, h_ini, h_fin)

        elif opcion == '9':
            print("\n--- CANCELAR RESERVA ---")
            id_res = input("ID de la reserva a cancelar: ")
            gestor.cancelar_reserva(id_res)

        elif opcion == '10':
            print("\n--- FILTRAR RESERVAS ---")
            print("(Dejar vacío para omitir filtro)")
            f = input("Fecha (YYYY-MM-DD): ").strip() or None
            s = input("ID Sala: ").strip() or None
            u = input("DNI Usuario: ").strip() or None
            gestor.filtrar_reservas(fecha=f, id_sala=s, dni_usuario=u)

        else:
            print("Opción no válida. Inténtalo de nuevo.")