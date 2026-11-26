from BD.connection import ejecutar

def registrar_1_ejemplar(codigo, id):
    return ejecutar(
        """
        INSERT INTO EJEMPLARES
        VALUES
        (NULL, %s, %s, 'disponible');
        """,
        (codigo, id)
    )