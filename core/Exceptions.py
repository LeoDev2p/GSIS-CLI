
class DataBaseError (Exception):
    def __init__(self, message, code = 0):
        super().__init__(message)
        self.code = code

    
    def Error (self):
        match self.code:
            case 1050:
                return "Intentas crear una tabla con un nombre que ya se está usando."
            case 1054:
                return "Intentas referenciar una columna que no existe en la tabla especificada."
            case 1064:
                return "Hay un error tipográfico, una coma faltante o una palabra clave SQL mal escrita."
            case 1070:
                return "Base de datos sin registro."

# Campo con restriccion check
class RestrictionError (DataBaseError):
    def __init__(self, message, code=0):
        super().__init__(message, code)

# cantidad incorrecta de prametros
class InvalidParameterCountError (DataBaseError):
    def __init__(self, message, code=0):
        super().__init__(message, code)

# la categoria no existe
class CategoryError (DataBaseError):
    def __init__(self, message, code=0):
        super().__init__(message, code)

# No existe la fila
class RowError (DataBaseError):
    def __init__(self, message, code=0):
        super().__init__(message, code)

# error de autenticacion
class AuthError (Exception):
    def __init__(self, code = 0):
        self.code = code
        super().__init__(self.Error ())

    def Error (self):
        match self.code:
            case 2040:
                return "Usuario incorrecto"
            case 2050:
                return "Contraseña incorrecta"
            case 2060:
                return "Email invalido"

# url incorrecta
class UrlError (Exception):
    def __init__(self, message):
        super().__init__(message)