import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
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
    cursor.close()