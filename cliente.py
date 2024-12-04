import socket
import json
from datetime import datetime

# Función para enviar la solicitud al servidor
def enviar_peticion(operacion, datos):
    host = '127.0.0.1'
    port = 65432
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Conexión establecida con el servidor en {host}:{port}")  # Confirmación de conexión al servidor

    request = {
        'operacion': operacion,
        'datos': datos
    }
    client_socket.sendall(json.dumps(request).encode())

    response = client_socket.recv(1024).decode()
    print(f"Respuesta del servidor: {response}")

    client_socket.close()

# Función para capturar los datos del empleado
def ingresar_datos_empleado():
    nombre = input("Ingrese el nombre del empleado: ")
    apellido = input("Ingrese el apellido del empleado: ")
    
    # Conversión de la fecha al formato correcto
    fecha_contratacion = input("Ingrese la fecha de contratación (YYYY-MM-DD): ")
    try:
        fecha_contratacion = datetime.strptime(fecha_contratacion, '%Y-%m-%d').date()
    except ValueError:
        print("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
        return
    
    direccion = input("Ingrese la dirección del empleado: ")
    id_ciudad = input("Ingrese el ID de la ciudad: ")
    id_departamento = input("Ingrese el ID del departamento: ")
    id_cargo = input("Ingrese el ID del cargo: ")

    return {
        'nombre': nombre,
        'apellido': apellido,
        'fecha_contratacion': fecha_contratacion.strftime('%Y-%m-%d'),  # Convertir la fecha a cadena
        'direccion': direccion,
        'id_ciudad': int(id_ciudad),
        'id_departamento': int(id_departamento),
        'id_cargo': int(id_cargo)
    }

# Función para capturar los datos para la actualización
def ingresar_datos_actualizar():
    id_empleado = input("Ingrese el ID del empleado a actualizar: ")
    direccion = input("Ingrese la nueva dirección: ")
    id_ciudad = input("Ingrese el nuevo ID de la ciudad: ")

    return {
        'id_empleado': int(id_empleado),
        'direccion': direccion,
        'id_ciudad': int(id_ciudad)
    }

# Función para capturar los datos para eliminar
def ingresar_datos_eliminar():
    id_empleado = input("Ingrese el ID del empleado a eliminar: ")

    return {
        'id_empleado': int(id_empleado)
    }

# Función para capturar los datos para consultar
def ingresar_datos_consultar():
    id_empleado = input("Ingrese el ID del empleado a consultar: ")

    return {
        'id_empleado': int(id_empleado)
    }

# Menú interactivo para elegir la operación
def menu():
    while True:
        print("\n----------------------")
        print("Bogotá ID 1")
        print("Medellín ID 2")
        print("Nueva York ID 3")
        print("Madrid ID 4")
        print("\n----------------------")
        print("\nMenú de operaciones:")
        print("1. Insertar empleado")
        print("2. Actualizar empleado")
        print("3. Consultar empleado")
        print("4. Borrar empleado")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            datos = ingresar_datos_empleado()
            enviar_peticion('insert', datos)

        elif opcion == '2':
            datos = ingresar_datos_actualizar()
            enviar_peticion('update', datos)

        elif opcion == '3':
            datos = ingresar_datos_consultar()
            enviar_peticion('select', datos)

        elif opcion == '4':
            datos = ingresar_datos_eliminar()
            enviar_peticion('delete', datos)

        elif opcion == '5':
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción correcta.")

# Ejecutar el menú
if __name__ == "__main__":
    menu()
