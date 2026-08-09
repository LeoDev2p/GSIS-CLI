"""Module for validation functions, including email, URL, and date validation."""

import re
from functools import wraps

from src.core.Exceptions import AuthError


def valitacion_email(func):
    """Validates that an argument is a correctly formatted email address.

    Decorator that checks the email argument of the decorated function using a
    regular expression. The email is looked up in this order:
        - `kwargs['email']` if present (e.g. `register`)
        - `args[4]` for `SaveSafe` style signatures (site, category, url, username, email, ...)
        - `args[0]` for `login` (the username is the master email).

    Args:
        func(callable): Function to be decorated that receives an email address.

    Returns:
        callable: Wrapper function with email validation.

    Raises:
        AuthError: If the email address is not in a valid format (code 2060).
    """

    @wraps(func)
    def wrappers(*args, **kwargs):
        email = kwargs.get("email")

        if not isinstance(email, str):
            # En metodos de instancia el primer argumento posicional es self
            offset = 1 if (args and not isinstance(args[0], (str, int))) else 0
            if len(args) > offset + 4:
                email = args[offset + 4]
            elif len(args) > offset:
                email = args[offset]
            else:
                email = None

        if not re.findall(
            r"\b[a-zA-Z0-9._]+@[a-z]+\.(?:[a-z]+|[a-z]+\.[a-z]+)\b", str(email)
        ):
            from src.security.integrity import register_failed_attempt

            data = register_failed_attempt()
            print(f"[DEBUG]: validation email {data}")
            atp = data.get("attempts", 0)

            raise AuthError(2060, atp)

        return func(*args, **kwargs)

    return wrappers


def validacion_link(url: str) -> bool:
    """Validate if a given URL is in a correct format."""
    if re.findall(
        r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=\w]*)",
        url,
    ):
        return True
    else:
        return False


def validate_date(date: str) -> bool:
    """Validate if a given date string is in the format 'YYYY-MM-DD'."""
    return bool(
        re.findall(r"\b\d{4}[-/](?:0[1-9]|1[0-2])[-/](?:[0-2][1-9]|3[01])\b", date)
    )


normalize = lambda dates: map(lambda x: x.replace("/", "-"), dates)
