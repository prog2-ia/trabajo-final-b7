from ui.menu import iniciar_interfaz
from entidades.gestorreserva import GestorReservas

def main():
    sistema = GestorReservas()
    iniciar_interfaz(sistema)

if __name__ == "__main__":
    main()