import os
import sys

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def salir_programa():
    sys.exit(0)