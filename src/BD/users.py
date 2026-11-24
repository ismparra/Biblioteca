from BD.connection import consultar, ejecutar
def login(usuario, passw):
    return consultar(
        """
        SELECT * FROM BIBLIOTECARIOS
        WHERE USUARIO = %s AND PASSWORD_HASH = %s;
        """,
        (usuario, passw)
    )

def buscar_user_by_username(user):
    return consultar(
        """
        SELCET * FROM BIBLIOTECARIOS
        WHERE USUARIO = %s
        """,
        (user,)
    )

def insertar_1_user(name, user, _pass, rol):
    return ejecutar(
        """
        INSERT INTO BIBLIOTECARIOS
        VALUES 
        (NULL, %s, %s, %s, %s, 'activo')
        """,
        (name, user, _pass, rol)
    )

def obtener_usuarios():
    return consultar(
        """
        SELECT * FROM BIBLIOTECARIOS
        """
    )

def dar_baja_1_usuario(id):
    return ejecutar(
        """
        UPDATE BIBLIOTECARIOS
        SET estado = 'inactivo'
        WHERE id_bibliotecario = %s;
        """,
        (id,)
    )

def dar_alta_1_usuario(id):
    return ejecutar(
        """
        UPDATE BIBLIOTECARIOS
        SET estado = 'activo'
        WHERE id_bibliotecario = %s;
        """,
        (id,)
    )