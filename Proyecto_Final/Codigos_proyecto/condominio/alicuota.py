import datetime
from csv_managment import *
from tabulate import tabulate

database = "./databases/alicuota.csv"
directorio = "./databases"

def registrar_alicuota(id, residente, estado_pago, porcentaje_alicuota, base_imponible, descripcion, multa, descuento, ajuste_extraordinario):
    fecha_registro = datetime.datetime.now().strftime('%Y-%m-%d')

    total_calculado = round((base_imponible * porcentaje_alicuota) + multa - descuento + ajuste_extraordinario,2)
    alicuota = [id, residente, estado_pago, porcentaje_alicuota, base_imponible, descripcion, fecha_registro, multa, descuento, ajuste_extraordinario, total_calculado]
    insertar(database, alicuota,directorio)

def mostrar_alicuotas():
    alicuotas = leer(database)
    imprimir_alicuotas(alicuotas)

def actualizar_alicuota(id, residente, estado_pago, porcentaje_alicuota, base_imponible, descripcion, multa, descuento, ajuste_extraordinario):
    alicuota_actual = buscar_por_id(database, id)

    if not alicuota_actual:
        print(f"No se encontró la alícuota con ID {id}")
        return
    
    total_calculado = (base_imponible * porcentaje_alicuota) + multa - descuento + ajuste_extraordinario

    alicuota = [id, residente, estado_pago, porcentaje_alicuota, base_imponible, descripcion, alicuota_actual[6], multa, descuento, ajuste_extraordinario, total_calculado]
    actualizar(database, id, alicuota)

def eliminar_alicuota(id):
    eliminar(database, id)

def buscar_alicuotas_pendientes():
    alicuotas = buscar(database, "pendiente")
    imprimir_alicuotas(alicuotas)

def buscar_alicuota(id):
    alicuota = buscar_por_id(database, id)
    if alicuota:
        imprimir_alicuotas([alicuota])
    else:
        print(f"No se encontró la alícuota con ID {id}")

colalign = ("center", "left", "center", "right", "right", "left", "center", "right", "right", "right", "right")

def imprimir_alicuotas(alicuotas):
    headers = ["ID", "Residente", "Estado de Pago", "Porcentaje Alícuota", "Base Imponible", "Descripción", "Fecha de Registro", "Multa", "Descuento", "Adicional", "Total"]
    anchos = [len(header) for header in headers]
    
    for fila in alicuotas:
        for i, celda in enumerate(fila):
            anchos[i] = max(anchos[i], len(str(celda)))
    

    formato_fila = " | ".join(f"{{:<{ancho}}}" for ancho in anchos) 
    linea = "+".join("-" * ancho for ancho in anchos)
    
    print(linea)
    print(formato_fila.format(*headers))
    print(linea)
    for fila in alicuotas:
        print(formato_fila.format(*fila))
    print(linea)