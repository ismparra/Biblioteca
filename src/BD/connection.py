import mysql.connector

def get_connection(usuario = "bib_admin", password = "Admin123!"):
    return mysql.connector.connect(
        host="localhost",
        user= usuario,
        password= password,
        database="biblioteca"
    )

def consultar(sql, params=None):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, params)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado

def ejecutar(sql, params=None):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute(sql, params)
    conexion.commit()
    filas_modificadas = cursor.rowcount
    cursor.close()
    conexion.close()
    return filas_modificadas