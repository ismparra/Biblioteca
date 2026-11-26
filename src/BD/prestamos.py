from BD.connection import ejecutar, consultar

def obtenerPrestamos():
    return consultar(
        """
        SELECT 
        p.id_prestamo, 
        a.nombre_completo as alumno, 
        l.titulo, 
        b.nombre_completo as bibliotecario, 
        p.fecha_prestamo,
        p.fecha_limite, 
        p.fecha_devolucion, 
        dias_retraso(p.id_prestamo) as atraso,
        e.codigo_barras
        FROM PRESTAMOS p JOIN EJEMPLARES e ON e.id_ejemplar = p.id_ejemplar
             JOIN LIBROS l ON e.id_libro = l.id_libro
             JOIN ALUMNOS a ON p.id_alumno = a.id_alumno
             JOIN BIBLIOTECARIOS b ON p.id_bibliotecario = b.id_bibliotecario;
        """ )
    
def registrar_1_devolucion(codigo):
    return ejecutar(
        "call registrar_devolucion(%s)",
        (codigo,)
    )