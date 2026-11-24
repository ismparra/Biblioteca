from BD.connection import consultar, ejecutar

def insert_1_alumno(name, mat):
    return ejecutar(
        """
        INSERT INTO ALUMNOS
        VALUES
        (NULL, %s, %s, 'activo')
        """,
        (name, mat)
    )

def obtener_alumnos():
    return consultar(
        """
        SELECT * FROM ALUMNOS
        """
    )

def dar_baja_1_alumno(id):
    return ejecutar(
        """
        UPDATE ALUMNOS
        SET estado = 'suspendido'
        WHERE id_alumno = %s;
        """,
        (id,)
    )

def dar_alta_1_alumno(id):
    return ejecutar(
        """
        UPDATE ALUMNOS
        SET estado = 'activo'
        WHERE id_alumno = %s;
        """,
        (id,)
    )