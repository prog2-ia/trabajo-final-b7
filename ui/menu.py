from entidades.recurso import Recurso
from entidades.usuario import UsuarioNormal, UsuarioPremium, Admin
from entidades.sala import SalaReuniones, Despacho, EspacioAbierto


def mostrar_opciones():
    print("\n" + "=" * 35)
    print("GESTOR DE RESERVAS COWORKING")
    print("=" * 35)
    print("1. Crear nuevo usuario")
    print("2. Crear nueva sala")
    print("3. Crear nuevo recurso")
    print("4. Crear nueva reserva")
    print("5. Listar todas las reservas")
    print("s. Salir del programa")
    print("=" * 35)


def iniciar_interfaz(gestor):
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
            print(f"Usuario '{username}' creado y añadido al gestor con éxito.")

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
            print("\n--- CREAR NUEVO RECURSO ---")
            id = input("ID del recurso (ej. PZ-02): ")
            nombre = input("Nombre descriptivo: ")
            # TODO: Mejoraremos esto en un futuro para implementar herencia para recursos.
            tipo = input("Tipo de recurso: ")

            # TODO: Realmente poder añadir recursos a salas mediante el gestor.
            nuevo_recurso = Recurso(id, nombre, tipo)

        elif opcion == '4':
            print("\n--- CREAR NUEVA RESERVA ---")
            dni_usr = input("DNI del Usuario: ")
            id_sala = input("ID de la Sala: ")
            fecha = input("Fecha (YYYY-MM-DD): ")

            # TODO: Gestionar horas reales y no con números
            hora_inicio = float(input("Hora de inicio (ej. 10.5 para las 10:30): "))
            hora_fin = float(input("Hora de fin (ej. 12.0 para las 12:00): "))
            num_personas = int(input("Número de personas que asistirán: "))

            gestor.crear_reserva(dni_usr, id_sala, fecha, hora_inicio, hora_fin, num_personas)

        elif opcion == '5':
            gestor.listar_reservas()

        else:
            print("Opción no válida. Por favor, introduce un número del 1 al 4, o 's' para salir.")