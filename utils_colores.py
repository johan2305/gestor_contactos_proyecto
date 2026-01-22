import re
import os

class Colores:
    """Colores para la consola"""
    ROJO = '\033[91m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

    @staticmethod
    def texto(color, texto):
        return f"{color}{texto}{Colores.RESET}"

def clear():
    """Limpia la consola según el sistema operativo"""
    os.system('cls' if os.name == 'nt' else 'clear')


# ------------------------
# VALIDACIONES
# ------------------------

def correo_valido(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.com$'
    return re.match(patron, correo.lower())


def telefono_valido(telefono):
    return telefono.isdigit() and len(telefono) == 10
