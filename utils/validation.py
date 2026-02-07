"""Module for validation functions, including email, URL, and date validation."""

import re
from functools import wraps

from core.Exceptions import AuthError


def valitacion_email(func):
    """Validates that an argument is a correctly formatted email address.

    Decorator that checks if the fifth argument (index 5) or the first argument (index 0) of the decorated function is 
    a valid email address using regular expressions.

    Args:
        func(callable): Function to be decorated that receives an email address.

    Returns:
        callable: Wrapper function with email validation.

    Raises:
        AuthError: If the email address is not in a valid format (code 2060).
    """
    @wraps(func)
    def wrappers(*args, **kwargs):
        email = args[5] if len(args) > 2 else args[0]
        print (f"[DEBUG]: {email}")
        if not re.findall(
            r"\b[a-zA-Z0-9._]+@[a-z]+\.(?:[a-z]+|[a-z]+\.[a-z]+)\b", email
        ):
            raise AuthError(2060)

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
