from BD.connection import consultar, ejecutar
def login(usuario, passw):
    return consultar(
        """
        call iniciar_sesion(%s,%s);
        """,
        (usuario, passw),
        "login"
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
        call registrar_usuario(%s, %s, %s, %s)
        """,
        (name, user, _pass, rol)
    )

def buscar_user(id):
    filas = consultar(
        """
        SELECT id_bibliotecario, nombre_completo, usuario, rol
        FROM BIBLIOTECARIOS
        WHERE id_bibliotecario = %s
        """,
        (id,)
    )
    return filas[0] if filas else None

def actualizar_1_user(id, name, user, _pass, rol):
    return ejecutar(
        """
        call actualizar_usuario(%s, %s, %s, %s, %s)
        """,
        (id, name, user, _pass, rol)
    )

def eliminar_1_user(id):
    return ejecutar(
        """
        call eliminar_usuario(%s)
        """,
        (id,)
    )

def obtener_usuarios():
    return consultar(
        """
        SELECT id_bibliotecario, nombre_completo, usuario, rol, estado
        FROM BIBLIOTECARIOS
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