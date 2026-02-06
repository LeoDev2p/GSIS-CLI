from datetime import date
import os
import time


# limpiar consola
def Clearconsole():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


# mostrar fecha actualizada
def date_today():
    d = date.today().strftime("%Y-%m-%d")
    return d


# calcular longitud de testo
lengthText = lambda lista, index: max(list(map(lambda x: len(x[index]), lista)))


def progress_bar():
    # El '\r' y el 'end=""' son los que fuerzan la actualización en la misma línea
    print()
    for i in range(101):
        print(f"\r[{'#'*(i//2):<50}] {i}%", end="", flush=True)
        time.sleep(0.03)
    print("\n")
