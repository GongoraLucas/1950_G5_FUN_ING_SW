import csv
import os

def insertar(path_archivo_csv, arreglo_con_datos, directorio):
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    with open(path_archivo_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(arreglo_con_datos)
    print(f"Alicuota registrada con exito en  '{path_archivo_csv}' ")

def leer(path_archivo_csv):
    if not verificar_existencia_archivo(path_archivo_csv):
        print(f"El archivo '{path_archivo_csv}' no existe.")
        return []

    with open(path_archivo_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        return [fila for fila in reader]

def buscar(path_archivo_csv, criterio_de_busqueda):
    datos_encontrados = []
    if not verificar_existencia_archivo(path_archivo_csv):
        print(f"El archivo '{path_archivo_csv}' no existe.")
        return None

    with open(path_archivo_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        for fila in reader:
            if criterio_de_busqueda in fila:
                datos_encontrados.append(fila) 
        if len(datos_encontrados) == 0: 
            print(f"No se encontraron resultados para el criterio '{criterio_de_busqueda}'.")
    return datos_encontrados

def buscar_por_id(path_archivo_csv, id):
    
    if not verificar_existencia_archivo(path_archivo_csv):
        print(f"El archivo '{path_archivo_csv}' no existe.")
        return None

    with open(path_archivo_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        for fila in reader:
            if id in fila:
                return fila  
    return None

def eliminar(path_archivo_csv, criterio_de_busqueda):
    if not verificar_existencia_archivo(path_archivo_csv):
        print(f"El archivo '{path_archivo_csv}' no existe.")
        return

    with open(path_archivo_csv, mode='r', newline='') as file:
        rows = list(csv.reader(file))

    nuevas_filas = [fila for fila in rows if criterio_de_busqueda not in fila]

    if len(nuevas_filas) != len(rows):
        with open(path_archivo_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(nuevas_filas)
        print(f"Registro con criterio '{criterio_de_busqueda}' eliminado.")
    else:
        print(f"No se encontraron registros para eliminar con el criterio '{criterio_de_busqueda}'.")

def actualizar(path_archivo_csv, criterio_de_busqueda, arreglo_con_datos):
    if not verificar_existencia_archivo(path_archivo_csv):
        print(f"El archivo '{path_archivo_csv}' no existe.")
        return

    with open(path_archivo_csv, mode='r', newline='') as file:
        rows = list(csv.reader(file))

    actualizado = False
    for index, fila in enumerate(rows):
        if criterio_de_busqueda in fila:
            rows[index] = arreglo_con_datos
            actualizado = True
            break

    if actualizado:
        with open(path_archivo_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        print(f"Registro con criterio '{criterio_de_busqueda}' actualizado.")
    else:
        print(f"No se encontró el registro para actualizar con el criterio '{criterio_de_busqueda}'.")

def verificar_existencia_archivo(path_archivo_csv):
    return os.path.exists(path_archivo_csv)
