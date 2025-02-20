from consola import *
from alicuota import *
import re

def mostrar_menu():
    while True:
        opciones_menu()
        opcion = obtener_opcion()
        if opcion == 0:
            continue
        ejecutar_opcion(opcion)

def opciones_menu():
    print("\t------MENU------\t")
    print("1. Registrar alicuota")
    print("2. Mostrar alicuotas")
    print("3. Buscar alicuota")
    print("4. Actualizar alicuota")
    print("5. Mostrar alicuotas pendientes por pagar")
    print("6. Borrar alicuota")
    print("7. Salir del programa")

def obtener_opcion():
    opcion = input("Ingresa tu opcion: ")
    if re.match(r"^[+]?\d+$",opcion):
        opcion = int(opcion)
        if opcion in range(1,8):
            return opcion
        else:
            print("Ingresa una opcion del 1 al 7")
            input("Presiona ENTER para volver al menu")
            limpiar_pantalla()
            return 0

    else:
        print("Ingresa una opcion valida")
        input("Presiona ENTER para volver al menu")
        limpiar_pantalla()
        return 0

def ejecutar_opcion(opcion):
    opciones = {
        1: opt_registrar_alicuota,
        2: opt_mostrar_alicuotas,
        3: opt_buscar_alicuota,
        4: opt_actualizar_alicuota,
        5: opt_mostrar_alicuotas_pendientes,
        6: opt_borrar_alicuota,
        7: salir_programa
    }
    if opcion in opciones:
        opciones[opcion]()


def opt_registrar_alicuota():
    print("Registrar una alícuota:")
    datos = solicitar_datos_alicuota()
    if datos:
        registrar_alicuota(*datos)
        print("Alícuota registrada correctamente.")
    input("Presiona ENTER PARA VOLVER AL MENU PRINCIPAL")
    limpiar_pantalla()

def opt_actualizar_alicuota():

    print("Actualizar una alícuota:")

    id = input("ID de la alícuota: ")

    alicuota_actual = buscar_por_id("./databases/alicuota.csv", id)

    if alicuota_actual:
        print("Datos actuales de la alícuota:")
        print(alicuota_actual)
        con_id = False
        datos = solicitar_datos_alicuota(con_id)
        if datos:
            actualizar_alicuota(id,*datos)
            print("Alícuota actualizada correctamente.")
    else:
        print("Alícuota no encontrada.")
    input("Presiona ENTER PARA VOLVER AL MENU PRINCIPAL")
    limpiar_pantalla()

def opt_mostrar_alicuotas():
    print("Mostrando todas las alícuotas:")
    mostrar_alicuotas()
    input("Presiona ENTER PARA VOLVER AL MENU PRINCIPAL")
    limpiar_pantalla()

def opt_buscar_alicuota():
    print("Buscar una alícuota por ID:")
    id = input("ID de la alícuota: ")
    buscar_alicuota(id)
    input("Presiona ENTER PARA VOLVER AL MENU PRINCIPAL")
    limpiar_pantalla()

def opt_mostrar_alicuotas_pendientes():
    print("Mostrando alícuotas pendientes por pagar:")
    buscar_alicuotas_pendientes()
    input("Presiona ENTER PARA VOLVER AL MENU PRINCIPAL")
    limpiar_pantalla()

def opt_borrar_alicuota():
    print("Eliminar una alícuota por ID:")
    id = input("ID de la alícuota: ")
    buscar_alicuota(id)
    verificacion=validar_pregunta("Estas seguro de eliminar esta alicuota (si/no): ",r"^(si|no)$","Ingresa si o no")
    if verificacion == "si":
        eliminar_alicuota(id)
    input("Presiona ENTER PARA VOLVER AL MENU PRINCIPAL")
    limpiar_pantalla()


def salir_programa():
    print("Saliendo del programa...")
    exit()

def solicitar_datos_alicuota(con_id = True):
    if con_id:
        id = ingresar_validar_id()

        

    
    residente = validar_texto("Nombre del residente: ")
    
    validacion_estado_pago = r"^(pendiente|pagado)$"
    mensaje_error_estado_pago = "El estado de pago debe ser 'pendiente' o 'pagado'."
    estado_pago = validar_pregunta("Estado de pago (pendiente/pagado): ", validacion_estado_pago, mensaje_error_estado_pago)

    validacion_porcentaje = r"^(0(\.\d+)?|1(\.0*)?)$"
    mensaje_error_porcentaje = "debe ser un valor decimal entre 0 y 1"
    porcentaje_alicuota = float(validar_pregunta("Porcentaje de alícuota: ",validacion_porcentaje,mensaje_error_porcentaje))

    base_imponible = validar_numero_decimal("Base imponible: ")
    
    descripcion = validar_texto("Descripción: ")

    multa = validar_numero_decimal("Monto de la multa: ")

    descuento = validar_numero_decimal("Monto de descuento: ")

    ajuste_extraordinario = validar_numero_decimal("Ajuste extraordinario: ")
    if con_id:
        return id, residente, estado_pago, porcentaje_alicuota, base_imponible, descripcion, multa, descuento, ajuste_extraordinario
    else:
        return residente, estado_pago, porcentaje_alicuota, base_imponible, descripcion, multa, descuento, ajuste_extraordinario


def validar_numero_decimal(pregunta):
    validacion_numero_decimal = r"^(?=.*\d)(?=.*\.)?.+$"
    mensaje_error_numero_decimal = "Por favor, ingresa un numero válido."
    
    valor = float(validar_pregunta(pregunta,validacion_numero_decimal,mensaje_error_numero_decimal))
    
    return valor

def validar_texto(pregunta):
    validacion_texto = r"^[a-zA-Z]+$"
    mensaje_error = "Debes ingresar solo letras"
    validar_pregunta(pregunta,validacion_texto,mensaje_error)

def validar_pregunta(pregunta,validacion,mensaje_error):
    while True:
        valor = input(pregunta)
        if re.match(validacion,valor):
            return valor
        print(mensaje_error)
        input("\n Aplasta Enter para volver a rellenar el campo de forma correcta\n")
    
def ingresar_validar_id ():
    validacion_id = r"^[a-zA-Z0-9]+$"
    while True:
        id = validar_pregunta("ID de la alícuota: ",validacion_id, "Ingresa numeros o letras")
        if not validar_id(id):
            return id
        print("el id ya existe")
        input("\n Aplasta Enter para volver a rellenar el campo de forma correcta\n")
