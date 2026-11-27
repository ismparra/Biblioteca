from BD.connection import consultar, ejecutar, get_connection

def consultar_1_alumno(mat):
    conexion = get_connection()
    try:
        # "", 0, 0 solo apartan el lugar de los parametros OUT
        res = conexion.cursor().callproc("consultar_alumno", (mat, "", 0, 0))
        return {"nombre": res[1], "activos": res[2], "vencidos": res[3]}
    finally:
        conexion.close()

def insert_1_alumno(name, mat):
    return ejecutar(
        """
        INSERT INTO ALUMNOS
        VALUES
        (NULL, %s, %s, 'activo')
        """,
        (name, mat)
    )

def buscar_alumno(id):
    filas = consultar(
        """
        SELECT * FROM ALUMNOS
        WHERE id_alumno = %s
        """,
        (id,)
    )
    return filas[0] if filas else None

def actualizar_1_alumno(id, name, mat):
    return ejecutar(
        """
        UPDATE ALUMNOS
        SET nombre_completo = %s, matricula = %s
        WHERE id_alumno = %s;
        """,
        (name, mat, id)
    )

def eliminar_1_alumno(id):
    return ejecutar(
        """
        call eliminar_alumno(%s)
        """,
        (id,)
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