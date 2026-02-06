import re
from functools import wraps
from core.Exceptions import AuthError


def valitacion_email(func):
    """Valida que un argumento sea un email con formato correcto.
    
    Decorador que verifica si el quinto argumento (índice 5) o el primer
    argumento (índice 0) de la función decorada es un email válido usando
    expresiones regulares.
    
    Args:
        func (callable): Función a decorar que recibe un email.
    
    Returns:
        callable: Función wrapper con validación de email.
    
    Raises:
        AuthError: Si el email no tiene formato válido (código 2060).
    """
    @wraps(func)
    def wrappers(*args, **kwargs):
        email = args[5] if len(args) > 2 else args[0]
        if not re.findall(
            r"\b[a-zA-Z0-9._]+@[a-z]+\.(?:[a-z]+|[a-z]+\.[a-z]+)\b", email
        ):
            raise AuthError(2060)

        return func(*args, **kwargs)

    return wrappers


def validacion_link(url):
    if re.findall(
        r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=\w]*)",
        url,
    ):
        return True
    else:
        return False


def validate_date(date):
    return bool(
        re.findall(r"\b\d{4}[-/](?:0[1-9]|1[0-2])[-/](?:[0-2][1-9]|3[01])\b", date)
    )


normalize = lambda dates: map(lambda x: x.replace("/", "-"), dates)
