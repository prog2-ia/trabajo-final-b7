# Gestor de Reservas de Coworking

Este proyecto es una de consola diseñada para administrar de forma sencilla las reservas de un espacio de coworking. 

El programa gestiona diferentes tipos de usuarios (Normal, Premium y Administrador) y distintos tipos de espacios, como salas de reuniones, despachos privados y espacios abiertos. El objetivo principal es organizar la disponibilidad de las salas, comprobando que se respete la capacidad máxima y evitando que se produzcan solapamientos de horarios en las reservas, entre otras cosas.

El programa se encuentra en desarrollo y algunas funcionalidades pueden no estar completas.

## Requisitos previos

* **Python 3.x** instalado en tu sistema.

## Instalación

Sigue estos pasos para configurar y ejecutar el programa en tu equipo:

1. **Descarga el código:**
   Clona este repositorio o descarga los archivos y extrae la carpeta en tu ordenador.
   ```bash
   git clone https://github.com/prog2-ia/trabajo-final-b7
   cd trabajo-final-b7

2. **Crea un entorno virtual (Opcional pero recomendado):**
   Utilizar un entorno virtual te permite mantener las dependencias de este proyecto aisladas, evitando conflictos con otros proyectos de Python.
   * Crea el entorno virtual llamado `venv`:
     ```bash
     python -m venv venv
     ```
   * Activa el entorno virtual:
     * En **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     * En **macOS / Linux**:
       ```bash
       source venv/bin/activate
       ```

3. **Instala las dependencias:**
   Una vez dentro de la carpeta del proyecto (y con el entorno virtual activado, si decidiste usarlo), instala los paquetes necesarios a través del archivo de requerimientos:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para comprobar el funcionamiento del sistema, puedes ejecutar el script main.py, el cual te mostrará el menú principal del programa con el que podrás empezar a gestionar de forma sencilla y simple (con más funcionalidades por implementar) el espacio de coworking. Para ejecutar el script puedes utilizar:

```bash
python3 main.py
```