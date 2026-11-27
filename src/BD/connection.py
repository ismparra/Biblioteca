import mysql.connector
from flask import has_request_context, session

# cada rol de la app entra a MySQL con su propia cuenta (database/usuarios.sql)
CUENTAS = {
    "administrador": ("bib_admin", "Admin123!"),
    "operador": ("bib_operador", "Operador123!"),
    "consulta": ("bib_consulta", "Consulta123!"),
    "login": ("bib_login", "Login123!"),   # solo puede ejecutar iniciar_sesion
}

def get_connection(cuenta=None):
    if cuenta is None:
        # sin sesion iniciada solo se tienen los permisos de consulta
        cuenta = (has_request_context() and session.get('rol')) or "consulta"
    usuario, password = CUENTAS[cuenta]
    return mysql.connector.connect(
        host="localhost",
        user=usuario,
        password=password,
        database="biblioteca"
    )

def consultar(sql, params=None, cuenta=None):
    conexion = get_connection(cuenta)
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        conexion.close()

def ejecutar(sql, params=None):
    conexion = get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, params)
        conexion.commit()
        return cursor.rowcount
    finally:
        conexion.close()
