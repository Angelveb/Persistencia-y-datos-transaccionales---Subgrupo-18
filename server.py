import socket
import mysql.connector
import json
from datetime import datetime

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0428',
    'database': 'recursos_humanos',
    'port': 3306
}

# Función para insertar el empleado en la base de datos
def insertar_empleado(data, cursor, conexion):
    # Convertir la fecha de nuevo a tipo date si es necesario
    fecha_contratacion = datetime.strptime(data['fecha_contratacion'], '%Y-%m-%d').date()

    query = """
    INSERT INTO empleados (nombre_empleado, apellido_empleado, fecha_contratacion, direccion, id_ciudad, id_departamento, id_cargo, estado)
    VALUES (%s, %s, %s, %s, %s, %s, %s, 'activo')
    """
    values = (
        data['nombre'],
        data['apellido'],
        fecha_contratacion,  # Insertar el objeto date en la base de datos
        data['direccion'],
        data['id_ciudad'],
        data['id_departamento'],
        data['id_cargo']
    )
    cursor.execute(query, values)
    conexion.commit()
    return "Empleado insertado exitosamente."

def actualizar_empleado(data, cursor, conexion):
    query = """
    UPDATE empleados SET direccion = %s, id_ciudad = %s WHERE id_empleado = %s
    """
    values = (data['direccion'], data['id_ciudad'], data['id_empleado'])
    cursor.execute(query, values)
    conexion.commit()
    return "Empleado actualizado exitosamente."

def seleccionar_empleado(data, cursor):
    query = "SELECT * FROM empleados WHERE id_empleado = %s"
    cursor.execute(query, (data['id_empleado'],))
    result = cursor.fetchone()

    if result:
        # Serializar las fechas a cadenas antes de devolverlas
        result['fecha_contratacion'] = result['fecha_contratacion'].strftime('%Y-%m-%d')
        return result
    else:
        return "Empleado no encontrado."

def borrar_empleado(data, cursor, conexion):
    # Insertar en históricos antes de borrar
    insertar_historico = """
    INSERT INTO historicos (id_empleado, tipo_operacion, detalles_operacion)
    VALUES (%s, 'delete', 'Empleado eliminado.')
    """
    cursor.execute(insertar_historico, (data['id_empleado'],))
    conexion.commit()

    # Marcar empleado como inactivo
    query = "UPDATE empleados SET estado = 'inactivo' WHERE id_empleado = %s"
    cursor.execute(query, (data['id_empleado'],))
    conexion.commit()
    return "Empleado marcado como inactivo y registrado en históricos."

# Configuración del socket server
def socket_server():
    host = '127.0.0.1'
    port = 65432
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor escuchando en {host}:{port}")

    while True:
        # Aceptar conexión del cliente
        client_socket, client_address = server_socket.accept()
        
        # Mostrar mensaje de confirmación de conexión
        print(f"Conexión establecida correctamente con {client_address}")
        
        try:
            conexion = mysql.connector.connect(**db_config)
            cursor = conexion.cursor(dictionary=True)

            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                request = json.loads(data)
                operation = request.get('operacion')

                if operation == 'insert':
                    response = insertar_empleado(request['datos'], cursor, conexion)
                elif operation == 'update':
                    response = actualizar_empleado(request['datos'], cursor, conexion)
                elif operation == 'select':
                    response = seleccionar_empleado(request['datos'], cursor)
                elif operation == 'delete':
                    response = borrar_empleado(request['datos'], cursor, conexion)
                else:
                    response = "Operación no reconocida."

                client_socket.sendall(json.dumps(response).encode())
        except Exception as e:
            print(f"Error: {e}")
            client_socket.sendall(f"Error: {e}".encode())
        finally:
            client_socket.close()
            cursor.close()
            conexion.close()

if __name__ == "__main__":
    socket_server()
