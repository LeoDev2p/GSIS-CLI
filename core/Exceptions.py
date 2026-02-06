class DataBaseError(Exception):
    def __init__(self, message, code=0):
        super().__init__(message)
        self.code = code

    def Error(self):
        match self.code:
            case 1050:
                return "You are trying to create a table with a name that is already in use."
            case 1054:
                return "You are trying to reference a column that does not exist in the specified table."
            case 1064:
                return "There is a typo, a missing comma, or a misspelled SQL keyword."
            case 1070:
                return "Database without registration."


# Campo con restriccion check
class RestrictionError(DataBaseError):
    def __init__(self, message, code=0):
        super().__init__(message, code)


# cantidad incorrecta de prametros
class InvalidParameterCountError(DataBaseError):
    def __init__(self, message, code=0):
        super().__init__(message, code)


# la categoria no existe
class CategoryError(DataBaseError):
    def __init__(self, message, code=0):
        super().__init__(message, code)


# No existe la fila
class RowError(DataBaseError):
    def __init__(self, message, code=0):
        super().__init__(message, code)


# error de autenticacion
class AuthError(Exception):
    def __init__(self, code=0):
        self.code = code
        super().__init__(self.Error())

    def Error(self):
        match self.code:
            case 2040:
                return "Incorrect user"
            case 2050:
                return "Incorrect password"
            case 2060:
                return "Invalid email"


class PasswordMismatchError(AuthError):
    def __init__(self, message, code=0):
        super().__init__(message)


class HashCorruptionError(AuthError):
    def __init__(self, message, code=0):
        super().__init__(message)


# url incorrecta
class UrlError(Exception):
    def __init__(self, message):
        super().__init__(message)
