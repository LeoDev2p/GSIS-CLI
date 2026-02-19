"""Module with utility functions for the application, including console management, date handling, text length calculation, and a progress bar display."""

import os
import time
from datetime import date


def Clearconsole():
    """Clear the console screen based on the operating system."""
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def date_today():
    """Fetch the current date and return it as a string in 'YYYY-MM-DD' format."""
    d = date.today().strftime("%Y-%m-%d")
    return d


lengthText = lambda lista, index: max(list(map(lambda x: len(x[index]), lista)))


def progress_bar():
    """Display a progress bar in the console."""
    # El '\r' y el 'end=""' son los que fuerzan la actualización en la misma línea
    print()
    for i in range(101):
        print(f"\r[{'#' * (i // 2):<50}] {i}%", end="", flush=True)
        time.sleep(0.03)
    print("\n")
