class Usuario:
    def __init__(self, dni, username, nombre, apellidos, email, telefono, tipo):
        self.dni = dni
        self.username = username
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono
        self.tipo = tipo

    def get_dni(self):
        return self.dni

    def get_username(self):
        return self.username

    def get_nombre(self):
        return self.nombre

    def get_apellidos(self):
        return self.apellidos

    def get_nombre_completo(self):
        return self.apellidos + ", " + self.nombre

    def get_email(self):
        return self.email

    def get_tlf(self):
        return self.telefono

    def get_tipo(self):
        return self.tipo

    def es_admin(self):
        return True if self.tipo == 2 else False

    def es_premium(self):
        return True if self.tipo == 1 else False

    def set_email(self, email):
        self.email = email
        return True  # TODO: Cuando demos en clase control de excepciones no siempre será True

    def set_username(self, username):
        self.username = username
        return True  # TODO: Cuando demos en clase control de excepciones no siempre será True

    def __str__(self):
        return f'''
        DNI: {self.dni}
        Nombre de Usuario: {self.username}
        Nombre: {self.nombre} {self.apellidos}
        Email: {self.email}
        Telefono: {self.telefono}
        Tipo: {"Premium" if self.tipo == 1 else "Admin" if self.tipo == 2 else "Normal"}
        '''