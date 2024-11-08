import mysql.connector
from mysql.connector import Error

def create_connection():
    """Establece la conexión a la base de datos MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='450642Osr$_&',
            database='base_de_datos',
            port=3307
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
