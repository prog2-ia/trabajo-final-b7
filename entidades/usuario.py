from abc import ABC, abstractmethod

class Usuario(ABC):

    def __init__(self, dni, username, nombre, apellidos, email, telefono, tipo):
        self.__dni = dni
        self.__username = username
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__email = email
        self.__telefono = telefono
        self.__tipo = tipo

    @property
    def dni(self):
        return self.__dni

    @dni.setter
    def dni(self, valor):
        self.__dni = valor

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, valor):
        self.__username = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    @property
    def apellidos(self):
        return self.__apellidos

    @apellidos.setter
    def apellidos(self, valor):
        self.__apellidos = valor

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        self.__email = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, valor):
        self.__tipo = valor

    def get_dni(self):
        return self.__dni

    def get_username(self):
        return self.__username

    def get_nombre(self):
        return self.__nombre

    def get_apellidos(self):
        return self.__apellidos

    def get_nombre_completo(self):
        return self.__apellidos + ", " + self.__nombre

    def get_email(self):
        return self.__email

    def get_tlf(self):
        return self.__telefono

    def get_tipo(self):
        return self.__tipo

    def es_admin(self):
        return self.__tipo == 2

    def es_premium(self):
        return self.__tipo == 1

    def set_email(self, email):
        self.__email = email
        return True

    def set_username(self, username):
        self.__username = username
        return True

    def puede_reservar_sala(self, sala):
        return sala.puede_reservar(self)

    def __str__(self):
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

    def __init__(self, dni, username, nombre, apellidos, email, telefono):
        super().__init__(dni, username, nombre, apellidos, email, telefono, 0)


class UsuarioPremium(Usuario):

    def __init__(self, dni, username, nombre, apellidos, email, telefono):
        super().__init__(dni, username, nombre, apellidos, email, telefono, 1)


class Admin(Usuario):

    def __init__(self, dni, username, nombre, apellidos, email, telefono):
        super().__init__(dni, username, nombre, apellidos, email, telefono, 2)

