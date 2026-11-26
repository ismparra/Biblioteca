from BD.connection import ejecutar, consultar

def insertar_libro(titulo, autor, categoria):
    return ejecutar(
            "INSERT INTO libros (titulo, autor, categoria) VALUES (%s, %s, %s)",
            (titulo, autor, categoria)
        )

def obtener_libros():
    return [(fila["titulo"], fila["id_libro"])
            for fila in consultar(
                "SELECT titulo, id_libro FROM libros"
            )]

def buscar_libros(q):
    return [(fila["titulo"], fila["id_libro"])
                for fila in consultar(
                    """
                    SELECT *
                    FROM libros
                    WHERE titulo LIKE %s
                    OR autor LIKE %s
                    """, 
                (f"%{q}%", f"%{q}%")
                )
            ]

def buscar_libro(id):
    return consultar(
        "SELECT id_libro, titulo, autor, categoria, ejemplares_disponibles(id_libro) as ejemplares" \
        " FROM LIBROS WHERE id_libro = %s",
        (id,))[0]

def buscar_libro_cod(codigo):
    return consultar("""
            SELECT * 
            FROM LIBROS NATURAL JOIN EJEMPLARES 
            WHERE codigo_barras = %s""",
            (codigo,))[0]

def eliminar_1_libro(id):
    return ejecutar(
        "CALL eliminar_libro(%s)",
        (id,)
    )

def actualizar_1_libro(id, titulo, autor, categoia):
    return ejecutar(
        """UPDATE LIBROS
           SET titulo = %s,
               autor = %s,
               categoria = %s
           WHERE id_libro = %s""",
        (titulo, autor, categoia, id)
    )