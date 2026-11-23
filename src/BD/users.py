from BD.connection import consultar
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