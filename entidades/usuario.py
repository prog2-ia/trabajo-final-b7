from abc import ABC, abstractmethod
from typing import Any

class Usuario(ABC):

    def __init__(self, dni: str, username: str, nombre: str, apellidos: str, email: str, telefono: str, tipo: int) -> None:
        self.__dni: str = dni
        self.__username: str = username
        self.__nombre: str = nombre
        self.__apellidos: str = apellidos
        self.__email: str = email
        self.__telefono: str = telefono
        self.__tipo: int = tipo

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, valor: str) -> None:
        self.__dni = valor

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, valor: str) -> None:
        self.__username = valor

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor

    @property
    def apellidos(self) -> str:
        return self.__apellidos

    @apellidos.setter
    def apellidos(self, valor: str) -> None:
        self.__apellidos = valor

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str) -> None:
        self.__email = valor

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        self.__telefono = valor

    @property
    def tipo(self) -> int:
        return self.__tipo

    @tipo.setter
    def tipo(self, valor: int) -> None:
        self.__tipo = valor

    def get_dni(self) -> str:
        return self.__dni

    def get_username(self) -> str:
        return self.__username

    def get_nombre(self) -> str:
        return self.__nombre

    def get_apellidos(self) -> str:
        return self.__apellidos

    def get_nombre_completo(self) -> str:
        return self.__apellidos + ", " + self.__nombre

    def get_email(self) -> str:
        return self.__email

    def get_tlf(self) -> str:
        return self.__telefono

    def get_tipo(self) -> int:
        return self.__tipo

    def es_admin(self) -> bool:
        return self.__tipo == 2

    def es_premium(self) -> bool:
        return self.__tipo == 1

    def set_email(self, email: str) -> bool:
        self.__email = email
        return True

    def set_username(self, username: str) -> bool:
        self.__username = username
        return True

    def puede_reservar_sala(self, sala: Any) -> bool:
        return sala.puede_reservar(self)

    def __str__(self) -> str:
        tipo_str = "Premium" if self.__tipo == 1 else "Admin" if self.__tipo == 2 else "Normal"
        return f'''
        DNI: {self.__dni}
        Nombre de Usuario: {self.__username}
        Nombre: {self.__nombre} {self.__apellidos}
        Email: {self.__email}
        Telefono: {self.__telefono}
        Tipo: {tipo_str}
        '''

class UsuarioNormal(Usuario):
    def __init__(self, dni: str, username: str, nombre: str, apellidos: str, email: str, telefono: str) -> None:
        super().__init__(dni, username, nombre, apellidos, email, telefono, 0)


class UsuarioPremium(Usuario):
    def __init__(self, dni: str, username: str, nombre: str, apellidos: str, email: str, telefono: str) -> None:
        super().__init__(dni, username, nombre, apellidos, email, telefono, 1)


class Admin(Usuario):
    def __init__(self, dni: str, username: str, nombre: str, apellidos: str, email: str, telefono: str) -> None:
        super().__init__(dni, username, nombre, apellidos, email, telefono, 2)

