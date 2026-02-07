"""Module Exception module for database errors, categories, authentication, and URL validation."""

class DataBaseError(Exception):
    """Custom exception class for handling database-related errors, with specific error codes for different types of database issues."""
    def __init__(self, message, code=0):
        """Constructor for DataBaseError that initializes the error message and code."""
        super().__init__(message)
        self.code = code

    def Error(self):
        """Function that returns a specific error message based on the error code."""
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
    """handling database constraint violations, inheriting from DataBaseError."""
    def __init__(self, message, code=0):
        super().__init__(message, code)


# cantidad incorrecta de prametros
class InvalidParameterCountError(DataBaseError):
    """Handling errors related to an incorrect number of parameters supplied to a database query."""
    def __init__(self, message, code=0):
        super().__init__(message, code)


# la categoria no existe
class CategoryError(DataBaseError):
    """It is launched when the category does not exist."""
    def __init__(self, message, code=0):
        super().__init__(message, code)


# No existe la fila
class RowError(DataBaseError):
    """Handling errors related to a non-existent row in the database."""
    def __init__(self, message, code=0):
        super().__init__(message, code)


# error de autenticacion
class AuthError(Exception):
    """Handling authtntication errors."""
    def __init__(self, code=0, attempts = 0):
        self.code = code
        self.attempts = attempts
        super().__init__(self.Error())

    def Error(self):
        """Return a specific error message based on the authentication error code."""
        match self.code:
            case 2040:
                return "Incorrect user"
            case 2050:
                return f"Incorrect password. Failed {self.attempts}/3 attempts and the database will be deleted."
            case 2060:
                return f"Invalid email. Failed {self.attempts}/3 attempts and the database will be deleted."


class PasswordMismatchError(AuthError):
    """Handling errors related to a password mismatch during authentication."""
    def __init__(self, message):
        super().__init__(message)


class HashCorruptionError(AuthError):
    """Handling errors related to hash corruption during authentication."""
    def __init__(self, message):
        super().__init__(message)

class SecurityError(AuthError):
    def __init__(self, message):
        super().__init__(message)

# url incorrecta
class UrlError(Exception):
    """Handling errors related to invalid URLs."""
    def __init__(self, message):
        super().__init__(message)
