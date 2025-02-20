import re
import getpass
from csv_managment import *
from consola import * 
import msvcrt




def iniciar_sesion():
    limpiar_pantalla()

    clave_incorrecta = True
    intentos_realizados = 0
    intentos_permitidos = 3

    if obtener_credenciales_autorizadas() == []:
        registrar_administrador()

    while clave_incorrecta:
        print("\t----LOGIN---\t")

        usuario, clave = obtener_credenciales()
        validacion_exitosa = validar_credenciales(usuario, clave)

        if validacion_exitosa:
            clave_incorrecta = False
            print("\nCredenciales válidas")
            input("Presiona ENTER para pasar al menú ...")
            limpiar_pantalla()

        else:
            print("\nCredenciales inválidas\n")
            intentos_realizados += 1
            print("Te quedan " + str(intentos_permitidos - intentos_realizados) + " intentos")
            input("Presiona ENTER para volver al Login ...")
            limpiar_pantalla()

            if intentos_realizados >= intentos_permitidos:
                print("Número de intentos permitidos alcanzados")
                salir_programa()


def registrar_administrador():
    print("\tREGISTRAR\t")
    credenciales = obtener_credenciales()
    insertar("./databases/administrador.csv", credenciales, "./databases")
    limpiar_pantalla()


def validar_credenciales(usuario, clave):
    usuario_autorizado, clave_autorizada = obtener_credenciales_autorizadas()[0]
    return usuario == usuario_autorizado and clave == clave_autorizada


def obtener_credenciales_autorizadas():
    credenciales_autorizadas = leer("./databases/administrador.csv")
    return credenciales_autorizadas

validacion_username = r'^[a-zA-Z]+$'
validacion_clave = r'^(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})'

def obtener_credenciales():
    usuario = validar_entrada("username", validacion_username, "Ingresa solo letras")
    clave = validar_entrada("clave", validacion_clave, "Ingresa al menos 8 caracteres y al menos un caracter especial")
    return [usuario, clave]


def validar_entrada(tipo, patron, mensaje_error):
    while True:
        if tipo == "clave":
            entrada = input_password("Ingresa la clave: ")
        elif tipo == "username":
            entrada = input("Ingresa el nombre de usuario: ")
        else:
            print("Ingresa un tipo de entrada válido")
            break
        if re.match(patron, entrada):
            return entrada
        print(mensaje_error)



def input_password(prompt="Contraseña: "):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        key = msvcrt.getch()
        # Si se presiona Enter
        if key in (b'\r', b'\n'):
            print()  # Salto de línea
            break
        # Si se presiona Backspace
        elif key == b'\x08':
            if len(password) > 0:
                password = password[:-1]
                # Borra el asterisco de la consola
                print('\b \b', end='', flush=True)
        # Si se presiona Ctrl+C
        elif key == b'\x03':
            raise KeyboardInterrupt
        else:
            try:
                ch = key.decode('utf-8')
            except UnicodeDecodeError:
                continue
            password += ch
            print('*', end='', flush=True)
    return password

